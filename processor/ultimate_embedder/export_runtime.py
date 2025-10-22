"""Embedding export orchestration extracted from the facade."""

from __future__ import annotations

import json
import logging
import os
import textwrap
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict

import numpy as np

try:  # Optional dependency for FAISS export
    import faiss  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    faiss = None  # type: ignore

if TYPE_CHECKING:  # pragma: no cover
    from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4


class ExportRuntime:
    """Coordinate exporting embeddings and metadata for local Qdrant usage."""

    def __init__(self, embedder: "UltimateKaggleEmbedderV4", logger: logging.Logger) -> None:
        self.embedder = embedder
        self.logger = logger

    def export_for_local_qdrant(self) -> Dict[str, str]:
        """Export embeddings in formats optimized for downstream upload."""

        embedder = self.embedder
        if embedder.embeddings is None:
            raise ValueError("No embeddings to export. Generate embeddings first.")

        embeddings = embedder._require_embeddings()
        companion_arrays = {
            name: array
            for name, array in embedder.embeddings_by_model.items()
            if name != embedder.model_name
        }

        self.logger.info("Exporting embeddings for local Qdrant integration...")

        exported_files: Dict[str, str] = {}
        base_path = embedder.export_config.get_output_path()

        if embedder.export_config.export_numpy:
            numpy_path = f"{base_path}_embeddings.npy"
            np.save(numpy_path, embeddings)
            exported_files["numpy"] = numpy_path
            self.logger.info("NumPy embeddings: %s", numpy_path)

            for companion_name, companion_array in companion_arrays.items():
                safe_name = companion_name.replace("-", "_")
                companion_path = f"{base_path}_{safe_name}_embeddings.npy"
                np.save(companion_path, companion_array)
                exported_files[f"numpy_{safe_name}"] = companion_path
                self.logger.info("NumPy embeddings (%s): %s", companion_name, companion_path)

        if embedder.export_config.export_jsonl:
            jsonl_path = f"{base_path}_qdrant.jsonl"
            self._export_qdrant_jsonl(jsonl_path, embeddings, companion_arrays)
            exported_files["jsonl"] = jsonl_path
            self.logger.info("Qdrant JSONL: %s", jsonl_path)

        if embedder.multivectors_by_model:
            multivector_path = f"{base_path}_multivectors.json"
            multivector_payload = {
                "channels": embedder.multivectors_by_model,
                "dimensions": embedder.multivector_dimensions,
                "comparators": embedder.multivector_comparators,
            }
            with open(multivector_path, "w", encoding="utf-8") as handle:
                json.dump(multivector_payload, handle, ensure_ascii=False)
            exported_files["multivectors"] = multivector_path
            self.logger.info("Multivector JSON: %s", multivector_path)

        if embedder.export_config.export_sparse_jsonl and any(embedder.sparse_vectors):
            sparse_path = f"{base_path}_sparse.jsonl"
            self._export_sparse_jsonl(sparse_path)
            exported_files["sparse_jsonl"] = sparse_path
            self.logger.info("Sparse JSONL: %s", sparse_path)

        if embedder.export_config.export_faiss:
            faiss_path = f"{base_path}_index.faiss"
            self._export_faiss_index(faiss_path)
            exported_files["faiss"] = faiss_path
            self.logger.info("FAISS index: %s", faiss_path)

        metadata_path = f"{base_path}_metadata.json"
        self._export_metadata(metadata_path)
        exported_files["metadata"] = metadata_path

        texts_path = f"{base_path}_texts.json"
        self._export_texts(texts_path)
        exported_files["texts"] = texts_path

        stats_path = f"{base_path}_stats.json"
        self._export_processing_stats(stats_path)
        exported_files["stats"] = stats_path

        script_path = f"{base_path}_upload_script.py"
        self._generate_upload_script(script_path, exported_files)
        exported_files["upload_script"] = script_path
        exported_files["qdrant_collection"] = embedder.get_target_collection_name()

        self.logger.info("Export complete; files ready for download:")
        for file_type, file_path in exported_files.items():
            if file_type == "qdrant_collection":
                self.logger.info("  %s: %s", file_type, file_path)
                continue

            if not os.path.exists(file_path):
                self.logger.warning("  %s: expected export missing at %s", file_type, file_path)
                continue

            file_size_mb = os.path.getsize(file_path) / 1024 / 1024
            self.logger.info("  %s: %s (%.1fMB)", file_type, os.path.basename(file_path), file_size_mb)

        return exported_files

    def _export_qdrant_jsonl(
        self,
        file_path: str,
        embeddings: np.ndarray,
        companion_arrays: Dict[str, np.ndarray],
    ) -> None:
        embedder = self.embedder

        dense_vector_names = [embedder.model_name, *companion_arrays.keys()]

        with open(file_path, "w", encoding="utf-8") as handle:
            total = len(embeddings)
            for index in range(total):
                metadata = embedder.chunks_metadata[index]
                text = embedder.chunk_texts[index]
                sparse_vector = embedder.sparse_vectors[index] if index < len(embedder.sparse_vectors) else None

                payload_model_info: Dict[str, Any] = {
                    "name": embedder.model_name,
                    "hf_model_id": embedder.model_config.hf_model_id,
                    "dimension": embedder.model_config.vector_dim,
                    "version": "v4",
                }

                companion_payload: Dict[str, Any] = {}
                vector_payload: Dict[str, Any] = {embedder.model_name: embeddings[index].tolist()}

                for companion_name, companion_array in companion_arrays.items():
                    vector_payload[companion_name] = companion_array[index].tolist()
                    config = embedder.companion_model_configs.get(companion_name)
                    companion_payload[companion_name] = {
                        "dimension": companion_array.shape[1],
                        "hf_model_id": config.hf_model_id if config else None,
                    }

                if companion_payload:
                    payload_model_info["companions"] = companion_payload

                multivector_channel_counts: Dict[str, int] = {}
                if embedder.multivectors_by_model:
                    multivector_meta: Dict[str, Any] = {}
                    for channel_name, channel_vectors in embedder.multivectors_by_model.items():
                        channel_dimension = embedder.multivector_dimensions.get(channel_name)
                        comparator = embedder.multivector_comparators.get(channel_name, "max_sim")
                        multivector_meta[channel_name] = {
                            "dimension": channel_dimension,
                            "comparator": comparator,
                        }

                        point_vectors = channel_vectors[index] if index < len(channel_vectors) else []
                        multivector_channel_counts[channel_name] = len(point_vectors)
                        vector_payload[channel_name] = {"vectors": point_vectors}

                    payload_model_info["multivectors"] = multivector_meta

                payload: Dict[str, Any] = {
                    **metadata,
                    "text_preview": text[:500],
                    "full_text_length": len(text),
                    "kaggle_export_timestamp": datetime.now().isoformat(),
                    "model_info": payload_model_info,
                    "primary_vector_name": embedder.model_name,
                    "dense_vector_names": dense_vector_names,
                }

                if companion_arrays:
                    payload["companion_vector_dimensions"] = {
                        name: info["dimension"] for name, info in companion_payload.items()
                    }

                if sparse_vector:
                    payload["sparse_vector"] = {
                        "indices": sparse_vector.get("indices", []),
                        "values": sparse_vector.get("values", []),
                        "tokens": sparse_vector.get("tokens", []),
                        "stats": sparse_vector.get("stats", {}),
                    }

                if multivector_channel_counts:
                    payload["multivector_counts"] = multivector_channel_counts
                    payload["multivector_channels"] = list(multivector_channel_counts.keys())

                qdrant_point: Dict[str, Any] = {
                    "id": index,
                    "payload": payload,
                    "vectors": vector_payload,
                }

                handle.write(json.dumps(qdrant_point, ensure_ascii=False) + "\n")

    def _export_sparse_jsonl(self, file_path: str) -> None:
        embedder = self.embedder

        if not embedder.sparse_vectors or not any(embedder.sparse_vectors):
            self.logger.info("No sparse vectors available for export; skipping sparse JSONL generation.")
            return

        with open(file_path, "w", encoding="utf-8") as handle:
            for index, sparse_vector in enumerate(embedder.sparse_vectors):
                if sparse_vector:
                    record = {
                        "id": index,
                        "sparse_vector": {
                            "indices": sparse_vector.get("indices", []),
                            "values": sparse_vector.get("values", []),
                        },
                        "tokens": sparse_vector.get("tokens", []),
                        "stats": sparse_vector.get("stats", {}),
                    }
                else:
                    record = {
                        "id": index,
                        "sparse_vector": {"indices": [], "values": []},
                        "tokens": [],
                        "stats": {},
                    }

                handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _export_faiss_index(self, file_path: str) -> None:
        if faiss is None:
            raise RuntimeError("FAISS export requires the `faiss` package to be installed")

        embeddings = self.embedder._require_embeddings()
        dimension = embeddings.shape[1]

        index = faiss.IndexFlatIP(dimension)
        embeddings_float32 = embeddings.astype(np.float32)
        index.add(embeddings_float32)  # type: ignore[arg-type]
        faiss.write_index(index, file_path)

    def _export_metadata(self, file_path: str) -> None:
        with open(file_path, "w", encoding="utf-8") as handle:
            json.dump(self.embedder.chunks_metadata, handle, indent=2, ensure_ascii=False)

    def _export_texts(self, file_path: str) -> None:
        with open(file_path, "w", encoding="utf-8") as handle:
            json.dump(self.embedder.chunk_texts, handle, indent=2, ensure_ascii=False)

    def _export_processing_stats(self, file_path: str) -> None:
        embedder = self.embedder
        embeddings = embedder.embeddings
        stats: Dict[str, Any] = {
            "kaggle_environment": embedder.is_kaggle,
            "model_config": {
                "name": embedder.model_name,
                "hf_model_id": embedder.model_config.hf_model_id,
                "vector_dimension": embedder.model_config.vector_dim,
                "max_tokens": embedder.model_config.max_tokens,
            },
            "gpu_config": {
                "device_count": embedder.device_count,
                "backend": embedder.gpu_config.backend,
                "precision": embedder.gpu_config.precision,
                "total_vram_gb": embedder.gpu_config.total_vram_gb,
            },
            "embedding_stats": {
                "total_embeddings": len(embeddings) if embeddings is not None else 0,
                "embedding_dimension": embeddings.shape[1] if embeddings is not None else 0,
                "memory_usage_mb": embeddings.nbytes / 1024 / 1024 if embeddings is not None else 0,
            },
            "processing_performance": dict(embedder.processing_stats),
            "export_timestamp": datetime.now().isoformat(),
        }

        progress_events = getattr(embedder.telemetry, "batch_progress_events", None)
        if progress_events:
            stats["batch_progress"] = progress_events

        if embedder.sparse_vectors:
            available = sum(1 for vector in embedder.sparse_vectors if vector)
            stats["sparse_vector_stats"] = {
                "total_chunks": len(embedder.sparse_vectors),
                "sparse_vectors_available": available,
                "coverage_ratio": available / len(embedder.sparse_vectors) if embedder.sparse_vectors else 0.0,
            }

        if embedder.embeddings_by_model:
            stats["dense_vector_layout"] = {
                name: {
                    "dimension": array.shape[1],
                    "memory_mb": array.nbytes / 1024 / 1024,
                    "is_primary": name == embedder.model_name,
                }
                for name, array in embedder.embeddings_by_model.items()
            }

        if embedder.multivectors_by_model:
            stats["multivector_layout"] = {
                name: {
                    "dimension": embedder.multivector_dimensions.get(name),
                    "comparator": embedder.multivector_comparators.get(name, "max_sim"),
                    "average_vectors_per_point": (
                        sum(len(vectors) for vectors in channel) / len(channel) if channel else 0.0
                    ),
                }
                for name, channel in embedder.multivectors_by_model.items()
            }

        if embedder.text_cache:
            stats["preprocessing_cache"] = embedder.text_cache.get_stats()

        with open(file_path, "w", encoding="utf-8") as handle:
            json.dump(stats, handle, indent=2, ensure_ascii=False)

    def _generate_upload_script(self, file_path: str, exported_files: Dict[str, str]) -> None:
        embedder = self.embedder

        collection_name = embedder.get_target_collection_name()

        vector_files_map: Dict[str, str] = {}
        vector_dimensions_map: Dict[str, int] = {}

        primary_numpy_filename = ""
        if "numpy" in exported_files:
            primary_numpy_filename = os.path.basename(exported_files["numpy"])
            vector_files_map[embedder.model_name] = primary_numpy_filename
            vector_dimensions_map[embedder.model_name] = embedder.model_config.vector_dim
        else:
            self.logger.warning(
                "Primary NumPy embeddings file missing; upload script will have limited functionality"
            )

        for model_name, array in embedder.embeddings_by_model.items():
            if model_name == embedder.model_name:
                continue
            safe_name = model_name.replace("-", "_")
            numpy_key = f"numpy_{safe_name}"
            companion_path = exported_files.get(numpy_key)
            if not companion_path:
                self.logger.warning(
                    "Companion embeddings for %s not exported; skipping in upload script",
                    model_name,
                )
                continue
            vector_files_map[model_name] = os.path.basename(companion_path)
            vector_dimensions_map[model_name] = array.shape[1]

        dense_vector_names = list(vector_files_map.keys())

        vector_files_json = json.dumps(vector_files_map)
        vector_dimensions_json = json.dumps(vector_dimensions_map)
        dense_vector_names_json = json.dumps(dense_vector_names)
        primary_vector_name = embedder.model_name

        script_content = textwrap.dedent(
            f'''#!/usr/bin/env python3
"""
Auto-generated Qdrant upload script for Ultimate Kaggle Embedder V4
Generated on: {datetime.now().isoformat()}

USAGE:
1. Download all exported files to your local machine
2. Make sure Qdrant is running locally (docker-compose up -d)
3. Install requirements: pip install qdrant-client numpy
4. Run this script: python {os.path.basename(file_path)}
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
    collection_name = "{collection_name}"

    # File paths (adjust if needed)
    files = {{
        "embeddings": "{primary_numpy_filename}",
        "metadata": "{os.path.basename(exported_files.get('metadata', ''))}",
        "texts": "{os.path.basename(exported_files.get('texts', ''))}",
        "stats": "{os.path.basename(exported_files.get('stats', ''))}",
        "jsonl": "{os.path.basename(exported_files.get('jsonl', ''))}",
        "sparse": "{os.path.basename(exported_files.get('sparse_jsonl', ''))}",
        "multivectors": "{os.path.basename(exported_files.get('multivectors', ''))}"
    }}

    vector_files = json.loads("""{vector_files_json}""")
    vector_dimensions = json.loads("""{vector_dimensions_json}""")
    dense_vector_names = json.loads("""{dense_vector_names_json}""")
    primary_vector_name = "{primary_vector_name}"

    vector_files = {{name: path for name, path in vector_files.items() if path}}
    dense_vector_names = [name for name in dense_vector_names if name in vector_files]

    try:
        client = QdrantClient(host=qdrant_host, port=qdrant_port)
        logger.info(f"Connected to Qdrant at {{qdrant_host}}:{{qdrant_port}}")

        logger.info("Loading exported data...")
        dense_vectors = {{name: np.load(path) for name, path in vector_files.items()}}

        with open(files["metadata"], "r", encoding="utf-8") as handle:
            metadata_list = json.load(handle)

        with open(files["texts"], "r", encoding="utf-8") as handle:
            texts_list = json.load(handle)

        multivector_channels = {{}}
        multivector_dimensions = {{}}
        multivector_comparators = {{}}

        if files.get("multivectors"):
            with open(files["multivectors"], "r", encoding="utf-8") as handle:
                multivector_blob = json.load(handle)
            multivector_channels = multivector_blob.get("channels", {{}})
            multivector_dimensions = multivector_blob.get("dimensions", {{}})
            multivector_comparators = multivector_blob.get("comparators", {{}})

        if not dense_vectors:
            raise RuntimeError("No dense embedding files were found; cannot proceed with upload")

        point_count = len(metadata_list)

        for name in dense_vector_names:
            vectors = dense_vectors.get(name)
            if vectors is None:
                raise RuntimeError(f"Missing dense vectors for {{name}}")
            if len(vectors) != point_count:
                raise ValueError(
                    f"Vector count mismatch for {{name}}: expected {{point_count}}, got {{len(vectors)}}"
                )
            vector_dim = vector_dimensions.get(name, vectors.shape[1])
            logger.info("Loaded %s embeddings for %s (%sD)", len(vectors), name, vector_dim)

        if files.get("sparse"):
            logger.info("Sparse sidecar detected: %s", files["sparse"])

        multivector_names = list(multivector_channels.keys())
        for name in multivector_names:
            channel_vectors = multivector_channels.get(name, [])
            if len(channel_vectors) != point_count:
                raise ValueError(
                    f"Multivector count mismatch for {{name}}: expected {{point_count}}, got {{len(channel_vectors)}}"
                )
        if multivector_names:
            logger.info("Multivector channels detected: %s", ", ".join(multivector_names))

        try:
            client.get_collection(collection_name)
            logger.info("Collection '%s' already exists", collection_name)
        except Exception:
            logger.info("Creating collection: %s", collection_name)
            vector_params = {{
                name: VectorParams(size=vector_dimensions.get(name, dense_vectors[name].shape[1]), distance=Distance.COSINE)
                for name in dense_vector_names
            }}
            for name in multivector_names:
                dimension = multivector_dimensions.get(name)
                if dimension is None:
                    channel_vectors = multivector_channels.get(name, [])
                    first_non_empty = next((vec for vec in channel_vectors if vec), [])
                    if first_non_empty:
                        dimension = len(first_non_empty[0])
                if dimension is None:
                    raise RuntimeError(f"Could not determine dimension for multivector channel {{name}}")
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
                hnsw_config={{
                    "m": 48,
                    "ef_construct": 512,
                    "full_scan_threshold": 50000,
                }},
                quantization_config={{
                    "scalar": {{
                        "type": "int8",
                        "quantile": 0.99,
                        "always_ram": True,
                    }}
                }},
            )

        logger.info("Preparing points for upload...")
        points = []

        for i in range(point_count):
            metadata = metadata_list[i]
            text = texts_list[i]
            vector_payload = {{
                name: dense_vectors[name][i].tolist()
                for name in dense_vector_names
            }}
            for name in multivector_names:
                channel_data = multivector_channels[name][i]
                if channel_data is None:
                    channel_data = []
                if channel_data and isinstance(channel_data[0], (list, tuple)):
                    channel_data = [list(vec) for vec in channel_data]
                vector_payload[name] = {{"vectors": channel_data}}
            payload_data = {{
                **metadata,
                "text_preview": text[:500],
                "full_text_length": len(text),
                "local_upload_timestamp": datetime.now().isoformat(),
                "primary_vector_name": primary_vector_name,
                "dense_vector_names": dense_vector_names,
            }}
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
        logger.info("Uploading %s points in %s batches...", len(points), total_batches)

        for start in range(0, len(points), batch_size):
            batch = points[start:start + batch_size]
            batch_num = (start // batch_size) + 1

            client.upsert(collection_name=collection_name, points=batch, wait=True)
            logger.info("Uploaded batch %s/%s (%s points)", batch_num, total_batches, len(batch))

        collection_info = client.get_collection(collection_name)
        logger.info("Upload complete; collection has %s points", collection_info.points_count)

        logger.info("Testing search...")
        test_results = client.search(
            collection_name=collection_name,
            query_vector=(
                primary_vector_name,
                dense_vectors[primary_vector_name][0].tolist(),
            ),
            limit=5,
        )

        logger.info("Search test successful; found %s results", len(test_results))
        logger.info("Embeddings are ready for use in collection: %s", collection_name)

    except Exception as exc:
        logger.error("Upload failed: %s", exc)
        raise


if __name__ == "__main__":
    upload_to_qdrant()
'''
        )

        with open(file_path, "w", encoding="utf-8") as handle:
            handle.write(script_content)


__all__ = ["ExportRuntime"]
