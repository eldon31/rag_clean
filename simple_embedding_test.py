#!/usr/bin/env python3
"""
Simple Embedding Test for Local CPU
Tests embedding pipeline with nomic-ai/CodeRankEmbed on small dataset
Optimized for local development before Kaggle T4 x2 deployment
"""

import json
import logging
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import time

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleEmbeddingTest:
    """Simple embedding test for local CPU validation"""
    
    def __init__(self, model_name: str = "nomic-ai/CodeRankEmbed"):
        """Initialize simple embedding test"""
        
        logger.info(f"🧪 Initializing Simple Embedding Test with {model_name}")
        
        # Load model (CPU-friendly)
        self.model = SentenceTransformer(model_name, trust_remote_code=True)
        self.model_name = model_name
        
        # Storage
        self.chunks = []
        self.embeddings = None
        
        logger.info("✅ Simple Embedding Test initialized")
    
    def load_sample_chunks(
        self, 
        chunks_dir: str = r"C:\Users\raze0\Documents\LLM_KNOWLEDGE_CREATOR\RAG\RAG_CLEAN\DOCS_CHUNKS_OUTPUT",
        max_chunks: int = 50
    ) -> Dict[str, Any]:
        """Load a small sample of chunks for testing"""
        
        logger.info(f"📂 Loading sample chunks (max: {max_chunks})")
        chunks_path = Path(chunks_dir)
        
        results = {
            "chunks_loaded": 0,
            "collections_sampled": {},
            "total_tokens": 0
        }
        
        # Sample from each collection
        for collection_dir in chunks_path.iterdir():
            if collection_dir.is_dir() and collection_dir.name != "__pycache__":
                collection_name = collection_dir.name
                collection_chunks = 0
                
                # Load first chunk file from each collection
                chunk_files = list(collection_dir.rglob("*_chunks.json"))
                if chunk_files and results["chunks_loaded"] < max_chunks:
                    try:
                        with open(chunk_files[0], 'r', encoding='utf-8') as f:
                            file_chunks = json.load(f)
                        
                        # Take first few chunks from this file
                        remaining = max_chunks - results["chunks_loaded"]
                        sample_chunks = file_chunks[:min(remaining, 10)]  # Max 10 per collection
                        
                        for chunk in sample_chunks:
                            # Add global ID
                            chunk["metadata"]["test_id"] = results["chunks_loaded"]
                            self.chunks.append(chunk)
                            results["chunks_loaded"] += 1
                            results["total_tokens"] += chunk["metadata"].get("token_count", 0)
                            collection_chunks += 1
                        
                        results["collections_sampled"][collection_name] = collection_chunks
                        logger.info(f"📄 Sampled {collection_chunks} chunks from {collection_name}")
                        
                    except Exception as e:
                        logger.error(f"❌ Error loading from {chunk_files[0]}: {e}")
        
        logger.info(f"✅ Loaded {results['chunks_loaded']} sample chunks")
        logger.info(f"📊 Collections: {results['collections_sampled']}")
        logger.info(f"🔢 Total tokens: {results['total_tokens']}")
        
        return results
    
    def generate_embeddings(self) -> Dict[str, Any]:
        """Generate embeddings for loaded chunks"""
        
        if not self.chunks:
            raise ValueError("No chunks loaded. Call load_sample_chunks() first.")
        
        logger.info(f"🔥 Generating embeddings for {len(self.chunks)} chunks")
        
        # Extract texts
        texts = [chunk["text"] for chunk in self.chunks]
        
        start_time = time.time()
        
        # Generate embeddings (CPU)
        logger.info("🔄 Processing embeddings...")
        self.embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        
        processing_time = time.time() - start_time
        
        results = {
            "embeddings_generated": len(self.embeddings),
            "embedding_dimension": self.embeddings.shape[1],
            "processing_time_seconds": processing_time,
            "embeddings_per_second": len(self.embeddings) / processing_time,
            "model_used": self.model_name
        }
        
        logger.info(f"✅ Generated {results['embeddings_generated']} embeddings")
        logger.info(f"📊 Dimension: {results['embedding_dimension']}")
        logger.info(f"⏱️ Time: {results['processing_time_seconds']:.2f}s")
        logger.info(f"🚀 Speed: {results['embeddings_per_second']:.1f} embeddings/second")
        
        return results
    
    def test_semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Test semantic search functionality"""
        
        if self.embeddings is None:
            raise ValueError("No embeddings generated. Call generate_embeddings() first.")
        
        logger.info(f"🔍 Testing search: '{query}' (top_k={top_k})")
        
        # Encode query
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for i, idx in enumerate(top_indices):
            result = {
                "rank": i + 1,
                "similarity": float(similarities[idx]),
                "chunk_metadata": self.chunks[idx]["metadata"],
                "text_preview": self.chunks[idx]["text"][:200] + "..."
            }
            results.append(result)
        
        logger.info(f"✅ Found {len(results)} results")
        for result in results:
            collection = result["chunk_metadata"].get("collection_name", "Unknown")
            logger.info(f"  {result['rank']}. {result['similarity']:.4f} - {collection}")
        
        return results
    
    def analyze_embeddings(self) -> Dict[str, Any]:
        """Analyze embedding quality"""
        
        if self.embeddings is None:
            raise ValueError("No embeddings to analyze.")
        
        logger.info("📊 Analyzing embedding quality...")
        
        # Calculate pairwise similarities
        similarities = cosine_similarity(self.embeddings)
        
        # Remove diagonal (self-similarity)
        mask = np.ones(similarities.shape, dtype=bool)
        np.fill_diagonal(mask, False)
        similarities_flat = similarities[mask]
        
        # Collection analysis
        collection_stats = {}
        collections = [chunk["metadata"].get("collection_name") for chunk in self.chunks]
        unique_collections = list(set(collections))
        
        for collection in unique_collections:
            if collection:
                indices = [i for i, c in enumerate(collections) if c == collection]
                if len(indices) > 1:
                    coll_embeddings = self.embeddings[indices]
                    coll_similarities = cosine_similarity(coll_embeddings)
                    
                    # Remove diagonal
                    coll_mask = np.ones(coll_similarities.shape, dtype=bool)
                    np.fill_diagonal(coll_mask, False)
                    coll_sims = coll_similarities[coll_mask]
                    
                    collection_stats[collection] = {
                        "chunk_count": len(indices),
                        "mean_intra_similarity": float(np.mean(coll_sims)),
                        "std_intra_similarity": float(np.std(coll_sims))
                    }
        
        analysis = {
            "total_embeddings": len(self.embeddings),
            "embedding_dimension": self.embeddings.shape[1],
            "overall_similarity_stats": {
                "mean": float(np.mean(similarities_flat)),
                "std": float(np.std(similarities_flat)),
                "min": float(np.min(similarities_flat)),
                "max": float(np.max(similarities_flat))
            },
            "collection_stats": collection_stats,
            "model_info": self.model_name
        }
        
        logger.info(f"📊 Analysis complete:")
        logger.info(f"   Overall mean similarity: {analysis['overall_similarity_stats']['mean']:.4f}")
        logger.info(f"   Collections analyzed: {len(collection_stats)}")
        
        return analysis
    
    def save_test_results(self, output_dir: str = "SIMPLE_EMBEDDING_TEST"):
        """Save test results"""
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save embeddings
        if self.embeddings is not None:
            np.save(str(output_path / "test_embeddings.npy"), self.embeddings)
        
        # Save chunks metadata
        chunks_metadata = [chunk["metadata"] for chunk in self.chunks]
        with open(output_path / "test_chunks_metadata.json", 'w', encoding='utf-8') as f:
            json.dump(chunks_metadata, f, indent=2, ensure_ascii=False)
        
        # Save chunk texts
        chunk_texts = [chunk["text"] for chunk in self.chunks]
        with open(output_path / "test_chunks_texts.json", 'w', encoding='utf-8') as f:
            json.dump(chunk_texts, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Test results saved to {output_path}")

def main():
    """Main test function"""
    
    print("🧪 Simple Embedding Test - Local CPU Version")
    print("=" * 50)
    
    # Initialize test
    embedder = SimpleEmbeddingTest()
    
    # Load sample chunks
    print("\n📂 Loading sample chunks...")
    loading_results = embedder.load_sample_chunks(max_chunks=30)  # Small test
    
    if loading_results["chunks_loaded"] > 0:
        print(f"✅ Loaded {loading_results['chunks_loaded']} chunks")
        
        # Generate embeddings
        print("\n🔥 Generating embeddings...")
        embedding_results = embedder.generate_embeddings()
        print(f"✅ Generated {embedding_results['embeddings_generated']} embeddings")
        print(f"⏱️ Processing time: {embedding_results['processing_time_seconds']:.2f}s")
        
        # Test searches
        test_queries = [
            "document processing and PDF conversion",
            "vector database and semantic search",
            "Python data validation with Pydantic",
            "API endpoints and REST documentation",
            "machine learning embeddings"
        ]
        
        print("\n🔍 Testing semantic search...")
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            results = embedder.test_semantic_search(query, top_k=3)
            for result in results:
                collection = result["chunk_metadata"].get("collection_name", "Unknown")
                print(f"  {result['rank']}. {result['similarity']:.4f} - {collection}")
        
        # Analyze quality
        print("\n📊 Analyzing embedding quality...")
        analysis = embedder.analyze_embeddings()
        print(f"Mean similarity: {analysis['overall_similarity_stats']['mean']:.4f}")
        print(f"Std similarity: {analysis['overall_similarity_stats']['std']:.4f}")
        
        # Save results
        print("\n💾 Saving test results...")
        embedder.save_test_results()
        
        print("\n🎉 Simple embedding test complete!")
        print("Ready for Kaggle T4 x2 enhancement! 🚀")
        
    else:
        print("❌ No chunks loaded - check your DOCS_CHUNKS_OUTPUT directory")

if __name__ == "__main__":
    main()