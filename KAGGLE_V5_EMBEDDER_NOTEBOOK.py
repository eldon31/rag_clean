#!/usr/bin/env python3
"""
KAGGLE V5 EMBEDDER - Complete Notebook Script
Optimized for Kaggle T4 x2 GPU Environment

SETUP:
1. Upload this notebook to Kaggle
2. Enable GPU (T4 x2)
3. Enable Internet
4. Run all cells

PATHS:
- Input: /kaggle/working/rag_clean/Chunked
- Output: /kaggle/working/rag_clean/Embeddings
- Models: /kaggle/working/models (auto-downloaded)
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# ============================================================================
# STEP 1: ENVIRONMENT SETUP
# ============================================================================

print("="*70)
print("KAGGLE V5 EMBEDDER - SETUP")
print("="*70)

# Set working directory
os.chdir("/kaggle/working")

# Create directory structure
directories = [
    "/kaggle/working/rag_clean",
    "/kaggle/working/rag_clean/Chunked",
    "/kaggle/working/rag_clean/Embeddings",
    "/kaggle/working/models",
    "/kaggle/working/processor"
]

for directory in directories:
    Path(directory).mkdir(parents=True, exist_ok=True)
    print(f"✓ Created: {directory}")

# ============================================================================
# STEP 2: INSTALL DEPENDENCIES
# ============================================================================

print("\n" + "="*70)
print("INSTALLING DEPENDENCIES")
print("="*70)

dependencies = [
    "sentence-transformers>=2.2.2",
    "transformers>=4.30.0",
    "torch>=2.0.0",
    "numpy>=1.24.0",
    "scikit-learn>=1.3.0",
    "faiss-gpu>=1.7.2",  # GPU version for Kaggle
    "psutil>=5.9.0",
    "qdrant-client>=1.7.0",
]

for package in dependencies:
    print(f"Installing {package}...")
    os.system(f"pip install -q {package}")

print("✓ All dependencies installed")

# ============================================================================
# STEP 3: DOWNLOAD V5 MODELS
# ============================================================================

print("\n" + "="*70)
print("DOWNLOADING V5 MODELS FROM HUGGINGFACE")
print("="*70)

# Model configurations with HuggingFace IDs
V5_MODELS = {
    "primary": {
        "name": "jina-code-embeddings-1.5b",
        "hf_id": "jinaai/jina-code-embeddings-1.5b",
        "size_gb": 3.0,
        "description": "Primary code embedding model (1536D, 32K tokens)"
    },
    "secondary": {
        "name": "bge-m3",
        "hf_id": "BAAI/bge-m3",
        "size_gb": 2.2,
        "description": "Multi-modal retrieval (1024D, 8K tokens)"
    },
    "reranker": {
        "name": "jina-reranker-v3",
        "hf_id": "jinaai/jina-reranker-v3",
        "size_gb": 1.2,
        "description": "CrossEncoder reranker (0.6B params, 131K tokens)"
    },
    "sparse": {
        "name": "qdrant-bm25",
        "hf_id": "Qdrant/bm25",
        "size_gb": 0.4,
        "description": "BM25 sparse vectors"
    },
    "onnx_fast": {
        "name": "qdrant-minilm-onnx",
        "hf_id": "Qdrant/all-MiniLM-L6-v2-onnx",
        "size_gb": 0.08,
        "description": "ONNX optimized (384D, 256 tokens)"
    }
}

# Download models
downloaded_models = []

for model_key, config in V5_MODELS.items():
    print(f"\n📥 Downloading {config['name']}...")
    print(f"   HF ID: {config['hf_id']}")
    print(f"   Size: ~{config['size_gb']} GB")
    print(f"   Description: {config['description']}")
    
    try:
        # Use huggingface-cli for reliable downloads
        cmd = f"huggingface-cli download {config['hf_id']} --local-dir /kaggle/working/models/{config['name']} --local-dir-use-symlinks False"
        result = os.system(cmd)
        
        if result == 0:
            print(f"   ✓ Downloaded successfully")
            downloaded_models.append(config['name'])
        else:
            print(f"   ⚠️  Download failed (exit code {result})")
    
    except Exception as e:
        print(f"   ✗ Error: {e}")

print(f"\n✓ Downloaded {len(downloaded_models)}/{len(V5_MODELS)} models")
print(f"Models: {', '.join(downloaded_models)}")

# ============================================================================
# STEP 4: COPY EMBEDDER CODE
# ============================================================================

print("\n" + "="*70)
print("SETTING UP EMBEDDER CODE")
print("="*70)

# Note: In Kaggle, you'll need to upload processor/kaggle_ultimate_embedder_v4.py
# as a dataset or copy it here

# For now, we'll use the uploaded file
if Path("/kaggle/input/rag-clean/processor/kaggle_ultimate_embedder_v4.py").exists():
    shutil.copy(
        "/kaggle/input/rag-clean/processor/kaggle_ultimate_embedder_v4.py",
        "/kaggle/working/processor/kaggle_ultimate_embedder_v4.py"
    )
    print("✓ Copied embedder from input dataset")
else:
    print("⚠️  Embedder not found in /kaggle/input/rag-clean/processor/")
    print("   Upload processor/kaggle_ultimate_embedder_v4.py as a Kaggle dataset")

# Add to Python path
sys.path.insert(0, "/kaggle/working")

# ============================================================================
# STEP 5: VERIFY CHUNKS INPUT
# ============================================================================

print("\n" + "="*70)
print("VERIFYING CHUNKS INPUT")
print("="*70)

chunks_dir = Path("/kaggle/working/rag_clean/Chunked")

if not chunks_dir.exists():
    print("⚠️  Chunks directory not found!")
    print("   Expected: /kaggle/working/rag_clean/Chunked")
    print("   Please upload your chunked documents as a Kaggle dataset")
    sys.exit(1)

# Count chunks
json_files = list(chunks_dir.rglob("*.json"))
total_chunks = 0

for json_file in json_files:
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                total_chunks += len(data)
    except Exception as e:
        print(f"   Warning: Could not read {json_file.name}: {e}")

print(f"✓ Found {len(json_files)} JSON files")
print(f"✓ Total chunks to embed: {total_chunks:,}")

# ============================================================================
# STEP 6: INITIALIZE EMBEDDER
# ============================================================================

print("\n" + "="*70)
print("INITIALIZING V5 EMBEDDER")
print("="*70)

from processor.kaggle_ultimate_embedder_v4 import (
    UltimateKaggleEmbedderV4,
    KaggleGPUConfig,
    KaggleExportConfig,
    RerankingConfig
)

# GPU Configuration for Kaggle T4 x2
gpu_config = KaggleGPUConfig(
    device_count=2,  # T4 x2
    vram_per_gpu_gb=15.83,
    total_vram_gb=31.66,
    max_memory_per_gpu=0.8,  # Use 80% per GPU
    enable_memory_efficient_attention=True,
    precision="fp16",  # Half precision for T4
    enable_mixed_precision=True,
    base_batch_size=32,
    dynamic_batching=True,
    backend="pytorch",  # Use PyTorch (or "onnx" for faster CPU)
    enable_torch_compile=True,
    kaggle_environment=True,
    output_path="/kaggle/working/rag_clean/Embeddings"
)

# Export Configuration
export_config = KaggleExportConfig(
    export_numpy=True,
    export_jsonl=True,
    export_faiss=True,
    export_pickle=False,
    export_sparse_jsonl=True,
    compress_embeddings=True,
    include_full_metadata=True,
    working_dir="/kaggle/working/rag_clean/Embeddings",
    output_prefix="v5_embeddings"
)

# Reranking Configuration (optional - adds 10-15% processing time)
reranking_config = RerankingConfig(
    model_name="jina-reranker-v3",
    enable_reranking=False,  # Disable for faster processing
    top_k_candidates=100,
    rerank_top_k=20
)

# Initialize embedder
print("Initializing embedder with:")
print(f"  Primary Model: jina-code-embeddings-1.5b")
print(f"  GPU Config: T4 x2, FP16, {gpu_config.base_batch_size} batch size")
print(f"  Sparse Vectors: Enabled")
print(f"  Reranking: {'Enabled' if reranking_config.enable_reranking else 'Disabled'}")

embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    gpu_config=gpu_config,
    export_config=export_config,
    reranking_config=reranking_config,
    enable_sparse=True,
    sparse_models=["qdrant-bm25"],
    matryoshka_dim=1536,  # Full dimension (or 768/512 for smaller)
)

print("✓ Embedder initialized successfully")

# ============================================================================
# STEP 7: LOAD CHUNKS
# ============================================================================

print("\n" + "="*70)
print("LOADING CHUNKS")
print("="*70)

loading_results = embedder.load_chunks_from_processing(
    chunks_dir="/kaggle/working/rag_clean/Chunked"
)

print(f"✓ Collections loaded: {loading_results['collections_loaded']}")
print(f"✓ Total chunks loaded: {loading_results['total_chunks_loaded']:,}")
print(f"✓ Memory usage: {loading_results['memory_usage_mb']:.1f} MB")

if loading_results.get('preprocessing_stats'):
    cache_stats = loading_results['preprocessing_stats']
    print(f"✓ Cache hit rate: {cache_stats.get('hit_rate', 0):.1%}")

print(f"\nChunks by collection:")
for collection, count in loading_results['chunks_by_collection'].items():
    print(f"  - {collection}: {count:,} chunks")

if loading_results.get('modal_hint_counts'):
    print(f"\nContent types detected:")
    for modal, count in loading_results['modal_hint_counts'].items():
        print(f"  - {modal}: {count:,} chunks")

# ============================================================================
# STEP 8: GENERATE EMBEDDINGS
# ============================================================================

print("\n" + "="*70)
print("GENERATING EMBEDDINGS (Kaggle T4 x2 Optimized)")
print("="*70)
print("This may take 10-30 minutes depending on chunk count...")
print("Monitoring GPU usage in real-time...\n")

start_time = datetime.now()

embedding_results = embedder.generate_embeddings_kaggle_optimized(
    enable_monitoring=True,
    save_intermediate=True
)

end_time = datetime.now()
duration = (end_time - start_time).total_seconds()

print(f"\n✓ Embedding generation complete!")
print(f"  Total embeddings: {embedding_results['total_embeddings_generated']:,}")
print(f"  Embedding dimension: {embedding_results['embedding_dimension']}")
print(f"  Processing time: {duration:.1f}s ({duration/60:.1f} minutes)")
print(f"  Speed: {embedding_results['chunks_per_second']:.1f} chunks/second")
print(f"  GPU count: {embedding_results['gpu_count']}")
print(f"  Batch size: {embedding_results['optimal_batch_size']}")
print(f"  Memory usage: {embedding_results['embedding_memory_mb']:.1f} MB")
print(f"  Memory per chunk: {embedding_results['memory_per_chunk_kb']:.2f} KB")

# ============================================================================
# STEP 9: EXPORT FOR LOCAL QDRANT
# ============================================================================

print("\n" + "="*70)
print("EXPORTING FOR LOCAL QDRANT")
print("="*70)

exported_files = embedder.export_for_local_qdrant()

print(f"✓ Exported {len(exported_files)} files:")
for file_type, file_path in exported_files.items():
    if file_type == "qdrant_collection":
        print(f"  - Target collection: {file_path}")
        continue
    
    file_size = os.path.getsize(file_path) / 1024 / 1024
    print(f"  - {file_type}: {os.path.basename(file_path)} ({file_size:.1f} MB)")

# ============================================================================
# STEP 10: CREATE DOWNLOAD ZIP
# ============================================================================

print("\n" + "="*70)
print("CREATING DOWNLOAD ZIP")
print("="*70)

embeddings_dir = Path("/kaggle/working/rag_clean/Embeddings")
zip_path = Path("/kaggle/working/v5_embeddings_complete.zip")

# Create zip file
import zipfile

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file_path in embeddings_dir.rglob("*"):
        if file_path.is_file():
            arcname = file_path.relative_to(embeddings_dir.parent)
            zipf.write(file_path, arcname=arcname)
            print(f"  Added: {arcname}")

zip_size = zip_path.stat().st_size / 1024 / 1024
print(f"\n✓ Created zip file: {zip_path}")
print(f"  Size: {zip_size:.1f} MB")
print(f"  Ready for download from Kaggle output panel")

# ============================================================================
# STEP 11: GENERATE SUMMARY REPORT
# ============================================================================

print("\n" + "="*70)
print("GENERATING SUMMARY REPORT")
print("="*70)

summary = {
    "generation_timestamp": datetime.now().isoformat(),
    "kaggle_environment": True,
    "gpu_config": {
        "device_count": gpu_config.device_count,
        "backend": gpu_config.backend,
        "precision": gpu_config.precision,
        "batch_size": embedding_results['optimal_batch_size']
    },
    "model_info": {
        "primary_model": "jina-code-embeddings-1.5b",
        "embedding_dimension": embedding_results['embedding_dimension'],
        "matryoshka_dimension": 1536,
        "sparse_enabled": True,
        "reranking_enabled": reranking_config.enable_reranking
    },
    "processing_stats": {
        "total_chunks": loading_results['total_chunks_loaded'],
        "total_embeddings": embedding_results['total_embeddings_generated'],
        "processing_time_seconds": duration,
        "chunks_per_second": embedding_results['chunks_per_second'],
        "memory_usage_mb": embedding_results['embedding_memory_mb']
    },
    "collections_processed": loading_results['chunks_by_collection'],
    "modal_distribution": loading_results.get('modal_hint_counts', {}),
    "exported_files": {
        k: os.path.basename(v) if isinstance(v, str) and os.path.exists(v) else v
        for k, v in exported_files.items()
    },
    "download": {
        "zip_file": str(zip_path.name),
        "zip_size_mb": zip_size,
        "location": "Kaggle output panel"
    },
    "next_steps": [
        "1. Download v5_embeddings_complete.zip from Kaggle output",
        "2. Extract on local machine",
        "3. Run upload script: python v5_embeddings_upload_script.py",
        "4. Verify in Qdrant: http://localhost:6333/dashboard"
    ]
}

summary_path = embeddings_dir / "embedding_summary.json"
with open(summary_path, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f"✓ Summary saved to: {summary_path}")

# ============================================================================
# FINAL OUTPUT
# ============================================================================

print("\n" + "="*70)
print("✅ EMBEDDING GENERATION COMPLETE")
print("="*70)
print(f"\n📊 Processing Summary:")
print(f"  Chunks processed: {loading_results['total_chunks_loaded']:,}")
print(f"  Embeddings generated: {embedding_results['total_embeddings_generated']:,}")
print(f"  Dimension: {embedding_results['embedding_dimension']}D")
print(f"  Processing time: {duration/60:.1f} minutes")
print(f"  Average speed: {embedding_results['chunks_per_second']:.1f} chunks/sec")
print(f"\n📦 Download:")
print(f"  File: {zip_path.name}")
print(f"  Size: {zip_size:.1f} MB")
print(f"  Location: Kaggle output panel → Download")
print(f"\n🎯 Next Steps:")
print(f"  1. Download the zip file")
print(f"  2. Extract on your local machine")
print(f"  3. Run the upload script: python v5_embeddings_upload_script.py")
print(f"  4. Access Qdrant: http://localhost:6333/dashboard")
print("\n" + "="*70)

# Save summary to easily accessible location
with open("/kaggle/working/EMBEDDING_SUMMARY.txt", 'w') as f:
    f.write(f"V5 Embedding Generation Complete\n")
    f.write(f"="*50 + "\n\n")
    f.write(f"Timestamp: {datetime.now().isoformat()}\n")
    f.write(f"Chunks: {loading_results['total_chunks_loaded']:,}\n")
    f.write(f"Embeddings: {embedding_results['total_embeddings_generated']:,}\n")
    f.write(f"Dimension: {embedding_results['embedding_dimension']}D\n")
    f.write(f"Time: {duration/60:.1f} minutes\n")
    f.write(f"Speed: {embedding_results['chunks_per_second']:.1f} chunks/sec\n")
    f.write(f"\nDownload: {zip_path.name} ({zip_size:.1f} MB)\n")

print("="*70)
print("All done! Check the output panel to download your embeddings.")
print("="*70)