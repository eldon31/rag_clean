#!/usr/bin/env python3
"""
Auto-generated Qdrant upload script for Ultimate Kaggle Embedder V4
Generated on: 2025-10-22T05:11:34.526999

USAGE:
1. Download all exported files to your local machine
2. Make sure Qdrant is running locally (docker-compose up -d)
3. Install requirements: pip install qdrant-client numpy
4. Run this script: python ultimate_embeddings_v4_upload_script.py
"""

import json
import logging
from datetime import datetime

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    MultiVectorConfig,
    MultiVectorComparator,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upload_to_qdrant():
    """Upload embeddings to local Qdrant instance."""

    # Configuration
    qdrant_host = "localhost"
    qdrant_port = 6333
    collection_name = "ultimate_embeddings_v4_jina_code_embeddings_1.5b"

    # File paths (adjust if needed)
    files = {
        "embeddings": "ultimate_embeddings_v4_embeddings.npy",
        "metadata": "ultimate_embeddings_v4_metadata.json",
        "texts": "ultimate_embeddings_v4_texts.json",
        "stats": "ultimate_embeddings_v4_stats.json",
        "jsonl": "ultimate_embeddings_v4_qdrant.jsonl",
        "sparse": "",
        "multivectors": ""
    }

    vector_files = json.loads("""{"jina-code-embeddings-1.5b": "ultimate_embeddings_v4_embeddings.npy"}""")
    vector_dimensions = json.loads("""{"jina-code-embeddings-1.5b": 1024}""")
    dense_vector_names = json.loads("""["jina-code-embeddings-1.5b"]""")
    primary_vector_name = "jina-code-embeddings-1.5b"

    vector_files = {name: path for name, path in vector_files.items() if path}
    dense_vector_names = [name for name in dense_vector_names if name in vector_files]

    try:
        client = QdrantClient(host=qdrant_host, port=qdrant_port)
        logger.info(f"Connected to Qdrant at {qdrant_host}:{qdrant_port}")

        logger.info("Loading exported data...")
        dense_vectors = {name: np.load(path) for name, path in vector_files.items()}

        with open(files["metadata"], "r", encoding="utf-8") as handle:
            metadata_list = json.load(handle)

        with open(files["texts"], "r", encoding="utf-8") as handle:
            texts_list = json.load(handle)

        multivector_channels = {}
        multivector_dimensions = {}
        multivector_comparators = {}

        if files.get("multivectors"):
            with open(files["multivectors"], "r", encoding="utf-8") as handle:
                multivector_blob = json.load(handle)
            multivector_channels = multivector_blob.get("channels", {})
            multivector_dimensions = multivector_blob.get("dimensions", {})
            multivector_comparators = multivector_blob.get("comparators", {})

        if not dense_vectors:
            raise RuntimeError("No dense embedding files were found; cannot proceed with upload")

        point_count = len(metadata_list)

        for name in dense_vector_names:
            vectors = dense_vectors.get(name)
            if vectors is None:
                raise RuntimeError(f"Missing dense vectors for {name}")
            if len(vectors) != point_count:
                raise ValueError(
                    f"Vector count mismatch for {name}: expected {point_count}, got {len(vectors)}"
                )
            vector_dim = vector_dimensions.get(name, vectors.shape[1])
            logger.info("Loaded %s embeddings for %s (%sD)", len(vectors), name, vector_dim)

        if files.get("sparse"):
            logger.info(f"Sparse sidecar detected: {files['sparse']}")

        multivector_names = list(multivector_channels.keys())
        for name in multivector_names:
            channel_vectors = multivector_channels.get(name, [])
            if len(channel_vectors) != point_count:
                raise ValueError(
                    f"Multivector count mismatch for {name}: expected {point_count}, got {len(channel_vectors)}"
                )
        if multivector_names:
            logger.info("Multivector channels detected: %s", ", ".join(multivector_names))

        try:
            client.get_collection(collection_name)
            logger.info(f"Collection '{collection_name}' already exists")
        except Exception:
            logger.info(f"Creating collection: {collection_name}")
            vector_params = {
                name: VectorParams(size=vector_dimensions.get(name, dense_vectors[name].shape[1]), distance=Distance.COSINE)
                for name in dense_vector_names
            }
            for name in multivector_names:
                dimension = multivector_dimensions.get(name)
                if dimension is None:
                    channel_vectors = multivector_channels.get(name, [])
                    first_non_empty = next((vec for vec in channel_vectors if vec), [])
                    if first_non_empty:
                        dimension = len(first_non_empty[0])
                if dimension is None:
                    raise RuntimeError(f"Could not determine dimension for multivector channel {name}")
                comparator_value = multivector_comparators.get(name, "max_sim")
                try:
                    comparator_enum = MultiVectorComparator(comparator_value)
                except ValueError:
                    logger.warning(
                        "Unknown comparator '%s' for multivector channel %s; defaulting to max_sim",
                        comparator_value,
                        name,
                    )
                    comparator_enum = MultiVectorComparator.MAX_SIM
                multivector_dimensions[name] = dimension
                vector_params[name] = VectorParams(
                    size=dimension,
                    distance=Distance.COSINE,
                    multivector_config=MultiVectorConfig(
                        comparator=comparator_enum
                    ),
                )
            if len(vector_params) == 1:
                vectors_config = next(iter(vector_params.values()))
            else:
                vectors_config = vector_params

            client.create_collection(
                collection_name=collection_name,
                vectors_config=vectors_config,
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

        for i in range(point_count):
            metadata = metadata_list[i]
            text = texts_list[i]
            vector_payload = {
                name: dense_vectors[name][i].tolist()
                for name in dense_vector_names
            }
            for name in multivector_names:
                channel_data = multivector_channels[name][i]
                if channel_data is None:
                    channel_data = []
                if channel_data and isinstance(channel_data[0], (list, tuple)):
                    channel_data = [list(vec) for vec in channel_data]
                vector_payload[name] = {"vectors": channel_data}
            payload_data = {
                **metadata,
                "text_preview": text[:500],
                "full_text_length": len(text),
                "local_upload_timestamp": datetime.now().isoformat(),
                "primary_vector_name": primary_vector_name,
                "dense_vector_names": dense_vector_names,
            }
            if multivector_names:
                payload_data.setdefault("multivector_channels", multivector_names)
                if multivector_dimensions:
                    payload_data.setdefault("multivector_dimensions", multivector_dimensions)
                if multivector_comparators:
                    payload_data.setdefault("multivector_comparators", multivector_comparators)
            point = PointStruct(
                id=i,
                vectors=vector_payload,
                payload=payload_data,
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
            query_vector=(
                primary_vector_name,
                dense_vectors[primary_vector_name][0].tolist(),
            ),
            limit=5,
        )

        logger.info(f"Search test successful; found {len(test_results)} results")
        logger.info(f"Embeddings are ready for use in collection: {collection_name}")

    except Exception as exc:
        logger.error(f"Upload failed: {exc}")
        raise


if __name__ == "__main__":
    upload_to_qdrant()
