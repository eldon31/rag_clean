#!/usr/bin/env python3
"""
LlamaIndex Multi-Model Embedder for V5 RAG System
Supports multiple embedding models with Matryoshka dimension truncation

Features:
- Multi-model embedding generation (Jina Code, BGE-M3, MiniLM)
- Matryoshka dimension support (128D-2048D)
- Batch processing for efficiency
- Sparse vector generation hooks (BM25, attention)
- Compatible with LlamaIndex BaseEmbedding interface
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.bridge.pydantic import PrivateAttr

# Import model registry
try:
    from processor.kaggle_ultimate_embedder_v4 import KAGGLE_OPTIMIZED_MODELS, ModelConfig
except ImportError:
    KAGGLE_OPTIMIZED_MODELS = {}
    ModelConfig = None

# Import sentence transformers
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

logger = logging.getLogger(__name__)


class MultiModelEmbedder(BaseEmbedding):
    """
    Multi-model embedder supporting multiple SentenceTransformer models
    
    Features:
    - Generates named vectors for multiple models
    - Matryoshka dimension truncation
    - Batch processing
    - Sparse vector hooks
    
    Example:
        embedder = MultiModelEmbedder(
            models={
                "jina-code": "jinaai/jina-embeddings-v3",
                "bge-m3": "BAAI/bge-m3"
            },
            matryoshka_dims={
                "jina-code": 1536,
                "bge-m3": 1024
            }
        )
        
        # Single embedding
        embedding = embedder.get_text_embedding("Sample text")
        
        # Batch embeddings
        embeddings = embedder.get_text_embedding_batch(["Text 1", "Text 2"])
    """
    
    _models: Dict[str, Any] = PrivateAttr()
    _model_configs: Dict[str, ModelConfig] = PrivateAttr()
    _matryoshka_dims: Dict[str, int] = PrivateAttr()
    _primary_model_name: str = PrivateAttr()
    
    def __init__(
        self,
        models: Optional[Dict[str, str]] = None,
        matryoshka_dims: Optional[Dict[str, int]] = None,
        primary_model: str = "jina-code",
        embed_batch_size: int = 32,
        normalize: bool = True,
        **kwargs: Any
    ):
        """
        Initialize multi-model embedder
        
        Args:
            models: Dict mapping names to HuggingFace model IDs
                   Default: {"jina-code": "jinaai/jina-embeddings-v3"}
            matryoshka_dims: Optional dimension truncation per model
            primary_model: Primary model name for get_text_embedding()
            embed_batch_size: Batch size for processing
            normalize: Normalize embeddings to unit vectors
            **kwargs: Additional LlamaIndex BaseEmbedding parameters
        """
        super().__init__(
            embed_batch_size=embed_batch_size,
            **kwargs
        )
        
        if SentenceTransformer is None:
            raise ImportError(
                "sentence-transformers not available. "
                "Install with: pip install sentence-transformers"
            )
        
        # Default models from registry
        if models is None:
            models = {
                "jina-code": "jinaai/jina-embeddings-v3"
            }
        
        self._primary_model_name = primary_model
        self._matryoshka_dims = matryoshka_dims or {}
        self._models = {}
        self._model_configs = {}
        self._normalize = normalize
        
        # Load models
        logger.info(f"Loading {len(models)} embedding models...")
        for name, model_id in models.items():
            try:
                logger.info(f"  Loading {name}: {model_id}")
                model = SentenceTransformer(model_id, trust_remote_code=True)
                self._models[name] = model
                
                # Get config from registry if available
                if KAGGLE_OPTIMIZED_MODELS and name in KAGGLE_OPTIMIZED_MODELS:
                    self._model_configs[name] = KAGGLE_OPTIMIZED_MODELS[name]
                    logger.info(f"    ✓ Config: {self._model_configs[name].vector_dim}D")
                else:
                    logger.info(f"    ✓ Loaded")
                
            except Exception as e:
                logger.error(f"  ✗ Failed to load {name}: {e}")
        
        if not self._models:
            raise ValueError("No models loaded successfully")
        
        if primary_model not in self._models:
            raise ValueError(
                f"Primary model '{primary_model}' not in loaded models: "
                f"{list(self._models.keys())}"
            )
        
        logger.info(
            f"✓ MultiModelEmbedder initialized with {len(self._models)} models"
        )
    
    @classmethod
    def class_name(cls) -> str:
        """Return class name for serialization"""
        return "MultiModelEmbedder"
    
    def _get_query_embedding(self, query: str) -> List[float]:
        """
        Internal method to get embedding for a single query
        
        Args:
            query: Query text
        
        Returns:
            Embedding vector as list of floats
        """
        return self.get_text_embedding(query)
    
    async def _aget_query_embedding(self, query: str) -> List[float]:
        """Async version of _get_query_embedding"""
        return self._get_query_embedding(query)
    
    def _get_text_embedding(self, text: str) -> List[float]:
        """
        Internal method to get embedding for single text
        
        Args:
            text: Input text
        
        Returns:
            Embedding vector from primary model
        """
        model = self._models[self._primary_model_name]
        embedding = model.encode([text], convert_to_numpy=True)[0]
        
        # Apply Matryoshka truncation if specified
        if self._primary_model_name in self._matryoshka_dims:
            target_dim = self._matryoshka_dims[self._primary_model_name]
            embedding = embedding[:target_dim]
        
        # Normalize if requested
        if self._normalize:
            embedding = embedding / np.linalg.norm(embedding)
        
        return embedding.tolist()
    
    async def _aget_text_embedding(self, text: str) -> List[float]:
        """Async version of _get_text_embedding"""
        return self._get_text_embedding(text)
    
    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Internal method to get embeddings for multiple texts
        
        Args:
            texts: List of input texts
        
        Returns:
            List of embedding vectors from primary model
        """
        model = self._models[self._primary_model_name]
        embeddings = model.encode(
            texts,
            batch_size=self.embed_batch_size,
            convert_to_numpy=True,
            show_progress_bar=len(texts) > 100
        )
        
        # Apply Matryoshka truncation if specified
        if self._primary_model_name in self._matryoshka_dims:
            target_dim = self._matryoshka_dims[self._primary_model_name]
            embeddings = embeddings[:, :target_dim]
        
        # Normalize if requested
        if self._normalize:
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / norms
        
        return embeddings.tolist()
    
    async def _aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Async version of _get_text_embeddings"""
        return self._get_text_embeddings(texts)
    
    def get_multi_model_embeddings(
        self,
        texts: List[str],
        model_names: Optional[List[str]] = None
    ) -> Dict[str, np.ndarray]:
        """
        Generate embeddings from multiple models
        
        Args:
            texts: List of input texts
            model_names: Models to use (default: all loaded models)
        
        Returns:
            Dict mapping model names to embedding arrays
        """
        if model_names is None:
            model_names = list(self._models.keys())
        
        results = {}
        
        for name in model_names:
            if name not in self._models:
                logger.warning(f"Model '{name}' not loaded, skipping")
                continue
            
            model = self._models[name]
            embeddings = model.encode(
                texts,
                batch_size=self.embed_batch_size,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            
            # Apply Matryoshka truncation
            if name in self._matryoshka_dims:
                target_dim = self._matryoshka_dims[name]
                embeddings = embeddings[:, :target_dim]
            
            # Normalize
            if self._normalize:
                norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
                embeddings = embeddings / norms
            
            results[name] = embeddings
        
        return results
    
    def get_named_vectors_for_qdrant(
        self,
        texts: List[str],
        model_names: Optional[List[str]] = None
    ) -> List[Dict[str, List[float]]]:
        """
        Generate named vectors compatible with Qdrant multi-vector format
        
        Args:
            texts: List of input texts
            model_names: Models to use
        
        Returns:
            List of dicts, each mapping model names to embedding vectors
            
        Example output:
            [
                {
                    "jina-code": [0.1, 0.2, ...],
                    "bge-m3": [0.3, 0.4, ...]
                },
                ...
            ]
        """
        multi_embeddings = self.get_multi_model_embeddings(texts, model_names)
        
        # Transpose: from {model: [embeddings]} to [{model: embedding}, ...]
        num_texts = len(texts)
        results = []
        
        for i in range(num_texts):
            named_vector = {}
            for model_name, embeddings in multi_embeddings.items():
                named_vector[model_name] = embeddings[i].tolist()
            results.append(named_vector)
        
        return results
    
    def generate_sparse_vectors(
        self,
        texts: List[str],
        method: str = "bm25"
    ) -> List[Dict[str, Any]]:
        """
        Generate sparse vectors for hybrid search
        
        Args:
            texts: List of input texts
            method: Sparse encoding method ("bm25" or "attention")
        
        Returns:
            List of sparse vector dicts with indices, values, tokens
        
        Note:
            This is a placeholder. Actual implementation requires
            sparse vector models (see Task 2.1, 2.2 in Phase 2 plan).
        """
        logger.warning(
            f"Sparse vector generation ({method}) not yet implemented. "
            "Returning empty sparse vectors. "
            "See Task 2.1/2.2 in V5_PHASE2_IMPLEMENTATION_PLAN.md"
        )
        
        # Return empty sparse vectors as placeholder
        return [
            {
                "indices": [],
                "values": [],
                "tokens": []
            }
            for _ in texts
        ]
    
    def get_hybrid_vectors(
        self,
        texts: List[str],
        include_sparse: bool = True,
        sparse_method: str = "bm25"
    ) -> Tuple[Dict[str, np.ndarray], Optional[List[Dict[str, Any]]]]:
        """
        Generate both dense and sparse vectors for hybrid search
        
        Args:
            texts: List of input texts
            include_sparse: Whether to generate sparse vectors
            sparse_method: Sparse encoding method
        
        Returns:
            Tuple of (dense_vectors_dict, sparse_vectors_list)
        """
        # Generate dense embeddings from all models
        dense_vectors = self.get_multi_model_embeddings(texts)
        
        # Generate sparse vectors if requested
        sparse_vectors = None
        if include_sparse:
            sparse_vectors = self.generate_sparse_vectors(texts, sparse_method)
        
        return dense_vectors, sparse_vectors
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about loaded models
        
        Returns:
            Dict with model metadata
        """
        info = {
            "num_models": len(self._models),
            "primary_model": self._primary_model_name,
            "models": {}
        }
        
        for name, model in self._models.items():
            model_info = {
                "loaded": True,
                "has_config": name in self._model_configs
            }
            
            if name in self._model_configs:
                config = self._model_configs[name]
                model_info.update({
                    "hf_model_id": config.hf_model_id,
                    "vector_dim": config.vector_dim,
                    "max_tokens": config.max_tokens
                })
            
            if name in self._matryoshka_dims:
                model_info["matryoshka_dim"] = self._matryoshka_dims[name]
            
            info["models"][name] = model_info
        
        return info


