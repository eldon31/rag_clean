import logging
from collections import defaultdict
from contextlib import contextmanager
from types import SimpleNamespace
from typing import Any, Dict, Generator, Iterable, List, Optional

import numpy as np
import pytest

from processor.ultimate_embedder.batch_runner import BatchRunner
from processor.ultimate_embedder.config import EnsembleConfig, KaggleGPUConfig, ModelConfig
from processor.ultimate_embedder.model_manager import ModelManager


class StubTelemetry:
    def __init__(self) -> None:
        self.batch_progress_events: List[Dict[str, Any]] = []
        self.gpu_lease_events: List[Dict[str, Any]] = []

    def reset_runtime_state(self) -> None:
        self.batch_progress_events.clear()
        self.gpu_lease_events.clear()

    def record_batch_progress(self, **payload: Any) -> None:
        self.batch_progress_events.append(payload)

    def record_gpu_lease_event(self, **payload: Any) -> None:
        self.gpu_lease_events.append(payload)


class StubModel:
    def __init__(self, name: str) -> None:
        self.name = name
        self.device_history: List[str] = []
        self.half_calls = 0

    def to(self, device: str) -> "StubModel":
        self.device_history.append(device)
        return self

    def half(self) -> "StubModel":
        self.half_calls += 1
        return self


class RecordingModelManager(ModelManager):
    def __init__(self, embedder: "StubEmbedder", logger: logging.Logger) -> None:
        super().__init__(embedder, logger)  # type: ignore[arg-type]
        self.stage_calls: List[str] = []
        self.hydrate_calls: List[Dict[str, Any]] = []

    def stage_model_to_cpu(self, model_name: str) -> None:
        self.stage_calls.append(model_name)
        super().stage_model_to_cpu(model_name)

    def hydrate_model_to_gpus(
        self,
        model_name: str,
        device_ids: Optional[List[int]] = None,
    ) -> Any:
        self.hydrate_calls.append({"model": model_name, "device_ids": tuple(device_ids or [])})
        return super().hydrate_model_to_gpus(model_name, device_ids=device_ids)


class StubEmbedder:
    def __init__(self, warm_cache: bool) -> None:
        self.model_name = "primary"
        self.model_config = ModelConfig(
            name="primary",
            hf_model_id="test/primary",
            vector_dim=4,
            max_tokens=16,
        )
        self.enable_ensemble = True
        self.device = "cpu"
        self.device_count = 1
        self.batch_hint_map = {"primary": 2, "bge-m3": 2}
        self.model_scales = {"primary": 1.0, "bge-m3": 2.0}
        self.chunk_texts = ["chunk-1", "chunk-2", "chunk-3", "chunk-4"]
        self.embeddings: Optional[np.ndarray] = None
        self.embeddings_by_model: Dict[str, np.ndarray] = {}
        self.rotation_events: List[Dict[str, Any]] = []
        self.mitigations: List[Dict[str, Any]] = []
        self.models = {name: StubModel(name) for name in ["primary", "bge-m3"]}

        self.gpu_config = KaggleGPUConfig(
            device_count=1,
            precision="fp32",
            dynamic_batching=False,
            base_batch_size=2,
            backend="pytorch",
        )
        self.gpu0_soft_limit_bytes = 256 * 1024 * 1024

        self.ensemble_config = EnsembleConfig(
            ensemble_models=["bge-m3"],
            weighting_strategy="equal",
            model_weights={"primary": 1.0, "bge-m3": 1.0},
            aggregation_method="weighted_average",
            parallel_encoding=False,
            sequential_passes=True,
            sequential_data_parallel=False,
            exclusive_mode=True,
            warm_cache_after_release=warm_cache,
        )

        self.telemetry = StubTelemetry()
        self.processing_stats: Dict[str, List[Any]] = defaultdict(list)
        self.matryoshka_dim: Optional[int] = None
        self.ensemble_device_map: Dict[str, str] = {}
        self.sequential_device_order: List[str] = ["cpu"]

        logger = logging.getLogger("exclusive-test.embedder")
        logger.setLevel(logging.CRITICAL)
        self.model_manager = RecordingModelManager(self, logger)

    # --- Facade helpers exercised by BatchRunner ---
    def _get_primary_model(self) -> StubModel:
        return self.models[self.model_name]

    def _get_or_load_ensemble_model(self, model_name: str) -> StubModel:
        return self.models[model_name]

    def _log_gpu_memory(self, *_args: Any, **_kwargs: Any) -> None:  # pragma: no cover - noop
        return

    def _describe_batch_slice(self, batch_slice: Optional[slice]) -> Dict[str, Any]:
        if batch_slice is None:
            return {
                "start": 0,
                "end": len(self.chunk_texts),
                "count": len(self.chunk_texts),
                "samples": [],
            }
        start = batch_slice.start or 0
        stop = batch_slice.stop or len(self.chunk_texts)
        return {
            "start": start,
            "end": stop,
            "count": stop - start,
            "samples": [],
        }

    def _format_batch_slice_info(self, info: Dict[str, Any]) -> str:
        return f"chunks={info.get('start', 0)}-{info.get('end', 0)}"

    def _get_batch_hint_for_model(self, model_name: str) -> int:
        return self.batch_hint_map.get(model_name, 2)

    def _normalize_embedding_matrix(self, embeddings: np.ndarray, _model_name: str) -> np.ndarray:
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1
        return embeddings / norms

    def _ensure_embedding_dimension(
        self,
        embeddings: np.ndarray,
        expected_dim: int,
    ) -> Any:
        if embeddings.shape[1] > expected_dim:
            return embeddings[:, :expected_dim], True
        if embeddings.shape[1] < expected_dim:
            padded = np.zeros((embeddings.shape[0], expected_dim), dtype=embeddings.dtype)
            padded[:, : embeddings.shape[1]] = embeddings
            return padded, True
        return embeddings, False

    def _select_sequential_device(self, model_name: str) -> str:
        return "cpu"

    def _unwrap_model(self, model: StubModel) -> StubModel:
        return model

    def _get_batch_progress_label(self, start: int, end: int) -> str:
        return f"{start}-{end}"

    def _collect_gpu_snapshots(self) -> Dict[str, Any]:
        return {}

    def _record_mitigation(self, event_type: str, **payload: Any) -> None:
        self.mitigations.append({"event_type": event_type, **payload})

    def _record_rotation_event(self, payload: Dict[str, Any]) -> None:
        self.rotation_events.append(payload)

    def _start_performance_monitoring(self) -> None:  # pragma: no cover - not exercised
        return

    def _stop_performance_monitoring(self) -> None:  # pragma: no cover - not exercised
        return

    def _require_embeddings(self) -> np.ndarray:
        if self.embeddings is None:
            raise RuntimeError("Embeddings not generated")
        return self.embeddings

    def _call_encode(
        self,
        model: StubModel,
        texts: Iterable[str],
        batch_size: int,
        device: str,
        progress_context: Any,
    ) -> np.ndarray:
        del batch_size, device, progress_context
        count = len(list(texts))
        scale = self.model_scales[model.name]
        return np.full((count, self.model_config.vector_dim), scale, dtype=np.float32)


