"""Unit tests for multivector population helpers."""

from __future__ import annotations

from unittest.mock import patch

import numpy as np

from processor.ultimate_embedder.config import KaggleExportConfig, KaggleGPUConfig
from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4
from processor.ultimate_embedder.runtime_config import FeatureToggleConfig


def test_populate_multivector_channels_builds_expected_structure() -> None:
    """Ensure multivector helpers generate matryoshka and companion channels."""

    feature_toggles = FeatureToggleConfig(
        enable_rerank=False,
        enable_sparse=False,
        sparse_models=[],
        sources={},
    )

    with patch.object(UltimateKaggleEmbedderV4, "_initialize_embedding_models", return_value=None), \
        patch.object(UltimateKaggleEmbedderV4, "_initialize_companion_models", return_value=None), \
        patch.object(UltimateKaggleEmbedderV4, "_initialize_sparse_models", return_value=None), \
        patch.object(UltimateKaggleEmbedderV4, "_initialize_reranking_model", return_value=None):
        embedder = UltimateKaggleEmbedderV4(
            model_name="jina-code-embeddings-1.5b",
            gpu_config=KaggleGPUConfig(device_count=0, kaggle_environment=False),
            export_config=KaggleExportConfig(
                export_numpy=False,
                export_jsonl=False,
                export_faiss=False,
                export_sparse_jsonl=False,
            ),
            feature_toggles=feature_toggles,
            force_cpu=True,
        )

    primary_matrix = np.arange(12, dtype=np.float32).reshape(3, 4)
    companion_matrix = (np.arange(12, dtype=np.float32).reshape(3, 4) + 1.0).astype(np.float32)

    embedder._populate_multivector_channels(
        final_embeddings=primary_matrix,
        per_model_embeddings={"bge-m3": companion_matrix},
    )

    matryoshka_key = f"{embedder.model_name}_matryoshka_4"
    assert matryoshka_key in embedder.multivectors_by_model
    assert len(embedder.multivectors_by_model[matryoshka_key]) == 3
    assert embedder.multivector_dimensions[matryoshka_key] == 4
    assert embedder.multivector_comparators[matryoshka_key] == "max_sim"

    companion_key = "bge-m3_dense"
    assert companion_key in embedder.multivectors_by_model
    assert embedder.multivector_dimensions[companion_key] == 4
    assert embedder.multivector_comparators[companion_key] == "max_sim"
    assert all(len(vectors) == 1 for vectors in embedder.multivectors_by_model[companion_key])