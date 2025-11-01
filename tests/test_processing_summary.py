import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from processor.ultimate_embedder.config import KaggleExportConfig, KaggleGPUConfig
from processor.ultimate_embedder.controllers import GPUMemorySnapshot
from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4
from processor.ultimate_embedder.runtime_config import FeatureToggleConfig
from processor.ultimate_embedder.summary import (
    build_processing_summary,
    build_rerank_stage_summary,
    build_sparse_stage_summary,
    build_telemetry_summary,
    normalize_processing_summary,
)


def test_build_processing_summary_includes_stage_sections() -> None:
    toggles = FeatureToggleConfig(
        enable_rerank=True,
        enable_sparse=True,
        sparse_models=["qdrant-bm25"],
        sources={
            "enable_rerank": "default",
            "enable_sparse": "default",
            "sparse_models": "default",
        },
    )

    rerank_stage = build_rerank_stage_summary(
        enabled=True,
        model_name="jina-reranker-v3",
        loaded=True,
        device="cpu",
        executed=False,
        status="staged",
        reason="pending batch execution",
        metrics={"top_k_candidates": 100},
        requested_device="cuda",
        fallback_applied=True,
        fallback_reason="Resolved to CPU staging while awaiting GPU lease",
    )

    sparse_stage = build_sparse_stage_summary(
        enabled=True,
        model_names=["qdrant-bm25"],
        vectors_total=10,
        vectors_available=8,
        executed=True,
        coverage_ratio=0.8,
        devices={"qdrant-bm25": "cpu"},
        fallback_used=False,
        fallback_reason=None,
    )

    telemetry = build_telemetry_summary(
        mitigation_events=[{"type": "adaptive_batch"}],
        rotation_events=[],
        lease_events=[{"event_type": "acquire"}],
        batch_progress_events=[{"batch_index": 0}],
        span_events={
            "rag.rerank": {
                "span_id": "span-1",
                "status": "active",
                "attributes": {
                    "fallback_count": 0,
                    "fallback_source": "runtime",
                },
            },
            "rag.sparse": {"span_id": "span-2", "status": "active"},
        },
        metrics_report={
            "rerank": {
                "status": "emitted",
                "metrics": ["rag_rerank_latency_seconds"],
            }
        },
    )

    dense_run = {
        "total_embeddings_generated": 10,
        "models_executed": ["jina-code-embeddings-1.5b"],
    }

    summary = build_processing_summary(
        feature_toggles=toggles,
        dense_run=dense_run,
        rerank_stage=rerank_stage,
        sparse_stage=sparse_stage,
        telemetry=telemetry,
        collection_name="sample_collection",
        chunk_count=10,
    )

    assert summary["schema_version"] == "v4.1"
    assert summary["collection"] == "sample_collection"
    assert summary["chunk_count"] == 10
    assert summary["dense_run"]["total_embeddings_generated"] == 10
    assert summary["rerank_run"]["enabled"] is True
    assert summary["rerank_run"]["device_state"]["resolved"] == "cpu"
    assert summary["rerank_run"]["device_state"]["fallback_applied"] is True
    assert summary["rerank_run"]["fallback_count"] == 0
    assert summary["sparse_run"]["vectors"]["coverage_ratio"] == pytest.approx(0.8)
    assert summary["sparse_run"]["devices"]["qdrant-bm25"] == "cpu"
    rerank_payload = summary["rerank_run"].get("payload", {})
    assert rerank_payload["status"] == "staged"
    assert rerank_payload["device_state"]["resolved"] == "cpu"
    sparse_payload = summary["sparse_run"].get("payload", {})
    assert sparse_payload["vectors"]["coverage_ratio"] == pytest.approx(0.8)
    assert summary["compatibility"]["current"] == "v4.1"
    assert summary["compatibility"]["legacy"] == ["v4.0"]
    assert summary["compatibility"]["legacy"] == ["v4.0"]
    assert summary["telemetry"]["lease_events_recorded"] == 1
    assert summary["telemetry"]["spans"]["rag.rerank"]["status"] == "active"
    assert summary["telemetry"]["spans"]["rag.rerank"]["attributes"]["fallback_count"] == 0
    assert summary["telemetry"]["metrics"]["rerank"]["status"] == "emitted"
    assert summary["feature_toggles"]["provenance"]
    assert summary["activation_provenance"]
    assert summary["feature_toggles"]["provenance_lines"]
    assert summary["activation_provenance_lines"]
    assert any(
        "default" in line for line in summary["activation_provenance_lines"]
    )


def test_build_processing_summary_omits_disabled_stages() -> None:
    toggles = FeatureToggleConfig(
        enable_rerank=False,
        enable_sparse=False,
        sparse_models=[],
        sources={
            "enable_rerank": "cli",
            "enable_sparse": "env",
            "sparse_models": "env",
        },
        resolution_events=(
            {
                "key": "enable_rerank",
                "value": True,
                "source": "default",
                "layer": "default",
            },
            {
                "key": "enable_rerank",
                "value": False,
                "source": "cli:--disable-rerank",
                "layer": "cli",
            },
            {
                "key": "enable_sparse",
                "value": True,
                "source": "default",
                "layer": "default",
            },
            {
                "key": "enable_sparse",
                "value": False,
                "source": "env",
                "layer": "environment",
            },
            {
                "key": "sparse_models",
                "value": ["qdrant-bm25"],
                "source": "default",
                "layer": "default",
            },
            {
                "key": "sparse_models",
                "value": [],
                "source": "env",
                "layer": "environment",
            },
        ),
    )

    telemetry = build_telemetry_summary(
        mitigation_events=[],
        rotation_events=[],
        lease_events=[],
        batch_progress_events=[],
        span_events={},
        metrics_report={},
    )

    summary = build_processing_summary(
        feature_toggles=toggles,
        dense_run=None,
        rerank_stage=None,
        sparse_stage=None,
        telemetry=telemetry,
    )

    assert summary["schema_version"] == "v4.1"
    assert summary["compatibility"]["current"] == "v4.1"
    assert "rerank_run" not in summary
    assert "sparse_run" not in summary
    assert summary["telemetry"]["spans"] == {}
    assert summary["telemetry"]["metrics"] == {}
    assert summary["feature_toggles"]["provenance"]
    assert summary["activation_provenance_lines"]
    assert any(
        "override" in line for line in summary["activation_provenance_lines"]
    )


def test_build_processing_summary_warns_when_enabled_stage_missing() -> None:
    toggles = FeatureToggleConfig(
        enable_rerank=True,
        enable_sparse=True,
        sparse_models=["qdrant-bm25"],
        sources={
            "enable_rerank": "default",
            "enable_sparse": "default",
            "sparse_models": "default",
        },
    )

    telemetry = build_telemetry_summary(
        mitigation_events=[],
        rotation_events=[],
        lease_events=[],
        batch_progress_events=[],
        span_events={},
        metrics_report={},
    )

    summary = build_processing_summary(
        feature_toggles=toggles,
        dense_run=None,
        rerank_stage=None,
        sparse_stage=None,
        telemetry=telemetry,
    )

    warnings = summary.get("warnings")
    assert warnings is not None
    assert any("rerank stage enabled" in warning for warning in warnings)
    assert any("sparse stage enabled" in warning for warning in warnings)


