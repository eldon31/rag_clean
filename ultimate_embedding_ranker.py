#!/usr/bin/env python3
"""
Ultimate Embedding System with Advanced Ranker
Processes 3,096 chunks from DOCS_CHUNKS_OUTPUT with intelligent ranking

Features:
- Batch embedding generation with nomic-ai/CodeRankEmbed
- Advanced semantic ranking and re-ranking
- Collection-aware scoring and boosting
- Quality metrics and cluster analysis
- Hybrid search with multiple ranking strategies
"""

import json
import logging
import numpy as np
import pickle
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict
import time

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UltimateEmbeddingRanker:
    """
    Ultimate embedding system with advanced ranking capabilities
    Optimized for the 3,096 chunks from docs processing
    """
    
    def __init__(self, model_name: str = "nomic-ai/CodeRankEmbed"):
        """Initialize the ultimate embedding ranker"""
        
        logger.info(f"🚀 Initializing Ultimate Embedding Ranker with {model_name}")
        
        # Load the embedding model
        self.model = SentenceTransformer(model_name, trust_remote_code=True)
        self.model_name = model_name
        
        # Collection weights for ranking
        self.collection_weights = {
            "Docling": 1.2,  # Document processing expertise
            "FAST_DOCS": 1.1,  # API documentation
            "pydantic_pydantic": 1.0,  # Standard weight
            "Qdrant": 1.3,  # Vector database expertise
            "Sentence_Transformers": 1.15  # ML embeddings expertise
        }
        
        # Strategy weights for ranking
        self.strategy_weights = {
            "hybrid_adaptive": 1.2,
            "api_documentation": 1.1,
            "programming_language_documentation": 1.0,
            "platform_documentation": 1.15,
            "hierarchical_precise": 1.1,
            "hierarchical_balanced": 1.0,
            "hierarchical_context": 1.05
        }
        
        # Ranking configurations
        self.ranking_configs = {
            "semantic_only": {"semantic_weight": 1.0, "collection_weight": 0.0, "strategy_weight": 0.0},
            "collection_boosted": {"semantic_weight": 0.7, "collection_weight": 0.2, "strategy_weight": 0.1},
            "hybrid_balanced": {"semantic_weight": 0.6, "collection_weight": 0.25, "strategy_weight": 0.15},
            "collection_focused": {"semantic_weight": 0.5, "collection_weight": 0.4, "strategy_weight": 0.1}
        }
        
        # Storage for embeddings and metadata
        self.embeddings = None
        self.chunks_metadata = []
        self.chunk_texts = []
        self.embedding_index = {}
        
        logger.info("✅ Ultimate Embedding Ranker initialized")
    
    def load_all_chunks(
        self, 
        chunks_dir: str = r"C:\Users\raze0\Documents\LLM_KNOWLEDGE_CREATOR\RAG\RAG_CLEAN\DOCS_CHUNKS_OUTPUT"
    ) -> Dict[str, Any]:
        """
        Load all chunks from the processed collections
        
        Returns:
            Dictionary with loading statistics
        """
        
        logger.info(f"📂 Loading chunks from {chunks_dir}")
        chunks_path = Path(chunks_dir)
        
        results = {
            "collections_loaded": 0,
            "total_chunks_loaded": 0,
            "chunks_by_collection": {},
            "loading_errors": []
        }
        
        # Reset storage
        self.chunks_metadata = []
        self.chunk_texts = []
        
        # Process each collection
        for collection_dir in chunks_path.iterdir():
            if collection_dir.is_dir() and collection_dir.name != "__pycache__":
                collection_name = collection_dir.name
                collection_chunks = 0
                
                logger.info(f"📁 Loading collection: {collection_name}")
                
                # Load chunks from JSON files
                for chunk_file in collection_dir.rglob("*_chunks.json"):
                    try:
                        with open(chunk_file, 'r', encoding='utf-8') as f:
                            file_chunks = json.load(f)
                        
                        for chunk in file_chunks:
                            # Add chunk to our storage
                            chunk_id = len(self.chunks_metadata)
                            
                            # Enhance metadata with global ID
                            chunk["metadata"]["global_chunk_id"] = chunk_id
                            chunk["metadata"]["collection_weight"] = self.collection_weights.get(collection_name, 1.0)
                            chunk["metadata"]["strategy_weight"] = self.strategy_weights.get(
                                chunk["metadata"].get("chunking_strategy", ""), 1.0
                            )
                            
                            self.chunks_metadata.append(chunk["metadata"])
                            self.chunk_texts.append(chunk["text"])
                            collection_chunks += 1
                        
                        logger.debug(f"  📄 Loaded {len(file_chunks)} chunks from {chunk_file.name}")
                        
                    except Exception as e:
                        error_msg = f"Error loading {chunk_file}: {e}"
                        logger.error(f"❌ {error_msg}")
                        results["loading_errors"].append(error_msg)
                
                results["chunks_by_collection"][collection_name] = collection_chunks
                results["collections_loaded"] += 1
                logger.info(f"✅ Collection '{collection_name}': {collection_chunks} chunks loaded")
        
        results["total_chunks_loaded"] = len(self.chunks_metadata)
        
        logger.info(f"🎯 Chunk loading complete!")
        logger.info(f"📊 Total chunks loaded: {results['total_chunks_loaded']}")
        logger.info(f"📊 Collections: {results['collections_loaded']}")
        logger.info(f"📊 By collection: {results['chunks_by_collection']}")
        
        return results
    
    def generate_embeddings_batch(
        self, 
        batch_size: int = 32,
        save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate embeddings for all loaded chunks with batch processing
        
        Args:
            batch_size: Number of chunks to process in each batch
            save_path: Optional path to save embeddings
            
        Returns:
            Embedding generation statistics
        """
        
        if not self.chunk_texts:
            raise ValueError("No chunks loaded. Call load_all_chunks() first.")
        
        logger.info(f"🔥 Generating embeddings for {len(self.chunk_texts)} chunks")
        logger.info(f"📦 Batch size: {batch_size}")
        
        start_time = time.time()
        
        # Generate embeddings in batches
        all_embeddings = []
        total_batches = (len(self.chunk_texts) + batch_size - 1) // batch_size
        
        for i in range(0, len(self.chunk_texts), batch_size):
            batch_texts = self.chunk_texts[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            
            logger.info(f"🔄 Processing batch {batch_num}/{total_batches} ({len(batch_texts)} chunks)")
            
            # Generate embeddings for this batch
            batch_embeddings = self.model.encode(
                batch_texts,
                show_progress_bar=True,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            
            all_embeddings.append(batch_embeddings)
            
            # Progress update
            processed = min(i + batch_size, len(self.chunk_texts))
            progress = (processed / len(self.chunk_texts)) * 100
            logger.info(f"✅ Batch {batch_num} complete. Progress: {progress:.1f}%")
        
        # Combine all embeddings
        self.embeddings = np.vstack(all_embeddings)
        
        processing_time = time.time() - start_time
        
        # Create embedding index for fast lookup
        for i, metadata in enumerate(self.chunks_metadata):
            self.embedding_index[metadata["global_chunk_id"]] = i
        
        # Calculate statistics
        results = {
            "total_embeddings_generated": len(self.embeddings),
            "embedding_dimension": self.embeddings.shape[1],
            "processing_time_seconds": processing_time,
            "embeddings_per_second": len(self.embeddings) / processing_time,
            "model_used": self.model_name,
            "batch_size": batch_size,
            "total_batches": total_batches
        }
        
        # Save embeddings if path provided
        if save_path:
            self._save_embeddings(save_path, results)
        
        logger.info(f"🎯 Embedding generation complete!")
        logger.info(f"📊 Generated {results['total_embeddings_generated']} embeddings")
        logger.info(f"📊 Dimension: {results['embedding_dimension']}")
        logger.info(f"⏱️ Processing time: {results['processing_time_seconds']:.2f}s")
        logger.info(f"🚀 Speed: {results['embeddings_per_second']:.1f} embeddings/second")
        
        return results
    
    def _save_embeddings(self, save_path: str, generation_stats: Dict[str, Any]):
        """Save embeddings and metadata to disk"""
        
        save_dir = Path(save_path)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Save embeddings as numpy array
        embeddings_file = save_dir / "embeddings.npy"
        if self.embeddings is not None:
            np.save(str(embeddings_file), self.embeddings)
        
        # Save metadata
        metadata_file = save_dir / "chunks_metadata.json"
        with open(str(metadata_file), 'w', encoding='utf-8') as f:
            json.dump(self.chunks_metadata, f, indent=2, ensure_ascii=False)
        
        # Save chunk texts
        texts_file = save_dir / "chunk_texts.json"
        with open(str(texts_file), 'w', encoding='utf-8') as f:
            json.dump(self.chunk_texts, f, indent=2, ensure_ascii=False)
        
        # Save generation statistics
        stats_file = save_dir / "embedding_generation_stats.json"
        with open(str(stats_file), 'w', encoding='utf-8') as f:
            json.dump(generation_stats, f, indent=2, ensure_ascii=False)
        
        # Save embedding index
        index_file = save_dir / "embedding_index.pkl"
        with open(str(index_file), 'wb') as f:
            pickle.dump(self.embedding_index, f)
        
        logger.info(f"💾 Embeddings saved to {save_dir}")
    
    def load_embeddings(self, load_path: str) -> bool:
        """Load previously generated embeddings from disk"""
        
        load_dir = Path(load_path)
        
        try:
            # Load embeddings
            embeddings_file = load_dir / "embeddings.npy"
            self.embeddings = np.load(str(embeddings_file))
            
            # Load metadata
            metadata_file = load_dir / "chunks_metadata.json"
            with open(str(metadata_file), 'r', encoding='utf-8') as f:
                self.chunks_metadata = json.load(f)
            
            # Load chunk texts
            texts_file = load_dir / "chunk_texts.json"
            with open(str(texts_file), 'r', encoding='utf-8') as f:
                self.chunk_texts = json.load(f)
            
            # Load embedding index
            index_file = load_dir / "embedding_index.pkl"
            with open(str(index_file), 'rb') as f:
                self.embedding_index = pickle.load(f)
            
            logger.info(f"✅ Loaded {len(self.embeddings)} embeddings from {load_dir}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load embeddings: {e}")
            return False
    
    def semantic_search(
        self, 
        query: str, 
        top_k: int = 10,
        ranking_mode: str = "hybrid_balanced",
        collection_filter: Optional[List[str]] = None,
        min_similarity: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Advanced semantic search with ranking
        
        Args:
            query: Search query
            top_k: Number of results to return
            ranking_mode: Ranking strategy to use
            collection_filter: Filter by specific collections
            min_similarity: Minimum similarity threshold
            
        Returns:
            Ranked search results with scores
        """
        
        if self.embeddings is None:
            raise ValueError("No embeddings loaded. Generate or load embeddings first.")
        
        logger.info(f"🔍 Semantic search: '{query}' (top_k={top_k}, mode={ranking_mode})")
        
        # Encode query
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        
        # Calculate semantic similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get ranking configuration
        config = self.ranking_configs.get(ranking_mode, self.ranking_configs["hybrid_balanced"])
        
        # Calculate composite scores
        composite_scores = []
        for i, (similarity, metadata) in enumerate(zip(similarities, self.chunks_metadata)):
            
            # Apply collection filter
            if collection_filter and metadata.get("collection_name") not in collection_filter:
                continue
            
            # Skip if below minimum similarity
            if similarity < min_similarity:
                continue
            
            # Calculate composite score
            semantic_score = similarity * config["semantic_weight"]
            collection_score = metadata.get("collection_weight", 1.0) * config["collection_weight"]
            strategy_score = metadata.get("strategy_weight", 1.0) * config["strategy_weight"]
            
            composite_score = semantic_score + collection_score + strategy_score
            
            composite_scores.append({
                "index": i,
                "composite_score": composite_score,
                "semantic_similarity": similarity,
                "collection_boost": collection_score,
                "strategy_boost": strategy_score,
                "metadata": metadata,
                "text": self.chunk_texts[i]
            })
        
        # Sort by composite score
        composite_scores.sort(key=lambda x: x["composite_score"], reverse=True)
        
        # Return top_k results
        results = composite_scores[:top_k]
        
        logger.info(f"✅ Found {len(results)} results (filtered from {len(similarities)} total)")
        
        return results
    
    def analyze_embedding_quality(self) -> Dict[str, Any]:
        """
        Analyze the quality of generated embeddings
        
        Returns:
            Quality metrics and analysis
        """
        
        if self.embeddings is None:
            raise ValueError("No embeddings to analyze. Generate embeddings first.")
        
        logger.info("📊 Analyzing embedding quality...")
        
        # Calculate similarity statistics
        all_similarities = cosine_similarity(self.embeddings)
        
        # Remove diagonal (self-similarity)
        mask = np.ones(all_similarities.shape, dtype=bool)
        np.fill_diagonal(mask, False)
        similarities_flat = all_similarities[mask]
        
        # Collection-based analysis
        collection_analysis = {}
        for collection in set(meta.get("collection_name") for meta in self.chunks_metadata):
            if collection:
                collection_indices = [
                    i for i, meta in enumerate(self.chunks_metadata) 
                    if meta.get("collection_name") == collection
                ]
                
                if len(collection_indices) > 1:
                    collection_embeddings = self.embeddings[collection_indices]
                    collection_similarities = cosine_similarity(collection_embeddings)
                    
                    # Remove diagonal
                    coll_mask = np.ones(collection_similarities.shape, dtype=bool)
                    np.fill_diagonal(coll_mask, False)
                    coll_sims = collection_similarities[coll_mask]
                    
                    collection_analysis[collection] = {
                        "chunk_count": len(collection_indices),
                        "mean_intra_similarity": float(np.mean(coll_sims)),
                        "std_intra_similarity": float(np.std(coll_sims)),
                        "max_intra_similarity": float(np.max(coll_sims)),
                        "min_intra_similarity": float(np.min(coll_sims))
                    }
        
        analysis = {
            "total_embeddings": len(self.embeddings),
            "embedding_dimension": self.embeddings.shape[1],
            "similarity_statistics": {
                "mean": float(np.mean(similarities_flat)),
                "std": float(np.std(similarities_flat)),
                "min": float(np.min(similarities_flat)),
                "max": float(np.max(similarities_flat)),
                "median": float(np.median(similarities_flat))
            },
            "collection_analysis": collection_analysis,
            "model_used": self.model_name
        }
        
        logger.info(f"📊 Quality analysis complete:")
        logger.info(f"   Mean similarity: {analysis['similarity_statistics']['mean']:.4f}")
        logger.info(f"   Std similarity: {analysis['similarity_statistics']['std']:.4f}")
        logger.info(f"   Collections analyzed: {len(collection_analysis)}")
        
        return analysis

def main():
    """Main function for testing the Ultimate Embedding Ranker"""
    
    embedder = UltimateEmbeddingRanker()
    
    # Load all chunks
    print("🔄 Loading chunks...")
    loading_results = embedder.load_all_chunks()
    
    if loading_results["total_chunks_loaded"] > 0:
        print(f"✅ Loaded {loading_results['total_chunks_loaded']} chunks")
        
        # Generate embeddings for first 100 chunks (test)
        print("🔄 Generating embeddings (test with first 100 chunks)...")
        embedder.chunk_texts = embedder.chunk_texts[:100]
        embedder.chunks_metadata = embedder.chunks_metadata[:100]
        
        embedding_results = embedder.generate_embeddings_batch(
            batch_size=16,
            save_path=r"C:\Users\raze0\Documents\LLM_KNOWLEDGE_CREATOR\RAG\RAG_CLEAN\TEST_EMBEDDINGS"
        )
        
        if embedding_results:
            print(f"✅ Generated {embedding_results['total_embeddings_generated']} embeddings")
            
            # Test search
            print("🔍 Testing semantic search...")
            results = embedder.semantic_search(
                "document processing and PDF conversion",
                top_k=5,
                ranking_mode="hybrid_balanced"
            )
            
            print(f"📋 Search results:")
            for i, result in enumerate(results):
                print(f"  {i+1}. Score: {result['composite_score']:.4f}")
                print(f"     Collection: {result['metadata'].get('collection_name')}")
                print(f"     Preview: {result['text'][:100]}...")
                print()
        
    else:
        print("❌ No chunks loaded!")

if __name__ == "__main__":
    main()