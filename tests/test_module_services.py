import json
import logging
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import numpy as np
import pytest

from processor.ultimate_embedder.batch_runner import BatchRunner
from processor.ultimate_embedder.chunk_loader import ChunkLoader
from processor.ultimate_embedder.config import (
    KaggleExportConfig,
    KaggleGPUConfig,
    ModelConfig,
    RerankingConfig,
)
from processor.ultimate_embedder.export_runtime import ExportRuntime
from processor.ultimate_embedder.model_manager import ModelManager
from processor.ultimate_embedder.monitoring import PerformanceMonitor
from processor.ultimate_embedder.rerank_pipeline import RerankPipeline
from processor.ultimate_embedder.sparse_pipeline import (
    build_sparse_vector_from_metadata,
    infer_modal_hint,
)
from processor.ultimate_embedder.telemetry import TelemetryTracker


def test_chunk_loader_enriches_metadata(tmp_path):
    chunk_dir = tmp_path / "qdrant_chunks"
    chunk_dir.mkdir()
    data = [
        {
            "text": "Example text",
            "metadata": {
                "token_count": 120,
                "source_path": "Docs/A.md",
                "search_keywords": ["existing"],
            },
        }
    ]
    with open(chunk_dir / "sample_chunks.json", "w", encoding="utf-8") as handle:
        json.dump(data, handle)

    loader = ChunkLoader(project_root=tmp_path, is_kaggle=False, logger=logging.getLogger(__name__))
    result = loader.load(
        str(chunk_dir),
        preprocess_text=lambda value: value.upper(),
        model_name="primary",
        model_vector_dim=3,
    )

    assert len(result.metadata) == 1
    assert result.processed_texts[0] == "EXAMPLE TEXT"
    assert result.summary["total_chunks_loaded"] == 1
    assert result.canonical_collection_hint == "qdrant_ecosystem"


def test_model_manager_records_cache_events(tmp_path):
    cache_root = tmp_path / "models--repo--id"
    snapshot_dir = cache_root / "snapshots" / "123"
    snapshot_dir.mkdir(parents=True)

    class DummyEmbedder:
        def __init__(self) -> None:
            self.device = "cpu"
            self.hf_cache_dir = tmp_path
            self.force_cache_refresh = False
            self.local_files_only = True
            self.telemetry = TelemetryTracker()

    manager = ModelManager(cast(Any, DummyEmbedder()), logging.getLogger(__name__))
    path = manager.ensure_model_snapshot("repo/id")

    assert snapshot_dir.samefile(path)
    assert manager.embedder.telemetry.cache_events


def test_batch_runner_aggregates_embeddings(build_embedder, monkeypatch):
    embedder = build_embedder()
    embedder.model_config.vector_dim = 3
    embedder.matryoshka_dim = 3
    embedder.enable_ensemble = True

    base_vectors = np.tile(np.arange(3, dtype=np.float32), (len(embedder.chunk_texts), 1))

    def fake_generate(texts, **_):
        return base_vectors[: len(texts)]

    monkeypatch.setattr(embedder, "generate_ensemble_embeddings", fake_generate)
    monkeypatch.setattr(embedder, "_ensure_embedding_dimension", lambda matrix, expected_dim=None: (matrix, False))
    monkeypatch.setattr(embedder, "_normalize_embedding_matrix", lambda matrix, name: matrix)
    monkeypatch.setattr(embedder, "_collect_gpu_snapshots", lambda: {})
    monkeypatch.setattr(embedder, "_log_batch_sources", lambda *args, **kwargs: None)
    monkeypatch.setattr(embedder, "_save_intermediate_results", lambda *args, **kwargs: None)
    monkeypatch.setattr(embedder, "_start_performance_monitoring", lambda: None)
    monkeypatch.setattr(embedder, "_stop_performance_monitoring", lambda: None)
    monkeypatch.setattr(embedder, "_require_embeddings", lambda: embedder.embeddings)

    runner = BatchRunner(embedder, logging.getLogger(__name__))
    results = runner.run(enable_monitoring=False, save_intermediate=False)

    assert results["total_embeddings_generated"] == len(embedder.chunk_texts)
    assert embedder.embeddings.shape == (len(embedder.chunk_texts), 3)
    assert np.allclose(embedder.embeddings, base_vectors)


