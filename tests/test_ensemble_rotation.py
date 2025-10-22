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

    progress_events = results.get("batch_progress")
    assert progress_events, "batch progress telemetry should be captured"
    progress_models = {event.get("model") for event in progress_events}
    assert progress_models == expected_models
    assert all(event.get("status") == "completed" for event in progress_events)
    assert all(isinstance(event.get("batch_index"), int) for event in progress_events)
    assert all(event.get("label") for event in progress_events)
    assert {event.get("device") for event in progress_events}


def test_rotation_failure_raises_and_logs(build_embedder):
    embedder = build_embedder()

    # Force the third ensemble model to fail on every encode attempt.
    target_model = embedder.models["qwen3-embedding-0.6b"]

    def _boom(*_, **__):
        raise RuntimeError("forced ensemble failure")

    target_model.encode = _boom  # type: ignore[assignment]

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


def test_progress_fallback_avoids_duplicate_tqdm(build_embedder):
    embedder = build_embedder()
    embedder.models[embedder.model_name].fail_on_tqdm_once = True

    results = embedder.generate_embeddings_kaggle_optimized(
        enable_monitoring=False,
        save_intermediate=False,
    )

    progress_events = results.get("batch_progress") or []
    assert progress_events, "batch progress telemetry should exist after fallback"
    assert all(event.get("status") == "completed" for event in progress_events)

    primary_model = embedder.models[embedder.model_name]
    assert primary_model.last_tqdm_kwargs is None