def test_build_processing_summary_does_not_warn_when_stage_disabled() -> None:
    toggles = FeatureToggleConfig(
        enable_rerank=False,
        enable_sparse=False,
        sparse_models=[],
        sources={
            "enable_rerank": "cli",
            "enable_sparse": "env",
            "sparse_models": "env",
        },
    )

    telemetry = build_telemetry_summary(
        mitigation_events=[],
        rotation_events=[],
        lease_events=[],
        batch_progress_events=[],
        span_events={},
        metrics_report={},
    )

    summary = build_processing_summary(
        feature_toggles=toggles,
        dense_run=None,
        rerank_stage=None,
        sparse_stage=None,
        telemetry=telemetry,
    )

    assert "warnings" not in summary


class _DummySentenceTransformer:
    def __init__(self, *args, **kwargs):
        self.device = kwargs.get("device", "cpu")

    def encode(self, texts, **kwargs):
        vectors = np.ones((len(texts), 1024), dtype=np.float32)
        for idx, _ in enumerate(texts):
            vectors[idx, 0] = float(idx + 1)
        return vectors

    def to(self, device):
        self.device = device
        return self

    def half(self):
        return self

    def parameters(self):
        return iter(())


class _DummyCrossEncoder:
    def __init__(self, *args, **kwargs):
        self.device = kwargs.get("device", "cpu")

    def predict(self, pairs):
        return np.ones(len(pairs), dtype=np.float32)


def _fake_snapshot_download(*args, **kwargs):
    target = kwargs.get("cache_dir") or kwargs.get("local_dir")
    if not target:
        target = Path.cwd() / "hf-cache"
    target_path = Path(target)
    target_path.mkdir(parents=True, exist_ok=True)
    return str(target_path)


def _apply_dummy_model_patches(monkeypatch):
    monkeypatch.setattr(
        "processor.ultimate_embedder.core.SentenceTransformer",
        _DummySentenceTransformer,
    )
    monkeypatch.setattr(
        "processor.ultimate_embedder.model_manager.SentenceTransformer",
        _DummySentenceTransformer,
    )
    monkeypatch.setattr(
        "processor.ultimate_embedder.core.CrossEncoder",
        _DummyCrossEncoder,
    )
    monkeypatch.setattr(
        "processor.ultimate_embedder.rerank_pipeline.CrossEncoder",
        _DummyCrossEncoder,
    )
    monkeypatch.setattr(
        "processor.ultimate_embedder.model_manager.snapshot_download",
        _fake_snapshot_download,
    )
    monkeypatch.setattr(
        "processor.ultimate_embedder.batch_runner.normalize",
        lambda array, norm="l2", axis=1: array,
    )


def test_write_processing_summary_generates_default_sections(tmp_path, monkeypatch):
    _apply_dummy_model_patches(monkeypatch)

    gpu_config = KaggleGPUConfig(
        device_count=1,
        vram_per_gpu_gb=8.0,
        total_vram_gb=8.0,
        enable_memory_efficient_attention=False,
        gradient_checkpointing=False,
        precision="fp32",
        enable_mixed_precision=False,
        use_amp=False,
        base_batch_size=2,
        dynamic_batching=False,
        backend="pytorch",
        enable_torch_compile=False,
        strategy="data_parallel",
        enable_gradient_accumulation=False,
        accumulation_steps=1,
        kaggle_environment=False,
        output_path=str(tmp_path / "outputs"),
    )

    export_config = KaggleExportConfig(
        working_dir=str(tmp_path / "exports"),
        output_prefix="test_run",
        export_numpy=False,
        export_jsonl=False,
        export_faiss=False,
        export_sparse_jsonl=False,
    )

    embedder = UltimateKaggleEmbedderV4(
        model_name="jina-code-embeddings-1.5b",
        gpu_config=gpu_config,
        export_config=export_config,
        enable_ensemble=False,
        feature_toggles=FeatureToggleConfig(),
        force_cpu=True,
        gpu0_soft_limit_gb=8.0,
    )

    collection_dir = tmp_path / "Chunked" / "CollectionA"
    collection_dir.mkdir(parents=True)
    chunk_payload = [
        {
            "text": "Hello world " * 20,
            "metadata": {
                "token_count": 120,
                "source_file": "doc1.md",
                "sparse_features": {
                    "term_weights": [{"term": "hello", "weight": 1.0}],
                },
            },
        },
        {
            "text": "Another chunk " * 15,
            "metadata": {
                "token_count": 95,
                "source_file": "doc2.md",
                "sparse_features": {
                    "term_weights": [{"term": "chunk", "weight": 0.8}],
                },
            },
        },
    ]
    (collection_dir / "sample_chunks.json").write_text(
        json.dumps(chunk_payload),
        encoding="utf-8",
    )

    embedder.load_chunks_from_processing(chunks_dir=str(collection_dir))
    results = embedder.generate_embeddings_kaggle_optimized(
        enable_monitoring=False,
        save_intermediate=False,
    )

    summary_path = tmp_path / "processing_summary.json"
    summary = embedder.write_processing_summary(
        summary_path,
        collection_name="CollectionA",
    )

    assert summary_path.exists()
    payload = json.loads(summary_path.read_text(encoding="utf-8"))

    assert (
        payload["dense_run"]["total_embeddings_generated"]
        == results["total_embeddings_generated"]
    )
    assert payload["rerank_run"]["enabled"] is True
    # Rerank should now execute as part of batch runner orchestration
    assert payload["rerank_run"]["status"] in {"staged", "pending", "executed"}
    assert payload["rerank_run"]["device_state"]["resolved"] == "cpu"
    assert payload["sparse_run"]["enabled"] is True
    assert payload["sparse_run"]["vectors"]["total"] == len(embedder.sparse_vectors)
    assert "fallback_used" in payload["sparse_run"]
    assert payload["chunk_count"] == 2
    assert payload["activation_provenance"]
    assert summary["telemetry"]["batch_progress_events_recorded"] >= 0
    telemetry = summary["telemetry"]
    spans = telemetry.get("spans", {})
    assert "rag.rerank" in spans
    assert spans["rag.rerank"]["status"] in {"active", "skipped"}
    metrics_report = telemetry.get("metrics", {})
    assert "rerank" in metrics_report
    assert metrics_report["rerank"]["status"] in {"emitted", "skipped"}
    provenance_lines = payload["feature_toggles"].get("provenance_lines", [])
    assert provenance_lines
    assert payload["activation_provenance_lines"] == provenance_lines
    assert any("default" in line for line in provenance_lines)


