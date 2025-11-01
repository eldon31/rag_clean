"""Public interface for the modular Ultimate Embedder package."""

from .config import (
    AdvancedPreprocessingConfig,
    AdvancedTextCache,
    EnsembleConfig,
    get_kaggle_model_config,
    KAGGLE_OPTIMIZED_MODELS,
    KaggleExportConfig,
    KaggleGPUConfig,
    ModelConfig,
    normalize_kaggle_model_names,
    resolve_kaggle_model_key,
    RERANKING_MODELS,
    RerankingConfig,
    SPARSE_MODELS,
)
from .runtime_config import FeatureToggleConfig, load_feature_toggles
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
    "get_kaggle_model_config",
    "KAGGLE_OPTIMIZED_MODELS",
    "KaggleExportConfig",
    "KaggleGPUConfig",
    "ModelConfig",
    "normalize_kaggle_model_names",
    "resolve_kaggle_model_key",
    "RERANKING_MODELS",
    "RerankingConfig",
    "SPARSE_MODELS",
    "FeatureToggleConfig",
    "load_feature_toggles",
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
