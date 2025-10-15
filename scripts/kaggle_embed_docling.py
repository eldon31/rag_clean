"""
Kaggle-optimized Docling Documentation Embedding Pipeline
For GPU T4 x2 with nomic-ai/nomic-embed-code (3584-dim, model parallelism)

This script processes Docling project documentation:
Collection name: docling

Input:
- Pre-chunked JSON files from output/docling/chunked/

Total: ~1060 chunks from 46 markdown files

UNIQUE ID STRATEGY:
- Format: docling:{filename}:chunk:{index}
- Example: docling:_docling-project_docling_1-overview.md:chunk:0

KAGGLE SETUP:
1. Upload this script to Kaggle
2. Upload the output/docling/chunked/ folder as a dataset
3. Set accelerator to GPU T4 x2
4. Run the notebook
5. Download the embeddings from /kaggle/working/
"""

import os

# Prevent transformers from attempting to load TensorFlow
os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
# Enable PyTorch memory optimization
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import hashlib

import numpy as np
import torch

# Guard against NumPy 2.x (Kaggle preinstalls 2.x)
if tuple(map(int, np.__version__.split(".")[:2])) >= (2, 0):
    raise RuntimeError(
        "NumPy 2.x detected. Please run `pip install -q --force-reinstall \"numpy==1.26.4\" \"scikit-learn==1.4.2\"` "
        "in a fresh Kaggle cell and restart the runtime before executing this script."
    )