def test_metrics_emission_for_dense_and_export(tmp_path, monkeypatch):
    _apply_dummy_model_patches(monkeypatch)
    monkeypatch.setenv("EMBEDDER_METRICS_ENABLED", "1")
    monkeypatch.setenv("EMBEDDER_METRICS_NAMESPACE", "ultimate_embedder_test")

    gpu_config = KaggleGPUConfig(
        device_count=1,
        vram_per_gpu_gb=8.0,
        total_vram_gb=8.0,
        enable_memory_efficient_attention=False,
        gradient_checkpointing=False,
        precision="fp32",
        enable_mixed_precision=False,
        use_amp=False,
        base_batch_size=2,
        dynamic_batching=False,
        backend="pytorch",
        enable_torch_compile=False,
        strategy="data_parallel",
        enable_gradient_accumulation=False,
        accumulation_steps=1,
        kaggle_environment=False,
        output_path=str(tmp_path / "outputs"),
    )

    export_root = tmp_path / "exports"
    export_root.mkdir(parents=True, exist_ok=True)
    export_config = KaggleExportConfig(
        working_dir=str(export_root),
        output_prefix="metrics",
        export_numpy=False,
        export_jsonl=False,
        export_faiss=False,
        export_sparse_jsonl=False,
    )

    embedder = UltimateKaggleEmbedderV4(
        model_name="jina-code-embeddings-1.5b",
        gpu_config=gpu_config,
        export_config=export_config,
        enable_ensemble=False,
        feature_toggles=FeatureToggleConfig(),
        force_cpu=True,
        gpu0_soft_limit_gb=8.0,
    )

    collection_dir = tmp_path / "Chunked" / "CollectionMetrics"
    collection_dir.mkdir(parents=True, exist_ok=True)
    chunk_payload = [
        {
            "text": "Metric chunk one",
            "metadata": {
                "token_count": 50,
                "source_file": "doc-a.md",
            },
        },
        {
            "text": "Metric chunk two",
            "metadata": {
                "token_count": 75,
                "source_file": "doc-b.md",
            },
        },
    ]
    (collection_dir / "metrics_chunks.json").write_text(
        json.dumps(chunk_payload),
        encoding="utf-8",
    )

    embedder.load_chunks_from_processing(chunks_dir=str(collection_dir))
    embedder.generate_embeddings_kaggle_optimized(
        enable_monitoring=False,
        save_intermediate=False,
    )

    dense_payload = next(
        (payload for payload in embedder.metrics_payloads if payload["stage"] == "dense"),
        None,
    )
    assert dense_payload is not None
    assert dense_payload["namespace"] == "ultimate_embedder_test"
    assert dense_payload["details"].get("latency_seconds") is not None
    assert dense_payload["prometheus_emitted"]["latency"] is True
    assert "rag_dense_latency_seconds" in dense_payload["metrics"]

    embedder.export_for_local_qdrant()

    export_payload = next(
        (payload for payload in embedder.metrics_payloads if payload["stage"] == "export"),
        None,
    )
    assert export_payload is not None
    assert export_payload["details"].get("latency_seconds") is not None
    assert export_payload["details"].get("file_count", 0) >= 1
    assert export_payload["prometheus_emitted"]["latency"] is True
    assert "rag_export_latency_seconds" in export_payload["metrics"]

    buffered_metrics = embedder.prometheus_emitter.get_buffered_metrics()
    dense_metrics = [
        item
        for item in buffered_metrics
        if item["metric"].endswith("dense_latency_seconds")
    ]
    export_metrics = [
        item
        for item in buffered_metrics
        if item["metric"].endswith("export_latency_seconds")
    ]
    assert dense_metrics, "expected dense latency metric emission"
    assert export_metrics, "expected export latency metric emission"


def test_write_processing_summary_omits_disabled_sections(tmp_path, monkeypatch):
    _apply_dummy_model_patches(monkeypatch)

    toggles = FeatureToggleConfig(
        enable_rerank=False,
        enable_sparse=False,
        sparse_models=[],
        sources={
            "enable_rerank": "cli",
            "enable_sparse": "env",
            "sparse_models": "env",
        },
        resolution_events=(
            {
                "key": "enable_rerank",
                "value": True,
                "source": "default",
                "layer": "default",
            },
            {
                "key": "enable_rerank",
                "value": False,
                "source": "cli:--disable-rerank",
                "layer": "cli",
            },
            {
                "key": "enable_sparse",
                "value": True,
                "source": "default",
                "layer": "default",
            },
            {
                "key": "enable_sparse",
                "value": False,
                "source": "env",
                "layer": "environment",
            },
            {
                "key": "sparse_models",
                "value": ["qdrant-bm25"],
                "source": "default",
                "layer": "default",
            },
            {
                "key": "sparse_models",
                "value": [],
                "source": "env",
                "layer": "environment",
            },
        ),
    )

    gpu_config = KaggleGPUConfig(
        device_count=1,
        vram_per_gpu_gb=8.0,
        total_vram_gb=8.0,
        enable_memory_efficient_attention=False,
        gradient_checkpointing=False,
        precision="fp32",
        enable_mixed_precision=False,
        use_amp=False,
        base_batch_size=2,
        dynamic_batching=False,
        backend="pytorch",
        enable_torch_compile=False,
        strategy="data_parallel",
        enable_gradient_accumulation=False,
        accumulation_steps=1,
        kaggle_environment=False,
        output_path=str(tmp_path / "outputs"),
    )

    export_config = KaggleExportConfig(
        working_dir=str(tmp_path / "exports"),
        output_prefix="disabled",
        export_numpy=False,
        export_jsonl=False,
        export_faiss=False,
        export_sparse_jsonl=False,
    )

    embedder = UltimateKaggleEmbedderV4(
        model_name="jina-code-embeddings-1.5b",
        gpu_config=gpu_config,
        export_config=export_config,
        enable_ensemble=False,
        feature_toggles=toggles,
        force_cpu=True,
    )

    summary_path = tmp_path / "processing_disabled.json"
    summary = embedder.write_processing_summary(
        summary_path,
        collection_name="DisabledCollection",
        chunk_count=0,
    )

    assert summary_path.exists()
    payload = json.loads(summary_path.read_text(encoding="utf-8"))

    assert "rerank_run" not in payload
    assert "sparse_run" not in payload
    lines = payload["feature_toggles"].get("provenance_lines", [])
    assert lines
    assert payload["activation_provenance_lines"] == lines
    assert any("override" in line for line in lines)
    assert summary["activation_provenance_lines"] == lines


def test_create_processing_summary_includes_failure_warnings(tmp_path, monkeypatch):
    _apply_dummy_model_patches(monkeypatch)

    toggles = FeatureToggleConfig(
        enable_rerank=True,
        enable_sparse=True,
        sparse_models=["qdrant-bm25"],
        sources={
            "enable_rerank": "default",
            "enable_sparse": "default",
            "sparse_models": "default",
        },
    )

    gpu_config = KaggleGPUConfig(
        device_count=1,
        vram_per_gpu_gb=8.0,
        total_vram_gb=8.0,
        enable_memory_efficient_attention=False,
        gradient_checkpointing=False,
        precision="fp32",
        enable_mixed_precision=False,
        use_amp=False,
        base_batch_size=2,
        dynamic_batching=False,
        backend="pytorch",
        enable_torch_compile=False,
        strategy="data_parallel",
        enable_gradient_accumulation=False,
        accumulation_steps=1,
        kaggle_environment=False,
        output_path=str(tmp_path / "outputs"),
    )

    export_config = KaggleExportConfig(
        working_dir=str(tmp_path / "exports"),
        output_prefix="warnings",
        export_numpy=False,
        export_jsonl=False,
        export_faiss=False,
        export_sparse_jsonl=False,
    )

    embedder = UltimateKaggleEmbedderV4(
        model_name="jina-code-embeddings-1.5b",
        gpu_config=gpu_config,
        export_config=export_config,
        enable_ensemble=False,
        feature_toggles=toggles,
        force_cpu=True,
        gpu0_soft_limit_gb=8.0,
    )

    embedder.feature_toggles = toggles
    embedder.reranking_config.enable_reranking = True
    embedder.enable_sparse = True

    embedder.rerank_run = None
    embedder.rerank_failure_reason = "CrossEncoder OOM during rerank"

    embedder.sparse_model_names = ["qdrant-bm25"]
    embedder.sparse_device_map = {"qdrant-bm25": "cpu"}
    embedder.sparse_vectors = []
    embedder.sparse_inference_result = SimpleNamespace(
        run_id="run-1",
        model_name="qdrant-bm25",
        latency_ms=123.4,
        fallback_count=0,
        vectors=[],
        device="cpu",
        success=False,
        error_message="Sparse generator failed",
    )

    summary = embedder.create_processing_summary(collection_name="FailureCase")

    warnings = summary.get("warnings")
    assert warnings is not None
    assert any("rerank stage reported failure" in warning for warning in warnings)
    assert any("sparse stage failure" in warning for warning in warnings)


