import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from processor.kaggle_ultimate_embedder_v4 import (
    EnsembleConfig,
    KaggleExportConfig,
    KaggleGPUConfig,
    UltimateKaggleEmbedderV4,
)


class FakeSentenceTransformer:
    """Lightweight stand-in for SentenceTransformer used in rotation tests."""

    def __init__(self, hf_model_id: str, **_: object) -> None:
        self.hf_model_id = hf_model_id
        self._device = "cpu"
        self.fail_next = False

    def encode(
        self,
        texts,
        batch_size: int = 32,
        show_progress_bar: bool = False,
        convert_to_numpy: bool = True,
        normalize_embeddings: bool = True,
        device: str | None = None,
    ):
        if self.fail_next:
            self.fail_next = False
            raise RuntimeError("forced failure for instrumentation test")

        count = len(texts)
        # Match ensemble expectations: 1024D vectors like Kaggle models.
        base = np.arange(count, dtype=np.float32).reshape(-1, 1)
        offset = float(abs(hash(self.hf_model_id)) % 11)
        embeddings = np.tile(base + offset, (1, 1024))
        return embeddings.astype(np.float32)

    def half(self):
        return self

    def to(self, device):
        self._device = device
        return self


@pytest.fixture(autouse=True)
def _patch_sentence_transformer(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "processor.kaggle_ultimate_embedder_v4.SentenceTransformer",
        FakeSentenceTransformer,
    )
    monkeypatch.setattr(
        "processor.kaggle_ultimate_embedder_v4.snapshot_download",
        lambda *args, **kwargs: str(tmp_path),
    )
    monkeypatch.setattr("torch.cuda.is_available", lambda: False)
    monkeypatch.setattr("torch.cuda.device_count", lambda: 0)
    monkeypatch.setattr("torch.compile", lambda model, mode=None: model)


def _build_embedder(tmp_path: Path) -> UltimateKaggleEmbedderV4:
    gpu_config = KaggleGPUConfig(device_count=1)
    export_config = KaggleExportConfig(working_dir=str(tmp_path))
    ensemble_config = EnsembleConfig(
        ensemble_models=[
            "jina-code-embeddings-1.5b",
            "bge-m3",
            "qwen3-embedding-0.6b",
        ],
        sequential_passes=True,
        parallel_encoding=False,
        sequential_data_parallel=False,
    )
    embedder = UltimateKaggleEmbedderV4(
        model_name="jina-code-embeddings-1.5b",
        gpu_config=gpu_config,
        export_config=export_config,
        enable_ensemble=True,
        ensemble_config=ensemble_config,
        force_cpu=True,
        local_files_only=True,
    )
    embedder.chunk_texts = [f"chunk-{idx}" for idx in range(6)]
    embedder.raw_chunk_texts = list(embedder.chunk_texts)
    embedder.chunks_metadata = [
        {"source_path": f"doc_{idx}.md", "global_chunk_id": idx}
        for idx in range(len(embedder.chunk_texts))
    ]
    return embedder


def test_rotation_events_capture_every_model(tmp_path):
    embedder = _build_embedder(tmp_path)

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


def test_rotation_failure_raises_and_logs(tmp_path):
    embedder = _build_embedder(tmp_path)

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