@contextmanager
def fake_lease(
    embedder: StubEmbedder,
    model_name: str,
    logger: logging.Logger,
    device_ids: Optional[List[int]] = None,
) -> Generator[SimpleNamespace, None, None]:
    del logger
    ids = device_ids or [0]

    def _record(event_type: str) -> None:
        embedder.telemetry.record_gpu_lease_event(
            event_type=event_type,
            model=model_name,
            device_ids=list(ids),
            vram_snapshots={idx: {"allocated_bytes": 0} for idx in ids},
        )

    lease = SimpleNamespace(
        device_ids=list(ids),
        summarize=lambda: {"model": model_name, "device_ids": list(ids), "vram_deltas_gb": {}},
    )

    _record("acquire")
    try:
        yield lease
    finally:
        _record("release")


@pytest.fixture(autouse=True)
def patch_gpu_lease(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "processor.ultimate_embedder.gpu_lease.lease_gpus",
        fake_lease,
    )


def _run_exclusive(warm_cache: bool) -> SimpleNamespace:
    embedder = StubEmbedder(warm_cache=warm_cache)
    runner = BatchRunner(embedder, logging.getLogger("exclusive-test.runner"))  # type: ignore[arg-type]
    results = runner.run_exclusive_ensemble(enable_monitoring=False, save_intermediate=False)
    return SimpleNamespace(embedder=embedder, results=results)


def test_exclusive_ensemble_sequential_execution() -> None:
    outcome = _run_exclusive(warm_cache=False)
    embedder = outcome.embedder
    results = outcome.results

    assert results["models_executed"] == ["primary", "bge-m3"]
    assert embedder.embeddings.shape == (4, 4)
    assert np.allclose(embedder.embeddings, np.full((4, 4), 0.5, dtype=np.float32))

    assert len(embedder.telemetry.batch_progress_events) == 4
    event_models = {event["model"] for event in embedder.telemetry.batch_progress_events}
    assert event_models == {"primary", "bge-m3"}

    primary_model = embedder.models["primary"]
    assert primary_model.device_history.count("cpu") == 2

    assert embedder.model_manager.stage_calls == ["primary"]
    hydrated_models = [entry["model"] for entry in embedder.model_manager.hydrate_calls]
    assert hydrated_models == ["primary", "bge-m3"]

    lease_events = [event["event_type"] for event in embedder.telemetry.gpu_lease_events]
    assert lease_events == ["acquire", "release", "acquire", "release"]


def test_warm_cache_skips_cpu_staging() -> None:
    outcome = _run_exclusive(warm_cache=True)
    embedder = outcome.embedder

    primary_model = embedder.models["primary"]
    assert primary_model.device_history.count("cpu") == 1

    assert embedder.model_manager.stage_calls == ["primary"]
    assert embedder.telemetry.batch_progress_events
    assert embedder.telemetry.gpu_lease_events