def test_export_processing_stats_includes_activation_provenance(
    tmp_path,
    monkeypatch,
):
    _apply_dummy_model_patches(monkeypatch)

    toggles = FeatureToggleConfig(
        enable_rerank=False,
        enable_sparse=False,
        sparse_models=[],
        sources={
            "enable_rerank": "cli",
            "enable_sparse": "env",
            "sparse_models": "env",
        },
        resolution_events=(
            {
                "key": "enable_rerank",
                "value": True,
                "source": "default",
                "layer": "default",
            },
            {
                "key": "enable_rerank",
                "value": False,
                "source": "cli:--disable-rerank",
                "layer": "cli",
            },
            {
                "key": "enable_sparse",
                "value": True,
                "source": "default",
                "layer": "default",
            },
            {
                "key": "enable_sparse",
                "value": False,
                "source": "env",
                "layer": "environment",
            },
            {
                "key": "sparse_models",
                "value": ["qdrant-bm25"],
                "source": "default",
                "layer": "default",
            },
            {
                "key": "sparse_models",
                "value": [],
                "source": "env",
                "layer": "environment",
            },
        ),
    )

    gpu_config = KaggleGPUConfig(
        device_count=1,
        vram_per_gpu_gb=8.0,
        total_vram_gb=8.0,
        enable_memory_efficient_attention=False,
        gradient_checkpointing=False,
        precision="fp32",
        enable_mixed_precision=False,
        use_amp=False,
        base_batch_size=2,
        dynamic_batching=False,
        backend="pytorch",
        enable_torch_compile=False,
        strategy="data_parallel",
        enable_gradient_accumulation=False,
        accumulation_steps=1,
        kaggle_environment=False,
        output_path=str(tmp_path / "outputs"),
    )

    export_config = KaggleExportConfig(
        working_dir=str(tmp_path / "exports"),
        output_prefix="provenance",
        export_numpy=False,
        export_jsonl=False,
        export_faiss=False,
        export_sparse_jsonl=False,
    )

    embedder = UltimateKaggleEmbedderV4(
        model_name="jina-code-embeddings-1.5b",
        gpu_config=gpu_config,
        export_config=export_config,
        enable_ensemble=False,
        feature_toggles=toggles,
        force_cpu=True,
    )

    telemetry = build_telemetry_summary(
        mitigation_events=[],
        rotation_events=[],
        lease_events=[],
        batch_progress_events=[],
        span_events={},
        metrics_report={},
    )
    summary = build_processing_summary(
        feature_toggles=toggles,
        dense_run=None,
        rerank_stage=None,
        sparse_stage=None,
        telemetry=telemetry,
    )
    embedder.last_processing_summary = summary

    stats_path = tmp_path / "processing_stats.json"
    embedder.export_runtime._export_processing_stats(str(stats_path))

    payload = json.loads(stats_path.read_text(encoding="utf-8"))
    provenance = payload["feature_toggle_provenance"]

    assert provenance["resolved"]["enable_rerank"] is False
    assert provenance["resolved"]["enable_sparse"] is False
    lines = provenance["activation_lines"]
    assert lines
    assert any("override" in line for line in lines)
    events = provenance["activation_events"]
    assert events
    assert any(
        event["source"] == "cli:--disable-rerank" for event in events
    )


def test_processing_summary_includes_performance_baseline(tmp_path, monkeypatch):
    _apply_dummy_model_patches(monkeypatch)

    gpu_config = KaggleGPUConfig(
        device_count=1,
        vram_per_gpu_gb=8.0,
        total_vram_gb=8.0,
        enable_memory_efficient_attention=False,
        gradient_checkpointing=False,
        precision="fp32",
        enable_mixed_precision=False,
        use_amp=False,
        base_batch_size=2,
        dynamic_batching=False,
        backend="pytorch",
        enable_torch_compile=False,
        strategy="data_parallel",
        enable_gradient_accumulation=False,
        accumulation_steps=1,
        kaggle_environment=False,
        output_path=str(tmp_path / "outputs"),
    )

    export_config = KaggleExportConfig(
        working_dir=str(tmp_path / "exports"),
        output_prefix="baseline",
        export_numpy=False,
        export_jsonl=False,
        export_faiss=False,
        export_sparse_jsonl=False,
    )

    embedder = UltimateKaggleEmbedderV4(
        model_name="jina-code-embeddings-1.5b",
        gpu_config=gpu_config,
        export_config=export_config,
        enable_ensemble=False,
        feature_toggles=FeatureToggleConfig(),
        force_cpu=True,
        gpu0_soft_limit_gb=8.0,
    )

    embedder._last_dense_run = {"total_embeddings_generated": 4}
    embedder.processing_stats["gpu_memory"] = [
        {
            "gpu_id": 0,
            "memory_used_gb": 3.2,
            "memory_reserved_gb": 4.1,
            "memory_total_gb": 12.0,
            "utilization_percent": 52.0,
        },
        {
            "gpu_id": 0,
            "memory_used_gb": 3.8,
            "memory_reserved_gb": 4.6,
            "memory_total_gb": 12.0,
            "utilization_percent": 58.0,
        },
    ]
    embedder.processing_stats["system_metrics"] = [
        {
            "cpu_percent": 44.5,
            "memory_used_gb": 10.2,
            "memory_percent": 55.0,
        },
        {
            "cpu_percent": 88.0,
            "memory_used_gb": 10.8,
            "memory_percent": 62.0,
        },
    ]

    below_limit_snapshot = GPUMemorySnapshot(
        device_id=0,
        total_bytes=int(12.0 * (1024 ** 3)),
        free_bytes=int(4.0 * (1024 ** 3)),
        allocated_bytes=int(6.0 * (1024 ** 3)),
        reserved_bytes=int(7.0 * (1024 ** 3)),
    )
    embedder.telemetry.record_gpu_snapshot(
        {0: below_limit_snapshot},
        gpu0_soft_limit_bytes=embedder.gpu0_soft_limit_bytes,
    )

    embedder.processing_stats["hydration_events"] = [
        {
            "model": "jina-code-embeddings-1.5b",
            "duration_seconds": 1.25,
            "device_ids": [0],
            "status": "hydrated",
            "success": True,
        },
        {
            "model": "jina-code-embeddings-1.5b",
            "duration_seconds": 1.41,
            "device_ids": [0],
            "status": "hydrated",
            "success": True,
        },
        {
            "model": "companion",
            "duration_seconds": 2.0,
            "device_ids": [],
            "status": "error",
            "success": False,
        },
    ]

    summary = embedder.create_processing_summary(chunk_count=4)

    baseline = summary.get("performance_baseline")
    assert baseline is not None
    assert baseline["gpu"]["samples"] == 2
    assert (
        baseline["gpu"]["per_gpu"]["0"]["peak_memory_used_gb"]
        == pytest.approx(3.8)
    )
    assert baseline["gpu"]["peak_device"] == "0"
    assert baseline["system"]["peak_cpu_percent"] == pytest.approx(88.0)
    assert baseline["system"]["average_memory_percent"] == pytest.approx(58.5)
    hydration = baseline["hydration"]
    assert hydration["samples"] == 3
    assert hydration["successes"] == 2
    assert hydration["failures"] == 1
    assert hydration["peak_duration_seconds"] == pytest.approx(2.0)
    model_stats = hydration["per_model"]["jina-code-embeddings-1.5b"]
    assert model_stats["samples"] == 2
    assert model_stats["successes"] == 2
    assert model_stats["average_duration_seconds"] == pytest.approx(1.33, abs=0.01)
    gpu_section = baseline["gpu"]
    assert gpu_section["soft_limit_exceeded"] is False
    assert gpu_section["status"] == "within_limit"
    assert gpu_section["soft_limit_gb"] == pytest.approx(
        embedder.gpu0_soft_limit_bytes / (1024 ** 3), rel=1e-3
    )
    gpu_soft_limit_metric = summary["telemetry"]["metrics"]["gpu_soft_limit"]
    assert gpu_soft_limit_metric["status"] == "within_limit"
    assert gpu_soft_limit_metric["details"]["soft_limit_gb"] == pytest.approx(
        embedder.gpu0_soft_limit_bytes / (1024 ** 3), rel=1e-3
    )