def test_sparse_pipeline_builds_vector():
    metadata = {
        "sparse_features": {
            "term_weights": [
                {"term": "vector", "weight": 2.0},
                {"term": "search", "weight": 1.0},
            ]
        }
    }

    vector = build_sparse_vector_from_metadata(metadata)
    assert vector is not None
    assert len(vector["indices"]) == 2
    assert np.linalg.norm(vector["values"]) == pytest.approx(1.0, rel=1e-3)

    hint = infer_modal_hint("def foo():\n    return 1", metadata={})
    assert hint == "code"


def test_rerank_pipeline_uses_cross_encoder(monkeypatch):
    scores = [0.9, 0.2]

    class FakeCrossEncoder:
        def __init__(self, *_, **__):
            pass

        def predict(self, pairs):
            return scores[: len(pairs)]

    monkeypatch.setattr("processor.ultimate_embedder.rerank_pipeline.CrossEncoder", FakeCrossEncoder)

    config = RerankingConfig(enable_reranking=True)
    pipeline = RerankPipeline(config, logging.getLogger(__name__))
    pipeline.ensure_model(device="cpu")

    class DummyEncoder:
        def encode(self, texts, convert_to_numpy, normalize_embeddings, device):
            return np.ones((len(texts), 3), dtype=np.float32)

    embeddings = np.stack([np.array([1, 0, 0], dtype=np.float32), np.array([0, 1, 0], dtype=np.float32)])
    metadata = [{"id": 0}, {"id": 1}]
    results = pipeline.search(
        "query",
        encode_model=DummyEncoder(),
        device="cpu",
        embeddings=embeddings,
        chunk_texts=["one", "two"],
        chunks_metadata=metadata,
        top_k=1,
        initial_candidates=2,
    )

    assert results[0]["chunk_id"] == 1
    assert results[0]["score"] == pytest.approx(scores[0])


def test_performance_monitor_start_stop(monkeypatch):
    embedder = SimpleNamespace(
        device_count=0,
        processing_stats={"system_metrics": [], "gpu_memory": []},
    )

    calls = []

    def fake_loop(self):
        calls.append(True)

    monkeypatch.setattr(PerformanceMonitor, "_monitor_loop", fake_loop)

    monitor = PerformanceMonitor(cast(Any, embedder), logging.getLogger(__name__))
    monitor.start()
    monitor.stop()

    assert not monitor._active
    assert calls


def test_export_runtime_generates_outputs(tmp_path):
    embeddings = np.array([[0.5, 0.5]], dtype=np.float32)

    class DummyEmbedder:
        def __init__(self) -> None:
            self.embeddings = embeddings
            self.embeddings_by_model = {"primary": embeddings}
            self.model_name = "primary"
            self.model_config = ModelConfig(
                name="primary",
                hf_model_id="repo/model",
                vector_dim=2,
                max_tokens=10,
            )
            self.device_count = 0
            self.gpu_config = KaggleGPUConfig()
            self.export_config = KaggleExportConfig(
                working_dir=str(tmp_path),
                output_prefix="unit",
                export_sparse_jsonl=False,
                export_faiss=False,
            )
            self.chunks_metadata = [{"id": 0}]
            self.chunk_texts = ["sample text"]
            self.sparse_vectors = [None]
            self.multivectors_by_model = {}
            self.multivector_dimensions = {}
            self.multivector_comparators = {}
            self.processing_stats = {"system_metrics": [], "gpu_memory": []}
            self.text_cache = None
            self.telemetry = TelemetryTracker()
            self.is_kaggle = False

        def _require_embeddings(self):
            return self.embeddings

        def get_target_collection_name(self) -> str:
            return "primary_collection"

    runtime = ExportRuntime(cast(Any, DummyEmbedder()), logging.getLogger(__name__))
    files = runtime.export_for_local_qdrant()

    expected_keys = {"numpy", "jsonl", "metadata", "texts", "stats", "upload_script", "qdrant_collection"}
    assert expected_keys.issubset(files.keys())
    for key in expected_keys - {"qdrant_collection"}:
        assert Path(files[key]).exists()
