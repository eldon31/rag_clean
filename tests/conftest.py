import sys
from pathlib import Path
from typing import Any, Callable, Dict, Optional

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from processor.ultimate_embedder import (  # noqa: E402
    EnsembleConfig,
    KaggleExportConfig,
    KaggleGPUConfig,
    UltimateKaggleEmbedderV4,
)


class FakeSentenceTransformer:
    """Lightweight stand-in for SentenceTransformer used in tests."""

    def __init__(self, hf_model_id: str, **_: object) -> None:
        self.hf_model_id = hf_model_id
        self._device = "cpu"
        self.fail_next = False
        self.fail_on_tqdm_once = False
        self.last_tqdm_kwargs: Optional[Dict[str, Any]] = None

    def encode(
        self,
        texts,
        batch_size: int = 32,
        show_progress_bar: bool = False,
        convert_to_numpy: bool = True,
        normalize_embeddings: bool = True,
        device: str | None = None,
        tqdm_kwargs: Optional[Dict[str, Any]] = None,
        **_: Any,
    ):
        self.last_tqdm_kwargs = tqdm_kwargs
        if self.fail_on_tqdm_once and tqdm_kwargs:
            self.fail_on_tqdm_once = False
            raise RuntimeError("forced tqdm failure for retry test")

        if self.fail_next:
            self.fail_next = False
            raise RuntimeError("forced failure for instrumentation test")

        count = len(texts)
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
        "processor.ultimate_embedder.core.SentenceTransformer",
        FakeSentenceTransformer,
    )
    monkeypatch.setattr(
        "processor.ultimate_embedder.model_manager.SentenceTransformer",
        FakeSentenceTransformer,
    )
    monkeypatch.setattr(
        "processor.ultimate_embedder.core.snapshot_download",
        lambda *args, **kwargs: str(tmp_path),
    )
    monkeypatch.setattr(
        "processor.ultimate_embedder.model_manager.snapshot_download",
        lambda *args, **kwargs: str(tmp_path),
    )
    monkeypatch.setattr("torch.cuda.is_available", lambda: False)
    monkeypatch.setattr("torch.cuda.device_count", lambda: 0)
    monkeypatch.setattr("torch.compile", lambda model, mode=None: model)


@pytest.fixture
def build_embedder(tmp_path) -> Callable[[], UltimateKaggleEmbedderV4]:
    def _builder() -> UltimateKaggleEmbedderV4:
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

    return _builder