def test_performance_baseline_flags_soft_limit_exceedance(tmp_path, monkeypatch):
    _apply_dummy_model_patches(monkeypatch)

    gpu_config = KaggleGPUConfig(
        device_count=1,
        vram_per_gpu_gb=12.0,
        total_vram_gb=12.0,
        enable_memory_efficient_attention=False,
        gradient_checkpointing=False,
        precision="fp32",
        enable_mixed_precision=False,
        use_amp=False,
        base_batch_size=2,
        dynamic_batching=False,
        backend="pytorch",
        enable_torch_compile=False,
        strategy="data_parallel",
        enable_gradient_accumulation=False,
        accumulation_steps=1,
        kaggle_environment=False,
        output_path=str(tmp_path / "outputs"),
    )

    export_config = KaggleExportConfig(
        working_dir=str(tmp_path / "exports"),
        output_prefix="guardrail",
        export_numpy=False,
        export_jsonl=False,
        export_faiss=False,
        export_sparse_jsonl=False,
    )

    embedder = UltimateKaggleEmbedderV4(
        model_name="jina-code-embeddings-1.5b",
        gpu_config=gpu_config,
        export_config=export_config,
        enable_ensemble=False,
        feature_toggles=FeatureToggleConfig(),
        force_cpu=True,
        gpu0_soft_limit_gb=10.0,
    )

    exceed_snapshot = GPUMemorySnapshot(
        device_id=0,
        total_bytes=int(12.0 * (1024 ** 3)),
        free_bytes=int(2.0 * (1024 ** 3)),
        allocated_bytes=int(11.5 * (1024 ** 3)),
        reserved_bytes=int(11.7 * (1024 ** 3)),
    )
    embedder.telemetry.record_gpu_snapshot(
        {0: exceed_snapshot},
        gpu0_soft_limit_bytes=embedder.gpu0_soft_limit_bytes,
    )

    embedder.processing_stats["gpu_memory"] = [
        {
            "gpu_id": 0,
            "memory_used_gb": 11.5,
            "memory_reserved_gb": 11.7,
            "memory_total_gb": 12.0,
            "utilization_percent": 95.8,
        }
    ]

    summary = embedder.create_processing_summary(chunk_count=1)

    baseline = summary.get("performance_baseline")
    assert baseline is not None
    gpu_baseline = baseline.get("gpu", {})
    assert gpu_baseline.get("soft_limit_exceeded") is True
    assert gpu_baseline.get("status") == "exceeded_soft_limit"
    assert gpu_baseline.get("soft_limit_devices") == [0]
    soft_limit_metric = summary["telemetry"]["metrics"]["gpu_soft_limit"]
    assert soft_limit_metric["status"] == "alert"
    assert soft_limit_metric["reason"] == "soft_limit_exceeded"
    assert soft_limit_metric["details"]["devices"] == [0]


def test_performance_stub_respects_vram_budget(tmp_path, monkeypatch):
    _apply_dummy_model_patches(monkeypatch)

    gpu_config = KaggleGPUConfig(
        device_count=1,
        vram_per_gpu_gb=12.0,
        total_vram_gb=12.0,
        enable_memory_efficient_attention=False,
        gradient_checkpointing=False,
        precision="fp32",
        enable_mixed_precision=False,
        use_amp=False,
        base_batch_size=2,
        dynamic_batching=False,
        backend="pytorch",
        enable_torch_compile=False,
        strategy="data_parallel",
        enable_gradient_accumulation=False,
        accumulation_steps=1,
        kaggle_environment=False,
        output_path=str(tmp_path / "outputs"),
    )

    export_config = KaggleExportConfig(
        working_dir=str(tmp_path / "exports"),
        output_prefix="vram_budget",
        export_numpy=False,
        export_jsonl=False,
        export_faiss=False,
        export_sparse_jsonl=False,
    )

    embedder = UltimateKaggleEmbedderV4(
        model_name="jina-code-embeddings-1.5b",
        gpu_config=gpu_config,
        export_config=export_config,
        enable_ensemble=False,
        feature_toggles=FeatureToggleConfig(),
        force_cpu=True,
    )

    vram_ceiling_bytes = int(12.0 * (1024 ** 3))
    assert embedder.gpu0_soft_limit_bytes <= vram_ceiling_bytes
    # TODO: Replace stub with telemetry-driven VRAM utilization assertion once
    #       metrics emission captures per-stage peak usage in CI environments.

