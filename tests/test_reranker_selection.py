import logging
from unittest.mock import MagicMock

import numpy as np
import pytest

from processor.ultimate_embedder.config import (
    KaggleExportConfig,
    KaggleGPUConfig,
    RerankingConfig,
)
from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4
from processor.ultimate_embedder.rerank_pipeline import _BiEncoderRerankerAdapter
from processor.ultimate_embedder.runtime_config import FeatureToggleConfig


@pytest.fixture(autouse=True)
def _silence_logging():
    logging.getLogger("processor.ultimate_embedder.core").setLevel(logging.CRITICAL)
    logging.getLogger("processor.ultimate_embedder.rerank_pipeline").setLevel(logging.CRITICAL)


def _noop(*args, **kwargs):
    return None


def _build_gpu_config(tmp_path):
    return KaggleGPUConfig(
        device_count=0,
        vram_per_gpu_gb=8.0,
        total_vram_gb=8.0,
        max_memory_per_gpu=0.8,
        enable_memory_efficient_attention=False,
        gradient_checkpointing=False,
        precision="fp32",
        enable_mixed_precision=False,
        use_amp=False,
        base_batch_size=16,
        dynamic_batching=False,
        max_sequence_length=2048,
        backend="pytorch",
        enable_torch_compile=False,
        strategy="data_parallel",
        enable_gradient_accumulation=False,
        accumulation_steps=1,
        kaggle_environment=False,
        output_path=str(tmp_path / "outputs"),
    )


def _build_feature_toggles():
    return FeatureToggleConfig(
        enable_rerank=True,
        enable_sparse=False,
        sparse_models=[],
        sources={
            "enable_rerank": "default",
            "enable_sparse": "default",
            "sparse_models": "default",
        },
        resolution_events=(),
    )


def test_initialize_reranking_model_falls_back_to_coderank(monkeypatch, tmp_path):
    sentinel_model = MagicMock(name="sentinel_reranker")

    def fake_create_reranker(*, model_name, spec, device, logger):
        if model_name == "jina-reranker-v3":
            raise RuntimeError("checkpoint incompatible")
        assert model_name == "coderank-bi-encoder"
        return sentinel_model

    monkeypatch.setattr(
        "processor.ultimate_embedder.core.create_reranker_from_spec",
        fake_create_reranker,
    )

    monkeypatch.setattr(
        UltimateKaggleEmbedderV4,
        "_initialize_embedding_models",
        _noop,
    )
    monkeypatch.setattr(
        UltimateKaggleEmbedderV4,
        "_initialize_companion_models",
        _noop,
    )
    monkeypatch.setattr(
        UltimateKaggleEmbedderV4,
        "_initialize_sparse_models",
        _noop,
    )

    gpu_config = _build_gpu_config(tmp_path)
    export_config = KaggleExportConfig(working_dir=str(tmp_path / "exports"))
    toggles = _build_feature_toggles()

    embedder = UltimateKaggleEmbedderV4(
        model_name="qwen3-embedding-0.6b",
        gpu_config=gpu_config,
        export_config=export_config,
        reranking_config=RerankingConfig(
            model_name="jina-reranker-v3",
            enable_reranking=True,
        ),
        feature_toggles=toggles,
        force_cpu=True,
        enable_sparse=False,
    )

    assert embedder.reranker is sentinel_model
    assert embedder.reranking_config.model_name == "coderank-bi-encoder"
    assert embedder.reranking_config.enable_reranking is True
    assert embedder.rerank_failure_reason is None
    assert embedder._rerank_runtime_reason is None


def test_initialize_reranking_model_falls_back_to_bge_when_coderank_fails(monkeypatch, tmp_path):
    sentinel_model = MagicMock(name="sentinel_bge")

    def fake_create_reranker(*, model_name, spec, device, logger):
        if model_name in {"jina-reranker-v3", "coderank-bi-encoder"}:
            raise RuntimeError("unavailable")
        assert model_name == "bge-reranker-v2-m3"
        return sentinel_model

    monkeypatch.setattr(
        "processor.ultimate_embedder.core.create_reranker_from_spec",
        fake_create_reranker,
    )

    for attr in (
        "_initialize_embedding_models",
        "_initialize_companion_models",
        "_initialize_sparse_models",
    ):
        monkeypatch.setattr(UltimateKaggleEmbedderV4, attr, _noop)

    gpu_config = _build_gpu_config(tmp_path)
    export_config = KaggleExportConfig(working_dir=str(tmp_path / "exports"))
    toggles = _build_feature_toggles()

    embedder = UltimateKaggleEmbedderV4(
        model_name="qwen3-embedding-0.6b",
        gpu_config=gpu_config,
        export_config=export_config,
        reranking_config=RerankingConfig(
            model_name="jina-reranker-v3",
            enable_reranking=True,
        ),
        feature_toggles=toggles,
        force_cpu=True,
        enable_sparse=False,
    )

    assert embedder.reranker is sentinel_model
    assert embedder.reranking_config.model_name == "bge-reranker-v2-m3"
    assert embedder.reranking_config.enable_reranking is True
    assert embedder.rerank_failure_reason is None
    assert embedder._rerank_runtime_reason is None


class _DummySentenceTransformer:
    def __init__(self):
        self.device = "cpu"

    def to(self, device):
        self.device = device
        return self

    def eval(self):
        return self

    def encode(self, texts, **kwargs):
        bases = [float(len(text) or 1) for text in texts]
        return np.asarray([[value] for value in bases], dtype=np.float32)


def test_bi_encoder_adapter_scores_pairs():
    adapter = _BiEncoderRerankerAdapter(_DummySentenceTransformer())

    scores = adapter.predict([
        ["q", "alpha"],
        ["q", "beta"],
        ["only_query"],
    ])

    assert len(scores) == 3
    assert scores[0] > scores[1]
    assert scores[2] == 0.0
