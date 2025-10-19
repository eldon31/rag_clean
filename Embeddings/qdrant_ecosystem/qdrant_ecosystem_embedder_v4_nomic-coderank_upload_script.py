#!/usr/bin/env python3
"""
Auto-generated Qdrant upload script for Ultimate Kaggle Embedder V4
Generated on: 2025-10-19T12:04:14.117831

USAGE:
1. Download all exported files to your local machine
2. Make sure Qdrant is running locally (docker-compose up -d)
3. Install requirements: pip install qdrant-client numpy
4. Run this script: python qdrant_ecosystem_embedder_v4_nomic-coderank_upload_script.py
"""

import json
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_to_qdrant():
    """Upload embeddings to local Qdrant instance"""
    
    # Configuration
    QDRANT_HOST = "localhost"
    QDRANT_PORT = 6333
    COLLECTION_NAME = "ultimate_embeddings_v4_nomic-coderank"
    
    # File paths (adjust if needed)
    FILES = {
        "embeddings": "qdrant_ecosystem_embedder_v4_nomic-coderank_embeddings.npy", 
        "metadata": "qdrant_ecosystem_embedder_v4_nomic-coderank_metadata.json",
        "texts": "qdrant_ecosystem_embedder_v4_nomic-coderank_texts.json",
        "stats": "qdrant_ecosystem_embedder_v4_nomic-coderank_stats.json",
        "jsonl": "qdrant_ecosystem_embedder_v4_nomic-coderank_qdrant.jsonl",
        "sparse": "qdrant_ecosystem_embedder_v4_nomic-coderank_sparse.jsonl"
    }
    
    try:
        # Connect to Qdrant
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    logger.info(f"Connected to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
        
        # Load data
    logger.info("Loading exported data...")
        embeddings = np.load(FILES["embeddings"])
        
        with open(FILES["metadata"], 'r', encoding='utf-8') as f:
            metadata_list = json.load(f)
            
        with open(FILES["texts"], 'r', encoding='utf-8') as f:
            texts_list = json.load(f)
        
    logger.info(f"Loaded {len(embeddings)} embeddings ({embeddings.shape[1]}D)")

        if FILES.get("sparse"):
            logger.info(f"Sparse sidecar detected: {FILES['sparse']}")
        
        # Create collection
        try:
            client.get_collection(COLLECTION_NAME)
            logger.info(f"Collection '{COLLECTION_NAME}' already exists")
        except:
            logger.info(f"Creating collection: {COLLECTION_NAME}")
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=embeddings.shape[1],
                    distance=Distance.COSINE
                ),
                # Optimized for large collections
                hnsw_config={
                    "m": 48,
                    "ef_construct": 512,
                    "full_scan_threshold": 50000
                },
                # Enable quantization for speed
                quantization_config={
                    "scalar": {
                        "type": "int8",
                        "quantile": 0.99,
                        "always_ram": True
                    }
                }
            )
        
        # Prepare points
    logger.info("Preparing points for upload...")
        points = []
        
        for i, (embedding, metadata, text) in enumerate(zip(embeddings, metadata_list, texts_list)):
            point = PointStruct(
                id=i,
                vector=embedding.tolist(),
                payload={
                    **metadata,
                    "text_preview": text[:500],
                    "full_text_length": len(text),
                    "local_upload_timestamp": datetime.now().isoformat()
                }
            )
            points.append(point)
        
        # Batch upload
        batch_size = 1000
        total_batches = (len(points) + batch_size - 1) // batch_size
        
    logger.info(f"Uploading {len(points)} points in {total_batches} batches...")
        
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=batch,
                wait=True
            )
            
            logger.info(f"Uploaded batch {batch_num}/{total_batches} ({len(batch)} points)")
        
        # Verify upload
        collection_info = client.get_collection(COLLECTION_NAME)
    logger.info(f"Upload complete; collection has {collection_info.points_count} points")
        
        # Test search
    logger.info("Testing search...")
        test_results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=embeddings[0].tolist(),
            limit=5
        )
        
    logger.info(f"Search test successful; found {len(test_results)} results")
    logger.info(f"Embeddings are ready for use in collection: {COLLECTION_NAME}")
        
    except Exception as e:
    logger.error(f"Upload failed: {e}")
        raise

if __name__ == "__main__":
    upload_to_qdrant()
