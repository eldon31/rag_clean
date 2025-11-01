"""Smoke tests for telemetry coverage with rerank and sparse stages."""
# sourcery skip: extract-duplicate-method, extract-duplicate-code

import json

import pytest

from processor.ultimate_embedder.prometheus_metrics import PrometheusMetricsEmitter
from processor.ultimate_embedder.runtime_config import FeatureToggleConfig
from processor.ultimate_embedder.summary import (
    build_processing_summary,
    build_rerank_stage_summary,
    build_sparse_stage_summary,
    build_telemetry_summary,
)


class TestPrometheusMetricsEmitter:
    """Test Prometheus metrics emission for pipeline stages."""

    def test_emitter_disabled_by_default(self) -> None:
        """Verify metrics emitter is disabled when environment variable not set."""
        emitter = PrometheusMetricsEmitter(enabled=False, namespace="rag")
        
        result = emitter.emit_latency_metric(
            stage="rerank",
            latency_seconds=0.5,
            labels={"device": "cuda:0"},
        )
        
        assert result is False
        assert len(emitter.get_buffered_metrics()) == 0

    def test_emitter_enabled_emits_latency_metric(self) -> None:
        """Verify latency histogram is emitted when enabled."""
        emitter = PrometheusMetricsEmitter(enabled=True, namespace="rag")
        
        result = emitter.emit_latency_metric(
            stage="rerank",
            latency_seconds=0.5,
            labels={"device": "cuda:0", "model": "jina-reranker-v2"},
        )
        
        assert result is True
        metrics = emitter.get_buffered_metrics()
        assert len(metrics) == 1
        assert metrics[0]["metric"] == "rag_rerank_latency_seconds"
        assert metrics[0]["type"] == "histogram"
        assert metrics[0]["value"] == 0.5
        assert metrics[0]["labels"]["device"] == "cuda:0"
        assert metrics[0]["labels"]["model"] == "jina-reranker-v2"

    def test_emitter_emits_gpu_peak_metric(self) -> None:
        """Verify GPU peak gauge is emitted with stage label."""
        emitter = PrometheusMetricsEmitter(enabled=True, namespace="rag")
        
        result = emitter.emit_gpu_peak_metric(
            stage="rerank",
            peak_bytes=2 * 1024**3,  # 2 GB
            labels={"device": "cuda:0"},
        )
        
        assert result is True
        metrics = emitter.get_buffered_metrics()
        assert len(metrics) == 1
        assert metrics[0]["metric"] == "rag_gpu_peak_bytes"
        assert metrics[0]["type"] == "gauge"
        assert metrics[0]["value"] == 2 * 1024**3
        assert metrics[0]["labels"]["stage"] == "rerank"
        assert metrics[0]["labels"]["device"] == "cuda:0"

    def test_emitter_buffer_clears_after_retrieval(self) -> None:
        """Verify metric buffer is cleared after get_buffered_metrics."""
        emitter = PrometheusMetricsEmitter(enabled=True, namespace="rag")
        
        emitter.emit_latency_metric(stage="sparse", latency_seconds=0.3)
        metrics_first = emitter.get_buffered_metrics()
        assert len(metrics_first) == 1
        
        metrics_second = emitter.get_buffered_metrics()
        assert len(metrics_second) == 0

    def test_emitter_custom_namespace(self) -> None:
        """Verify custom namespace is applied to metric names."""
        emitter = PrometheusMetricsEmitter(enabled=True, namespace="custom")
        
        emitter.emit_latency_metric(stage="rerank", latency_seconds=0.5)
        metrics = emitter.get_buffered_metrics()
        
        assert metrics[0]["metric"] == "custom_rerank_latency_seconds"


