#!/usr/bin/env python3
"""
Sparse Vector Generation for V5 RAG System
Implements BM25 and attention-based sparse vectors for hybrid search

Features:
- BM25 sparse encoding (Qdrant/bm25 model)
- Attention-based sparse encoding (Qdrant attention models)
- Multi-channel sparse vectors
- Qdrant-compatible format
- Batch processing support
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple
from collections import Counter
import re

import numpy as np

# Import sentence transformers
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

logger = logging.getLogger(__name__)


class SparseVectorEncoder:
    """
    Base class for sparse vector encoding
    
    Sparse vectors are represented as:
    {
        "indices": [int, ...],  # Token/feature indices
        "values": [float, ...],  # Weights for each index
        "tokens": [str, ...]     # Human-readable tokens (optional)
    }
    """
    
    def encode(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Encode texts into sparse vectors
        
        Args:
            texts: List of input texts
        
        Returns:
            List of sparse vector dicts
        """
        raise NotImplementedError
    
    def encode_single(self, text: str) -> Dict[str, Any]:
        """Encode single text"""
        return self.encode([text])[0]


class BM25SparseEncoder(SparseVectorEncoder):
    """
    BM25-based sparse vector encoder using Qdrant BM25 model
    
    Features:
    - Statistical term weighting
    - IDF normalization
    - Configurable k1 and b parameters
    - Fast batch processing
    
    Example:
        encoder = BM25SparseEncoder()
        sparse_vectors = encoder.encode([
            "Document about machine learning",
            "Tutorial on deep learning"
        ])
    """
    
    def __init__(
        self,
        model_name: str = "Qdrant/bm25",
        k1: float = 1.5,
        b: float = 0.75,
        use_model: bool = True
    ):
        """
        Initialize BM25 encoder
        
        Args:
            model_name: HuggingFace model ID for BM25
            k1: BM25 k1 parameter (term frequency saturation)
            b: BM25 b parameter (length normalization)
            use_model: Use SentenceTransformer model if available
        """
        self.k1 = k1
        self.b = b
        self.model = None
        self.use_model = use_model
        
        if use_model and SentenceTransformer is not None:
            try:
                logger.info(f"Loading BM25 model: {model_name}")
                self.model = SentenceTransformer(model_name, trust_remote_code=True)
                logger.info("✓ BM25 model loaded")
            except Exception as e:
                logger.warning(
                    f"Failed to load BM25 model ({e}). "
                    "Falling back to statistical BM25 implementation."
                )
                self.model = None
        
        # Document statistics for IDF calculation
        self.doc_freq: Dict[str, int] = {}
        self.num_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.vocabulary: Dict[str, int] = {}  # token -> index mapping
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple word tokenization"""
        # Extract words (3+ chars, alphanumeric)
        tokens = re.findall(r'\b[a-zA-Z0-9]{3,}\b', text.lower())
        return tokens
    
    def _update_statistics(self, texts: List[str]) -> None:
        """Update document statistics for IDF calculation"""
        for text in texts:
            tokens = self._tokenize(text)
            unique_tokens = set(tokens)
            
            for token in unique_tokens:
                self.doc_freq[token] = self.doc_freq.get(token, 0) + 1
                
                # Add to vocabulary if new
                if token not in self.vocabulary:
                    self.vocabulary[token] = len(self.vocabulary)
        
        self.num_docs += len(texts)
        
        # Update average document length
        total_length = sum(len(self._tokenize(text)) for text in texts)
        self.avg_doc_length = (
            (self.avg_doc_length * (self.num_docs - len(texts)) + total_length)
            / self.num_docs
        )
    
    def _calculate_idf(self, term: str) -> float:
        """Calculate IDF score for a term"""
        if self.num_docs == 0:
            return 0.0
        
        df = self.doc_freq.get(term, 0)
        # IDF = log((N - df + 0.5) / (df + 0.5))
        idf = np.log((self.num_docs - df + 0.5) / (df + 0.5) + 1.0)
        return max(0.0, idf)
    
    def _calculate_bm25_score(self, term_freq: int, doc_length: int, idf: float) -> float:
        """Calculate BM25 score for a term in a document"""
        # BM25 formula
        numerator = term_freq * (self.k1 + 1)
        denominator = term_freq + self.k1 * (
            1 - self.b + self.b * (doc_length / max(self.avg_doc_length, 1))
        )
        return idf * (numerator / denominator)
    
    def encode(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Encode texts into BM25 sparse vectors
        
        Args:
            texts: List of input texts
        
        Returns:
            List of sparse vector dicts with indices, values, tokens
        """
        if self.model is not None:
            # Use pre-trained model
            return self._encode_with_model(texts)
        else:
            # Use statistical BM25
            return self._encode_statistical(texts)
    
    def _encode_with_model(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Encode using SentenceTransformer BM25 model"""
        try:
            # Encode texts
            embeddings = self.model.encode(
                texts,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            
            # Convert dense embeddings to sparse format
            # (Model-specific processing may vary)
            sparse_vectors = []
            for embedding in embeddings:
                # Get non-zero indices and values
                non_zero_indices = np.nonzero(embedding)[0]
                non_zero_values = embedding[non_zero_indices]
                
                sparse_vectors.append({
                    "indices": non_zero_indices.tolist(),
                    "values": non_zero_values.tolist(),
                    "tokens": []  # Token mapping not available from model
                })
            
            return sparse_vectors
            
        except Exception as e:
            logger.error(f"Model encoding failed: {e}. Falling back to statistical.")
            return self._encode_statistical(texts)
    
    def _encode_statistical(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Encode using statistical BM25 implementation"""
        # Update statistics with current batch
        self._update_statistics(texts)
        
        sparse_vectors = []
        
        for text in texts:
            tokens = self._tokenize(text)
            doc_length = len(tokens)
            
            # Calculate term frequencies
            term_freq = Counter(tokens)
            
            # Calculate BM25 scores
            bm25_scores = {}
            for term, freq in term_freq.items():
                idf = self._calculate_idf(term)
                score = self._calculate_bm25_score(freq, doc_length, idf)
                
                if term in self.vocabulary:
                    bm25_scores[term] = score
            
            # Sort by score and take top terms
            top_terms = sorted(
                bm25_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:100]  # Top 100 terms
            
            # Build sparse vector
            indices = [self.vocabulary[term] for term, _ in top_terms]
            values = [score for _, score in top_terms]
            tokens = [term for term, _ in top_terms]
            
            sparse_vectors.append({
                "indices": indices,
                "values": values,
                "tokens": tokens
            })
        
        return sparse_vectors


class AttentionSparseEncoder(SparseVectorEncoder):
    """
    Attention-based sparse vector encoder
    
    Uses model attention weights to generate sparse representations
    
    Features:
    - Transformer attention-based weighting
    - Token-level importance scoring
    - Compatible with Qdrant sparse vectors
    
    Example:
        encoder = AttentionSparseEncoder(
            model_name="Qdrant/all_miniLM_L6_v2_with_attentions"
        )
        sparse_vectors = encoder.encode(["Sample text"])
    """
    
    def __init__(
        self,
        model_name: str = "Qdrant/all_miniLM_L6_v2_with_attentions",
        top_k: int = 100
    ):
        """
        Initialize attention-based encoder
        
        Args:
            model_name: HuggingFace model ID with attention outputs
            top_k: Number of top attention weights to keep
        """
        self.top_k = top_k
        self.model = None
        
        if SentenceTransformer is None:
            raise ImportError(
                "sentence-transformers required for attention-based encoding"
            )
        
        try:
            logger.info(f"Loading attention model: {model_name}")
            self.model = SentenceTransformer(model_name, trust_remote_code=True)
            logger.info("✓ Attention model loaded")
        except Exception as e:
            raise RuntimeError(f"Failed to load attention model: {e}")
    
    def encode(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Encode texts using attention weights
        
        Args:
            texts: List of input texts
        
        Returns:
            List of sparse vector dicts
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        try:
            # Encode with attention outputs
            # Note: This requires model-specific implementation
            # depending on how attention weights are exposed
            embeddings = self.model.encode(
                texts,
                convert_to_numpy=True,
                show_progress_bar=False,
                output_value='token_embeddings'  # Get token-level outputs
            )
            
            sparse_vectors = []
            
            for embedding in embeddings:
                # Calculate attention-based importance scores
                # (Simplified: use L2 norm of token embeddings as importance)
                token_importance = np.linalg.norm(embedding, axis=1)
                
                # Get top-k tokens
                top_indices = np.argsort(token_importance)[-self.top_k:]
                top_values = token_importance[top_indices]
                
                # Normalize to sum to 1
                top_values = top_values / np.sum(top_values)
                
                sparse_vectors.append({
                    "indices": top_indices.tolist(),
                    "values": top_values.tolist(),
                    "tokens": []  # Token text not available without tokenizer
                })
            
            return sparse_vectors
            
        except Exception as e:
            logger.error(f"Attention encoding failed: {e}")
            # Return empty sparse vectors as fallback
            return [
                {"indices": [], "values": [], "tokens": []}
                for _ in texts
            ]


class HybridSparseEncoder:
    """
    Hybrid sparse encoder combining BM25 and attention-based methods
    
    Features:
    - Multi-channel sparse vectors (BM25 + attention)
    - Channel-specific weighting
    - Flexible combination strategies
    
    Example:
        encoder = HybridSparseEncoder(
            use_bm25=True,
            use_attention=True,
            bm25_weight=0.7,
            attention_weight=0.3
        )
        
        sparse_vectors = encoder.encode(["Sample text"])
    """
    
    def __init__(
        self,
        use_bm25: bool = True,
        use_attention: bool = False,
        bm25_weight: float = 0.7,
        attention_weight: float = 0.3,
        bm25_model: str = "Qdrant/bm25",
        attention_model: str = "Qdrant/all_miniLM_L6_v2_with_attentions"
    ):
        """
        Initialize hybrid encoder
        
        Args:
            use_bm25: Enable BM25 encoding
            use_attention: Enable attention-based encoding
            bm25_weight: Weight for BM25 channel
            attention_weight: Weight for attention channel
            bm25_model: BM25 model name
            attention_model: Attention model name
        """
        self.use_bm25 = use_bm25
        self.use_attention = use_attention
        self.bm25_weight = bm25_weight
        self.attention_weight = attention_weight
        
        self.bm25_encoder = None
        self.attention_encoder = None
        
        if use_bm25:
            self.bm25_encoder = BM25SparseEncoder(model_name=bm25_model)
            logger.info("✓ BM25 encoder initialized")
        
        if use_attention:
            try:
                self.attention_encoder = AttentionSparseEncoder(model_name=attention_model)
                logger.info("✓ Attention encoder initialized")
            except Exception as e:
                logger.warning(f"Attention encoder failed to initialize: {e}")
                self.use_attention = False
    
    def encode(
        self,
        texts: List[str],
        return_separate: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Encode texts with hybrid sparse encoding
        
        Args:
            texts: List of input texts
            return_separate: Return separate BM25 and attention vectors
        
        Returns:
            List of sparse vector dicts (combined or separate channels)
        """
        results = {}
        
        # Generate BM25 vectors
        if self.use_bm25 and self.bm25_encoder is not None:
            bm25_vectors = self.bm25_encoder.encode(texts)
            results["bm25"] = bm25_vectors
        
        # Generate attention vectors
        if self.use_attention and self.attention_encoder is not None:
            attention_vectors = self.attention_encoder.encode(texts)
            results["attention"] = attention_vectors
        
        if return_separate:
            # Return named channels
            return [
                {
                    channel: results[channel][i]
                    for channel in results
                }
                for i in range(len(texts))
            ]
        else:
            # Combine into single sparse vector
            return self._combine_vectors(results, len(texts))
    
    def _combine_vectors(
        self,
        channel_vectors: Dict[str, List[Dict[str, Any]]],
        num_texts: int
    ) -> List[Dict[str, Any]]:
        """Combine multi-channel sparse vectors into single vectors"""
        combined = []
        
        for i in range(num_texts):
            # Collect all indices and values from all channels
            all_indices = {}
            
            if "bm25" in channel_vectors:
                bm25 = channel_vectors["bm25"][i]
                for idx, val in zip(bm25["indices"], bm25["values"]):
                    all_indices[idx] = all_indices.get(idx, 0) + val * self.bm25_weight
            
            if "attention" in channel_vectors:
                attention = channel_vectors["attention"][i]
                for idx, val in zip(attention["indices"], attention["values"]):
                    all_indices[idx] = all_indices.get(idx, 0) + val * self.attention_weight
            
            # Sort by index
            sorted_items = sorted(all_indices.items())
            
            combined.append({
                "indices": [idx for idx, _ in sorted_items],
                "values": [val for _, val in sorted_items],
                "tokens": []
            })
        
        return combined


# Usage example
if __name__ == "__main__":
    # Example 1: BM25 sparse encoding
    bm25_encoder = BM25SparseEncoder()
    
    texts = [
        "Machine learning is a subset of artificial intelligence",
        "Deep learning uses neural networks with multiple layers",
        "Natural language processing handles text and speech"
    ]
    
    bm25_sparse = bm25_encoder.encode(texts)
    print("BM25 Sparse Vectors:")
    for i, vec in enumerate(bm25_sparse):
        print(f"  Text {i}: {len(vec['indices'])} non-zero entries")
        if vec['tokens']:
            print(f"    Top tokens: {vec['tokens'][:5]}")
    
    # Example 2: Hybrid encoding
    print("\nHybrid Sparse Encoding:")
    hybrid_encoder = HybridSparseEncoder(
        use_bm25=True,
        use_attention=False,  # Set to True if attention model available
        bm25_weight=0.7
    )
    
    hybrid_sparse = hybrid_encoder.encode(texts)
    print(f"Generated {len(hybrid_sparse)} hybrid sparse vectors")
    
    # Example 3: Multi-channel format for Qdrant
    print("\nMulti-channel Format:")
    multi_channel = hybrid_encoder.encode(texts, return_separate=True)
    print(f"Channels per vector: {list(multi_channel[0].keys())}")