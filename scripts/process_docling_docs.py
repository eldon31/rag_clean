"""
Docling Documentation Processing Pipeline for Kaggle
Optimized for GPU T4 x2 with nomic-ai/nomic-embed-code (3584-dim, model parallelism)

This script processes Docling project documentation:
Collection name: docling

Input directory:
- Docs/docling-project_docling/ (~50+ markdown files)

UNIQUE ID STRATEGY:
- Format: docling:{filename}:chunk:{index}
- Example: docling:_docling-project_docling_1-overview.md:chunk:0
"""

import os

# Prevent transformers from attempting to load TensorFlow (not available on Kaggle by default)
os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
# Enable PyTorch memory optimization
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import json
import re
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
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, ScalarQuantization, ScalarQuantizationConfig

# Configuration - Optimized for Kaggle GPU T4 x2
EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
BATCH_SIZE = 8  # Conservative batch size for T4 GPUs
COLLECTION_NAME = "docling"
MAX_CHUNK_SIZE = 1500  # Characters per chunk
MIN_CHUNK_SIZE = 100  # Minimum chunk size
QDRANT_URL = "http://localhost:6333"

# Paths
INPUT_DIR = Path("Docs/docling-project_docling")
OUTPUT_CHUNKED_DIR = Path("output/docling/chunked")

# Save to /kaggle/working for easy download (falls back to local output/ if not on Kaggle)
KAGGLE_WORKING = Path("/kaggle/working")
if KAGGLE_WORKING.exists():
    OUTPUT_EMBEDDINGS_DIR = KAGGLE_WORKING
else:
    OUTPUT_EMBEDDINGS_DIR = Path("output/docling/embeddings")

def setup_directories():
    OUTPUT_CHUNKED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
    print("✓ Output directories ready")

def string_to_id(text: str) -> int:
    """Convert string ID to integer using hash"""
    return int(hashlib.sha256(text.encode()).hexdigest(), 16) % (2**63)

def chunk_markdown_file(content: str, source_file: str) -> List[Dict]:
    """Chunk markdown content"""
    chunks = []

    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    sections = []
    current_section = {"heading": "", "level": 0, "content": ""}
    last_pos = 0

    for match in heading_pattern.finditer(content):
        if current_section["content"].strip():
            sections.append(current_section.copy())

        level = len(match.group(1))
        heading = match.group(2).strip()
        start_pos = match.start()

        if last_pos < start_pos:
            if sections:
                sections[-1]["content"] += content[last_pos:start_pos]
            else:
                current_section["content"] = content[last_pos:start_pos]

        current_section = {
            "heading": heading,
            "level": level,
            "content": match.group(0) + "\n"
        }
        last_pos = match.end()

    if last_pos < len(content):
        current_section["content"] += content[last_pos:]
    if current_section["content"].strip():
        sections.append(current_section)

    if not sections:
        sections = [{"heading": source_file.replace('.md', ''), "level": 1, "content": content}]

    chunk_index = 0
    for section in sections:
        section_content = section["content"].strip()

        if not section_content or len(section_content) < MIN_CHUNK_SIZE:
            continue

        if len(section_content) > MAX_CHUNK_SIZE:
            paragraphs = section_content.split('\n\n')
            current_chunk = ""

            for para in paragraphs:
                if len(current_chunk) + len(para) > MAX_CHUNK_SIZE and current_chunk:
                    chunks.append({
                        "chunk_id": f"{COLLECTION_NAME}:{source_file}:chunk:{chunk_index}",
                        "content": current_chunk.strip(),
                        "metadata": {
                            "source": source_file,
                            "heading": section["heading"],
                            "heading_level": section["level"],
                            "chunk_index": chunk_index,
                            "collection": COLLECTION_NAME
                        }
                    })
                    chunk_index += 1
                    current_chunk = para + "\n\n"
                else:
                    current_chunk += para + "\n\n"

            if current_chunk.strip():
                chunks.append({
                    "chunk_id": f"{COLLECTION_NAME}:{source_file}:chunk:{chunk_index}",
                    "content": current_chunk.strip(),
                    "metadata": {
                        "source": source_file,
                        "heading": section["heading"],
                        "heading_level": section["level"],
                        "chunk_index": chunk_index,
                        "collection": COLLECTION_NAME
                    }
                })
                chunk_index += 1
        else:
            chunks.append({
                "chunk_id": f"{COLLECTION_NAME}:{source_file}:chunk:{chunk_index}",
                "content": section_content,
                "metadata": {
                    "source": source_file,
                    "heading": section["heading"],
                    "heading_level": section["level"],
                    "chunk_index": chunk_index,
                    "collection": COLLECTION_NAME
                }
            })
            chunk_index += 1

    for chunk in chunks:
        chunk["metadata"]["total_chunks"] = len(chunks)

    return chunks