class TestTelemetrySpansWithMetrics:
    """Test OpenTelemetry spans include metrics emission status."""

    def test_rerank_span_active_includes_metrics_status(self) -> None:
        """Verify rerank span with active status includes emission metadata."""
        telemetry = build_telemetry_summary(
            mitigation_events=[],
            rotation_events=[],
            lease_events=[],
            batch_progress_events=[],
            span_events={
                "rag.rerank": {
                    "span_id": "span-rerank-1",
                    "status": "active",
                    "reason": "Query-time reranking executed",
                    "latency_ms": 145.3,
                    "batch_size": 32,
                    "gpu_peak_gb": 2.1,
                    "candidate_count": 100,
                    "fallback_used": False,
                    "attributes": {
                        "fallback_count": 0,
                        "fallback_source": "runtime",
                    },
                    "timestamp": 1234567890.0,
                }
            },
            metrics_report={
                "rerank": {
                    "status": "emitted",
                    "metrics": ["rag_rerank_latency_seconds", "rag_gpu_peak_bytes"],
                    "details": {
                        "latency_seconds": 0.1453,
                        "gpu_peak_gb": 2.1,
                        "prometheus_latency_emitted": True,
                        "prometheus_gpu_emitted": True,
                        "fallback_count": 0,
                        "fallback_source": "runtime",
                    },
                    "timestamp": 1234567890.0,
                }
            },
        )
        
        assert "rag.rerank" in telemetry["spans"]
        rerank_span = telemetry["spans"]["rag.rerank"]
        assert rerank_span["status"] == "active"
        assert "latency_ms" not in rerank_span  # filtered out by build_telemetry_summary
        assert rerank_span["attributes"]["fallback_count"] == 0
        assert rerank_span["attributes"].get("fallback_source") == "runtime"
        
        assert "rerank" in telemetry["metrics"]
        rerank_metrics = telemetry["metrics"]["rerank"]
        assert rerank_metrics["status"] == "emitted"
        assert "rag_rerank_latency_seconds" in rerank_metrics["metrics"]
        assert "rag_gpu_peak_bytes" in rerank_metrics["metrics"]
        assert rerank_metrics["details"]["fallback_count"] == 0
        assert rerank_metrics["details"].get("fallback_source") == "runtime"

    def test_sparse_span_active_includes_metrics_status(self) -> None:
        """Verify sparse span with active status includes emission metadata."""
        telemetry = build_telemetry_summary(
            mitigation_events=[],
            rotation_events=[],
            lease_events=[],
            batch_progress_events=[],
            span_events={
                "rag.sparse": {
                    "span_id": "span-sparse-1",
                    "status": "active",
                    "batch_size": 128,
                    "coverage_ratio": 0.95,
                    "fallback_used": False,
                    "timestamp": 1234567890.0,
                }
            },
            metrics_report={
                "sparse": {
                    "status": "emitted",
                    "metrics": ["rag_sparse_latency_seconds"],
                    "details": {
                        "latency_seconds": 0.423,
                        "prometheus_latency_emitted": True,
                    },
                    "timestamp": 1234567890.0,
                }
            },
        )
        
        assert "rag.sparse" in telemetry["spans"]
        sparse_span = telemetry["spans"]["rag.sparse"]
        assert sparse_span["status"] == "active"
        
        assert "sparse" in telemetry["metrics"]
        sparse_metrics = telemetry["metrics"]["sparse"]
        assert sparse_metrics["status"] == "emitted"
        assert "rag_sparse_latency_seconds" in sparse_metrics["metrics"]

    def test_disabled_stage_skips_metrics_emission(self) -> None:
        """Verify disabled stages record skip reason without emission."""
        telemetry = build_telemetry_summary(
            mitigation_events=[],
            rotation_events=[],
            lease_events=[],
            batch_progress_events=[],
            span_events={
                "rag.rerank": {
                    "span_id": "span-rerank-disabled",
                    "status": "skipped",
                    "reason": "Disabled via CLI flag",
                    "attributes": {
                        "fallback_count": 1,
                        "fallback_reason": "feature_disabled",
                        "fallback_source": "cli",
                    },
                    "timestamp": 1234567890.0,
                }
            },
            metrics_report={
                "rerank": {
                    "status": "skipped",
                    "reason": "stage disabled",
                    "metrics": ["rag_rerank_latency_seconds", "rag_gpu_peak_bytes"],
                    "details": {
                        "fallback_count": 1,
                        "fallback_reason": "feature_disabled",
                        "fallback_source": "cli",
                    },
                    "timestamp": 1234567890.0,
                }
            },
        )
        
        rerank_span = telemetry["spans"]["rag.rerank"]
        assert rerank_span["status"] == "skipped"
        assert rerank_span["reason"] == "Disabled via CLI flag"
        assert rerank_span["attributes"]["fallback_count"] == 1
        assert rerank_span["attributes"]["fallback_reason"] == "feature_disabled"
        assert rerank_span["attributes"]["fallback_source"] == "cli"
        
        rerank_metrics = telemetry["metrics"]["rerank"]
        assert rerank_metrics["status"] == "skipped"
        assert rerank_metrics["reason"] == "stage disabled"
        assert rerank_metrics["details"]["fallback_count"] == 1
        assert rerank_metrics["details"]["fallback_reason"] == "feature_disabled"
        assert rerank_metrics["details"]["fallback_source"] == "cli"

    def test_rerank_span_error_includes_fallback_details(self) -> None:
        """Verify rerank error span records fallback metadata for diagnostics."""
        telemetry = build_telemetry_summary(
            mitigation_events=[],
            rotation_events=[],
            lease_events=[],
            batch_progress_events=[],
            span_events={
                "rag.rerank": {
                    "span_id": "span-rerank-error",
                    "status": "error",
                    "reason": "CUDA OOM; fallback engaged",
                    "timestamp": 1234567890.0,
                    "attributes": {
                        "fallback_count": 1,
                        "fallback_reason": "execution_failed",
                        "fallback_source": "runtime",
                    },
                }
            },
            metrics_report={
                "rerank": {
                    "status": "emitted",
                    "metrics": [
                        "rag_rerank_latency_seconds",
                        "rag_gpu_peak_bytes",
                        "rerank_fallback_total",
                    ],
                    "details": {
                        "fallback_count": 1,
                        "fallback_reason": "execution_failed",
                        "fallback_source": "runtime",
                        "device_fallback_applied": False,
                    },
                    "timestamp": 1234567890.0,
                }
            },
        )

        rerank_span = telemetry["spans"]["rag.rerank"]
        assert rerank_span["status"] == "error"
        assert rerank_span["attributes"]["fallback_count"] == 1
        assert rerank_span["attributes"]["fallback_reason"] == "execution_failed"
        assert rerank_span["attributes"]["fallback_source"] == "runtime"

        rerank_metrics = telemetry["metrics"]["rerank"]
        assert rerank_metrics["status"] == "emitted"
        assert rerank_metrics["details"]["fallback_count"] == 1
        assert rerank_metrics["details"]["fallback_reason"] == "execution_failed"
        assert rerank_metrics["details"]["fallback_source"] == "runtime"