# Check GPU availability
print(f"\n{'='*60}")
print("GPU SETUP")
print(f"{'='*60}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
if torch.cuda.is_available():
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        print(f"  Memory: {torch.cuda.get_device_properties(i).total_memory / 1e9:.2f} GB")
print(f"{'='*60}\n")

from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer

# Configuration
EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
BATCH_SIZE = 8  # Conservative for T4 GPUs
COLLECTION_NAME = "docling"
USE_MODEL_PARALLEL = True  # Use multi-GPU if available

# Paths - Works with git cloned repo in Kaggle
# Auto-detects if running in Kaggle or locally
CHUNKED_INPUT_DIR = Path("/kaggle/working/rad_clean/output/docling/chunked")

# Fallback to local path if not on Kaggle
if not CHUNKED_INPUT_DIR.exists():
    CHUNKED_INPUT_DIR = Path("output/docling/chunked")

# Output to /kaggle/working for easy download
KAGGLE_WORKING = Path("/kaggle/working")
if KAGGLE_WORKING.exists():
    OUTPUT_EMBEDDINGS_DIR = KAGGLE_WORKING
else:
    OUTPUT_EMBEDDINGS_DIR = Path("output/docling/embeddings")
    OUTPUT_EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

def string_to_id(text: str) -> int:
    """Convert string ID to integer using hash (for Qdrant)"""
    return int(hashlib.sha256(text.encode()).hexdigest(), 16) % (2**63)

def load_chunks() -> List[Dict]:
    """Load all pre-chunked JSON files"""
    print(f"\n{'='*60}")
    print("LOADING PRE-CHUNKED DATA")
    print(f"{'='*60}")
    print(f"Input directory: {CHUNKED_INPUT_DIR}")
    
    if not CHUNKED_INPUT_DIR.exists():
        raise FileNotFoundError(
            f"Chunked data not found at {CHUNKED_INPUT_DIR}\n"
            f"Please upload the output/docling/chunked/ folder as a Kaggle dataset"
        )
    
    all_chunks = []
    chunk_files = sorted(CHUNKED_INPUT_DIR.glob("*_chunks.json"))
    
    if not chunk_files:
        raise FileNotFoundError(
            f"No chunk files found in {CHUNKED_INPUT_DIR}\n"
            f"Expected files like: *_chunks.json"
        )
    
    print(f"Found {len(chunk_files)} chunk files\n")
    
    for chunk_file in chunk_files:
        try:
            with open(chunk_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            if chunks:
                all_chunks.extend(chunks)
                print(f"  ✓ {chunk_file.name}: {len(chunks)} chunks")
        
        except Exception as e:
            print(f"  ✗ Error loading {chunk_file.name}: {e}")
    
    print(f"\n{'='*60}")
    print(f"✓ Total chunks loaded: {len(all_chunks)}")
    print(f"{'='*60}\n")
    
    return all_chunks

def embed_chunks(chunks: List[dict]) -> List[dict]:
    """Generate embeddings using nomic-embed-code with GPU acceleration"""
    print(f"\n{'='*60}")
    print("GENERATING EMBEDDINGS")
    print(f"{'='*60}")
    print(f"Model: {EMBEDDING_MODEL}")
    print(f"Vector dimension: 3584")
    print(f"Batch size: {BATCH_SIZE}")
    
    num_gpus = torch.cuda.device_count()
    print(f"Available GPUs: {num_gpus}")
    print(f"Using model parallelism: {USE_MODEL_PARALLEL and num_gpus >= 2}")
    
    start_time = datetime.now()
    all_embeddings = []
    
    if USE_MODEL_PARALLEL and num_gpus >= 2:
        print("\n🚀 Loading model with OPTIMIZED model parallelism...")
        print("   Strategy: Layers distributed across GPUs")
        print("   Memory limits: GPU0=13GB, GPU1=13GB")
        
        tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL, trust_remote_code=True)
        
        # Load model with automatic device mapping (model parallelism)
        model = AutoModel.from_pretrained(
            EMBEDDING_MODEL,
            torch_dtype=torch.float16,  # Half precision for memory efficiency
            device_map="auto",  # Automatic layer distribution
            trust_remote_code=True
        )
        
        print("✓ Model loaded with multi-GPU distribution")
        
        def encode_batch(texts: List[str]) -> np.ndarray:
            """Encode texts using model parallelism"""
            inputs = tokenizer(
                texts,
                padding=True,
                truncation=True,
                max_length=2048,
                return_tensors="pt"
            )
            
            # Move inputs to first GPU
            inputs = {k: v.to('cuda:0') for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model(**inputs)
                # Mean pooling
                embeddings = outputs.last_hidden_state.mean(dim=1)
            
            return embeddings.cpu().numpy()
    
    else:
        # Single GPU or CPU fallback
        print("\n🚀 Loading model with SentenceTransformer...")
        model = SentenceTransformer(EMBEDDING_MODEL, trust_remote_code=True)
        
        if torch.cuda.is_available():
            model = model.to('cuda')
            print("✓ Model loaded on GPU")
        else:
            print("✓ Model loaded on CPU (will be slow)")
        
        def encode_batch(texts: List[str]) -> np.ndarray:
            return model.encode(texts, batch_size=BATCH_SIZE, show_progress_bar=False)
    
    # Process chunks in batches
    total_chunks = len(chunks)
    print(f"\nProcessing {total_chunks} chunks in batches of {BATCH_SIZE}...")
    
    for i in range(0, total_chunks, BATCH_SIZE):
        batch_chunks = chunks[i:i + BATCH_SIZE]
        texts = [chunk.get('content', '') for chunk in batch_chunks]
        
        # Generate embeddings
        embeddings = encode_batch(texts)
        
        # Create embedding data
        for idx, (chunk, embedding) in enumerate(zip(batch_chunks, embeddings)):
            chunk_id = chunk.get('chunk_id', f"chunk_{i + idx}")
            
            embedding_data = {
                "id": chunk_id,
                "text": chunk.get('content', ''),
                "embedding": embedding.tolist(),
                "metadata": chunk.get('metadata', {})
            }
            all_embeddings.append(embedding_data)
        
        # Cleanup
        del embeddings
        
        # Aggressive cache clearing every 5 batches
        if i % (BATCH_SIZE * 5) == 0 and torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Progress reporting
        processed = min(i + BATCH_SIZE, total_chunks)
        elapsed = (datetime.now() - start_time).total_seconds()
        rate = processed / elapsed if elapsed > 0 else 0
        eta = (total_chunks - processed) / rate if rate > 0 else 0
        
        print(f"  Progress: {processed}/{total_chunks} chunks "
              f"({processed/total_chunks*100:.1f}%) - "
              f"{rate:.1f} chunks/sec - ETA: {eta/60:.1f} min")
    
    # Save embeddings
    output_file = OUTPUT_EMBEDDINGS_DIR / f"{COLLECTION_NAME}_embeddings.jsonl"
    print(f"\n💾 Saving embeddings to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for embedding_data in all_embeddings:
            f.write(json.dumps(embedding_data, ensure_ascii=False) + '\n')
    
    elapsed_time = (datetime.now() - start_time).total_seconds()
    print(f"✓ Embeddings saved: {len(all_embeddings)} chunks")
    print(f"✓ Time elapsed: {elapsed_time/60:.1f} minutes")
    print(f"✓ Average speed: {len(all_embeddings)/elapsed_time:.1f} chunks/sec")
    
    return all_embeddings

def save_summary(chunks: List[Dict], embeddings: List[Dict], elapsed_time: float):
    """Save processing summary"""
    summary_file = OUTPUT_EMBEDDINGS_DIR / f"{COLLECTION_NAME}_embedding_summary.json"
    
    summary = {
        "collection": COLLECTION_NAME,
        "timestamp": datetime.now().isoformat(),
        "model": EMBEDDING_MODEL,
        "vector_dimension": 3584,
        "total_chunks": len(chunks),
        "total_embeddings": len(embeddings),
        "processing_time_minutes": round(elapsed_time / 60, 2),
        "average_speed_chunks_per_sec": round(len(embeddings) / elapsed_time, 2),
        "gpu_count": torch.cuda.device_count(),
        "batch_size": BATCH_SIZE,
        "files_processed": len(set(c["metadata"]["source"] for c in chunks if "metadata" in c and "source" in c["metadata"])),
    }
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Summary saved to {summary_file}")
    return summary

def main():
    """Main pipeline execution"""
    pipeline_start = datetime.now()
    
    print(f"\n{'='*60}")
    print("DOCLING DOCS EMBEDDING PIPELINE")
    print(f"{'='*60}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Model: {EMBEDDING_MODEL}")
    print(f"Input: {CHUNKED_INPUT_DIR}")
    print(f"Output: {OUTPUT_EMBEDDINGS_DIR}")
    print(f"Started: {pipeline_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # Load pre-chunked data
    chunks = load_chunks()
    
    if not chunks:
        print("❌ No chunks loaded!")
        return
    
    # Generate embeddings
    embeddings = embed_chunks(chunks)
    
    # Calculate total time
    pipeline_end = datetime.now()
    total_time = (pipeline_end - pipeline_start).total_seconds()
    
    # Save summary
    summary = save_summary(chunks, embeddings, total_time)
    
    print(f"\n{'='*60}")
    print("✓ PIPELINE COMPLETED")
    print(f"{'='*60}")
    print(f"Total chunks: {summary['total_chunks']}")
    print(f"Total embeddings: {summary['total_embeddings']}")
    print(f"Vector dimension: {summary['vector_dimension']}")
    print(f"Total time: {summary['processing_time_minutes']} minutes")
    print(f"Average speed: {summary['average_speed_chunks_per_sec']} chunks/sec")
    print(f"Output file: {OUTPUT_EMBEDDINGS_DIR / f'{COLLECTION_NAME}_embeddings.jsonl'}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"{'='*60}\n")
    
    print("\n📦 NEXT STEPS:")
    print("1. Download the embeddings file from /kaggle/working/")
    print("2. Upload to Qdrant using upload_to_qdrant.py")
    print("3. Or use the embeddings directly in your RAG application")

if __name__ == "__main__":
    main()
