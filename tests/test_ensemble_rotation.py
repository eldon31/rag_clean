import pytest


def test_rotation_events_capture_every_model(build_embedder):
    embedder = build_embedder()

    results = embedder.generate_embeddings_kaggle_optimized(
        enable_monitoring=False,
        save_intermediate=False,
    )

    rotation_events = results.get("ensemble_rotation")
    assert rotation_events, "rotation telemetry should be recorded"

    models_seen = {event["model"] for event in rotation_events}
    expected_models = {
        embedder.model_name,
        *embedder.ensemble_config.ensemble_models,
    }
    assert models_seen == expected_models

    batches = {event["batch_index"] for event in rotation_events}
    assert batches == {0}, "single batch run should log batch index 0"

    for event in rotation_events:
        assert event["status"] == "completed"
        assert isinstance(event.get("duration_seconds"), float)
        assert event.get("chunk_count") == len(embedder.chunk_texts)
        assert event.get("chunk_samples"), "chunk samples should be included"


def test_rotation_failure_raises_and_logs(build_embedder):
    embedder = build_embedder()

    # Force the third ensemble model to fail on its next encode call.
    embedder.models["qwen3-embedding-0.6b"].fail_next = True

    with pytest.raises(RuntimeError):
        embedder.generate_embeddings_kaggle_optimized(
            enable_monitoring=False,
            save_intermediate=False,
        )

    assert embedder.rotation_events, "rotation telemetry should capture failure"
    failure_event = embedder.rotation_events[-1]
    assert failure_event["model"] == "qwen3-embedding-0.6b"
    assert failure_event["status"] == "failed"
    assert failure_event.get("batch_index") == 0