class TestProcessingSummaryWithMetrics:
    """Test processing_summary.json includes metrics emission outcomes."""

    def test_summary_includes_rerank_and_sparse_metrics_when_enabled(self) -> None:
        """Verify processing summary persists metrics emission outcomes."""
        toggles = FeatureToggleConfig(
            enable_rerank=True,
            enable_sparse=True,
            sparse_models=["naver/splade_v2_distil"],
            sources={
                "enable_rerank": "default",
                "enable_sparse": "default",
                "sparse_models": "default",
            },
        )

        rerank_stage = build_rerank_stage_summary(
            enabled=True,
            model_name="jina-reranker-v2-base-multilingual",
            loaded=True,
            device="cuda:0",
            executed=True,
            status="completed",
            reason="Query-time reranking executed",
            metrics={"top_k_candidates": 100, "rerank_top_k": 20, "batch_size": 32},
            requested_device="cuda",
            fallback_applied=False,
            fallback_reason=None,
        )

        rerank_stage.update(
            {
                "run_id": "rerank-run-123",
                "latency_ms": 145.3,
                "gpu_peak_gb": 2.1,
                "batch_size": 32,
                "candidate_ids": ["doc-1", "doc-2"],
                "scores": [0.91, 0.73],
                "dense_scores": [0.82, 0.64],
                "query": "demo query",
                "candidate_metadata": [
                    {"id": "doc-1"},
                    {"id": "doc-2"},
                ],
                "result_count": 2,
                "initial_candidate_count": 4,
            }
        )

        sparse_stage = build_sparse_stage_summary(
            enabled=True,
            model_names=["naver/splade_v2_distil"],
            vectors_total=3096,
            vectors_available=3096,
            executed=True,
            coverage_ratio=1.0,
            devices={"sparse_0": "cuda:1"},
            fallback_used=False,
            fallback_reason=None,
            latency_ms=423.0,
            run_id="sparse-run-321",
            success=True,
            error_message=None,
            fallback_count=0,
            device="cuda:1",
        )

        telemetry = build_telemetry_summary(
            mitigation_events=[],
            rotation_events=[],
            lease_events=[],
            batch_progress_events=[],
            span_events={
                "rag.rerank": {
                    "span_id": "span-rerank-1",
                    "status": "active",
                    "timestamp": 1234567890.0,
                },
                "rag.sparse": {
                    "span_id": "span-sparse-1",
                    "status": "active",
                    "timestamp": 1234567890.0,
                },
            },
            metrics_report={
                "rerank": {
                    "status": "emitted",
                    "metrics": ["rag_rerank_latency_seconds", "rag_gpu_peak_bytes"],
                    "details": {
                        "prometheus_latency_emitted": True,
                        "prometheus_gpu_emitted": True,
                    },
                    "timestamp": 1234567890.0,
                },
                "sparse": {
                    "status": "emitted",
                    "metrics": ["rag_sparse_latency_seconds"],
                    "details": {
                        "prometheus_latency_emitted": True,
                    },
                    "timestamp": 1234567890.0,
                },
            },
        )

        dense_run = {"total_embeddings_generated": 3096}

        summary = build_processing_summary(
            feature_toggles=toggles,
            dense_run=dense_run,
            rerank_stage=rerank_stage,
            sparse_stage=sparse_stage,
            telemetry=telemetry,
            collection_name="test_collection",
            chunk_count=3096,
        )

        # Verify rerank_run and sparse_run sections exist
        assert "rerank_run" in summary
        assert summary["rerank_run"]["enabled"] is True
        assert summary["rerank_run"]["executed"] is True

        assert "sparse_run" in summary
        assert summary["sparse_run"]["enabled"] is True
        assert summary["sparse_run"]["executed"] is True
        assert summary["sparse_run"]["vectors"]["coverage_ratio"] == pytest.approx(1.0)

        rerank_payload = summary["rerank_run"]["payload"]
        assert rerank_payload["run_id"] == "rerank-run-123"
        assert rerank_payload["scores"] == pytest.approx([0.91, 0.73])
        assert rerank_payload["dense_scores"] == pytest.approx([0.82, 0.64])
        assert rerank_payload["initial_candidate_count"] == 4
        assert rerank_payload["result_count"] == 2

        sparse_payload = summary["sparse_run"]["payload"]
        assert sparse_payload["run_id"] == "sparse-run-321"
        assert sparse_payload["vectors"]["coverage_ratio"] == pytest.approx(1.0)
        assert sparse_payload["success"] is True
        assert sparse_payload["fallback_count"] == 0
        assert sparse_payload["device"] == "cuda:1"

        assert summary["compatibility"]["current"] == "v4.1"
        assert summary["compatibility"]["legacy"] == ["v4.0"]

        # Verify telemetry metrics sections
        assert "telemetry" in summary
        assert "metrics" in summary["telemetry"]
        assert summary["telemetry"]["metrics"]["rerank"]["status"] == "emitted"
        assert summary["telemetry"]["metrics"]["sparse"]["status"] == "emitted"

    def test_summary_omits_rerank_and_sparse_sections_when_disabled(self) -> None:
        """Verify processing summary omits rerank_run/sparse_run when stages disabled."""
        toggles = FeatureToggleConfig(
            enable_rerank=False,
            enable_sparse=False,
            sparse_models=[],
            sources={
                "enable_rerank": "cli_flag",
                "enable_sparse": "cli_flag",
                "sparse_models": "default",
            },
        )

        telemetry = build_telemetry_summary(
            mitigation_events=[],
            rotation_events=[],
            lease_events=[],
            batch_progress_events=[],
            span_events={
                "rag.rerank": {
                    "span_id": "span-rerank-disabled",
                    "status": "skipped",
                    "reason": "Disabled via CLI flag",
                    "timestamp": 1234567890.0,
                },
                "rag.sparse": {
                    "span_id": "span-sparse-disabled",
                    "status": "skipped",
                    "reason": "Disabled via CLI flag",
                    "timestamp": 1234567890.0,
                },
            },
            metrics_report={
                "rerank": {
                    "status": "skipped",
                    "reason": "stage disabled",
                    "metrics": ["rag_rerank_latency_seconds", "rag_gpu_peak_bytes"],
                    "timestamp": 1234567890.0,
                },
                "sparse": {
                    "status": "skipped",
                    "reason": "stage disabled",
                    "metrics": ["rag_sparse_latency_seconds"],
                    "timestamp": 1234567890.0,
                },
            },
        )

        dense_run = {"total_embeddings_generated": 3096}

        summary = build_processing_summary(
            feature_toggles=toggles,
            dense_run=dense_run,
            rerank_stage=None,  # None when disabled
            sparse_stage=None,  # None when disabled
            telemetry=telemetry,
            collection_name="test_collection",
            chunk_count=3096,
        )

        # Verify rerank_run and sparse_run sections are absent
        assert "rerank_run" not in summary
        assert "sparse_run" not in summary

        # Verify feature toggles reflect disabled state
        assert summary["feature_toggles"]["enable_rerank"] is False
        assert summary["feature_toggles"]["enable_sparse"] is False

        # Verify metrics report skip reasons
        assert summary["telemetry"]["metrics"]["rerank"]["status"] == "skipped"
        assert summary["telemetry"]["metrics"]["rerank"]["reason"] == "stage disabled"
        assert summary["telemetry"]["metrics"]["sparse"]["status"] == "skipped"
        assert summary["telemetry"]["metrics"]["sparse"]["reason"] == "stage disabled"

    def test_metrics_disabled_but_stages_enabled_records_skip(self) -> None:
        """Verify stages enabled but metrics disabled records emitter disabled reason."""
        toggles = FeatureToggleConfig(
            enable_rerank=True,
            enable_sparse=True,
            sparse_models=["naver/splade_v2_distil"],
            sources={
                "enable_rerank": "default",
                "enable_sparse": "default",
                "sparse_models": "default",
            },
        )

        rerank_stage = build_rerank_stage_summary(
            enabled=True,
            model_name="jina-reranker-v2-base-multilingual",
            loaded=True,
            device="cpu",
            executed=False,
            status="staged",
            reason="Staged for query-time execution",
            metrics={"top_k_candidates": 100},
            requested_device="cuda",
            fallback_applied=False,
            fallback_reason=None,
        )

        sparse_stage = build_sparse_stage_summary(
            enabled=True,
            model_names=["naver/splade_v2_distil"],
            vectors_total=3096,
            vectors_available=3096,
            executed=True,
            coverage_ratio=1.0,
            devices={"sparse_0": "cpu"},
            fallback_used=False,
            fallback_reason=None,
        )

        telemetry = build_telemetry_summary(
            mitigation_events=[],
            rotation_events=[],
            lease_events=[],
            batch_progress_events=[],
            span_events={
                "rag.rerank": {
                    "span_id": "span-rerank-1",
                    "status": "active",
                    "timestamp": 1234567890.0,
                },
                "rag.sparse": {
                    "span_id": "span-sparse-1",
                    "status": "active",
                    "timestamp": 1234567890.0,
                },
            },
            metrics_report={
                "rerank": {
                    "status": "skipped",
                    "reason": "metrics emitter disabled",
                    "metrics": ["rag_rerank_latency_seconds", "rag_gpu_peak_bytes"],
                    "timestamp": 1234567890.0,
                },
                "sparse": {
                    "status": "skipped",
                    "reason": "metrics emitter disabled",
                    "metrics": ["rag_sparse_latency_seconds"],
                    "timestamp": 1234567890.0,
                },
            },
        )

        dense_run = {"total_embeddings_generated": 3096}

        summary = build_processing_summary(
            feature_toggles=toggles,
            dense_run=dense_run,
            rerank_stage=rerank_stage,
            sparse_stage=sparse_stage,
            telemetry=telemetry,
            collection_name="test_collection",
            chunk_count=3096,
        )

        # Verify rerank_run and sparse_run sections exist (stages enabled)
        assert "rerank_run" in summary
        assert "sparse_run" in summary

        # Verify metrics report emitter disabled reason
        assert summary["telemetry"]["metrics"]["rerank"]["status"] == "skipped"
        assert summary["telemetry"]["metrics"]["rerank"]["reason"] == "metrics emitter disabled"
        assert summary["telemetry"]["metrics"]["sparse"]["status"] == "skipped"
        assert summary["telemetry"]["metrics"]["sparse"]["reason"] == "metrics emitter disabled"


