from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from processor.ultimate_embedder.config import KaggleExportConfig, KaggleGPUConfig
from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4
from processor.ultimate_embedder.runtime_config import FeatureToggleConfig


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


def _build_embedder(enable_ensemble: bool | None) -> UltimateKaggleEmbedderV4:
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
        output_path=str(Path.cwd() / "_debug_outputs"),
    )

    export_config = KaggleExportConfig(
        working_dir=str(Path.cwd() / "_debug_exports"),
        output_prefix="debug",
        export_numpy=False,
        export_jsonl=False,
        export_faiss=False,
        export_sparse_jsonl=False,
    )

    return UltimateKaggleEmbedderV4(
        model_name="jina-code-embeddings-1.5b",
        gpu_config=gpu_config,
        export_config=export_config,
        enable_ensemble=enable_ensemble,
        feature_toggles=FeatureToggleConfig(),
        force_cpu=True,
        gpu0_soft_limit_gb=8.0,
    )


def _run(enable_ensemble: bool | None) -> dict[str, object]:
    embedder = _build_embedder(enable_ensemble)
    chunk_dir = Path("_debug_chunks")
    chunk_dir.mkdir(parents=True, exist_ok=True)
    long_text = " ".join(["debug" for _ in range(80)])
    payload = [
        {
            "text": long_text,
            "metadata": {
                "token_count": 96,
                "source_path": "debug/source.md",
                "heading_text": "Debug Heading",
            },
        },
        {
            "text": long_text,
            "metadata": {
                "token_count": 104,
                "source_path": "debug/source.md",
                "heading_text": "Debug Heading 2",
            },
        },
    ]
    (chunk_dir / "sample.json").write_text(json.dumps(payload), encoding="utf-8")

    patches = [
        patch("processor.ultimate_embedder.core.SentenceTransformer", _DummySentenceTransformer),
        patch("processor.ultimate_embedder.model_manager.SentenceTransformer", _DummySentenceTransformer),
        patch("processor.ultimate_embedder.core.CrossEncoder", _DummyCrossEncoder),
        patch("processor.ultimate_embedder.rerank_pipeline.CrossEncoder", _DummyCrossEncoder),
        patch("processor.ultimate_embedder.model_manager.snapshot_download", _fake_snapshot_download),
        patch("processor.ultimate_embedder.batch_runner.normalize", lambda array, norm="l2", axis=1: array),
    ]

    with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5]:
        embedder.load_chunks_from_processing(str(chunk_dir))
        embedder.generate_embeddings_kaggle_optimized(
            enable_monitoring=False,
            save_intermediate=False,
        )
        summary = embedder.write_processing_summary(
            Path("_debug_summary.json"),
            collection_name="test",
        )
    return {
        "requested": enable_ensemble,
        "state": summary.get("ensemble_state", {}),
    }


def main() -> None:
    for requested in (True, False, None):
        result = _run(requested)
        print("requested=", result["requested"])
        print(json.dumps(result["state"], indent=2))


if __name__ == "__main__":
    main()
