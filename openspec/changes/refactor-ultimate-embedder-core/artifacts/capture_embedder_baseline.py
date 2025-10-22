"""Utility for capturing baseline telemetry and export snapshots for UltimateKaggleEmbedderV4.

This script mirrors the dry-run fixtures from the test suite to generate repeatable
outputs that can be used to validate the refactor plan under
`openspec/changes/refactor-ultimate-embedder-core`.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
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

    def encode(
        self,
        texts: Iterable[str],
        batch_size: int = 32,
        show_progress_bar: bool = False,
        convert_to_numpy: bool = True,
        normalize_embeddings: bool = True,
        device: str | None = None,
    ):
        if self.fail_next:
            self.fail_next = False
            raise RuntimeError("forced failure for instrumentation test")

        texts = list(texts)
        count = len(texts)
        base = np.arange(count, dtype=np.float32).reshape(-1, 1)
        offset = float(abs(hash(self.hf_model_id)) % 11)
        embeddings = np.tile(base + offset, (1, 1024))
        return embeddings.astype(np.float32)

    def half(self):
        return self

    def to(self, device: str):
        self._device = device
        return self


def _ensure_test_patches(workspace_root: Path, cache_dir: Path) -> None:
    """Patch heavy dependencies so the baseline run stays offline and deterministic."""

    import torch  # noqa: WPS433

    from processor.ultimate_embedder import core as embedder_core

    embedder_core.SentenceTransformer = FakeSentenceTransformer
    embedder_core.snapshot_download = lambda *args, **kwargs: str(cache_dir)
    embedder_core.CrossEncoder = FakeSentenceTransformer

    os.environ.setdefault("HF_HOME", str(cache_dir))
    os.environ.setdefault("HF_HUB_OFFLINE", "1")

    torch.cuda.is_available = lambda: False  # type: ignore[assignment]
    torch.cuda.device_count = lambda: 0  # type: ignore[assignment]
    torch.compile = lambda model, mode=None: model  # type: ignore[assignment]


def _serialise(obj: Any) -> Any:
    """Convert objects returned by the embedder into JSON-friendly values."""

    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj

    if isinstance(obj, Path):
        return str(obj)

    if isinstance(obj, np.generic):
        return obj.item()

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if is_dataclass(obj):
        return _serialise(asdict(obj))

    if isinstance(obj, dict):
        return {str(key): _serialise(value) for key, value in obj.items()}

    if isinstance(obj, (list, tuple, set)):
        return [_serialise(value) for value in obj]

    return repr(obj)


def capture_baseline(output_dir: Path) -> Path:
    """Run the embedder and capture telemetry/export baselines."""

    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = output_dir / "hf_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    export_root = output_dir / "exports"
    export_root.mkdir(parents=True, exist_ok=True)

    _ensure_test_patches(ROOT, cache_dir)

    gpu_config = KaggleGPUConfig(device_count=1)
    export_config = KaggleExportConfig(working_dir=str(export_root))
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

    results = embedder.generate_embeddings_kaggle_optimized(
        enable_monitoring=False,
        save_intermediate=True,
    )

    export_manifest = embedder.export_for_local_qdrant()

    manifest_path = output_dir / "baseline_exports_manifest.json"
    manifest_payload = {
        key: {
            "path": value,
            "exists": os.path.exists(value),
            "size_bytes": os.path.getsize(value) if os.path.exists(value) else None,
        }
        for key, value in export_manifest.items()
    }
    with manifest_path.open("w", encoding="utf-8") as handle:
        json.dump(_serialise(manifest_payload), handle, indent=2, sort_keys=True)

    target_path = output_dir / "baseline_results.json"
    with target_path.open("w", encoding="utf-8") as handle:
        json.dump(_serialise(results), handle, indent=2, sort_keys=True)

    return target_path


def main() -> None:
    output_dir = Path(__file__).resolve().parent / "baseline_run"
    artifact_path = capture_baseline(output_dir)
    print(f"Baseline captured at: {artifact_path}")


if __name__ == "__main__":
    main()