class TestGpuAlertThresholds:
    """Test GPU alert threshold detection and helper methods."""

    def test_gpu_alert_warning_threshold_detection(self) -> None:
        """Verify warning alert fires when GPU peak exceeds 11.5 GB."""
        emitter = PrometheusMetricsEmitter(enabled=True, namespace="rag")

        # 11.6 GB should trigger warning
        warning_bytes = int(11.6 * 1024**3)
        alert_level, threshold_exceeded = emitter.check_gpu_alert_threshold(
            peak_bytes=warning_bytes
        )

        assert threshold_exceeded is True
        assert alert_level == "warning"

    def test_gpu_alert_critical_threshold_detection(self) -> None:
        """Verify critical alert fires when GPU peak exceeds 12 GB."""
        emitter = PrometheusMetricsEmitter(enabled=True, namespace="rag")

        # 12.1 GB should trigger critical
        critical_bytes = int(12.1 * 1024**3)
        alert_level, threshold_exceeded = emitter.check_gpu_alert_threshold(
            peak_bytes=critical_bytes
        )

        assert threshold_exceeded is True
        assert alert_level == "critical"

    def test_gpu_alert_no_threshold_exceeded(self) -> None:
        """Verify no alert when GPU peak below warning threshold."""
        emitter = PrometheusMetricsEmitter(enabled=True, namespace="rag")

        # 8.4 GB should not trigger any alert
        normal_bytes = int(8.4 * 1024**3)
        alert_level, threshold_exceeded = emitter.check_gpu_alert_threshold(
            peak_bytes=normal_bytes
        )

        assert threshold_exceeded is False
        assert alert_level == "none"

    def test_alert_threshold_helper_methods(self) -> None:
        """Verify alert threshold helper returns correct values."""
        emitter = PrometheusMetricsEmitter(enabled=True, namespace="rag")

        thresholds = emitter.get_alert_thresholds_gb()

        assert thresholds["soft_limit"] == 10.0
        assert thresholds["warning"] == 11.5
        assert thresholds["critical"] == 12.0

    def test_gpu_alert_warning_boundary(self) -> None:
        """Verify exact warning threshold boundary behavior."""
        emitter = PrometheusMetricsEmitter(enabled=True, namespace="rag")

        # Exactly 11.5 GB should trigger warning
        exact_warning_bytes = int(11.5 * 1024**3)
        alert_level, threshold_exceeded = emitter.check_gpu_alert_threshold(
            peak_bytes=exact_warning_bytes
        )

        assert threshold_exceeded is True
        assert alert_level == "warning"

    def test_gpu_alert_critical_boundary(self) -> None:
        """Verify exact critical threshold boundary behavior."""
        emitter = PrometheusMetricsEmitter(enabled=True, namespace="rag")

        # Exactly 12 GB should trigger critical
        exact_critical_bytes = int(12.0 * 1024**3)
        alert_level, threshold_exceeded = emitter.check_gpu_alert_threshold(
            peak_bytes=exact_critical_bytes
        )

        assert threshold_exceeded is True
        assert alert_level == "critical"


