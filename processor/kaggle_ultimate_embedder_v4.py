"""Compatibility shim for the legacy Kaggle Ultimate Embedder module."""

from __future__ import annotations

import warnings

from processor.ultimate_embedder import (
    AdaptiveBatchController,
    AdvancedPreprocessingConfig,
    AdvancedTextCache,
    EnsembleConfig,
    GPUMemorySnapshot,
    KAGGLE_OPTIMIZED_MODELS,
    KaggleExportConfig,
    KaggleGPUConfig,
    ModelConfig,
    RERANKING_MODELS,
    RerankingConfig,
    SPARSE_MODELS,
    TelemetryTracker,
    collect_gpu_snapshots,
    resolve_rotation_payload_limit,
)
from processor.ultimate_embedder.core import (
    UltimateKaggleEmbedderV4,
    main,
)

warnings.warn(
    "processor.kaggle_ultimate_embedder_v4 is deprecated; import from "
    "processor.ultimate_embedder.core instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "UltimateKaggleEmbedderV4",
    "main",
    "AdaptiveBatchController",
    "GPUMemorySnapshot",
    "collect_gpu_snapshots",
    "TelemetryTracker",
    "resolve_rotation_payload_limit",
    "AdvancedPreprocessingConfig",
    "AdvancedTextCache",
    "EnsembleConfig",
    "KAGGLE_OPTIMIZED_MODELS",
    "KaggleExportConfig",
    "KaggleGPUConfig",
    "ModelConfig",
    "RERANKING_MODELS",
    "RerankingConfig",
    "SPARSE_MODELS",
]