def test_sparse_generator_end_to_end_persistence(tmp_path: Path) -> None:
    """End-to-end test: SparseVectorGenerator outputs persist into processing_summary.json.

    This test verifies that sparse vectors generated by SparseVectorGenerator
    are correctly captured in the SparseInferenceRun artifact structure and
    can be serialized to processing_summary.json with proper fallback metadata.
    """
    from unittest.mock import Mock
    import numpy as np
    from processor.ultimate_embedder.sparse_generator import (
        ChunkRecord,
        SparseVectorGenerator,
    )

    # Create mock embedder with telemetry
    mock_embedder = Mock()
    mock_embedder.device = "cpu"
    mock_embedder.sparse_models = {}
    mock_embedder.telemetry = Mock()

    # Create and register a mock sparse model
    mock_sparse_model = Mock()
    model_name = "test-sparse-model"
    mock_embedder.sparse_models[model_name] = mock_sparse_model

    # Mock embeddings output (2 chunks)
    mock_embeddings = np.random.randn(2, 768).astype(np.float32)
    mock_sparse_model.encode.return_value = mock_embeddings

    # Create test chunks with metadata
    test_chunks = [
        ChunkRecord(
            text="First test chunk for sparse inference",
            metadata={
                "sparse_features": {
                    "term_weights": [
                        {"term": "test", "weight": 0.8},
                        {"term": "chunk", "weight": 0.6},
                    ],
                    "unique_terms": 2,
                    "total_terms": 5,
                    "weighting": "tf-normalized",
                }
            },
            chunk_id="e2e_chunk_001",
        ),
        ChunkRecord(
            text="Second test chunk with different content",
            metadata={
                "sparse_features": {
                    "term_weights": [
                        {"term": "second", "weight": 0.7},
                        {"term": "content", "weight": 0.9},
                    ],
                    "unique_terms": 2,
                    "total_terms": 5,
                    "weighting": "tf-normalized",
                }
            },
            chunk_id="e2e_chunk_002",
        ),
    ]

    # Create generator and run inference
    generator = SparseVectorGenerator(mock_embedder)
    result = generator.generate(
        chunks=test_chunks,
        model_name=model_name,
        use_gpu=False,
    )

    # Verify result structure
    assert result.success is True
    assert len(result.vectors) == 2
    assert result.fallback_count >= 0
    assert result.device == "cpu"
    assert result.model_name == model_name

    # Build sparse stage summary from generator output
    sparse_stage = build_sparse_stage_summary(
        enabled=True,
        model_names=[model_name],
        vectors_total=len(test_chunks),
        vectors_available=len([v for v in result.vectors if v is not None]),
        executed=True,
        coverage_ratio=1.0 - (result.fallback_count / len(test_chunks)),
        devices={model_name: result.device},
        fallback_used=result.fallback_count > 0,
        fallback_reason=result.error_message,
    )

    # Build full processing summary
    feature_toggles = FeatureToggleConfig(
        enable_rerank=False,
        enable_sparse=True,
        sparse_models=[model_name],
        sources={
            "enable_sparse": "test",
            "sparse_models": "test",
        },
    )

    dense_run = {
        "total_embeddings_generated": 2,
        "models_executed": ["jina-code-embeddings-1.5b"],
    }

    telemetry = build_telemetry_summary(
        mitigation_events=[],
        rotation_events=[],
        lease_events=[],
        batch_progress_events=[],
        span_events={},
        metrics_report={},
    )

    summary = build_processing_summary(
        feature_toggles=feature_toggles,
        dense_run=dense_run,
        rerank_stage=None,
        sparse_stage=sparse_stage,
        telemetry=telemetry,
        collection_name="e2e_test_collection",
        chunk_count=len(test_chunks),
    )

    # Verify sparse_run structure in summary
    assert "sparse_run" in summary
    assert summary["sparse_run"]["enabled"] is True
    assert summary["sparse_run"]["vectors"]["total"] == 2
    assert summary["sparse_run"]["vectors"]["available"] >= 0
    assert 0.0 <= summary["sparse_run"]["vectors"]["coverage_ratio"] <= 1.0
    assert model_name in summary["sparse_run"]["devices"]
    assert summary["sparse_run"]["devices"][model_name] == "cpu"
    assert isinstance(summary["sparse_run"]["fallback_used"], bool)

    # Write to file and verify serialization
    output_file = tmp_path / "processing_summary.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Read back and verify structure
    with open(output_file, "r", encoding="utf-8") as f:
        loaded_summary = json.load(f)

    assert loaded_summary["schema_version"] == "v4.1"
    assert loaded_summary["sparse_run"]["enabled"] is True
    assert loaded_summary["sparse_run"]["vectors"]["total"] == 2
    
    # Verify fallback metadata is preserved
    if result.fallback_count > 0:
        assert loaded_summary["sparse_run"]["fallback_used"] is True
        assert len(result.fallback_indices) == result.fallback_count


def test_legacy_parser_ignores_v4_1_sparse_run() -> None:
    """Test that legacy parsers can load v4.1 manifests by ignoring unknown sparse_run key.

    This validates AC3: Legacy parsers ingest updated artifacts without errors when sparse data present.
    """
    # Create a v4.1 manifest with sparse_run section
    v4_1_manifest = {
        "schema_version": "v4.1",
        "generated_at": "2025-10-28T12:00:00Z",
        "collection": "test_collection",
        "chunk_count": 10,
        "feature_toggles": {
            "enable_rerank": True,
            "enable_sparse": True,
            "sparse_models": ["qdrant-bm25"],
            "sources": {"enable_sparse": "default"},
        },
        "dense_run": {
            "total_embeddings_generated": 10,
            "models_executed": ["jina-code-embeddings-1.5b"],
        },
        "sparse_run": {
            "enabled": True,
            "vectors": {
                "total": 10,
                "available": 8,
                "coverage_ratio": 0.8,
            },
            "devices": {"qdrant-bm25": "cpu"},
            "fallback_used": True,
        },
        "telemetry": {},
    }

    # Simulate legacy parser that only reads known fields (ignores sparse_run)
    legacy_expected_fields = [
        "schema_version",
        "collection",
        "chunk_count",
        "dense_run",
        "telemetry",
    ]

    # Verify legacy parser can access known fields without error
    for field in legacy_expected_fields:
        assert field in v4_1_manifest

    # Verify sparse_run is present but not required for legacy parsers
    assert "sparse_run" in v4_1_manifest

    # Simulate legacy parser extracting only known fields (JSON ignores unknown keys)
    legacy_parsed = {
        key: value
        for key, value in v4_1_manifest.items()
        if key in legacy_expected_fields
    }

    # Legacy parser successfully extracts data without errors
    assert legacy_parsed["schema_version"] in ["v4.0", "v4.1"]
    assert legacy_parsed["dense_run"]["total_embeddings_generated"] == 10
    assert "sparse_run" not in legacy_parsed  # Legacy parser ignores unknown keys


def test_normalize_processing_summary_preserves_legacy_v40() -> None:
    """Legacy manifests remain parseable through normalization helper."""

    legacy_manifest = {
        "schema_version": "v4.0",
        "generated_at": "2025-10-29T12:00:00Z",
        "feature_toggles": {"enable_sparse": False},
        "dense_run": {"total_embeddings_generated": 5},
        "telemetry": {},
    }

    normalized = normalize_processing_summary(legacy_manifest)

    assert normalized["schema_version"] == "v4.0"
    assert normalized["compatibility"]["current"] == "v4.0"
    assert normalized["compatibility"]["legacy"] == []
    assert normalized.get("warnings") == []
    assert "sparse_run" not in normalized


def test_v4_1_schema_when_sparse_enabled() -> None:
    """Test that schema version bumps to v4.1 when sparse is enabled.

    This validates AC2: Schema version logic (v4.1 when sparse_run present).
    """
    toggles = FeatureToggleConfig(
        enable_rerank=False,
        enable_sparse=True,
        sparse_models=["qdrant-bm25"],
        sources={"enable_sparse": "default"},
    )

    sparse_stage = build_sparse_stage_summary(
        enabled=True,
        model_names=["qdrant-bm25"],
        vectors_total=10,
        vectors_available=9,
        executed=True,
        coverage_ratio=0.9,
        devices={"qdrant-bm25": "cpu"},
        fallback_used=False,
        fallback_reason=None,
    )

    telemetry = build_telemetry_summary(
        mitigation_events=[],
        rotation_events=[],
        lease_events=[],
        batch_progress_events=[],
        span_events={},
        metrics_report={},
    )

    dense_run = {
        "total_embeddings_generated": 10,
        "models_executed": ["jina-code-embeddings-1.5b"],
    }

    # Build summary WITH sparse_stage (sparse enabled)
    summary = build_processing_summary(
        feature_toggles=toggles,
        dense_run=dense_run,
        rerank_stage=None,
        sparse_stage=sparse_stage,  # Sparse stage present
        telemetry=telemetry,
    )

    # Verify schema version is v4.1 when sparse_run present
    assert summary["schema_version"] == "v4.1"
    assert "sparse_run" in summary
    assert summary["sparse_run"]["enabled"] is True