class TestSparseFallbackCoverage:
    """Test sparse fallback coverage with degraded input scenarios."""

    def test_sparse_fallback_degraded_inputs(self) -> None:
        """Verify sparse fallback handles mixed degraded/clean chunks."""
        from processor.ultimate_embedder.summary import build_sparse_stage_summary

        # Simulate 850 of 1000 chunks with valid sparse vectors (15% degraded)
        sparse_stage = build_sparse_stage_summary(
            enabled=True,
            model_names=["naver/splade_v2_distil"],
            vectors_total=1000,
            vectors_available=850,
            executed=True,
            coverage_ratio=0.85,
            devices={"sparse_0": "cuda:0"},
            fallback_used=True,
            fallback_reason="150 chunks below minimum token threshold (10 tokens)",
        )

        assert sparse_stage["enabled"] is True
        assert sparse_stage["executed"] is True
        assert sparse_stage["vectors"]["total"] == 1000
        assert sparse_stage["vectors"]["available"] == 850
        assert sparse_stage["vectors"]["coverage_ratio"] == pytest.approx(0.85)
        assert sparse_stage["fallback_used"] is True
        assert "150 chunks" in sparse_stage["fallback_reason"]

    def test_sparse_fallback_empty_chunks(self) -> None:
        """Verify sparse fallback handles empty chunks gracefully."""
        from processor.ultimate_embedder.summary import build_sparse_stage_summary

        # Simulate all chunks empty (0% coverage)
        sparse_stage = build_sparse_stage_summary(
            enabled=True,
            model_names=["naver/splade_v2_distil"],
            vectors_total=100,
            vectors_available=0,
            executed=True,
            coverage_ratio=0.0,
            devices={"sparse_0": "cpu"},
            fallback_used=True,
            fallback_reason="All chunks empty or below minimum token threshold",
        )

        assert sparse_stage["vectors"]["coverage_ratio"] == pytest.approx(0.0)
        assert sparse_stage["fallback_used"] is True
        assert "empty" in sparse_stage["fallback_reason"].lower()

    def test_sparse_fallback_ultra_short_chunks(self) -> None:
        """Verify sparse fallback handles ultra-short chunks (<10 tokens)."""
        from processor.ultimate_embedder.summary import build_sparse_stage_summary

        # Simulate 92% coverage with 8% ultra-short chunks
        sparse_stage = build_sparse_stage_summary(
            enabled=True,
            model_names=["naver/splade_v2_distil"],
            vectors_total=500,
            vectors_available=460,
            executed=True,
            coverage_ratio=0.92,
            devices={"sparse_0": "cuda:0"},
            fallback_used=True,
            fallback_reason="40 chunks below 10-token threshold",
        )

        assert sparse_stage["vectors"]["coverage_ratio"] == pytest.approx(0.92)
        assert sparse_stage["fallback_used"] is True
        assert "10-token" in sparse_stage["fallback_reason"]

    def test_sparse_fallback_special_characters_only(self) -> None:
        """Verify sparse fallback handles special-character-only chunks."""
        from processor.ultimate_embedder.summary import build_sparse_stage_summary

        # Simulate chunks with only special characters (no textual content)
        sparse_stage = build_sparse_stage_summary(
            enabled=True,
            model_names=["naver/splade_v2_distil"],
            vectors_total=50,
            vectors_available=0,
            executed=True,
            coverage_ratio=0.0,
            devices={"sparse_0": "cpu"},
            fallback_used=True,
            fallback_reason="Non-textual content (special characters only)",
        )

        assert sparse_stage["vectors"]["coverage_ratio"] == pytest.approx(0.0)
        assert sparse_stage["fallback_used"] is True
        assert "special characters" in sparse_stage["fallback_reason"].lower()

    def test_sparse_fallback_no_degradation(self) -> None:
        """Verify sparse reports no fallback when all chunks valid."""
        from processor.ultimate_embedder.summary import build_sparse_stage_summary

        # Simulate perfect coverage (100%)
        sparse_stage = build_sparse_stage_summary(
            enabled=True,
            model_names=["naver/splade_v2_distil"],
            vectors_total=3096,
            vectors_available=3096,
            executed=True,
            coverage_ratio=1.0,
            devices={"sparse_0": "cuda:0"},
            fallback_used=False,
            fallback_reason=None,
        )

        assert sparse_stage["vectors"]["coverage_ratio"] == pytest.approx(1.0)
        assert sparse_stage["fallback_used"] is False
        # When fallback_reason is None, it's not included in the dict
        assert "fallback_reason" not in sparse_stage