# Usage example
if __name__ == "__main__":
    # Example 1: Single model embedder
    embedder = MultiModelEmbedder(
        models={"jina-code": "jinaai/jina-embeddings-v3"},
        primary_model="jina-code"
    )
    
    # Single embedding
    text = "This is a test document about machine learning."
    embedding = embedder.get_text_embedding(text)
    print(f"Single embedding shape: {len(embedding)}D")
    
    # Batch embeddings
    texts = [
        "Document about neural networks",
        "Article on deep learning",
        "Tutorial for transformers"
    ]
    embeddings = embedder.get_text_embedding_batch(texts)
    print(f"Batch embeddings: {len(embeddings)} x {len(embeddings[0])}D")
    
    # Example 2: Multi-model embedder with Matryoshka
    multi_embedder = MultiModelEmbedder(
        models={
            "jina-code": "jinaai/jina-embeddings-v3",
            "bge-m3": "BAAI/bge-m3"
        },
        matryoshka_dims={
            "jina-code": 1536,  # Truncate to 1536D
            "bge-m3": 1024      # Truncate to 1024D
        },
        primary_model="jina-code"
    )
    
    # Multi-model embeddings
    multi_embeddings = multi_embedder.get_multi_model_embeddings(texts)
    print(f"\nMulti-model embeddings:")
    for model_name, emb_array in multi_embeddings.items():
        print(f"  {model_name}: {emb_array.shape}")
    
    # Qdrant named vectors format
    named_vectors = multi_embedder.get_named_vectors_for_qdrant(texts)
    print(f"\nQdrant named vectors: {len(named_vectors)} items")
    print(f"  Vector names: {list(named_vectors[0].keys())}")
    
    # Model info
    info = multi_embedder.get_model_info()
    print(f"\nModel info:")
    print(f"  Primary: {info['primary_model']}")
    print(f"  Total models: {info['num_models']}")