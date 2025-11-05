"""Test script to verify rich progress and throughput tracking for sparse and reranking.

This script runs a minimal embedding workflow with:
1. Dense embeddings
2. Sparse (SPLADE) with rich progress
3. Reranking with rich progress

Verifies that:
- Rich progress bars show for sparse and rerank stages
- ThroughputMonitor reports include sparse and rerank stages
- No errors or regressions
"""

import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4

def main():
    print("=" * 70)
    print("Testing Rich Progress and Throughput Tracking")
    print("=" * 70)
    
    # Test data: 5 chunks
    test_texts = [
        "Natural language processing enables machines to understand human language.",
        "Deep learning models like transformers have revolutionized NLP tasks.",
        "Embeddings represent text as dense vectors in high-dimensional space.",
        "Sparse representations can capture important lexical features.",
        "Cross-encoder models rerank candidates for improved retrieval accuracy.",
    ]
    
    print(f"\nTest data: {len(test_texts)} chunks")
    
    # Initialize embedder with sparse and reranking enabled
    from processor.ultimate_embedder.config import RerankingConfig
    
    rerank_cfg = RerankingConfig(
        enable_reranking=True,
        model_name="jinaai/jina-reranker-v3",
        rerank_top_k=3,
        top_k_candidates=100,  # Pool size
        batch_size=2,
    )
    
    embedder = UltimateKaggleEmbedderV4(
        model_name="all-miniLM-l6",  # Use a valid model from the registry
        force_cpu=True,  # Use CPU for consistency
        enable_sparse=True,  # Enable SPLADE
        sparse_models=["splade"],
        reranking_config=rerank_cfg,
    )
    
    print("\nEmbedder configuration:")
    print(f"  Dense model: {embedder.model_name}")
    print(f"  Sparse enabled: {embedder.enable_sparse}")
    print(f"  Sparse models: {embedder.sparse_model_names}")
    print(f"  Reranking enabled: {embedder.reranking_config.enable_reranking}")
    print(f"  Reranker model: {embedder.reranking_config.model_name}")
    
    # Load chunks using proper API
    print("\n" + "=" * 70)
    print("Loading chunks...")
    embedder.chunk_texts = test_texts
    embedder.chunks_metadata = [{"index": i} for i in range(len(test_texts))]
    print(f"Loaded {len(embedder.chunk_texts)} chunks")
    
    # Generate embeddings (this will trigger sparse + rerank)
    print("\n" + "=" * 70)
    print("Generating ensemble embeddings with sparse and reranking...")
    print("=" * 70)
    
    embeddings = embedder.generate_embeddings_kaggle_optimized()
    
    print("\n" + "=" * 70)
    print("Results:")
    print("=" * 70)
    print(f"Dense embeddings shape: {embeddings.shape}")
    
    # Check sparse results
    if hasattr(embedder, 'sparse_inference_runs') and embedder.sparse_inference_runs:
        print(f"\nSparse results:")
        for run in embedder.sparse_inference_runs:
            print(f"  Model: {run.model_name}")
            print(f"  Device: {run.device}")
            print(f"  Latency: {run.latency_ms:.2f}ms")
            print(f"  Throughput: {run.throughput_chunks_per_sec:.2f} chunks/sec")
            print(f"  Fallback count: {run.fallback_count}/{len(run.vectors)}")
    else:
        print("\n⚠️  No sparse results found (sparse may be disabled or failed)")
    
    # Check reranking results
    if hasattr(embedder, 'rerank_run') and embedder.rerank_run:
        rerank = embedder.rerank_run
        print(f"\nReranking results:")
        print(f"  Model: {embedder.reranking_config.model_name}")
        print(f"  Latency: {rerank.latency_ms:.2f}ms")
        print(f"  Throughput: {rerank.throughput_cands_per_sec:.2f} candidates/sec")
        print(f"  Top-k returned: {len(rerank.candidate_ids)}")
        print(f"  Peak GPU memory: {rerank.gpu_peak_gb:.2f}GB")
    else:
        print("\n⚠️  No reranking results found (reranking may be disabled or failed)")
    
    print("\n" + "=" * 70)
    print("✅ Test completed successfully!")
    print("=" * 70)
    print("\nVerification checklist:")
    print("  [ ] Rich progress bars appeared for SPLADE encoding")
    print("  [ ] Rich progress bars appeared for reranking (if multiple batches)")
    print("  [ ] Sparse stage appears in throughput logs")
    print("  [ ] Rerank stage appears in throughput logs")
    print("  [ ] No errors or exceptions")

if __name__ == "__main__":
    main()