def chunk_documents() -> List[Dict]:
    print(f"\n{'='*60}")
    print("CHUNKING DOCUMENTS")
    print(f"{'='*60}")

    if not INPUT_DIR.exists():
        print(f"❌ Error: {INPUT_DIR} not found!")
        return []

    all_chunks = []
    unique_ids = set()

    md_files = sorted(INPUT_DIR.glob("*.md"))
    print(f"Found {len(md_files)} markdown files\n")

    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                print(f"  ⊘ {md_file.name}: Empty")
                continue

            chunks = chunk_markdown_file(content, md_file.name)

            if chunks:
                for chunk in chunks:
                    chunk_id = chunk["chunk_id"]
                    if chunk_id in unique_ids:
                        print(f"  ⚠️ Duplicate ID: {chunk_id}")
                    unique_ids.add(chunk_id)

                output_file = OUTPUT_CHUNKED_DIR / f"{md_file.stem}_chunks.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(chunks, f, ensure_ascii=False, indent=2)

                all_chunks.extend(chunks)
                print(f"  ✓ {md_file.name}: {len(chunks)} chunks")

        except Exception as e:
            print(f"  ✗ Error: {md_file.name}: {e}")

    print(f"\n{'='*60}")
    print(f"✓ Total chunks: {len(all_chunks)}")
    print(f"✓ Unique IDs: {len(unique_ids)}")
    print(f"{'='*60}\n")

    return all_chunks

def embed_chunks(chunks: List[dict]) -> List[dict]:
    print(f"\n{'='*60}")
    print("GENERATING EMBEDDINGS")
    print(f"{'='*60}")

    start_time = datetime.now()
    all_embeddings = []

    print("\n🚀 Loading model with SentenceTransformer...")
    model = SentenceTransformer(EMBEDDING_MODEL, trust_remote_code=True)
    if torch.cuda.is_available():
        model = model.to('cuda')
    print("✓ Model loaded on GPU" if torch.cuda.is_available() else "✓ Model loaded on CPU")

    def encode_batch(texts: List[str]) -> np.ndarray:
        return model.encode(texts, batch_size=BATCH_SIZE, show_progress_bar=False)

    total_chunks = len(chunks)
    print(f"\nProcessing {total_chunks} chunks...")

    for i in range(0, total_chunks, BATCH_SIZE):
        batch_chunks = chunks[i:i + BATCH_SIZE]
        texts = [chunk.get('content', '') for chunk in batch_chunks]
        embeddings = encode_batch(texts)

        for idx, (chunk, embedding) in enumerate(zip(batch_chunks, embeddings)):
            all_embeddings.append({
                "id": chunk.get('chunk_id', f"chunk_{i + idx}"),
                "text": chunk.get('content', ''),
                "embedding": embedding.tolist(),
                "metadata": chunk.get('metadata', {})
            })

        processed = min(i + BATCH_SIZE, total_chunks)
        elapsed = (datetime.now() - start_time).total_seconds()
        rate = processed / elapsed if elapsed > 0 else 0
        eta = (total_chunks - processed) / rate if rate > 0 else 0

        print(f"  {processed}/{total_chunks} ({processed/total_chunks*100:.1f}%) - {rate:.1f} chunks/sec - ETA: {eta/60:.1f} min")

    output_file = OUTPUT_EMBEDDINGS_DIR / f"{COLLECTION_NAME}_embeddings.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for emb in all_embeddings:
            f.write(json.dumps(emb, ensure_ascii=False) + '\n')

    print(f"\n✓ Saved: {len(all_embeddings)} embeddings")
    print(f"✓ Time: {(datetime.now() - start_time).total_seconds()/60:.1f} minutes")

    return all_embeddings

def upload_to_qdrant(embeddings: List[dict]):
    print(f"\n{'='*60}")
    print("UPLOADING TO QDRANT")
    print(f"{'='*60}")

    client = QdrantClient(url=QDRANT_URL)

    # Create collection if it doesn't exist
    vector_size = len(embeddings[0]['embedding']) if embeddings else 3584

    try:
        client.get_collection(COLLECTION_NAME)
        print(f"✓ Collection '{COLLECTION_NAME}' already exists")
    except:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            ),
            quantization_config=ScalarQuantization(
                scalar=ScalarQuantizationConfig(
                    type="int8",
                    quantile=0.99,
                    always_ram=True
                )
            )
        )
        print(f"✓ Created collection '{COLLECTION_NAME}' with vector size {vector_size}")

    # Upload in batches
    points = []
    for emb in embeddings:
        points.append(PointStruct(
            id=string_to_id(emb['id']),
            vector=emb['embedding'],
            payload={
                'text': emb['text'],
                **emb['metadata']
            }
        ))

    batch_size = 100
    total_points = len(points)
    uploaded = 0

    for i in range(0, total_points, batch_size):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch
        )
        uploaded += len(batch)
        print(f"  Uploaded {uploaded}/{total_points} points")

    print(f"✓ Successfully uploaded {total_points} points to collection '{COLLECTION_NAME}'")

def main():
    pipeline_start = datetime.now()

    print(f"\n{'='*60}")
    print("DOCLING DOCS PROCESSING PIPELINE")
    print(f"{'='*60}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Input: {INPUT_DIR}")
    print(f"{'='*60}\n")

    setup_directories()
    chunks = chunk_documents()

    if not chunks:
        print("❌ No chunks!")
        return

    embeddings = embed_chunks(chunks)
    upload_to_qdrant(embeddings)

    total_time = (datetime.now() - pipeline_start).total_seconds()

    print(f"\n{'='*60}")
    print("✓ COMPLETED")
    print(f"{'='*60}")
    print(f"Chunks: {len(chunks)}")
    print(f"Embeddings: {len(embeddings)}")
    print(f"Time: {total_time/60:.1f} minutes")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()