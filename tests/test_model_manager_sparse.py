"""Coverage for sparse and ensemble integration paths in ModelManager."""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from processor.ultimate_embedder.config import KaggleGPUConfig, ModelConfig
from processor.ultimate_embedder.model_manager import ModelManager


class DummyEmbedder:
    """Minimal embedder stub for ModelManager sparse tests."""

    def __init__(self) -> None:
        self.sparse_model_names = ["splade"]
        self.enable_sparse = True
        self._sparse_runtime_reason = None
        self.sparse_models = {}
        self.sparse_device_map = {}
        self.models = {}
        self.device = "cuda"
        self.device_count = 1
        self.enable_ensemble = False
        self.ensemble_config = None
        self.embedding_backend = "local"
        self.model_name = "dummy-model"
        self.telemetry = MagicMock()
        self.telemetry.record_cache_event = MagicMock()
        self.telemetry.record_mitigation = MagicMock()
        self.processing_stats = {"hydration_events": []}
        self.hf_cache_dir = Path(tempfile.mkdtemp())
        self.force_cache_refresh = False
        self.local_files_only = True
        self.primary_model = None
        self.model_config = ModelConfig(
            name="dummy-model",
            hf_model_id="dummy/model",
            vector_dim=768,
            max_tokens=512,
            trust_remote_code=False,
            supports_flash_attention=False,
            recommended_batch_size=8,
        )
        self.gpu_config = KaggleGPUConfig()
        self.gpu_config.backend = "pytorch"
        self.gpu_config.precision = "fp32"
        self.gpu_config.gradient_checkpointing = False
        self.gpu_config.enable_memory_efficient_attention = False
        self.gpu_config.enable_torch_compile = False
        self.force_cpu = False

    def _record_mitigation(self, event_type: str, **details: object) -> None:
        self.telemetry.record_mitigation(event_type, **details)

    def _record_model_dtype(self, model_name: str, model: object) -> None:
        self.recorded_dtype = (model_name, model)


@pytest.fixture()
def patch_sentence_transformer(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock_model = MagicMock(name="SparseSentenceTransformer")
    factory = MagicMock(return_value=mock_model)
    monkeypatch.setattr(
        "processor.ultimate_embedder.model_manager.SentenceTransformer",
        factory,
    )
    return mock_model


def test_initialize_sparse_models_registers_model(patch_sentence_transformer: MagicMock) -> None:
    embedder = DummyEmbedder()
    manager = ModelManager(embedder, logging.getLogger("test"))

    manager.initialize_sparse_models()

    assert embedder.sparse_models["splade"] is patch_sentence_transformer
    assert embedder.models["splade"] is patch_sentence_transformer
    assert embedder.sparse_device_map["splade"] == "cpu"
    assert embedder.recorded_dtype[0] == "splade"


def test_initialize_ensemble_models_allows_local_backends(monkeypatch: pytest.MonkeyPatch) -> None:
    embedder = DummyEmbedder()
    embedder.enable_ensemble = True
    embedder.embedding_backend = "pytorch"
    embedder.ensemble_config = MagicMock()
    embedder.ensemble_config.ensemble_models = ["bge-m3"]
    embedder.ensemble_config.exclusive_mode = True

    manager = ModelManager(embedder, logging.getLogger("ensemble-test"))

    calls: list[tuple[str, str]] = []

    def fake_load(self: ModelManager, model_name: str, device: str) -> object:
        calls.append((model_name, device))
        self.embedder.models[model_name] = object()
        return self.embedder.models[model_name]

    monkeypatch.setattr(ModelManager, "_load_ensemble_model", fake_load)

    manager._initialize_ensemble_models()

    assert calls == [("bge-m3", "cpu")]


def test_initialize_ensemble_models_skips_remote_backend(monkeypatch: pytest.MonkeyPatch) -> None:
    embedder = DummyEmbedder()
    embedder.enable_ensemble = True
    embedder.embedding_backend = "api"
    embedder.ensemble_config = MagicMock()
    embedder.ensemble_config.ensemble_models = ["bge-m3"]
    embedder.ensemble_config.exclusive_mode = True

    manager = ModelManager(embedder, logging.getLogger("ensemble-remote"))
    spy = MagicMock()
    monkeypatch.setattr(ModelManager, "_load_ensemble_model", spy)

    manager._initialize_ensemble_models()

    spy.assert_not_called()


def test_initialize_primary_model_updates_backend_on_fallback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    embedder = DummyEmbedder()
    embedder.device = "cpu"
    embedder.device_count = 0
    embedder.models = {}
    embedder.hf_cache_dir = tmp_path
    embedder.gpu_config.backend = "onnx"
    embedder.embedding_backend = "onnx"

    manager = ModelManager(embedder, logging.getLogger("fallback"))

    monkeypatch.setattr(
        "processor.ultimate_embedder.model_manager.ONNX_AVAILABLE",
        True,
    )
    monkeypatch.setattr(
        ModelManager,
        "_ensure_model_snapshot",
        MagicMock(return_value=tmp_path),
    )
    monkeypatch.setattr(
        ModelManager,
        "_load_onnx_model",
        MagicMock(side_effect=RuntimeError("onnx failure")),
    )
    fallback_model = object()
    monkeypatch.setattr(
        ModelManager,
        "_load_pytorch_model",
        MagicMock(return_value=fallback_model),
    )

    manager.initialize_primary_model()

    assert embedder.primary_model is fallback_model
    assert embedder.embedding_backend == "pytorch"
    assert embedder.gpu_config.backend == "pytorch"