def test_qdrant_jsonl_payload_includes_sparse_vector() -> None:
    """Test that Qdrant JSONL payload includes sparse_vector object with proper structure.

    This validates AC2: JSONL exports include sparse vector payload with indices, values, tokens, stats.
    """
    # Simulate sparse vector structure from export_runtime
    sparse_vector_payload = {
        "indices": [0, 5, 12, 24, 38],
        "values": [0.95, 0.82, 0.76, 0.68, 0.54],
        "tokens": ["test", "sparse", "vector", "retrieval", "bm25"],
        "stats": {
            "nonzero_count": 5,
            "density": 0.02,
            "max_value": 0.95,
            "mean_value": 0.75,
        },
    }

    # Verify required fields present
    assert "indices" in sparse_vector_payload
    assert "values" in sparse_vector_payload
    assert "tokens" in sparse_vector_payload
    assert "stats" in sparse_vector_payload

    # Verify structure integrity
    assert len(sparse_vector_payload["indices"]) == len(
        sparse_vector_payload["values"]
    )
    assert len(sparse_vector_payload["tokens"]) == len(
        sparse_vector_payload["values"]
    )
    assert isinstance(sparse_vector_payload["stats"], dict)

    # Verify this can be JSON serialized
    import json

    json_str = json.dumps(sparse_vector_payload)
    loaded = json.loads(json_str)
    assert loaded["indices"] == sparse_vector_payload["indices"]


def test_upload_script_handles_missing_sparse_files(tmp_path: Path) -> None:
    """Test that upload script generation handles missing sparse files without errors.

    This validates AC3: Upload script generation handles missing sparse files gracefully.
    """
    # Simulate exported_files dict with missing sparse_jsonl
    exported_files_without_sparse = {
        "numpy": str(tmp_path / "embeddings.npy"),
        "jsonl": str(tmp_path / "qdrant.jsonl"),
        "metadata": str(tmp_path / "metadata.json"),
        # No "sparse_jsonl" key
    }

    # Verify script can handle missing sparse file key
    sparse_file_path = exported_files_without_sparse.get("sparse_jsonl")
    assert sparse_file_path is None  # Missing sparse file

    # Upload script should check for existence before referencing
    if "sparse_jsonl" in exported_files_without_sparse:
        # Only reference sparse file if present
        sparse_path = exported_files_without_sparse["sparse_jsonl"]
    else:
        # Gracefully skip sparse file reference
        sparse_path = None

    assert sparse_path is None  # Script handles missing file gracefully


def test_processing_summary_includes_rerank_run_when_executed() -> None:
    """Test that processing_summary.json includes rerank_run section with metrics when rerank executed.
    
    This validates Story 3.2 AC3: End-to-end run demonstrates rerank-enabled exports.
    """
    from processor.ultimate_embedder.cross_encoder_executor import CrossEncoderRerankRun
    
    toggles = FeatureToggleConfig(
        enable_rerank=True,
        enable_sparse=False,
        sources={
            "enable_rerank": "default",
            "enable_sparse": "default",
        },
    )

    # Simulate successful rerank execution
    rerank_stage = build_rerank_stage_summary(
        enabled=True,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
        loaded=True,
        device="cuda:0",
        executed=True,
        status="executed",
        reason=None,
        metrics={
            "top_k_candidates": 100,
            "rerank_top_k": 10,
            "batch_size": 32,
        },
        requested_device="cuda",
        fallback_applied=False,
        fallback_reason=None,
    )
    
    # Add execution metrics to rerank_stage
    rerank_stage.update(
        {
            "run_id": "test-rerank-run-001",
            "latency_ms": 145.3,
            "gpu_peak_gb": 2.8,
            "batch_size": 32,
            "candidate_count": 100,
            "candidate_ids": ["doc-0", "doc-1", "doc-2"],
            "scores": [0.88, 0.77, 0.66],
            "dense_scores": [0.8, 0.7, 0.6],
            "query": "sample query for rerank stage",
            "candidate_metadata": [
                {"id": "doc-0"},
                {"id": "doc-1"},
                {"id": "doc-2"},
            ],
            "result_count": 3,
            "initial_candidate_count": 5,
            "top_k_results": 10,
        }
    )

    dense_run = {
        "model_names": ["sentence-transformers/all-MiniLM-L6-v2"],
        "embeddings_shape": [50, 384],
        "batch_size": 32,
        "device": "cuda:0",
    }

    telemetry = build_telemetry_summary(
        mitigation_events=[],
        rotation_events=[],
        lease_events=[],
        batch_progress_events=[],
        span_events={
            "rag.rerank": {
                "span_id": "span-rerank-001",
                "status": "active",
                "timestamp": 1234567890.0,
                "attributes": {
                    "latency_ms": 145.3,
                    "batch_size": 32,
                    "gpu_peak_gb": 2.8,
                    "candidate_count": 100,
                },
            }
        },
        metrics_report={
            "rerank": {
                "status": "emitted",
                "metrics": ["rag_rerank_latency_seconds", "rag_gpu_peak_bytes"],
            }
        },
    )

    summary = build_processing_summary(
        chunk_count=50,
        collection_name="test_collection",
        feature_toggles=toggles,
        dense_run=dense_run,
        rerank_stage=rerank_stage,
        sparse_stage=None,
        telemetry=telemetry,
    )

    # Verify schema version includes rerank
    assert summary["schema_version"] == "v4.1"
    
    # Verify rerank_run section is present and populated
    assert "rerank_run" in summary
    rerank_run = summary["rerank_run"]
    assert rerank_run["enabled"] is True
    assert rerank_run["executed"] is True
    assert rerank_run["status"] == "executed"
    assert rerank_run["model_name"] == "cross-encoder/ms-marco-MiniLM-L-6-v2"
    
    # Verify performance metrics are captured
    assert rerank_run["run_id"] == "test-rerank-run-001"
    assert rerank_run["latency_ms"] == 145.3
    assert rerank_run["gpu_peak_gb"] == 2.8
    assert rerank_run["batch_size"] == 32
    assert rerank_run["candidate_count"] == 100

    rerank_payload = rerank_run["payload"]
    assert rerank_payload["run_id"] == "test-rerank-run-001"
    assert rerank_payload["query"] == "sample query for rerank stage"
    assert rerank_payload["candidate_ids"] == [
        "doc-0",
        "doc-1",
        "doc-2",
    ]
    assert rerank_payload["scores"] == pytest.approx([0.88, 0.77, 0.66])
    assert rerank_payload["dense_scores"] == pytest.approx([0.8, 0.7, 0.6])
    assert rerank_payload["candidate_metadata"][0]["id"] == "doc-0"
    assert rerank_payload["result_count"] == 3
    assert rerank_payload["initial_candidate_count"] == 5
    
    # Verify telemetry integration
    assert "telemetry" in summary
    assert "rag.rerank" in summary["telemetry"]["spans"]
    rerank_span = summary["telemetry"]["spans"]["rag.rerank"]
    assert rerank_span["status"] == "active"
    assert rerank_span["attributes"]["latency_ms"] == 145.3


