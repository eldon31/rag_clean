#!/usr/bin/env python3
"""
Auto-generated Qdrant upload script for Ultimate Kaggle Embedder V4
Generated on: 2025-10-19T13:34:09.632210

USAGE:
1. Download all exported files to your local machine
2. Make sure Qdrant is running locally (docker-compose up -d)
3. Install requirements: pip install qdrant-client numpy
4. Run this script: python sentence_transformers_embedder_v4_nomic-coderank_upload_script.py
"""

import json
import logging
from datetime import datetime

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upload_to_qdrant():
    """Upload embeddings to local Qdrant instance."""

    # Configuration
    qdrant_host = "localhost"
    qdrant_port = 6333
    collection_name = "sentence_transformers_v4_nomic_coderank"

    # File paths (adjust if needed)
    files = {
        "embeddings": "sentence_transformers_embedder_v4_nomic-coderank_embeddings.npy",
        "metadata": "sentence_transformers_embedder_v4_nomic-coderank_metadata.json",
        "texts": "sentence_transformers_embedder_v4_nomic-coderank_texts.json",
        "stats": "sentence_transformers_embedder_v4_nomic-coderank_stats.json",
        "jsonl": "sentence_transformers_embedder_v4_nomic-coderank_qdrant.jsonl",
        "sparse": "sentence_transformers_embedder_v4_nomic-coderank_sparse.jsonl"
    }

    try:
        client = QdrantClient(host=qdrant_host, port=qdrant_port)
        logger.info(f"Connected to Qdrant at {qdrant_host}:{qdrant_port}")

        logger.info("Loading exported data...")
        embeddings = np.load(files["embeddings"])

        with open(files["metadata"], "r", encoding="utf-8") as handle:
            metadata_list = json.load(handle)

        with open(files["texts"], "r", encoding="utf-8") as handle:
            texts_list = json.load(handle)

        logger.info(f"Loaded {len(embeddings)} embeddings ({embeddings.shape[1]}D)")

        if files.get("sparse"):
            logger.info(f"Sparse sidecar detected: {files['sparse']}")

        try:
            client.get_collection(collection_name)
            logger.info(f"Collection '{collection_name}' already exists")
        except Exception:
            logger.info(f"Creating collection: {collection_name}")
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=embeddings.shape[1],
                    distance=Distance.COSINE,
                ),
                hnsw_config={
                    "m": 48,
                    "ef_construct": 512,
                    "full_scan_threshold": 50000,
                },
                quantization_config={
                    "scalar": {
                        "type": "int8",
                        "quantile": 0.99,
                        "always_ram": True,
                    }
                },
            )

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
                    "local_upload_timestamp": datetime.now().isoformat(),
                },
            )
            points.append(point)

        batch_size = 1000
        total_batches = (len(points) + batch_size - 1) // batch_size
        logger.info(f"Uploading {len(points)} points in {total_batches} batches...")

        for start in range(0, len(points), batch_size):
            batch = points[start:start + batch_size]
            batch_num = (start // batch_size) + 1

            client.upsert(collection_name=collection_name, points=batch, wait=True)
            logger.info(f"Uploaded batch {batch_num}/{total_batches} ({len(batch)} points)")

        collection_info = client.get_collection(collection_name)
        logger.info(f"Upload complete; collection has {collection_info.points_count} points")

        logger.info("Testing search...")
        test_results = client.search(
            collection_name=collection_name,
            query_vector=embeddings[0].tolist(),
            limit=5,
        )

        logger.info(f"Search test successful; found {len(test_results)} results")
        logger.info(f"Embeddings are ready for use in collection: {collection_name}")

    except Exception as exc:
        logger.error(f"Upload failed: {exc}")
        raise


if __name__ == "__main__":
    upload_to_qdrant()
