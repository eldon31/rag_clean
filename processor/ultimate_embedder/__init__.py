"""Public interface for the modular Ultimate Embedder package."""

from .config import (
    AdvancedPreprocessingConfig,
    AdvancedTextCache,
    EnsembleConfig,
    KAGGLE_OPTIMIZED_MODELS,
    KaggleExportConfig,
    KaggleGPUConfig,
    ModelConfig,
    RERANKING_MODELS,
    RerankingConfig,
    SPARSE_MODELS,
)
from .batch_runner import BatchRunner
from .export_runtime import ExportRuntime
from .controllers import AdaptiveBatchController, GPUMemorySnapshot, collect_gpu_snapshots
from .monitoring import PerformanceMonitor
from .rerank_pipeline import RerankPipeline
from .sparse_pipeline import build_sparse_vector_from_metadata, infer_modal_hint
from .core import UltimateKaggleEmbedderV4, main
from .telemetry import TelemetryTracker, resolve_rotation_payload_limit
from .progress import BatchProgressContext

__all__ = [
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
    "AdaptiveBatchController",
    "GPUMemorySnapshot",
    "collect_gpu_snapshots",
    "UltimateKaggleEmbedderV4",
    "main",
    "TelemetryTracker",
    "resolve_rotation_payload_limit",
    "RerankPipeline",
    "build_sparse_vector_from_metadata",
    "infer_modal_hint",
    "BatchRunner",
    "ExportRuntime",
    "PerformanceMonitor",
    "BatchProgressContext",
]
