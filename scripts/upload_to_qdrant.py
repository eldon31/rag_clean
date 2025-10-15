"""
Safe Qdrant Upload Script with Duplicate Prevention

This script uploads embeddings to Qdrant with safeguards against duplicates.
"""

import json
import hashlib
from pathlib import Path
from typing import List, Dict
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

# Configuration
QDRANT_URL = "http://localhost:6333"
BATCH_SIZE = 100  # Upload in batches of 100 points

def string_to_id(text: str) -> int:
    """Convert string ID to integer using hash (Qdrant requires int IDs for some operations)"""
    return int(hashlib.sha256(text.encode()).hexdigest(), 16) % (2**63)

class QdrantUploader:
    def __init__(self, url: str = QDRANT_URL):
        self.client = QdrantClient(url=url)
        print(f"✓ Connected to Qdrant at {url}")
    
    def create_collection(self, collection_name: str, vector_size: int = 3584, recreate: bool = False, use_quantization: str = "scalar"):
        """
        Create a Qdrant collection if it doesn't exist
        
        Args:
            collection_name: Name of the collection
            vector_size: Dimension of embeddings (3584 for nomic-embed-code)
            recreate: If True, delete and recreate collection
            use_quantization: Quantization type: "scalar" (recommended), "binary", or None
        """
        from qdrant_client.models import (
            ScalarQuantization, 
            ScalarQuantizationConfig,
            BinaryQuantization,
            BinaryQuantizationConfig,
            ScalarType
        )
        
        if recreate:
            if self.client.collection_exists(collection_name):
                print(f"⚠️  Deleting existing collection: {collection_name}")
                self.client.delete_collection(collection_name)
        
        if not self.client.collection_exists(collection_name):
            # Configure quantization
            quantization_config = None
            if use_quantization == "scalar":
                quantization_config = ScalarQuantization(
                    scalar=ScalarQuantizationConfig(
                        type=ScalarType.INT8,
                        quantile=0.99,  # Exclude 1% outliers
                        always_ram=True  # Keep quantized vectors in RAM for speed
                    )
                )
                print(f"  🔧 Using scalar (int8) quantization: 4x compression, 99% accuracy")
            elif use_quantization == "binary":
                quantization_config = BinaryQuantization(
                    binary=BinaryQuantizationConfig(
                        always_ram=True
                    )
                )
                print(f"  🔧 Using binary (1-bit) quantization: 32x compression, ~95% accuracy")
            
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
                quantization_config=quantization_config
            )
            print(f"✓ Created collection: {collection_name} (vector_size={vector_size})")
        else:
            print(f"✓ Collection already exists: {collection_name}")
    
    def check_source_exists(self, collection_name: str, source_file: str) -> bool:
        """
        Check if a source file already has data in the collection
        
        Args:
            collection_name: Name of the collection
            source_file: Source filename to check
            
        Returns:
            True if source file exists in collection
        """
        try:
            result = self.client.scroll(
                collection_name=collection_name,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="source",
                            match=MatchValue(value=source_file)
                        )
                    ]
                ),
                limit=1
            )
            return len(result[0]) > 0
        except Exception:
            return False
    
    def delete_source_data(self, collection_name: str, source_file: str):
        """
        Delete all points from a specific source file
        
        Args:
            collection_name: Name of the collection
            source_file: Source filename to delete
        """
        self.client.delete(
            collection_name=collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(value=source_file)
                    )
                ]
            )
        )
        print(f"  ✓ Deleted existing data for: {source_file}")
    
    def upload_embeddings(
        self,
        embeddings_file: Path,
        collection_name: str,
        mode: str = "upsert",
        check_duplicates: bool = True
    ):
        """
        Upload embeddings from JSONL file to Qdrant
        
        Args:
            embeddings_file: Path to JSONL embeddings file
            collection_name: Target collection name
            mode: 'upsert' (update/insert), 'skip' (skip if exists), 'replace' (delete then insert)
            check_duplicates: Whether to check for existing source files
        """
        print(f"\n{'='*60}")
        print(f"UPLOADING TO QDRANT")
        print(f"{'='*60}")
        print(f"File: {embeddings_file}")
        print(f"Collection: {collection_name}")
        print(f"Mode: {mode}")
        print(f"Check duplicates: {check_duplicates}")
        
        # Load embeddings
        embeddings = []
        with open(embeddings_file, 'r', encoding='utf-8') as f:
            for line in f:
                embeddings.append(json.loads(line))
        
        print(f"✓ Loaded {len(embeddings)} embeddings")
        
        # Check for duplicates by source file
        if check_duplicates and mode in ["skip", "replace"]:
            sources = set()
            for emb in embeddings:
                source = emb.get('metadata', {}).get('source')
                if source:
                    sources.add(source)
            
            print(f"\nChecking {len(sources)} unique source files...")
            
            for source in sources:
                exists = self.check_source_exists(collection_name, source)
                if exists:
                    if mode == "skip":
                        print(f"  ⊘ Skipping: {source} (already exists)")
                        # Remove from upload list
                        embeddings = [e for e in embeddings 
                                    if e.get('metadata', {}).get('source') != source]
                    elif mode == "replace":
                        print(f"  ♻️  Replacing: {source}")
                        self.delete_source_data(collection_name, source)
                else:
                    print(f"  ✓ New source: {source}")
        
        if not embeddings:
            print("\n⚠️  No embeddings to upload (all skipped or deleted)")
            return
        
        # Convert to PointStruct objects
        print(f"\nPreparing {len(embeddings)} points for upload...")
        points = []
        
        for idx, emb in enumerate(embeddings):
            # Extract fields
            chunk_id = emb.get('id', f"chunk_{idx}")
            text = emb.get('text', '')
            vector = emb.get('embedding', [])
            metadata = emb.get('metadata', {})
            
            # Create payload (metadata + text)
            payload = {
                "text": text,
                "source": metadata.get('source', 'unknown'),
                "subdir": metadata.get('subdir', ''),
                "collection": metadata.get('collection', collection_name),
                "chunk_index": metadata.get('chunk_index', idx),
                "indexed_at": datetime.now().isoformat()
            }
            
            # Add any additional metadata fields
            for key, value in metadata.items():
                if key not in payload:
                    payload[key] = value
            
            # Create point with integer ID
            point = PointStruct(
                id=string_to_id(chunk_id),
                vector=vector,
                payload=payload
            )
            points.append(point)
        
        # Upload in batches
        print(f"\nUploading in batches of {BATCH_SIZE}...")
        total_uploaded = 0
        
        for i in range(0, len(points), BATCH_SIZE):
            batch = points[i:i + BATCH_SIZE]
            self.client.upsert(
                collection_name=collection_name,
                points=batch
            )
            total_uploaded += len(batch)
            print(f"  Progress: {total_uploaded}/{len(points)} points uploaded "
                  f"({total_uploaded/len(points)*100:.1f}%)")
        
        # Verify
        collection_info = self.client.get_collection(collection_name)
        print(f"\n{'='*60}")
        print(f"✓ UPLOAD COMPLETED")
        print(f"{'='*60}")
        print(f"Collection: {collection_name}")
        print(f"Total points in collection: {collection_info.points_count}")
        print(f"Points uploaded: {total_uploaded}")
        print(f"{'='*60}\n")

