import logging
from processor.ultimate_embedder.controllers import (
    AdaptiveBatchController,
    GPUMemorySnapshot,
    collect_gpu_snapshots,
)
from processor.ultimate_embedder.telemetry import (
    TelemetryTracker,
    resolve_rotation_payload_limit,
)


def test_telemetry_tracker_records_and_limits(monkeypatch):
    monkeypatch.setenv("EMBEDDER_ROTATION_LIMIT", "1")
    limit = resolve_rotation_payload_limit(log=logging.getLogger("test"))
    tracker = TelemetryTracker(rotation_payload_limit=limit)

    tracker.record_mitigation("startup", status="ok")
    assert tracker.mitigation_events[0]["type"] == "startup"

    tracker.record_cache_event({"model_id": "foo"})
    assert tracker.cache_events

    tracker.record_rotation_event({"model": "primary"})
    tracker.record_rotation_event({"model": "companion"})
    assert tracker.rotation_overflow_count == 1

    tracker.reset_runtime_state()
    assert not tracker.mitigation_events
    assert not tracker.rotation_events
    assert tracker.cache_events, "cache history should persist across resets"


def test_collect_gpu_snapshots_cpu_path():
    snapshots = collect_gpu_snapshots(device="cpu", device_count=1)
    assert snapshots == {}


def test_adaptive_batch_controller_reduces_on_pressure():
    controller = AdaptiveBatchController(
        primary_batch=16,
        device_count=1,
        gpu0_soft_limit_bytes=1024,
        companion_enabled=True,
    )
    snapshot = GPUMemorySnapshot(
        device_id=0,
        total_bytes=2048,
        free_bytes=100,
        allocated_bytes=1948,
        reserved_bytes=1948,
    )
    event = controller.register_snapshot({0: snapshot})
    assert event is not None
    assert controller.primary_batch < 16


def test_generate_embeddings_integration(build_embedder, monkeypatch, tmp_path):
    monkeypatch.delenv("EMBEDDER_ROTATION_LIMIT", raising=False)
    embedder = build_embedder()
    embedder.telemetry.record_cache_event({"model_id": embedder.model_name, "status": "cache_hit"})

    export_calls = []
    export_payload = {
        "numpy": str(tmp_path / "unit_embeddings.npy"),
        "jsonl": str(tmp_path / "unit_qdrant.jsonl"),
        "qdrant_collection": "test-collection",
    }

    def _fake_export():
        export_calls.append(True)
        return export_payload

    monkeypatch.setattr(embedder.export_runtime, "export_for_local_qdrant", _fake_export)

    results = embedder.generate_embeddings_kaggle_optimized(
        enable_monitoring=False,
        save_intermediate=False,
    )

    assert results["total_embeddings_generated"] == len(embedder.chunk_texts)
    assert results["ensemble_rotation"], "rotation telemetry should be captured"
    assert results["mitigation_events"] == embedder.mitigation_events
    assert results["ensemble_rotation_limit"] == embedder.rotation_payload_limit
    assert "gpu_snapshot_summary" in results
    assert results["embedding_dimension"] == embedder.model_config.vector_dim
    assert results["cache_events"] == embedder.cache_events
    assert any(event.get("status") == "cache_hit" for event in results["cache_events"])

    exported = embedder.export_for_local_qdrant()
    assert export_calls
    assert exported == export_payload
