"""Tests for the export runtime JSONL writer."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

from processor.ultimate_embedder.export_runtime import ExportRuntime
from processor.ultimate_embedder.summary import SCHEMA_VERSION
from processor.ultimate_embedder.runtime_config import FeatureToggleConfig


class _DummyModelConfig:
    def __init__(self, hf_model_id: str, vector_dim: int, max_tokens: int = 1024) -> None:
        self.hf_model_id = hf_model_id
        self.vector_dim = vector_dim
        self.max_tokens = max_tokens


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


class _ExportTelemetryStub:
    def __init__(self) -> None:
        self.batch_progress_events: List[Dict[str, Any]] = []
        self.gpu_lease_events: List[Dict[str, Any]] = []
        self.last_span: Optional[Dict[str, Any]] = None

    def record_span_presence(self, *args, **kwargs) -> None:
        self.last_span = {"args": args, "kwargs": kwargs}


class _ExportConfigStub:
    def __init__(self, root: Path) -> None:
        self.working_dir = str(root)
        self.output_prefix = "export_artifact"
        self.export_numpy = True
        self.export_jsonl = False
        self.export_faiss = False
        self.export_sparse_jsonl = False

    def get_output_path(self, suffix: str = "", collection_name: Optional[str] = None) -> str:
        target_dir = Path(self.working_dir)
        if collection_name:
            safe_collection = "".join(
                char if char.isalnum() or char in {"-", "_"} else "_"
                for char in collection_name
            ).strip("_") or "collection"
            target_dir = target_dir / safe_collection
        target_dir.mkdir(parents=True, exist_ok=True)
        return str(target_dir / f"{self.output_prefix}{suffix}")


class _ExportEmbedderStub:
    def __init__(self, root: Path) -> None:
        self.model_name = "primary-model"
        self.model_config = _DummyModelConfig("primary/model", 3)
        self.embeddings = np.array([[0.1, 0.2, 0.3]], dtype=np.float32)
        self.embeddings_by_model: Dict[str, np.ndarray] = {
            self.model_name: self.embeddings,
            "vendor/model-name": np.array([[0.9, 0.8, 0.7]], dtype=np.float32),
        }
        self.companion_model_configs = {
            "vendor/model-name": _DummyModelConfig("vendor/model-name", 3)
        }
        self.chunks_metadata: List[Dict[str, Any]] = [{"chunk_id": "chunk-1"}]
        self.chunk_texts: List[str] = ["example chunk"]
        self.sparse_vectors: List[Dict[str, Any]] = [{}]
        self.multivectors_by_model: Dict[str, Any] = {}
        self.multivector_dimensions: Dict[str, int] = {}
        self.multivector_comparators: Dict[str, str] = {}
        self.processing_stats: Dict[str, List[Dict[str, Any]]] = {"dense_batches": []}
        self.export_config = _ExportConfigStub(root)
        self.telemetry = _ExportTelemetryStub()
        self.gpu_config = type(
            "GPUConfigStub",
            (),
            {"backend": "pytorch", "precision": "fp32", "total_vram_gb": 0.0},
        )()
        self.device = "cpu"
        self.device_count = 1
        self.feature_toggles = FeatureToggleConfig()
        self.metrics_payloads: List[Dict[str, Any]] = []
        self.is_kaggle = False
        self.last_processing_summary: Dict[str, Any] = {}
        self.text_cache = None
        self.reranking_config = type(
            "RerankConfigStub",
            (),
            {
                "enable_reranking": False,
                "top_k_candidates": 0,
                "rerank_top_k": 0,
                "batch_size": 0,
            },
        )()
        self.rerank_run = None
        self.rerank_failure_reason = None
        self.fused_candidates: Dict[str, Any] = {}
        self._requested_rerank_device = "cpu"
        self.reranker_device = "cpu"
        self.rerank_fallback_count = 0
        self.rerank_fallback_reason = None
        self.rerank_fallback_source = None

    def _require_embeddings(self) -> np.ndarray:
        return self.embeddings

    def get_active_collection_alias(self) -> Optional[str]:
        return "alias/sample"

    def get_target_collection_name(self) -> str:
        return "sample_collection"

    def _emit_metrics_for_stage(
        self,
        stage: str,
        *,
        active: bool,
        reason: str,
        details: Optional[Dict[str, Any]] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.metrics_payloads.append(
            {
                "stage": stage,
                "active": active,
                "reason": reason,
                "details": details or {},
                "attributes": attributes or {},
            }
        )


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


def test_export_qdrant_jsonl_includes_multivectors(tmp_path: Path) -> None:
    """Verify multivector channels are emitted when provided by the embedder."""

    embedder = _StubEmbedder()
    channel_name = "primary-model_matryoshka_2"
    embedder.multivectors_by_model = {channel_name: [[[0.1, 0.2]]]}
    embedder.multivector_dimensions = {channel_name: 2}
    embedder.multivector_comparators = {channel_name: "max_sim"}

    runtime = ExportRuntime(embedder, logging.getLogger("export-runtime-test"))

    embeddings = embedder.embeddings_by_model[embedder.model_name]
    companion_arrays = {
        name: array
        for name, array in embedder.embeddings_by_model.items()
        if name != embedder.model_name
    }

    output_path = tmp_path / "points.jsonl"
    runtime._export_qdrant_jsonl(str(output_path), embeddings, companion_arrays)

    record = json.loads(output_path.read_text(encoding="utf-8").strip())
    payload = record["payload"]

    multivectors = payload["model_info"].get("multivectors")
    assert multivectors is not None
    assert channel_name in multivectors
    assert multivectors[channel_name]["dimension"] == 2
    assert multivectors[channel_name]["comparator"] == "max_sim"

    vector_payload = record["vectors"].get(channel_name)
    assert vector_payload == {"vectors": [[0.1, 0.2]]}


def test_export_for_local_qdrant_sanitizes_companion_filenames(tmp_path: Path) -> None:
    """Companion embeddings use filesystem-safe filenames during export."""

    embedder = _ExportEmbedderStub(tmp_path)
    runtime = ExportRuntime(embedder, logging.getLogger("export-runtime-test"))

    exported = runtime.export_for_local_qdrant()

    companion_key = "numpy_vendor_model_name"
    assert companion_key in exported

    companion_path = Path(exported[companion_key])
    assert companion_path.exists()
    assert companion_path.name.endswith("vendor_model_name_embeddings.npy")
    assert "alias_sample" in str(companion_path.parent)

    upload_script = Path(exported["upload_script"]).read_text(encoding="utf-8")
    assert "vendor_model_name_embeddings.npy" in upload_script