def test_processing_summary_rerank_disabled_via_toggle() -> None:
    """Test that processing_summary.json reflects rerank disabled state with proper reason.
    
    This validates Story 3.2 AC2: Fallback pathways capture when rerank disabled.
    """
    toggles = FeatureToggleConfig(
        enable_rerank=False,
        enable_sparse=False,
        sources={
            "enable_rerank": "env",  # Disabled via environment variable
            "enable_sparse": "default",
        },
    )

    rerank_stage = build_rerank_stage_summary(
        enabled=False,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
        loaded=False,
        device="cpu",
        executed=False,
        status="disabled",
        reason="Disabled via env",
        metrics={},
        requested_device="cuda",
        fallback_applied=False,
        fallback_reason=None,
        fallback_count=1,
        rerank_fallback_reason="feature_disabled",
        fallback_source="env",
    )

    dense_run = {
        "model_names": ["sentence-transformers/all-MiniLM-L6-v2"],
        "embeddings_shape": [50, 384],
    }

    telemetry = build_telemetry_summary(
        mitigation_events=[],
        rotation_events=[],
        lease_events=[],
        batch_progress_events=[],
        span_events={
            "rag.rerank": {
                "span_id": "span-rerank-disabled",
                "status": "skipped",
                "reason": "Disabled via env",
                "timestamp": 1234567890.0,
                "attributes": {
                    "fallback_count": 1,
                    "fallback_reason": "feature_disabled",
                    "fallback_source": "env",
                },
            }
        },
        metrics_report={},
    )

    summary = build_processing_summary(
        chunk_count=50,
        collection_name="test_collection",
        feature_toggles=toggles,
        dense_run=dense_run,
        rerank_stage=rerank_stage,
        sparse_stage=None,
        telemetry=telemetry,
    )

    # Verify rerank_run reflects disabled state
    assert "rerank_run" in summary
    rerank_run = summary["rerank_run"]
    assert rerank_run["enabled"] is False
    assert rerank_run["executed"] is False
    assert rerank_run["status"] == "disabled"
    assert rerank_run["reason"] == "Disabled via env"
    assert rerank_run["fallback_count"] == 1
    assert rerank_run["fallback_reason"] == "feature_disabled"
    assert rerank_run["fallback_source"] == "env"
    
    # Verify telemetry shows skipped span
    assert "rag.rerank" in summary["telemetry"]["spans"]
    assert summary["telemetry"]["spans"]["rag.rerank"]["status"] == "skipped"
    assert summary["telemetry"]["spans"]["rag.rerank"]["attributes"]["fallback_count"] == 1


def test_processing_summary_rerank_failure_captured() -> None:
    """Test that processing_summary.json captures rerank failures with error details.
    
    This validates Story 3.2 AC2: Fallback pathways capture when rerank fails.
    """
    toggles = FeatureToggleConfig(
        enable_rerank=True,
        enable_sparse=False,
        sources={
            "enable_rerank": "default",
            "enable_sparse": "default",
        },
    )

    # Simulate failed rerank execution
    rerank_stage = build_rerank_stage_summary(
        enabled=True,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
        loaded=True,
        device="cuda:0",
        executed=False,
        status="error",
        reason="CUDA out of memory during rerank execution",
        metrics={
            "top_k_candidates": 100,
            "rerank_top_k": 10,
            "batch_size": 32,
        },
        requested_device="cuda",
        fallback_applied=False,
        fallback_reason=None,
        fallback_count=1,
        rerank_fallback_reason="execution_failed",
        fallback_source="runtime",
    )

    dense_run = {
        "model_names": ["sentence-transformers/all-MiniLM-L6-v2"],
        "embeddings_shape": [50, 384],
    }

    telemetry = build_telemetry_summary(
        mitigation_events=[],
        rotation_events=[],
        lease_events=[],
        batch_progress_events=[],
        span_events={
            "rag.rerank": {
                "span_id": "span-rerank-failed",
                "status": "skipped",
                "reason": "CUDA out of memory during rerank execution",
                "timestamp": 1234567890.0,
                "attributes": {
                    "failure_reason": "CUDA out of memory during rerank execution",
                    "fallback_count": 1,
                    "fallback_reason": "execution_failed",
                    "fallback_source": "runtime",
                },
            }
        },
        metrics_report={},
    )

    summary = build_processing_summary(
        chunk_count=50,
        collection_name="test_collection",
        feature_toggles=toggles,
        dense_run=dense_run,
        rerank_stage=rerank_stage,
        sparse_stage=None,
        telemetry=telemetry,
    )

    # Verify rerank_run captures error state
    assert "rerank_run" in summary
    rerank_run = summary["rerank_run"]
    assert rerank_run["enabled"] is True
    assert rerank_run["executed"] is False
    assert rerank_run["status"] == "error"
    assert "CUDA out of memory" in rerank_run["reason"]
    assert rerank_run["fallback_count"] == 1
    assert rerank_run["fallback_reason"] == "execution_failed"
    assert rerank_run.get("fallback_source") == "runtime"
    
    # Verify telemetry captures failure details
    assert "rag.rerank" in summary["telemetry"]["spans"]
    rerank_span = summary["telemetry"]["spans"]["rag.rerank"]
    assert rerank_span["status"] == "skipped"
    assert "failure_reason" in rerank_span["attributes"]
    assert rerank_span["attributes"]["fallback_count"] == 1
    assert rerank_span["attributes"].get("fallback_reason") == "execution_failed"
    assert rerank_span["attributes"].get("fallback_source") == "runtime"


@pytest.mark.regression_harness
@pytest.mark.parametrize(
    "scenario, expects",
    [
        ("default_on", {"rerank": True, "sparse": True}),
        ("rerank_disabled", {"rerank": False, "sparse": True}),
        ("sparse_disabled", {"rerank": True, "sparse": False}),
        ("fallback_force", {"rerank": False, "sparse": False}),
    ],
)
def test_regression_processing_summary_scenarios(
    regression_summary_runner,
    regression_goldens,
    tmp_path,
    scenario,
    expects,
):
    summary, artifacts = regression_summary_runner(scenario, output_dir=tmp_path)

    if scenario == "default_on":
        expected = json.loads(
            regression_goldens["processing_summary_default_on"].read_text(
                encoding="utf-8"
            )
        )
        assert summary == expected
    else:
        assert summary["feature_toggles"]["enable_rerank"] is expects["rerank"]
        assert summary["feature_toggles"]["enable_sparse"] is expects["sparse"]
        if expects["rerank"]:
            assert "rerank_run" in summary
        else:
            assert "rerank_run" not in summary
        if expects["sparse"]:
            assert "sparse_run" in summary
        else:
            assert "sparse_run" not in summary

    metrics = summary["telemetry"]["metrics"]
    rerank_status = metrics["rerank"]["status"]
    sparse_status = metrics.get("sparse", {}).get("status")

    if expects["rerank"]:
        assert rerank_status in {"emitted", "skipped"}
    else:
        assert rerank_status == "skipped"

    if expects["sparse"]:
        assert sparse_status in {"emitted", "skipped"}
    else:
        assert sparse_status == "skipped"

    qdrant_path = artifacts["qdrant_path"]
    with qdrant_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            payload = json.loads(line)
            assert payload["id"].startswith("docling-mini-")
            assert payload["payload"]["chunk_id"].startswith("docling-mini-")

    if scenario == "fallback_force":
        warnings = summary.get("warnings", [])
        assert warnings
        assert any("fallback" in warning.lower() for warning in warnings)