@pytest.mark.regression_harness
def test_regression_telemetry_default_matches_golden(
    regression_summary_runner,
    regression_goldens,
):
    summary, _ = regression_summary_runner("default_on")
    expected = json.loads(
        regression_goldens["processing_summary_default_on"].read_text(encoding="utf-8")
    )

    assert summary["telemetry"] == expected["telemetry"]


@pytest.mark.regression_harness
def test_regression_telemetry_rerank_disabled(regression_summary_runner):
    summary, _ = regression_summary_runner("rerank_disabled")
    telemetry = summary["telemetry"]

    rerank_span = telemetry["spans"]["rag.rerank"]
    assert rerank_span["status"] == "skipped"
    assert "Disabled via CLI" in rerank_span["reason"]

    rerank_metrics = telemetry["metrics"]["rerank"]
    assert rerank_metrics["status"] == "skipped"
    assert "Disabled" in rerank_metrics["reason"]

    sparse_metrics = telemetry["metrics"].get("sparse")
    assert sparse_metrics
    assert sparse_metrics["status"] in {"emitted", "skipped"}


@pytest.mark.regression_harness
def test_regression_telemetry_dense_fallback(regression_summary_runner):
    summary, _ = regression_summary_runner("fallback_force")
    telemetry = summary["telemetry"]

    rerank_metrics = telemetry["metrics"]["rerank"]
    sparse_metrics = telemetry["metrics"]["sparse"]
    assert rerank_metrics["status"] == "skipped"
    assert sparse_metrics["status"] == "skipped"

    rerank_span = telemetry["spans"]["rag.rerank"]
    sparse_span = telemetry["spans"]["rag.sparse"]
    assert rerank_span["status"] == "skipped"
    assert sparse_span["status"] == "skipped"
    assert "fallback" in rerank_span["reason"].lower()
    assert "fallback" in sparse_span["reason"].lower()

