"""Tests for the export runtime JSONL writer."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from processor.ultimate_embedder.export_runtime import ExportRuntime
from processor.ultimate_embedder.summary import SCHEMA_VERSION


class _DummyModelConfig:
    def __init__(self, hf_model_id: str, vector_dim: int) -> None:
        self.hf_model_id = hf_model_id
        self.vector_dim = vector_dim


class _DummyCompanionConfig:
    def __init__(self, hf_model_id: str) -> None:
        self.hf_model_id = hf_model_id


class _StubEmbedder:
    """Minimal stub satisfying ExportRuntime dependencies."""

    def __init__(self) -> None:
        self.model_name = "primary-model"
        self.model_config = _DummyModelConfig("primary/model", 3)
        self.companion_model_configs: Dict[str, _DummyCompanionConfig] = {
            "companion-model": _DummyCompanionConfig("companion/model"),
        }
        self.embeddings_by_model: Dict[str, np.ndarray] = {
            self.model_name: np.array([[0.1, 0.2, 0.3]], dtype=np.float32),
            "companion-model": np.array([[0.4, 0.5, 0.6]], dtype=np.float32),
        }
        self.chunks_metadata: List[Dict[str, Any]] = [{"chunk_id": "chunk-1"}]
        self.chunk_texts: List[str] = ["example chunk"]
        self.sparse_vectors: List[Dict[str, Any]] = [
            {
                "indices": [0, 1],
                "values": [0.9, 0.1],
                "tokens": ["token-a", "token-b"],
                "stats": {"weighting": "tf"},
            }
        ]
        self.multivectors_by_model: Dict[str, Any] = {}
        self.multivector_dimensions: Dict[str, int] = {}
        self.multivector_comparators: Dict[str, str] = {}


def test_export_qdrant_jsonl_uses_schema_version(tmp_path: Path) -> None:
    """Ensure JSONL payload advertises the v4.1 schema version."""

    embedder = _StubEmbedder()
    runtime = ExportRuntime(embedder, logging.getLogger("export-runtime-test"))

    embeddings = embedder.embeddings_by_model[embedder.model_name]
    companion_arrays = {
        name: array
        for name, array in embedder.embeddings_by_model.items()
        if name != embedder.model_name
    }

    output_path = tmp_path / "points.jsonl"
    runtime._export_qdrant_jsonl(str(output_path), embeddings, companion_arrays)

    assert output_path.exists()

    lines = output_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1

    record = json.loads(lines[0])
    payload = record["payload"]

    assert payload["model_info"]["version"] == SCHEMA_VERSION
    assert payload["dense_vector_names"] == [embedder.model_name, "companion-model"]