def main():
    """Upload all 4 correct collections"""
    uploader = QdrantUploader()
    
    # Upload Viator API
    print("\n=== UPLOADING VIATOR API ===")
    uploader.create_collection("viator_api", vector_size=3584, use_quantization="scalar")
    uploader.upload_embeddings(
        embeddings_file=Path("output/embeddings/viator_api_embeddings.jsonl"),
        collection_name="viator_api",
        mode="upsert",
        check_duplicates=True
    )
    
    # Upload Fast Docs
    print("\n=== UPLOADING FAST DOCS ===")
    uploader.create_collection("fast_docs", vector_size=3584, use_quantization="scalar")
    uploader.upload_embeddings(
        embeddings_file=Path("output/embeddings/fast_docs_embeddings.jsonl"),
        collection_name="fast_docs",
        mode="upsert",
        check_duplicates=True
    )
    
    # Upload Pydantic Docs
    print("\n=== UPLOADING PYDANTIC DOCS ===")
    uploader.create_collection("pydantic_docs", vector_size=3584, use_quantization="scalar")
    uploader.upload_embeddings(
        embeddings_file=Path("output/embeddings/pydantic_docs_embeddings.jsonl"),
        collection_name="pydantic_docs",
        mode="upsert",
        check_duplicates=True
    )
    
    # Upload Inngest Ecosystem
    print("\n=== UPLOADING INNGEST ECOSYSTEM ===")
    uploader.create_collection("inngest_ecosystem", vector_size=3584, use_quantization="scalar")
    uploader.upload_embeddings(
        embeddings_file=Path("output/embeddings/inngest_ecosystem_embeddings.jsonl"),
        collection_name="inngest_ecosystem",
        mode="upsert",
        check_duplicates=True
    )

if __name__ == "__main__":
    main()
