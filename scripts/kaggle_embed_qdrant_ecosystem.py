"""
Kaggle-optimized Qdrant Ecosystem Embedding Pipeline
For GPU T4 x2 with nomic-ai/nomic-embed-code (768-dim, data parallelism)

This script processes Qdrant ecosystem documentation:
Collection name: qdrant_ecosystem

Input:
- Pre-chunked JSON files from output/qdrant_ecosystem/ subdirectories

UNIQUE ID STRATEGY:
- Format: qdrant_ecosystem:{subdir}:{filename}:chunk:{index}
- Example: qdrant_ecosystem:qdrant_client_docs:_qdrant_qdrant-client_1-overview_chunks.json:chunk:0

KAGGLE SETUP:
1. Upload this script to Kaggle
2. Upload the output/qdrant_ecosystem/ folder as a dataset
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
from typing import List, Dict, Callable, Optional
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

def validate_gpu_setup():
    """Validate GPU setup and calculate optimal batch size"""
    print(f"\n{'='*60}")
    print("GPU VALIDATION & BATCH SIZE CALCULATION")
    print(f"{'='*60}")

    if not torch.cuda.is_available():
        print("❌ No CUDA GPUs detected!")
        return False

    num_gpus = torch.cuda.device_count()
    print(f"✓ {num_gpus} GPU(s) detected")

    # Check each GPU
    for i in range(num_gpus):
        props = torch.cuda.get_device_properties(i)
        vram_gb = props.total_memory / 1e9
        print(f"GPU {i}: {props.name} - {vram_gb:.2f} GB VRAM")

        if abs(vram_gb - EXPECTED_GPU_VRAM_GB) > 1.0:  # Allow 1GB tolerance
            print(f"⚠ Warning: Expected ~{EXPECTED_GPU_VRAM_GB} GB VRAM, got {vram_gb:.2f} GB")
        else:
            print(f"✓ VRAM matches expected Tesla T4 specification")

    # Calculate optimal batch size
    available_vram_per_gpu = EXPECTED_GPU_VRAM_GB - MODEL_VRAM_GB - VRAM_BUFFER_GB
    max_batch_per_gpu = int(available_vram_per_gpu / CHUNK_VRAM_ESTIMATE_GB)

    if USE_DATA_PARALLEL and num_gpus >= 2:
        total_max_batch = max_batch_per_gpu * 2
    else:
        total_max_batch = max_batch_per_gpu

    # Cap at 24 as per spec
    optimal_batch = min(total_max_batch, 24)

    print(f"\nBatch Size Calculation:")
    print(f"  Model VRAM: {MODEL_VRAM_GB} GB")
    print(f"  Safety buffer: {VRAM_BUFFER_GB} GB")
    print(f"  Available VRAM per GPU: {available_vram_per_gpu:.2f} GB")
    print(f"  Max chunks per GPU: {max_batch_per_gpu}")
    print(f"  Data parallelism: {USE_DATA_PARALLEL and num_gpus >= 2}")
    print(f"  Optimal batch size: {optimal_batch}")

    global BATCH_SIZE
    if optimal_batch < BATCH_SIZE:
        print(f"⚠ Reducing batch size from {BATCH_SIZE} to {optimal_batch} due to VRAM constraints")
        BATCH_SIZE = optimal_batch
    else:
        print(f"✓ Using configured batch size: {BATCH_SIZE}")

    print(f"{'='*60}\n")
    return True

from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer

# Configuration
EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
BATCH_SIZE = 24  # Optimized for 15.83GB VRAM per T4 (with 2GB buffer)
COLLECTION_NAME = "qdrant_ecosystem"
USE_DATA_PARALLEL = True  # Use data parallelism for speed

# Model specs
MODEL_VRAM_GB = 6.8  # nomic-embed-code VRAM usage
MODEL_DIMENSION = 768
MODEL_MAX_TOKENS = 2048
CHUNK_VRAM_ESTIMATE_GB = 0.15  # Estimated VRAM per chunk
VRAM_BUFFER_GB = 2.0  # Safety buffer
EXPECTED_GPU_VRAM_GB = 15.83  # Tesla T4 VRAM
MODEL_TORCH_DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32
MODEL_KWARGS = {"torch_dtype": MODEL_TORCH_DTYPE}

# Paths - Works with git cloned repo in Kaggle
# Auto-detects if running in Kaggle or locally
ECOSYSTEM_INPUT_DIR = Path("/kaggle/working/rad_clean/output/qdrant_ecosystem")

# Fallback to local path if not on Kaggle or repo cloned elsewhere
if not ECOSYSTEM_INPUT_DIR.exists():
    ECOSYSTEM_INPUT_DIR = Path("output/qdrant_ecosystem")


def _maybe_copy_from_kaggle_inputs(target_dir: Path) -> None:
    """Copy dataset from /kaggle/input into target_dir if present."""
    kaggle_input_root = Path("/kaggle/input")
    if not kaggle_input_root.exists():
        return

    import shutil

    for dataset_dir in sorted(kaggle_input_root.iterdir()):
        if not dataset_dir.is_dir():
            continue

        candidate_paths = [
            dataset_dir / "output" / "qdrant_ecosystem",
            dataset_dir / "qdrant_ecosystem",
        ]

        for candidate in candidate_paths:
            if candidate.exists() and any(candidate.glob("**/*_chunks.json")):
                print(f"Found qdrant_ecosystem data in Kaggle dataset: {candidate}")
                target_dir.mkdir(parents=True, exist_ok=True)
                shutil.copytree(candidate, target_dir, dirs_exist_ok=True)
                print(f"Copied dataset to: {target_dir.resolve()}")
                return


if not ECOSYSTEM_INPUT_DIR.exists():
    _maybe_copy_from_kaggle_inputs(ECOSYSTEM_INPUT_DIR)

# Output to /kaggle/working for easy download
KAGGLE_WORKING = Path("/kaggle/working")
if KAGGLE_WORKING.exists():
    OUTPUT_EMBEDDINGS_DIR = KAGGLE_WORKING
else:
    OUTPUT_EMBEDDINGS_DIR = Path("output/qdrant_ecosystem/embeddings")
    OUTPUT_EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

def string_to_id(text: str) -> int:
    """Convert string ID to integer using hash (for Qdrant)"""
    return int(hashlib.sha256(text.encode()).hexdigest(), 16) % (2**63)

def load_chunks() -> List[Dict]:
    """Load all pre-chunked JSON files from qdrant_ecosystem subdirectories"""
    print(f"\n{'='*60}")
    print("LOADING PRE-CHUNKED QDRANT ECOSYSTEM DATA")
    print(f"{'='*60}")
    print(f"Input directory: {ECOSYSTEM_INPUT_DIR}")

    if not ECOSYSTEM_INPUT_DIR.exists():
        raise FileNotFoundError(
            f"Ecosystem data not found at {ECOSYSTEM_INPUT_DIR}\n"
            f"Please upload the output/qdrant_ecosystem/ folder as a Kaggle dataset"
        )

    # Auto-detect subdirectories
    subdirs = [d for d in ECOSYSTEM_INPUT_DIR.iterdir() if d.is_dir()]
    if not subdirs:
        raise FileNotFoundError(
            f"No subdirectories found in {ECOSYSTEM_INPUT_DIR}\n"
            f"Expected subdirectories like: qdrant_client_docs, qdrant_documentation, etc."
        )

    print(f"Found {len(subdirs)} subdirectories: {[d.name for d in subdirs]}")

    all_chunks = []
    total_files = 0

    for subdir in subdirs:
        chunk_files = sorted(subdir.glob("*_chunks.json"))
        if not chunk_files:
            print(f"  ⚠ No chunk files in {subdir.name}")
            continue

        print(f"\n  Processing {subdir.name}: {len(chunk_files)} files")

        for chunk_file in chunk_files:
            try:
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)

                if chunks:
                    # Enrich metadata with subdirectory info
                    normalized_chunks = []
                    for raw_chunk in chunks:
                        if not isinstance(raw_chunk, dict):
                            chunk = {
                                "content": str(raw_chunk),
                                "metadata": {}
                            }
                        else:
                            chunk = dict(raw_chunk)

                        metadata = chunk.get('metadata')
                        if not isinstance(metadata, dict):
                            metadata = dict(metadata) if metadata else {}
                            chunk['metadata'] = metadata

                        metadata.setdefault('subdirectory', subdir.name)
                        metadata.setdefault('source_file', chunk_file.name)
                        normalized_chunks.append(chunk)

                    chunks = normalized_chunks

                    all_chunks.extend(chunks)
                    print(f"    ✓ {chunk_file.name}: {len(chunks)} chunks")

            except Exception as e:
                print(f"    ✗ Error loading {chunk_file.name}: {e}")

        total_files += len(chunk_files)

    print(f"\n{'='*60}")
    print(f"✓ Total chunks loaded: {len(all_chunks)} from {total_files} files")
    print(f"✓ Subdirectories processed: {len(subdirs)}")
    print(f"{'='*60}\n")

    return all_chunks

def embed_chunks(chunks: List[dict]) -> List[dict]:
    """Generate embeddings using nomic-embed-code with GPU acceleration"""
    global BATCH_SIZE
    print(f"\n{'='*60}")
    print("GENERATING EMBEDDINGS")
    print(f"{'='*60}")
    print(f"Model: {EMBEDDING_MODEL}")
    print(f"Vector dimension: {MODEL_DIMENSION}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Model dtype: {MODEL_TORCH_DTYPE}")

    num_gpus = torch.cuda.device_count()
    print(f"Available GPUs: {num_gpus}")

    desired_parallel = USE_DATA_PARALLEL and num_gpus >= 2
    print(f"Desired data parallelism: {desired_parallel}")

    start_time = datetime.now()
    all_embeddings = []
    encode_batch_fn: Optional[Callable[[List[str]], np.ndarray]] = None
    actual_parallel = False
    model_gpu0 = model_gpu1 = None
    model = None

    if desired_parallel:
        try:
            print("\n🚀 Loading model with DATA PARALLELISM for MAXIMUM SPEED...")
            print("   Strategy: Full model on each GPU, split batches")
            print("   GPU 0: Process batch[0::2] (even indices)")
            print("   GPU 1: Process batch[1::2] (odd indices)")
            print(f"   Effective batch size: {BATCH_SIZE} ({BATCH_SIZE//2} per GPU)")

            # Load model on GPU 0
            model_gpu0 = SentenceTransformer(
                EMBEDDING_MODEL,
                trust_remote_code=True,
                device='cuda:0',
                model_kwargs=MODEL_KWARGS,
            )
            model_gpu0.eval()

            # Load model on GPU 1
            model_gpu1 = SentenceTransformer(
                EMBEDDING_MODEL,
                trust_remote_code=True,
                device='cuda:1',
                model_kwargs=MODEL_KWARGS,
            )
            model_gpu1.eval()

            actual_parallel = True
            print("✓ Models loaded on both GPUs")

            def encode_batch_parallel(texts: List[str]) -> np.ndarray:
                """Encode texts using data parallelism across 2 GPUs"""
                if not texts:
                    return np.empty((0, MODEL_DIMENSION))

                split_point = max(1, len(texts) // 2)
                texts_gpu0 = texts[:split_point]
                texts_gpu1 = texts[split_point:]

                embeddings_parts = []
                with torch.no_grad():
                    if texts_gpu0:
                        embeddings_parts.append(
                            model_gpu0.encode(
                                texts_gpu0,
                                batch_size=len(texts_gpu0),
                                show_progress_bar=False,
                                convert_to_numpy=True,
                            )
                        )
                    if texts_gpu1:
                        embeddings_parts.append(
                            model_gpu1.encode(
                                texts_gpu1,
                                batch_size=len(texts_gpu1),
                                show_progress_bar=False,
                                convert_to_numpy=True,
                            )
                        )

                if not embeddings_parts:
                    return np.empty((0, MODEL_DIMENSION))

                return np.vstack(embeddings_parts)

            encode_batch_fn = encode_batch_parallel

        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                print("⚠ Data parallel model load ran out of memory. Falling back to single GPU mode.")
                torch.cuda.empty_cache()
                model_gpu0 = model_gpu1 = None
            else:
                raise e

    if not actual_parallel:
        print("\n🚀 Loading model on single GPU/CPU...")
        model = SentenceTransformer(
            EMBEDDING_MODEL,
            trust_remote_code=True,
            model_kwargs=MODEL_KWARGS,
        )

        if torch.cuda.is_available():
            model = model.to('cuda:0')
            print("✓ Model loaded on GPU 0")
        else:
            print("✓ Model loaded on CPU (will be slow)")

        def encode_batch_single(texts: List[str]) -> np.ndarray:
            return model.encode(
                texts,
                batch_size=max(1, min(len(texts), BATCH_SIZE)),
                show_progress_bar=False,
                convert_to_numpy=True,
            )

        encode_batch_fn = encode_batch_single

    print(f"Using data parallelism: {actual_parallel}")

    if encode_batch_fn is None:
        raise RuntimeError("Failed to initialize embedding model.")

    # Process chunks in batches
    total_chunks = len(chunks)
    print(f"\nProcessing {total_chunks} chunks in batches of {BATCH_SIZE}...")

    oom_count = 0
    max_oom_retries = 3
    current_batch_size = BATCH_SIZE
    batches_processed = 0
    index = 0

    while index < total_chunks:
        batch_start = index
        batch_chunks = chunks[batch_start:batch_start + current_batch_size]
        texts = [chunk.get('content', '') for chunk in batch_chunks]

        # Generate embeddings with OOM handling
        try:
            embeddings = encode_batch_fn(texts)
        except RuntimeError as e:
            if ("out of memory" in str(e).lower() and
                    oom_count < max_oom_retries and
                    current_batch_size > 1):
                oom_count += 1
                reduction = max(1, current_batch_size // 4)  # Reduce by ~25%
                new_batch_size = max(1, current_batch_size - reduction)
                if new_batch_size == current_batch_size:
                    new_batch_size = max(1, current_batch_size - 1)
                print(
                    f"⚠ OOM detected! Reducing batch size from {current_batch_size} to {new_batch_size}"
                )
                current_batch_size = new_batch_size
                BATCH_SIZE = new_batch_size
                torch.cuda.empty_cache()
                continue
            else:
                raise e

        # Create embedding data with unique IDs
        for idx, (chunk, embedding) in enumerate(zip(batch_chunks, embeddings)):
            subdir = chunk.get('metadata', {}).get('subdirectory', 'unknown')
            filename = chunk.get('metadata', {}).get('source_file', f'chunk_{batch_start + idx}')
            chunk_index = chunk.get('chunk_index', idx)
            chunk_id = f"qdrant_ecosystem:{subdir}:{filename}:chunk:{chunk_index}"
            
            embedding_data = {
                "id": chunk_id,
                "text": chunk.get('content', ''),
                "embedding": embedding.tolist(),
                "metadata": chunk.get('metadata', {})
            }
            all_embeddings.append(embedding_data)
        
        # Cleanup
        del embeddings

        batches_processed += 1
        index += len(batch_chunks)

        # Aggressive cache clearing every 5 batches
        if batches_processed % 5 == 0 and torch.cuda.is_available():
            torch.cuda.empty_cache()

        # Progress reporting with GPU memory
        processed = index
        elapsed = (datetime.now() - start_time).total_seconds()
        rate = processed / elapsed if elapsed > 0 else 0
        eta = (total_chunks - processed) / rate if rate > 0 else 0

        # GPU memory usage
        gpu_memory = ""
        if torch.cuda.is_available():
            gpu_memory = f" | GPU Memory: {torch.cuda.memory_allocated()/1e9:.1f}/{torch.cuda.get_device_properties(0).total_memory/1e9:.1f} GB"
        
        print(f"  Progress: {processed}/{total_chunks} chunks "
              f"({processed/total_chunks*100:.1f}%) - "
              f"{rate:.1f} chunks/sec - ETA: {eta/60:.1f} min{gpu_memory}")    # Save embeddings
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
    """Save processing summary with subdirectory stats"""
    summary_file = OUTPUT_EMBEDDINGS_DIR / f"{COLLECTION_NAME}_embedding_summary.json"

    # Calculate per-subdirectory stats
    subdir_stats = {}
    for chunk in chunks:
        subdir = chunk.get('metadata', {}).get('subdirectory', 'unknown')
        if subdir not in subdir_stats:
            subdir_stats[subdir] = 0
        subdir_stats[subdir] += 1

    summary = {
        "collection": COLLECTION_NAME,
        "timestamp": datetime.now().isoformat(),
        "model": EMBEDDING_MODEL,
        "vector_dimension": 768,
        "total_chunks": len(chunks),
        "total_embeddings": len(embeddings),
        "processing_time_minutes": round(elapsed_time / 60, 2),
        "average_speed_chunks_per_sec": round(len(embeddings) / elapsed_time, 2),
        "gpu_count": torch.cuda.device_count(),
        "batch_size": BATCH_SIZE,
        "subdirectories_processed": len(subdir_stats),
        "chunks_per_subdirectory": subdir_stats,
    }

    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"✓ Summary saved to {summary_file}")
    return summary

def main():
    """Main pipeline execution"""
    pipeline_start = datetime.now()
    
    print(f"\n{'='*60}")
    print("QDRANT ECOSYSTEM EMBEDDING PIPELINE")
    print(f"{'='*60}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Model: {EMBEDDING_MODEL}")
    print(f"Input: {ECOSYSTEM_INPUT_DIR}")
    print(f"Output: {OUTPUT_EMBEDDINGS_DIR}")
    print(f"Started: {pipeline_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # Validate GPU setup
    if not validate_gpu_setup():
        print("❌ GPU validation failed! Check your Kaggle accelerator settings.")
        return    # Load pre-chunked data
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
    print(f"Subdirectories: {summary['subdirectories_processed']}")
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