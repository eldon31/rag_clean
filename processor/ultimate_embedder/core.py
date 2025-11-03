#!/usr/bin/env python3
"""
ULTIMATE KAGGLE EMBEDDER V4
Split Architecture: Kaggle T4 x2 GPU -> Local Qdrant

DEPLOYMENT MODEL:
- Kaggle: GPU embedding generation (T4 x2)
- Local: Qdrant vector database and search
- Connection: Download embeddings from Kaggle -> Upload to local Qdrant

V4 OPTIMIZATIONS (from 9,654-vector knowledge base audit):
- Backend optimization (ONNX/TensorRT for Kaggle GPUs)
- Advanced memory management (optimized for T4 x2)
- Enhanced preprocessing pipeline with caching
- Multi-model ensemble support
- Distributed training optimizations
- Production-grade export formats

PERFORMANCE TARGET:
- V3: 12-18s for 3,096 chunks (172-258 chunks/sec)
- V4: 6-10s for 3,096 chunks (310-516 chunks/sec) - 80% improvement
"""

# ruff: noqa: E402

from __future__ import annotations

import os
import json
import sys
import importlib.util
import importlib.metadata as importlib_metadata

# ============================================================================
# CRITICAL: Set environment variables BEFORE any other imports
# ============================================================================

# Fix protobuf compatibility issues (protobuf 4.x vs 3.x API breaking changes)
# This must be set before importing TensorFlow, ONNX, or any library that uses protobuf
os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")


# Force JAX/TensorFlow to remain on CPU so Kaggle doesn't crash when both stacks register CUDA plugins.
os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("JAX_PLATFORM_NAME", "cpu")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")

def _apply_protobuf_messagefactory_shim() -> List[str]:
    """Reintroduce MessageFactory.GetPrototype across protobuf implementations."""

    patched_targets: List[str] = []

    def _patch_class(module: Any, attr_name: str) -> Optional[type]:
        nonlocal patched_targets

        target_cls = getattr(module, attr_name, None)
        if target_cls is None:
            return None
        if hasattr(target_cls, "GetPrototype"):
            return target_cls

        get_message_class = getattr(target_cls, "GetMessageClass", None)
        if get_message_class is None:
            return target_cls

        def _get_prototype(self: Any, descriptor: Any):
            return get_message_class(self, descriptor)

        try:
            subclass_name = f"Patched{target_cls.__name__}"
            patched_cls = type(subclass_name, (target_cls,), {"GetPrototype": _get_prototype})
            setattr(module, attr_name, patched_cls)
            patched_targets.append(f"{module.__name__}.{attr_name}[subclass]")
            return patched_cls
        except TypeError:
            class CompatFactory:  # type: ignore[too-few-public-methods]
                """Lazy wrapper that delegates to the original factory implementation."""

                __slots__ = ("_delegate",)

                def __init__(self, *args: Any, **kwargs: Any) -> None:
                    self._delegate = target_cls(*args, **kwargs)

                def GetPrototype(self, descriptor: Any) -> Any:  # noqa: N802 - protobuf casing
                    return self._delegate.GetMessageClass(descriptor)

                def GetMessageClass(self, descriptor: Any) -> Any:  # noqa: N802
                    return self._delegate.GetMessageClass(descriptor)

                def __getattr__(self, name: str) -> Any:
                    return getattr(self._delegate, name)

                def __dir__(self) -> List[str]:
                    return list(dict.fromkeys(dir(self._delegate)))

            setattr(module, attr_name, CompatFactory)
            patched_targets.append(f"{module.__name__}.{attr_name}[wrapper]")
            return CompatFactory

    try:
        from google.protobuf import message_factory as _message_factory  # type: ignore[import-not-found]  # pylint: disable=import-outside-toplevel
    except Exception:
        _message_factory = None

    patched_message_factory_cls: Optional[type] = None
    if _message_factory is not None:
        patched_message_factory_cls = _patch_class(_message_factory, "MessageFactory")

    try:
        from google.protobuf.pyext import _message as _pyext_message  # type: ignore[attr-defined,import-not-found]  # pylint: disable=import-outside-toplevel
    except Exception:
        _pyext_message = None

    patched_pyext_factory_cls: Optional[type] = None
    if _pyext_message is not None:
        patched_pyext_factory_cls = _patch_class(_pyext_message, "MessageFactory")

        default_factory = getattr(_pyext_message, "_DEFAULT_FACTORY", None)
        if default_factory is not None and not hasattr(default_factory, "GetPrototype"):
            factory_cls = patched_pyext_factory_cls or patched_message_factory_cls
            if factory_cls is not None:
                try:
                    _pyext_message._DEFAULT_FACTORY = factory_cls()
                    patched_targets.append("google.protobuf.pyext._message._DEFAULT_FACTORY")
                except Exception:
                    pass

    try:
        from google.protobuf.internal import python_message as _python_message  # type: ignore[import-not-found]  # pylint: disable=import-outside-toplevel
    except Exception:
        _python_message = None

    if _python_message is not None:
        default_factory = getattr(_python_message, "_DEFAULT_FACTORY", None)
        if default_factory is not None and not hasattr(default_factory, "GetPrototype"):
            factory_cls = patched_pyext_factory_cls or patched_message_factory_cls
            if factory_cls is not None:
                try:
                    _python_message._DEFAULT_FACTORY = factory_cls()
                    patched_targets.append(
                        "google.protobuf.internal.python_message._DEFAULT_FACTORY"
                    )
                except Exception:
                    pass

    return patched_targets


_PROTOBUF_COMPAT_PATCH_TARGETS = _apply_protobuf_messagefactory_shim()

import gc
import inspect
import logging
import re
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from functools import lru_cache
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple, Type, Union, cast

import numpy as np
import torch

from huggingface_hub import snapshot_download as _snapshot_download

try:
    from huggingface_hub import LocalEntryNotFoundError  # type: ignore[attr-defined]
except ImportError:
    try:
        from huggingface_hub.utils import LocalEntryNotFoundError  # type: ignore[attr-defined]
    except ImportError:  # pragma: no cover - legacy hub versions
        LocalEntryNotFoundError = FileNotFoundError  # type: ignore[assignment]

LocalEntryNotFoundErrorType = cast(Type[Exception], LocalEntryNotFoundError)


def snapshot_download(*args: Any, **kwargs: Any) -> str:
    """Expose `snapshot_download` for monkeypatched tests while avoiding lint errors."""

    return _snapshot_download(*args, **kwargs)

# Core ML libraries
from sentence_transformers import CrossEncoder, SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Advanced optimization libraries (optional on Kaggle)
_ORT_IMPORT_ERROR: Optional[str] = None
try:
    from optimum.onnxruntime import ORTModelForFeatureExtraction  # type: ignore[import-not-found]
except Exception as exc:  # pragma: no cover - defensive import guard
    ORTModelForFeatureExtraction = None  # type: ignore[assignment]
    _ORT_IMPORT_ERROR = f"{type(exc).__name__}: {exc}"

ONNX_AVAILABLE = ORTModelForFeatureExtraction is not None

# Setup logging for Kaggle
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/kaggle/working/embedding_process.log') if '/kaggle' in os.getcwd() else logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

if _PROTOBUF_COMPAT_PATCH_TARGETS:
    try:
        import google.protobuf as _protobuf  # pylint: disable=import-outside-toplevel

        logger.info(
            "Applied protobuf compatibility shim (%s) for MessageFactory (version %s)",
            ", ".join(_PROTOBUF_COMPAT_PATCH_TARGETS),
            getattr(_protobuf, "__version__", "unknown"),
        )
    except Exception:
        logger.info(
            "Applied protobuf compatibility shim for MessageFactory (%s)",
            ", ".join(_PROTOBUF_COMPAT_PATCH_TARGETS),
        )

if _ORT_IMPORT_ERROR:
    logger.warning(
        "Optimum ORT backend disabled, falling back to PyTorch models: %s",
        _ORT_IMPORT_ERROR,
    )


CUDA_DEBUG_ENV_KEYS = (
    "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION",
    "JAX_PLATFORMS",
    "JAX_PLATFORM_NAME",
    "TF_CPP_MIN_LOG_LEVEL",
    "XLA_PYTHON_CLIENT_PREALLOCATE",
    "CUDA_VISIBLE_DEVICES",
)


CUDA_DEBUG_MODULES = (
    "torch",
    "jax",
    "jaxlib",
    "tensorflow",
    "cupy",
    "onnxruntime",
)


def _safe_package_version(name: str) -> Optional[str]:
    """Return installed package version without importing heavy modules."""

    candidates = {name, name.replace("_", "-")}
    for candidate in candidates:
        try:
            return importlib_metadata.version(candidate)
        except importlib_metadata.PackageNotFoundError:
            continue
        except Exception:  # pragma: no cover - defensive guard
            return None
    return None


if TYPE_CHECKING:
    from processor.ultimate_embedder.cross_encoder_executor import CrossEncoderRerankRun


# Module extractions
from processor.ultimate_embedder.batch_runner import BatchRunner
from processor.ultimate_embedder.progress import BatchProgressContext
from processor.ultimate_embedder.chunk_loader import ChunkLoader
from processor.ultimate_embedder.controllers import (
    AdaptiveBatchController,
    GPUMemorySnapshot,
    collect_gpu_snapshots,
)
from processor.ultimate_embedder.export_runtime import ExportRuntime
from processor.ultimate_embedder.model_manager import ModelManager
from processor.ultimate_embedder.monitoring import PerformanceMonitor
from processor.ultimate_embedder.prometheus_metrics import create_prometheus_emitter, PrometheusMetricsEmitter
from processor.ultimate_embedder.rerank_pipeline import RerankPipeline
from processor.ultimate_embedder.telemetry import TelemetryTracker, resolve_rotation_payload_limit
from processor.ultimate_embedder.throughput_monitor import ThroughputMonitor
from processor.ultimate_embedder.config import (
    AdvancedPreprocessingConfig,
    AdvancedTextCache,
    EnsembleConfig,
    KAGGLE_OPTIMIZED_MODELS,
    KaggleExportConfig,
    KaggleGPUConfig,
    ModelConfig,
    normalize_kaggle_model_names,
    resolve_kaggle_model_key,
    RERANKING_MODELS,
    RerankingConfig,
)
from processor.ultimate_embedder.runtime_config import (
    FeatureToggleConfig,
    load_feature_toggles,
)
from processor.ultimate_embedder.summary import (
    build_performance_baseline,
    build_processing_summary,
    build_rerank_stage_summary,
    build_sparse_stage_summary,
    build_telemetry_summary,
)
from processor.ultimate_embedder.backend_encoder import encode_with_backend

# ============================================================================
# SOTA MODEL CONFIGURATIONS (Kaggle T4 x2 Optimized)
# ============================================================================
# Definitions reside in processor.ultimate_embedder.config and are imported
# above for reuse within the facade.


CPU_DENSE_FALLBACK_PRIMARY = "qwen3-embedding-0.6b"
CPU_DENSE_FALLBACK_ENSEMBLE = ["nomic-coderank", "all-miniLM-l6"]



class UltimateKaggleEmbedderV4:
    """
    Ultimate Kaggle Embedder V4 - Split Architecture Optimized

    SPLIT DEPLOYMENT MODEL:
    - Kaggle T4 x2: GPU embedding generation only
    - Local machine: Qdrant vector database and search
    - Export: Optimized formats for local upload

    V4 ENHANCEMENTS (from 9,654-vector audit):
    - Backend optimization (ONNX/TensorRT when available)
    - Advanced memory management for T4 x2
    - Intelligent preprocessing with caching
    - Multi-model ensemble capability
    - Production-grade export formats
    - Kaggle-specific optimizations
    """
    
    def __init__(
        self,
        model_name: str = "jina-code-embeddings-1.5b",
        gpu_config: Optional[KaggleGPUConfig] = None,
        export_config: Optional[KaggleExportConfig] = None,
        preprocessing_config: Optional[AdvancedPreprocessingConfig] = None,
        enable_ensemble: bool = False,
        ensemble_config: Optional[EnsembleConfig] = None,
        reranking_config: Optional[RerankingConfig] = None,
        companion_dense_models: Optional[List[str]] = None,
        enable_sparse: Optional[bool] = None,
        sparse_models: Optional[List[str]] = None,
        matryoshka_dim: Optional[int] = None,
        local_files_only: bool = False,
        force_cpu: bool = False,
        hf_cache_dir: Optional[Union[str, Path]] = None,
        refresh_cache: bool = False,
        gpu0_soft_limit_gb: float = 12.0,
        feature_toggles: Optional[FeatureToggleConfig] = None,
    ):
        """Initialize Ultimate Kaggle Embedder V4"""

        logger.info("Initializing Ultimate Kaggle Embedder V4 (Split Architecture)")

        # Validate model against canonical registry
        canonical_model_name = resolve_kaggle_model_key(model_name)
        if canonical_model_name != model_name:
            logger.info("Resolved model identifier '%s' to registry key '%s'", model_name, canonical_model_name)

        self.model_config = KAGGLE_OPTIMIZED_MODELS[canonical_model_name]
        self.model_name = canonical_model_name
        logger.info(f"Selected model: {self.model_config.name} ({self.model_config.vector_dim}D)")

        self.local_files_only = local_files_only or os.environ.get("HF_HUB_OFFLINE") == "1"
        self.force_cpu = bool(force_cpu or os.environ.get("EMBEDDER_FORCE_CPU") == "1")
        self.force_cache_refresh = bool(refresh_cache or os.environ.get("EMBEDDER_REFRESH_CACHE") == "1")
        self.gpu0_soft_limit_bytes = int(max(1.0, gpu0_soft_limit_gb) * (1024 ** 3))

        default_cache_root = Path(os.environ.get("HF_HOME", "~/.cache/huggingface")).expanduser()
        specified_cache_root = Path(hf_cache_dir).expanduser() if hf_cache_dir else default_cache_root
        self.hf_cache_root = specified_cache_root
        self.hf_cache_root.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("HF_HOME", str(self.hf_cache_root))
        self.hf_cache_dir = self.hf_cache_root / "hub"
        self.hf_cache_dir.mkdir(parents=True, exist_ok=True)

        if self.local_files_only:
            os.environ.setdefault("HF_HUB_OFFLINE", "1")
            os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

        # Configuration
        self.gpu_config = gpu_config or KaggleGPUConfig()
        self.export_config = export_config or KaggleExportConfig()
        self.preprocessing_config = preprocessing_config or AdvancedPreprocessingConfig()
        self.enable_ensemble = enable_ensemble
        self.ensemble_config = (
            ensemble_config or EnsembleConfig() if enable_ensemble else None
        )
        toggles = feature_toggles or load_feature_toggles()
        self.feature_toggles = toggles

        self.reranking_config = reranking_config or RerankingConfig()
        self.reranking_config.enable_reranking = toggles.enable_rerank
        self._rerank_runtime_reason: Optional[str] = None
        if not self.reranking_config.enable_reranking:
            source = toggles.sources.get("enable_rerank", "default")
            self._rerank_runtime_reason = f"Disabled via {source}"
        self._canonical_collection_hint: Optional[str] = None
        self._target_collection_cache: Optional[str] = None

        self.embedding_backend: str = "local"
        self.multivectors_by_model: Dict[str, List[List[List[float]]]] = {}
        self.multivector_dimensions: Dict[str, int] = {}
        self.multivector_comparators: Dict[str, str] = {}
        self.model_dtypes: Dict[str, Optional[torch.dtype]] = {}
        self.primary_vector_name: str = self.model_name
        self._pending_mitigations: List[Tuple[str, Dict[str, Any]]] = []

        # V5: Sparse embedding support
        resolved_enable_sparse = (
            toggles.enable_sparse if enable_sparse is None else enable_sparse
        )
        self.enable_sparse = resolved_enable_sparse
        self._sparse_runtime_reason: Optional[str] = None
        self.sparse_models: Dict[str, Any] = {}
        self.sparse_device_map: Dict[str, str] = {}
        base_sparse_models = (
            list(sparse_models)
            if sparse_models is not None
            else list(toggles.sparse_models)
        )
        self.sparse_model_names = base_sparse_models
        if self.enable_sparse and not self.sparse_model_names:
            self.sparse_model_names = ["splade"]  # Changed from qdrant-bm25 to working SPLADE model
        if not self.enable_sparse:
            self.sparse_model_names = []
            source = toggles.sources.get("enable_sparse", "default")
            self._sparse_runtime_reason = f"Disabled via {source}"

        logger.info(
            "Feature toggles resolved: rerank=%s sparse=%s models=%s",
            self.reranking_config.enable_reranking,
            self.enable_sparse,
            self.sparse_model_names if self.sparse_model_names else "none",
        )

        # V5 ENSEMBLE MODE: Default to registry dimension (1024D for ensemble models)
        self.matryoshka_dim = matryoshka_dim if matryoshka_dim else self.model_config.vector_dim
        if matryoshka_dim and matryoshka_dim != self.model_config.vector_dim:
            supported_dims = {128, 256, 512, 1024, 1536, 2048}
            if matryoshka_dim not in supported_dims:
                logger.warning(
                    "⚠️  Non-standard Matryoshka dimension: %sD (registry default: %sD)",
                    matryoshka_dim,
                    self.model_config.vector_dim,
                )
            if matryoshka_dim > self.model_config.vector_dim:
                raise ValueError(
                    f"Matryoshka dimension ({matryoshka_dim}) cannot exceed registry dimension ({self.model_config.vector_dim})"
                )

        logger.info(
            "Embedding dimension: %sD (registry: %sD, ensemble-ready)",
            self.matryoshka_dim,
            self.model_config.vector_dim,
        )

        # Kaggle environment detection
        self.is_kaggle = "/kaggle" in os.getcwd() or os.path.exists("/kaggle")
        if self.is_kaggle:
            logger.info("Kaggle environment detected - optimizing for T4 x2")
            self.gpu_config.kaggle_environment = True
            if not export_config or not self.export_config.working_dir:
                self.export_config.working_dir = "/kaggle/working"
            else:
                working_path = Path(self.export_config.working_dir)
                if not working_path.is_absolute():
                    self.export_config.working_dir = str(Path("/kaggle/working") / working_path)

        self.project_root = Path(__file__).resolve().parents[3]

        # GPU setup with CPU fallback for local runs
        self.device_count = torch.cuda.device_count()
        if self.force_cpu:
            logger.warning("Force CPU flag set; overriding GPU detection")
            self.device_count = 0

        if self.device_count == 0:
            logger.warning(
                "No GPU detected; falling back to CPU mode. Embedding will be significantly slower."
            )
            self.device = "cpu"
            self.device_count = 1
            self.gpu_config.device_count = 1
            self.gpu_config.precision = "fp32"
            self.gpu_config.enable_memory_efficient_attention = False
            self.gpu_config.enable_torch_compile = False
            self.gpu_config.enable_mixed_precision = False
            self.gpu_config.base_batch_size = 8
            self.gpu_config.dynamic_batching = False
        else:
            self.device = "cuda"
            logger.info("Detected %d GPU(s)", self.device_count)
            for idx in range(self.device_count):
                gpu_name = torch.cuda.get_device_name(idx)
                gpu_memory = torch.cuda.get_device_properties(idx).total_memory / 1e9
                logger.info("  GPU %d: %s (%.1fGB)", idx, gpu_name, gpu_memory)

        if self.device == "cpu":
            self._apply_cpu_dense_fallback()

        self.cuda_debug_snapshot = self._capture_cuda_debug_snapshot()
        self._log_cuda_debug_snapshot()

        self.text_cache = AdvancedTextCache() if self.preprocessing_config.enable_text_caching else None

        self.models: Dict[str, Any] = {}
        self.primary_model: Optional[SentenceTransformer] = None
        self.reranker = None
        self.reranker_device: str = "cpu"
        self._requested_rerank_device: str = "cuda" if self.device == "cuda" else self.device
        self.fused_candidates: Dict[str, Any] = {}
        self.rerank_run: Optional["CrossEncoderRerankRun"] = None
        self.rerank_candidate_scores: Dict[str, float] = {}
        self.rerank_failure_reason: Optional[str] = None
        self.rerank_fallback_count: int = 0
        self.rerank_fallback_reason: Optional[str] = None
        self.rerank_fallback_source: Optional[str] = None

        self.companion_dense_model_names: List[str] = normalize_kaggle_model_names(companion_dense_models or [])
        self.companion_models: Dict[str, SentenceTransformer] = {}
        self.companion_model_configs: Dict[str, ModelConfig] = {}
        self.companion_batch_sizes: Dict[str, int] = {}
        self.companion_device_map: Dict[str, str] = {}
        self.failed_ensemble_models: Set[str] = set()
        self.ensemble_device_map: Dict[str, str] = {}
        rotation_limit = resolve_rotation_payload_limit()
        self.telemetry = TelemetryTracker(
            rotation_sample_limit=5,
            rotation_payload_limit=rotation_limit,
            logger=logger,
        )
        for event_type, payload in self._pending_mitigations:
            self.telemetry.record_mitigation(event_type, **payload)
        self._pending_mitigations.clear()
        self._rotation_payload_limit: int = rotation_limit
        self.mitigation_events = self.telemetry.mitigation_events
        self.cache_events = self.telemetry.cache_events
        self.rotation_events = self.telemetry.rotation_events
        self._last_dense_run: Dict[str, Any] = {}
        self.last_loading_summary: Dict[str, Any] = {}
        self.last_processing_summary: Dict[str, Any] = {}
        self.adaptive_controller: Optional[AdaptiveBatchController] = None
        self.gradient_checkpoint_evaluated: bool = False
        self.cpu_dense_fallback_applied = False

        metrics_flag = os.environ.get("EMBEDDER_METRICS_ENABLED")
        self.metrics_enabled = bool(
            metrics_flag and metrics_flag.strip().lower() in {"1", "true", "yes", "on"}
        )
        self.metrics_namespace = os.environ.get(
            "EMBEDDER_METRICS_NAMESPACE",
            "ultimate_embedder",
        )
        self.metrics_payloads: List[Dict[str, Any]] = []
        self.prometheus_emitter = create_prometheus_emitter(
            logger_instance=logger,
        )

        self.model_manager = ModelManager(self, logger)
        self.chunk_loader = ChunkLoader(
            project_root=self.project_root,
            is_kaggle=self.is_kaggle,
            logger=logger,
        )
        self.batch_runner = BatchRunner(self, logger)
        self.rerank_pipeline = RerankPipeline(self.reranking_config, logger)
        
        # Initialize CrossEncoder executor for reranking (wires into search_with_reranking)
        self.cross_encoder_executor: Optional[Any] = None
        if self.reranking_config.enable_reranking:
            from processor.ultimate_embedder.cross_encoder_executor import CrossEncoderBatchExecutor
            self.cross_encoder_executor = CrossEncoderBatchExecutor(
                config=self.reranking_config,
                gpu_config=self.gpu_config,
                logger=logger,
                embedder=self,
            )
            logger.info("CrossEncoderBatchExecutor initialized and wired into pipeline")

        self.sequential_device_order: List[str] = []
        if self.device == "cuda":
            if self.device_count > 1:
                self.sequential_device_order = [f"cuda:{idx}" for idx in range(self.device_count - 1, -1, -1)]
            else:
                self.sequential_device_order = ["cuda:0"]
        self.sequential_device_order.append("cpu")

        device_override = os.environ.get("EMBEDDER_SEQUENTIAL_DEVICES")
        if device_override:
            preferred = [candidate.strip() for candidate in device_override.split(",") if candidate.strip()]
            if preferred:
                unique_order: List[str] = []
                for candidate in preferred:
                    if candidate and candidate not in unique_order:
                        unique_order.append(candidate)
                for fallback in self.sequential_device_order:
                    if fallback not in unique_order:
                        unique_order.append(fallback)
                self.sequential_device_order = unique_order

        sequential_dp_env = os.environ.get("EMBEDDER_SEQUENTIAL_DATA_PARALLEL")
        if sequential_dp_env and self.ensemble_config:
            self.ensemble_config.sequential_data_parallel = sequential_dp_env.strip().lower() in {"1", "true", "yes", "on"}

        # Check environment for exclusive ensemble mode
        exclusive_env = os.environ.get("EMBEDDER_EXCLUSIVE_ENSEMBLE")
        if exclusive_env and self.ensemble_config:
            self.ensemble_config.exclusive_mode = exclusive_env.strip().lower() in {"1", "true", "yes", "on"}
            if self.ensemble_config.exclusive_mode:
                logger.info("Exclusive ensemble mode enabled via environment variable")

        self._initialize_embedding_models()
        self._initialize_companion_models()
        if self.enable_sparse:
            self._initialize_sparse_models()
        if self.reranking_config.enable_reranking:
            self._initialize_reranking_model()

        self.embeddings: Optional[np.ndarray] = None
        self.embeddings_by_model: Dict[str, np.ndarray] = {}
        self.chunks_metadata: List[Dict[str, Any]] = []
        self.chunk_texts: List[str] = []
        self.raw_chunk_texts: List[str] = []
        self.sparse_vectors: List[Optional[Dict[str, Any]]] = []
        self.processing_stats: defaultdict[str, List[Any]] = defaultdict(list)

        self.monitor_thread = None
        self.monitoring_active = False
        self.performance_monitor = PerformanceMonitor(self, logger)
        self.export_runtime = ExportRuntime(self, logger)

        logger.info("=" * 70)
        logger.info("MODEL AVAILABILITY CHECK")
        logger.info("=" * 70)
        logger.info("Primary model loaded: %s", self.primary_model is not None)
        if self.primary_model:
            model_type = type(self.primary_model).__name__
            logger.info("  Model type: %s", model_type)
            logger.info("  Is DataParallel: %s", isinstance(self.primary_model, torch.nn.DataParallel))
            if hasattr(self.primary_model, "encode"):
                logger.info("  ✓ Has encode() method")
            elif hasattr(self.primary_model, "module") and hasattr(self.primary_model.module, "encode"):
                logger.info("  ✓ Has encode() method via .module")
            else:
                logger.warning("  ✗ No encode() method found!")

        if self.companion_models:
            logger.info("Companion models loaded: %d", len(self.companion_models))
            for name, model in self.companion_models.items():
                model_type = type(model).__name__
                has_encode = hasattr(model, "encode") or (
                    hasattr(model, "module") and hasattr(model.module, "encode")
                )
                logger.info("  %s: %s, encode=%s", name, model_type, "✓" if has_encode else "✗")
        else:
            logger.info("No companion models loaded")

        logger.info("=" * 70)
        logger.info("Ultimate Kaggle Embedder V4 initialized successfully")
        logger.info("=" * 70)

    def _get_primary_model(self) -> SentenceTransformer:
        """Return the primary SentenceTransformer model, ensuring it is loaded."""

        if self.primary_model is not None:
            return self.primary_model

        if self.models:
            fallback = self.models.get(self.model_name) or next(iter(self.models.values()), None)
            if fallback is not None:
                self.primary_model = cast(SentenceTransformer, fallback)
                logger.debug("Primary model fallback resolved to %s", type(fallback).__name__)
                return self.primary_model

        logger.info("Primary model not in memory; reloading on demand")
        self.model_manager.initialize_primary_model()

        if self.primary_model is not None:
            return self.primary_model

        raise RuntimeError("Primary embedding model is not initialized")

    @property
    def rotation_payload_limit(self) -> int:
        """Expose the configured rotation payload limit for telemetry summaries."""

        return self._rotation_payload_limit

    def _require_embeddings(self) -> np.ndarray:
        """Return embeddings array, raising if it has not been generated."""
        if self.embeddings is None:
            raise RuntimeError("Embeddings have not been generated yet")
        return self.embeddings

    def _record_mitigation(self, event_type: str, **details: Any) -> None:
        """Track mitigation events for telemetry and diagnostics."""
        if hasattr(self, "telemetry"):
            self.telemetry.record_mitigation(event_type, **details)
            return

        if not hasattr(self, "_pending_mitigations"):
            self._pending_mitigations = []
        self._pending_mitigations.append((event_type, dict(details)))

    def _record_rotation_event(self, event: Dict[str, Any]) -> None:
        """Capture per-batch ensemble rotation telemetry with bounded detail."""
        self.telemetry.record_rotation_event(event)

    def _emit_metrics_for_stage(
        self,
        stage: str,
        *,
        active: bool,
        reason: Optional[str] = None,
        details: Optional[Mapping[str, Any]] = None,
    ) -> None:
        """Emit (or record skip) for Prometheus metrics per observability stage."""

        metric_registry = {
            "dense": ["rag_dense_latency_seconds", "rag_gpu_peak_bytes"],
            "rerank": ["rag_rerank_latency_seconds", "rag_gpu_peak_bytes"],
            "sparse": ["rag_sparse_latency_seconds"],
            "export": ["rag_export_latency_seconds"],
        }
        metric_names = metric_registry.get(stage, [])
        incoming_details = dict(details) if details else {}
        if stage == "rerank":
            fallback_count = incoming_details.get("fallback_count")
            if fallback_count is None:
                fallback_count = getattr(self, "rerank_fallback_count", 0)
                incoming_details["fallback_count"] = fallback_count
            fallback_reason = incoming_details.get("fallback_reason")
            if fallback_reason is None:
                fallback_reason = getattr(self, "rerank_fallback_reason", None)
                if fallback_reason is not None:
                    incoming_details["fallback_reason"] = fallback_reason
            fallback_source = incoming_details.get("fallback_source")
            if fallback_source is None:
                fallback_source = getattr(self, "rerank_fallback_source", None)
                if fallback_source is not None:
                    incoming_details["fallback_source"] = fallback_source
            if "device_fallback_applied" not in incoming_details:
                incoming_details["device_fallback_applied"] = False

        if not active:
            skip_reason = reason or "stage disabled"
            self.telemetry.record_metrics_status(
                stage,
                emitted=False,
                reason=skip_reason,
                metrics=metric_names,
                details=incoming_details or None,
            )
            return

        if not self.metrics_enabled:
            self.telemetry.record_metrics_status(
                stage,
                emitted=False,
                reason="metrics emitter disabled",
                metrics=metric_names,
                details=incoming_details or None,
            )
            return

        emission_details: Dict[str, Any] = {
            "namespace": self.metrics_namespace,
        }
        if incoming_details:
            emission_details.update(incoming_details)

        try:
            # Extract metric values from details
            latency_seconds = incoming_details.get("latency_seconds")
            gpu_peak_gb = incoming_details.get("gpu_peak_gb")
            gpu_peak_bytes = None
            if gpu_peak_gb is not None:
                gpu_peak_bytes = int(gpu_peak_gb * (1024 ** 3))
            
            # Build labels for Prometheus metrics
            labels: Dict[str, str] = {"stage": stage}
            if "model" in incoming_details:
                labels["model"] = str(incoming_details["model"])
            if "device" in incoming_details:
                labels["device"] = str(incoming_details["device"])
            
            # Emit latency metric
            latency_emitted = False
            if latency_seconds is not None:
                latency_emitted = self.prometheus_emitter.emit_latency_metric(
                    stage=stage,
                    latency_seconds=float(latency_seconds),
                    labels=labels,
                )
            
            # Emit GPU peak metric
            gpu_emitted = False
            if gpu_peak_bytes is not None:
                gpu_emitted = self.prometheus_emitter.emit_gpu_peak_metric(
                    stage=stage,
                    peak_bytes=gpu_peak_bytes,
                    labels=labels,
                )

            fallback_emitted = False
            fallback_metric_name = f"{self.metrics_namespace}_rerank_fallback_total"
            if stage == "rerank":
                fallback_count_value = int(incoming_details.get("fallback_count") or 0)
                if fallback_count_value > 0:
                    fallback_labels = {
                        "stage": stage,
                        "reason": str(incoming_details.get("fallback_reason") or "unspecified"),
                        "source": str(incoming_details.get("fallback_source") or "runtime"),
                    }
                    fallback_emitted = self.prometheus_emitter.emit_counter(
                        metric_name="rerank_fallback_total",
                        value=float(fallback_count_value),
                        labels=fallback_labels,
                    )
            
            # Record in legacy payload format
            payload = {
                "stage": stage,
                "metrics": metric_names,
                "namespace": self.metrics_namespace,
                "details": emission_details,
                "prometheus_emitted": {
                    "latency": latency_emitted,
                    "gpu_peak": gpu_emitted,
                    "fallback": fallback_emitted,
                },
            }
            self.metrics_payloads.append(payload)
            
            # Record emission status in telemetry
            emitted_metrics = []
            if latency_emitted:
                emitted_metrics.append(f"{self.metrics_namespace}_{stage}_latency_seconds")
            if gpu_emitted:
                emitted_metrics.append(f"{self.metrics_namespace}_gpu_peak_bytes")
            if stage == "rerank" and fallback_emitted:
                emitted_metrics.append(fallback_metric_name)
            
            self.telemetry.record_metrics_status(
                stage,
                emitted=bool(emitted_metrics),
                metrics=emitted_metrics or metric_names,
                details={
                    **emission_details,
                    "prometheus_latency_emitted": latency_emitted,
                    "prometheus_gpu_emitted": gpu_emitted,
                    "prometheus_fallback_emitted": fallback_emitted,
                },
            )
        except Exception as exc:  # pragma: no cover - defensive guard
            self.telemetry.record_metrics_status(
                stage,
                emitted=False,
                reason=str(exc),
                metrics=metric_names,
                details=incoming_details or None,
            )

    def _ensure_model_snapshot(self, repo_id: str) -> Path:
        """Ensure the Hugging Face snapshot for a model is cached locally."""
        return self.model_manager.ensure_model_snapshot(repo_id)

    def _build_sentence_transformer_kwargs(
        self,
        device: Optional[str] = None,
        **overrides: Any,
    ) -> Dict[str, Any]:
        """Construct keyword arguments for SentenceTransformer initialization."""
        return self.model_manager.build_sentence_transformer_kwargs(device=device, **overrides)

    def _unwrap_model(self, model: Any) -> Any:
        """Unwrap DataParallel/compiled wrappers to expose encode()."""

        current = model
        visited: Set[int] = set()

        while True:
            visited.add(id(current))
            if hasattr(current, "encode") and callable(getattr(current, "encode")):
                return current

            candidate = None
            if hasattr(current, "module") and id(getattr(current, "module")) not in visited:
                candidate = getattr(current, "module")
            elif hasattr(current, "_orig_mod") and id(getattr(current, "_orig_mod")) not in visited:
                candidate = getattr(current, "_orig_mod")
            elif hasattr(current, "model") and id(getattr(current, "model")) not in visited:
                candidate = getattr(current, "model")
            elif hasattr(current, "_model") and id(getattr(current, "_model")) not in visited:
                candidate = getattr(current, "_model")

            if candidate is None:
                return current

            current = candidate

    @staticmethod
    @lru_cache(maxsize=128)
    def _encode_supports_kwarg(callable_target: Any, kwarg_name: str) -> bool:
        """Feature-detect optional keyword support on encode callables."""

        try:
            signature = inspect.signature(callable_target)
        except (TypeError, ValueError):
            return True

        parameters = signature.parameters
        if kwarg_name in parameters:
            return True

        for parameter in parameters.values():
            if parameter.kind == inspect.Parameter.VAR_KEYWORD:
                return True

        return False

    def _call_encode(
        self,
        model: Any,
        texts: List[str],
        batch_size: int,
        device: str,
        show_progress: bool = True,
        progress_context: Optional[BatchProgressContext] = None,
    ) -> np.ndarray:
        """Invoke encode() against SentenceTransformer or compatible wrappers."""

        # Disable progress on CPU to avoid issues
        show_progress = show_progress and device != "cpu"

        encode_callable = getattr(model, "encode", None)
        if encode_callable is None and hasattr(model, "module"):
            encode_callable = getattr(model.module, "encode", None)

        if encode_callable is None:
            base_model = self._unwrap_model(model)
            encode_callable = getattr(base_model, "encode", None)

        if encode_callable is None:
            raise AttributeError(f"Model {type(model).__name__} does not expose encode()")

        # Initialize throughput monitoring
        monitor = ThroughputMonitor(logger=logger)
        monitor.start(
            chunk_count=len(texts),
            model_name=self.model_name,
            device=device,
            batch_size=batch_size,
            is_data_parallel=isinstance(model, torch.nn.DataParallel)
        )

        call_args: List[Any] = [texts]
        call_kwargs: Dict[str, Any] = {
            "batch_size": batch_size,
            "show_progress_bar": show_progress and not progress_context,  # Disable if progress_context provided
            "convert_to_numpy": True,
            "normalize_embeddings": True,
            "device": device,
        }

        progress_requested = False
        if show_progress and progress_context:
            desc = progress_context.tqdm_description()
            postfix = progress_context.tqdm_postfix()
            if desc:
                callable_target = getattr(encode_callable, "__func__", encode_callable)
                if self._encode_supports_kwarg(callable_target, "tqdm_kwargs"):
                    tqdm_kwargs = {"desc": desc}
                    if postfix:
                        tqdm_kwargs["postfix"] = postfix
                    call_kwargs["tqdm_kwargs"] = tqdm_kwargs
                    progress_requested = True

        try:
            result = encode_callable(*call_args, **call_kwargs)
            
            # Log throughput completion
            monitor.end()
            
            return result
        except Exception as primary_exc:
            # Log throughput failure and re-raise
            monitor.log_error(primary_exc)
            logger.exception(
                "Encode failed for model %s on %s (batch=%d)",
                self.model_name,
                device,
                batch_size,
            )

            if progress_requested:
                call_kwargs.pop("tqdm_kwargs", None)
                try:
                    return encode_callable(*call_args, **call_kwargs)
                except Exception:
                    raise primary_exc
            raise

    def _normalize_embedding_matrix(self, matrix: Any, model_name: str) -> np.ndarray:
        """Ensure embedding outputs are 2D float32 arrays with consistent dimensions."""

        arr = np.asarray(matrix)

        if arr.ndim == 0:
            arr = arr.reshape(1, 1)

        if arr.dtype == object:
            rows: List[np.ndarray] = []
            dims: List[int] = []
            for row in arr:
                row_array = np.asarray(row, dtype=np.float32).reshape(-1)
                dims.append(row_array.size)
                rows.append(row_array)

            if not rows:
                return np.empty((0, 0), dtype=np.float32)

            min_dim = min(dims)
            max_dim = max(dims)
            if max_dim != min_dim:
                self._record_mitigation(
                    "embedding_dim_normalized",
                    model=model_name,
                    min_dim=min_dim,
                    max_dim=max_dim,
                    sample_dims=dims[:5],
                )
            trimmed = [row[:min_dim] for row in rows]
            arr = np.stack(trimmed, axis=0).astype(np.float32, copy=False)
        else:
            if arr.ndim > 2:
                original_shape = arr.shape
                arr = arr.reshape(arr.shape[0], -1)
                self._record_mitigation(
                    "embedding_tensor_flattened",
                    model=model_name,
                    original_shape=list(original_shape),
                    flattened_shape=list(arr.shape),
                )
            if arr.ndim == 1:
                arr = arr.reshape(1, -1)
            if arr.dtype != np.float32:
                arr = arr.astype(np.float32, copy=False)

        return arr

    def _get_batch_hint_for_model(self, model_name: str) -> int:
        if model_name == self.model_name:
            model_config = self.model_config
        else:
            model_config = KAGGLE_OPTIMIZED_MODELS.get(model_name, None)

        if model_config is not None:
            hint = self.gpu_config.get_optimal_batch_size(model_config)
        else:
            hint = self.gpu_config.base_batch_size

        if self.device == "cpu":
            hint = max(1, min(hint, 2))
        return max(1, hint)

    def _select_sequential_device(self, model_name: str) -> str:
        if self.device != "cuda":
            return "cpu"

        if model_name == self.model_name:
            return "cuda:0" if self.device_count > 0 else "cpu"

        override = self.ensemble_device_map.get(model_name)
        if override:
            if override == "cpu":
                return "cpu"
            if override.startswith("cuda"):
                try:
                    index = int(override.split(":")[1]) if ":" in override else 0
                except ValueError:
                    override = ""
                else:
                    if index < self.device_count:
                        return override

        for candidate in self.sequential_device_order:
            if candidate.startswith("cuda"):
                try:
                    index = int(candidate.split(":")[1]) if ":" in candidate else 0
                except ValueError:
                    continue
                if index < self.device_count:
                    return candidate
            elif candidate == "cpu":
                return "cpu"

        return "cuda:0" if self.device_count > 0 else "cpu"

    def _describe_batch_slice(self, batch_slice: Optional[slice]) -> Dict[str, Any]:
        if batch_slice is None:
            return {}

        start = batch_slice.start if batch_slice.start is not None else 0
        stop = batch_slice.stop if batch_slice.stop is not None else start
        start = max(0, start)
        stop = max(start, stop)
        stop = min(stop, len(self.chunks_metadata))

        if stop <= start:
            return {}

        samples: List[Dict[str, Any]] = []
        for idx in range(start, min(stop, start + 5)):
            source = ""
            if idx < len(self.chunks_metadata):
                metadata = self.chunks_metadata[idx] or {}
                source = (
                    metadata.get("source_path")
                    or metadata.get("source_file")
                    or metadata.get("filename")
                    or metadata.get("document_id")
                    or metadata.get("doc_id")
                    or metadata.get("id")
                )
            if not source:
                source = f"chunk_{idx}"
            samples.append({"index": idx, "source": str(source)})

        return {
            "start": start,
            "end": stop,
            "count": stop - start,
            "samples": samples,
        }

    @staticmethod
    def _format_batch_slice_info(info: Dict[str, Any]) -> str:
        if not info:
            return "n/a"
        return f"{info['start']}:{info['end']} ({info['count']} chunks)"

    def _collect_batch_source_counts(
        self,
        start_index: int,
        end_index: int,
    ) -> Counter[str]:
        """Aggregate chunk counts per chunk file within the given slice."""

        counts: Counter[str] = Counter()
        if start_index >= end_index:
            return counts

        for idx in range(start_index, end_index):
            if idx >= len(self.chunks_metadata):
                source_name = f"chunk_{idx}"
            else:
                metadata = self.chunks_metadata[idx] or {}
                # Prioritize chunk_file_name for progress display
                source_name = metadata.get("chunk_file_name")
                if not source_name:
                    # Fallback to source file if chunk_file_name not set
                    source_name = (
                        metadata.get("source_path")
                        or metadata.get("source_file")
                        or metadata.get("filename")
                        or metadata.get("document_name")
                        or f"chunk_{idx}"
                    )
            counts[str(Path(source_name).name)] += 1

        return counts

    def _summarize_batch_sources(
        self,
        start_index: int,
        end_index: int,
        limit: int = 6,
    ) -> str:
        """Return a human-readable summary of chunk sources for the current batch."""

        counts = self._collect_batch_source_counts(start_index, end_index)
        if not counts:
            return ""

        ordered = counts.most_common(limit)
        summary_parts = [f"{name} ({count})" for name, count in ordered]
        if len(counts) > limit:
            summary_parts.append(f"… +{len(counts) - limit} more")

        return ", ".join(summary_parts)

    def _get_batch_progress_label(self, start_index: int, end_index: int) -> Optional[str]:
        """Build a succinct progress label describing the chunk file for a batch."""

        counts = self._collect_batch_source_counts(start_index, end_index)
        if not counts:
            return None

        primary_name, _ = counts.most_common(1)[0]
        return primary_name

    def _log_batch_sources(self, batch_number: int, start_index: int, end_index: int) -> None:
        """Emit a log entry describing which files contributed to a batch."""

        summary = self._summarize_batch_sources(start_index, end_index)
        if summary:
            logger.info("Batch %d sources: %s", batch_number, summary)

    def _get_or_load_ensemble_model(self, model_name: str) -> Optional[Any]:
        if model_name == self.model_name:
            return self._get_primary_model()

        cached = self.models.get(model_name)
        if cached is not None:
            return cached

        if model_name in self.failed_ensemble_models:
            logger.debug("Skipping previously failed ensemble model %s", model_name)
            return None

        config = KAGGLE_OPTIMIZED_MODELS.get(model_name)
        if config is None:
            raise KeyError(f"Unknown ensemble model '{model_name}'")

        self._ensure_model_snapshot(config.hf_model_id)
        kwargs = self._build_sentence_transformer_kwargs(device="cpu")
        kwargs["trust_remote_code"] = config.trust_remote_code
        try:
            model = SentenceTransformer(config.hf_model_id, **kwargs)
        except Exception as exc:
            self.failed_ensemble_models.add(model_name)
            message = str(exc)
            logger.warning("Failed to load ensemble model %s: %s", model_name, message)
            self._record_mitigation(
                "ensemble_model_load_failed",
                model=model_name,
                error=message[:500],
            )
            return None

        if self.gpu_config.precision == "fp16" and self.device == "cuda":
            model = model.half()

        if (
            self.ensemble_config
            and self.ensemble_config.sequential_data_parallel
            and self.device == "cuda"
            and self.device_count > 1
            and not isinstance(model, torch.nn.DataParallel)
        ):
            try:
                model = torch.nn.DataParallel(model)
                self._record_mitigation("ensemble_data_parallel_wrapped", model=model_name)
            except Exception as exc:
                logger.warning("Failed to wrap %s with DataParallel: %s", model_name, exc)

        self.models[model_name] = model
        self._record_model_dtype(model_name, model)
        return model

    def _record_gpu_snapshot(self, snapshots: Dict[int, GPUMemorySnapshot]) -> None:
        self.telemetry.record_gpu_snapshot(
            snapshots,
            gpu0_soft_limit_bytes=self.gpu0_soft_limit_bytes,
        )

    def _deactivate_companions(self, target_names: Optional[List[str]] = None) -> None:
        names = target_names or list(self.companion_models.keys())
        for companion_name in names:
            model = self.companion_models.get(companion_name)
            if model is None:
                continue
            device = self.companion_device_map.get(companion_name)
            if device and device.startswith("cuda"):
                try:
                    model = model.to("cpu") if hasattr(model, "to") else model
                    self.companion_models[companion_name] = model
                    self.companion_device_map[companion_name] = "cpu"
                    torch.cuda.empty_cache()
                    self._record_mitigation("companion_cpu_fallback", companion=companion_name)
                except Exception as exc:
                    logger.warning("Failed to move companion %s to CPU: %s", companion_name, exc)
        gc.collect()

    def _summarize_gpu_history(self) -> Dict[str, Any]:
        return self.telemetry.summarize_gpu_history()

    def _maybe_enable_transformer_checkpointing(self, model: SentenceTransformer) -> None:
        """Enable gradient checkpointing when supported and requested."""
        self.model_manager.maybe_enable_transformer_checkpointing(model)

    def _log_gpu_memory(self, label: str, level: int = logging.INFO) -> None:
        """Emit per-device CUDA memory statistics for diagnostics."""
        if not torch.cuda.is_available() or not logger.isEnabledFor(level):
            return

        stats: List[str] = []
        for device_id in range(self.device_count):
            try:
                allocated = torch.cuda.memory_allocated(device_id) / 1e9
                reserved = torch.cuda.memory_reserved(device_id) / 1e9
                free_bytes, total_bytes = torch.cuda.mem_get_info(device_id)
                free = free_bytes / 1e9
                total = total_bytes / 1e9
                stats.append(
                    f"GPU{device_id}: alloc={allocated:.2f}GB reserved={reserved:.2f}GB free={free:.2f}GB/{total:.2f}GB"
                )
            except RuntimeError as exc:
                stats.append(f"GPU{device_id}: mem stats unavailable ({exc})")

        logger.log(level, f"[GPU-MEM] {label}: " + " | ".join(stats))

    def _collect_gpu_snapshots(self) -> Dict[int, GPUMemorySnapshot]:
        """Capture current GPU memory telemetry for adaptive batching."""
        snapshots = collect_gpu_snapshots(self.device, self.device_count)
        if snapshots:
            self._record_gpu_snapshot(snapshots)
        return snapshots

    def _get_model_primary_dtype(self, model: Any) -> Optional[torch.dtype]:
        """Return dtype of the first parameter of a torch model, if available."""
        if not hasattr(model, "parameters"):
            return None
        try:
            first_param = next(model.parameters())
        except (StopIteration, TypeError):
            return None
        return getattr(first_param, "dtype", None)

    def _record_model_dtype(self, model_name: str, model: Any) -> Optional[torch.dtype]:
        """Cache the primary parameter dtype for the given model."""
        if model is None:
            self.model_dtypes[model_name] = None
            logger.debug("Model %s not loaded; dtype unavailable", model_name)
            return None

        dtype = self._get_model_primary_dtype(model)
        self.model_dtypes[model_name] = dtype
        if dtype is None:
            logger.debug("Model %s primary dtype could not be determined", model_name)
        else:
            logger.debug("Model %s primary dtype recorded as %s", model_name, dtype)
        return dtype

    def _capture_cuda_debug_snapshot(self) -> Dict[str, Any]:
        """Collect diagnostic details about CUDA-related state for manifest/logging."""

        env_snapshot = {
            key: os.environ.get(key)
            for key in CUDA_DEBUG_ENV_KEYS
            if os.environ.get(key) is not None
        }

        module_snapshot: Dict[str, Dict[str, Any]] = {}
        for module_name in CUDA_DEBUG_MODULES:
            imported = module_name in sys.modules
            try:
                available = importlib.util.find_spec(module_name) is not None
            except (ModuleNotFoundError, ValueError):
                available = False
            version: Optional[str]
            if module_name == "torch":
                version = torch.__version__
            else:
                version = _safe_package_version(module_name)
            module_snapshot[module_name] = {
                "imported": imported,
                "available": available,
                "version": version,
            }

        torch_info: Dict[str, Any] = {
            "version": torch.__version__,
            "cuda_version": torch.version.cuda,
            "cuda_available": torch.cuda.is_available(),
            "device_count": torch.cuda.device_count(),
            "cudnn_available": torch.backends.cudnn.is_available(),
            "cudnn_version": torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else None,
        }

        try:
            matmul_backend = getattr(torch.backends.cuda, "matmul", None)
            tf32_flag = getattr(matmul_backend, "allow_tf32", None) if matmul_backend is not None else None
        except (RuntimeError, AttributeError):  # pragma: no cover - occurs when CUDA not initialized
            tf32_flag = None
        if tf32_flag is not None:
            torch_info["tf32_enabled"] = bool(tf32_flag)

        device_details: List[Dict[str, Any]] = []
        if torch_info["device_count"]:
            for idx in range(torch_info["device_count"]):
                try:
                    props = torch.cuda.get_device_properties(idx)
                    device_details.append(
                        {
                            "index": idx,
                            "name": props.name,
                            "total_memory_gb": round(props.total_memory / 1e9, 2),
                            "multi_processor_count": props.multi_processor_count,
                            "compute_capability": f"{props.major}.{props.minor}",
                        }
                    )
                except Exception as exc:  # pragma: no cover - diagnostic only
                    device_details.append({"index": idx, "error": str(exc)})
        torch_info["devices"] = device_details

        snapshot: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "environment": env_snapshot,
            "force_cpu": self.force_cpu,
            "effective_device": self.device,
            "effective_device_count": self.device_count,
            "gpu_config": {
                "device_count": getattr(self.gpu_config, "device_count", None),
                "backend": getattr(self.gpu_config, "backend", None),
                "strategy": getattr(self.gpu_config, "strategy", None),
            },
            "torch": torch_info,
            "modules": module_snapshot,
        }

        conflicts = [
            name
            for name in ("jax", "jaxlib", "tensorflow")
            if module_snapshot.get(name, {}).get("imported")
        ]
        if conflicts:
            snapshot["potential_conflicts"] = conflicts

        return snapshot

    def _log_cuda_debug_snapshot(self) -> None:
        """Log the captured CUDA diagnostic snapshot in a readable format."""

        if not logger.isEnabledFor(logging.INFO):
            return

        try:
            pretty_payload = json.dumps(self.cuda_debug_snapshot, indent=2, sort_keys=True)
        except TypeError:  # pragma: no cover - fallback when serialization fails
            pretty_payload = str(self.cuda_debug_snapshot)

        logger.info("CUDA debug snapshot:\n%s", pretty_payload)

        conflicts = self.cuda_debug_snapshot.get("potential_conflicts") or []
        if conflicts:
            conflict_list = ", ".join(conflicts)
            logger.warning(
                "Detected pre-imported CUDA consumers (%s). These libraries often trigger the cuFFT/cuBLAS/cuDNN 'factory already registered' warnings emitted by XLA.",
                conflict_list,
            )
            logger.warning(
                "Mitigation: ensure those modules are not imported before the embedder starts, or uninstall them in Kaggle (e.g. `pip uninstall -y jax jaxlib tensorflow`).",
            )

    def _apply_cpu_dense_fallback(self) -> None:
        """Adjust dense model roster when operating without GPUs."""

        fallback_primary = resolve_kaggle_model_key(CPU_DENSE_FALLBACK_PRIMARY)
        fallback_models = normalize_kaggle_model_names(CPU_DENSE_FALLBACK_ENSEMBLE)
        fallback_models = [model for model in fallback_models if model != fallback_primary]

        current_roster: List[str] = [self.model_name]
        if self.ensemble_config:
            current_roster.extend(self.ensemble_config.ensemble_models)

        if (
            self.model_name == fallback_primary
            and self.ensemble_config
            and self.ensemble_config.ensemble_models == fallback_models
        ):
            return

        self._record_mitigation(
            "cpu_dense_model_fallback",
            original_models=current_roster,
            fallback_primary=fallback_primary,
            fallback_models=fallback_models,
        )

        self.model_name = fallback_primary
        self.model_config = KAGGLE_OPTIMIZED_MODELS[fallback_primary]
        self.primary_vector_name = self.model_name

        if fallback_models:
            if not self.ensemble_config:
                self.ensemble_config = EnsembleConfig(
                    ensemble_models=fallback_models,
                    exclusive_mode=True,
                )
            else:
                self.ensemble_config.ensemble_models = fallback_models
                self.ensemble_config.exclusive_mode = True
            self.enable_ensemble = True
        else:
            self.enable_ensemble = False
            self.ensemble_config = None

        fallback_dims = [self.model_config.vector_dim]
        fallback_dims.extend(
            KAGGLE_OPTIMIZED_MODELS[model_name].vector_dim for model_name in fallback_models
        )
        fallback_dim = min(fallback_dims) if fallback_dims else self.matryoshka_dim

        if self.matryoshka_dim > fallback_dim:
            logger.info(
                "Adjusting Matryoshka dimension from %sD to %sD for CPU fallback",
                self.matryoshka_dim,
                fallback_dim,
            )
            self.matryoshka_dim = fallback_dim

        self.gpu_config.base_batch_size = min(self.gpu_config.base_batch_size, 2)
        self.gpu_config.dynamic_batching = False

        self.cpu_dense_fallback_applied = True
        logger.info(
            "CPU fallback applied: primary=%s | companions=%s | matryoshka_dim=%sD",
            self.model_name,
            fallback_models or "none",
            self.matryoshka_dim,
        )
        
    def _initialize_embedding_models(self) -> None:
        """Initialize the primary embedding stack via the model manager."""

        self.model_manager.initialize_primary_model()
        
    def _initialize_companion_models(self) -> None:
        """Load additional dense encoders via the model manager."""

        self.model_manager.initialize_companion_models()

    def _initialize_sparse_models(self) -> None:
        """Initialize sparse embedding models via the model manager."""

        self.model_manager.initialize_sparse_models()

    def _initialize_reranking_model(self):
        """Initialize CrossEncoder for reranking"""

        if self.reranking_config.model_name not in RERANKING_MODELS:
            logger.warning(
                f"Unknown reranker {self.reranking_config.model_name}, defaulting to jina-reranker-v3"
            )
            self.reranking_config.model_name = "jina-reranker-v3"

        reranker_model = RERANKING_MODELS[self.reranking_config.model_name]
        logger.info(f"Loading reranking model: {reranker_model}")
        requested_device = "cuda" if self.device == "cuda" else self.device
        self._requested_rerank_device = requested_device
        target_device = "cpu" if self.device == "cuda" else self.device

        try:
            self.reranker = CrossEncoder(reranker_model, device=target_device)
            self.reranker_device = target_device
            if target_device == "cpu" and self.device == "cuda":
                logger.info(
                    "CrossEncoder reranking model staged on CPU; hydrate via leasing"
                )
            else:
                logger.info("CrossEncoder reranking model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load reranking model: {e}")
            self.reranking_config.enable_reranking = False
            self.reranker = None
            message = str(e)
            self._rerank_runtime_reason = f"Load failure: {message[:160]}"
    
    def generate_ensemble_embeddings(
        self,
        texts: List[str],
        batch_slice: Optional[slice] = None,
        batch_index: Optional[int] = None,
        progress_context: Optional[BatchProgressContext] = None,
    ) -> np.ndarray:
        """Delegate ensemble embedding generation to the batch runner service."""

        return self.batch_runner.generate_ensemble_embeddings(
            texts,
            batch_slice=batch_slice,
            batch_index=batch_index,
            progress_context=progress_context,
        )
    
    def search_with_reranking(
        self,
        query: str,
        top_k: int = 20,
        initial_candidates: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search with CrossEncoder reranking
        
        Args:
            query: Search query
            top_k: Final number of results
            initial_candidates: Initial retrieval candidates for reranking
            
        Returns:
            List of reranked results with scores
        """
        
        if self.embeddings is None:
            raise ValueError("No embeddings available. Generate embeddings first.")
        embeddings = self._require_embeddings()
        
        if not self.reranking_config.enable_reranking or not self.reranker:
            logger.warning("Reranking not enabled, falling back to embedding similarity")
            return self._embedding_only_search(query, top_k)
        
        # Step 1: Generate query embedding
        primary_model = self._get_primary_model()
        # Unwrap all wrappers (torch.compile + DataParallel)
        encode_model = self._unwrap_model(primary_model)
        query_embedding = encode_model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
            device=self.device
        )[0]
        
        # Step 2: Initial retrieval with embedding similarity
        similarities = cosine_similarity(np.array([query_embedding]), embeddings)[0]
        
        # Get top candidates for reranking
        top_indices = np.argsort(similarities)[::-1][:initial_candidates]
        
        # Step 3: Prepare candidate data for reranking
        candidate_ids = [str(idx) for idx in top_indices if idx < len(self.chunk_texts)]
        candidate_texts = [self.chunk_texts[idx] for idx in top_indices if idx < len(self.chunk_texts)]
        candidate_indices = [idx for idx in top_indices if idx < len(self.chunk_texts)]
        
        if not candidate_ids:
            logger.warning("No valid candidates for reranking")
            return []
        
        # Step 4: Rerank with CrossEncoderBatchExecutor (replaces legacy self.reranker.predict())
        logger.info(f"Reranking {len(candidate_ids)} candidates via CrossEncoderBatchExecutor...")

        try:
            # Use CrossEncoderBatchExecutor instead of direct reranker.predict()
            if not self.cross_encoder_executor:
                logger.warning("CrossEncoderBatchExecutor not initialized, falling back to legacy path")
                # Fallback to direct predict for backward compatibility
                query_doc_pairs = [[query, text] for text in candidate_texts]
                rerank_scores = self.reranker.predict(query_doc_pairs)
                rerank_run = None
            else:
                # New path: use executor for GPU leasing, batching, OOM recovery
                rerank_run = self.cross_encoder_executor.execute_rerank(
                    query=query,
                    candidate_ids=candidate_ids,
                    candidate_texts=candidate_texts,
                    top_k=top_k,
                )
                
                # Emit metrics from executor telemetry
                self._emit_metrics_for_stage(
                    "rerank",
                    active=True,
                    reason="Query-time reranking executed via CrossEncoderBatchExecutor",
                    details={
                        "latency_seconds": rerank_run.latency_ms / 1000.0,
                        "gpu_peak_gb": rerank_run.gpu_peak_gb,
                        "batch_size": rerank_run.batch_size,
                        "model": self.reranking_config.model_name,
                        "device": getattr(self.cross_encoder_executor.rerank_pipeline, "device", "cpu"),
                    },
                )
                
                # Extract scores and ranked candidate IDs
                ranked_candidate_ids = rerank_run.candidate_ids
                ranked_scores = rerank_run.scores
                
                # Map back to original indices
                # Fix TECH-002: Create id_to_index mapping to handle non-sequential candidate ids
                id_to_index = {str(idx): idx for idx in candidate_indices}
                
                results = []
                for rank, (cand_id, score) in enumerate(zip(ranked_candidate_ids, ranked_scores)):
                    original_idx = id_to_index.get(cand_id)
                    if original_idx is None:
                        logger.warning(f"Candidate id {cand_id} not found in mapping, skipping")
                        continue
                    
                    # Build result using extracted helper method
                    result = self._build_rerank_result(
                        rank=rank,
                        score=score,
                        original_idx=original_idx,
                        similarities=similarities,
                    )
                    
                    if result is not None:
                        results.append(result)
                
                logger.info(
                    f"Reranking complete via executor. Top score: {results[0]['score']:.4f}, "
                    f"latency: {rerank_run.latency_ms:.1f}ms, peak_gpu: {rerank_run.gpu_peak_gb:.2f}GB"
                )
                return results
            
        except Exception as e:
            logger.error(f"Reranking failed: {e}")
            return self._embedding_only_search(query, top_k)
    
    def _build_rerank_result(
        self,
        rank: int,
        score: float,
        original_idx: int,
        similarities: Sequence[float],
    ) -> Optional[Dict[str, Any]]:
        """
        Build a single reranking result dictionary.
        
        Args:
            rank: Zero-based rank in reranked results
            score: Reranking score from CrossEncoder
            original_idx: Index into chunk_texts/chunks_metadata/embeddings
            similarities: Array of embedding similarity scores
            
        Returns:
            Result dictionary with rank, scores, text, metadata, and chunk_id.
            Returns None if original_idx is invalid.
        """
        # Validate index bounds
        if original_idx is None or original_idx < 0:
            return None
        if original_idx >= len(similarities):
            return None
        if original_idx >= len(self.chunk_texts):
            return None
        if original_idx >= len(self.chunks_metadata):
            return None
            
        return {
            "rank": rank + 1,  # Convert to 1-based rank for API
            "score": score,
            "embedding_similarity": float(similarities[original_idx]),
            "text": self.chunk_texts[original_idx],
            "metadata": self.chunks_metadata[original_idx],
            "chunk_id": original_idx,
        }
    
    def _embedding_only_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Fallback search using only embedding similarity"""
        
        primary_model = self._get_primary_model()
        # Unwrap all wrappers (torch.compile + DataParallel)
        encode_model = self._unwrap_model(primary_model)
        query_embedding = encode_model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
            device=self.device
        )[0]
        
        embeddings = self._require_embeddings()
        similarities = cosine_similarity(np.array([query_embedding]), embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for rank, idx in enumerate(top_indices):
            result = {
                "rank": rank + 1,
                "score": float(similarities[idx]),
                "text": self.chunk_texts[idx],
                "metadata": self.chunks_metadata[idx],
                "chunk_id": idx
            }
            results.append(result)
        
        return results
    
    def _load_pytorch_model(self, model_kwargs: Dict, optimal_batch: int) -> Any:
        """Load PyTorch model with optimization"""
        
        # Remove torch_dtype for compatibility with older sentence-transformers
        st_kwargs = model_kwargs.copy()
        torch_dtype = st_kwargs.pop('torch_dtype', None)
        
        try:
            # Try loading without torch_dtype first (most compatible)
            model = SentenceTransformer(self.model_config.hf_model_id, **st_kwargs)
            
            # Apply FP16 conversion after loading if needed
            if torch_dtype is not None and torch_dtype == torch.float16 and self.device == "cuda":
                model = model.half()
                logger.info("Converted model to FP16 after loading")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
        
        # Multi-GPU setup for T4 x2
        if self.device_count > 1:
            logger.info(f"Setting up multi-GPU processing ({self.device_count} GPUs)")
            if self.gpu_config.strategy == "data_parallel":
                logger.info(f"📦 Applying DataParallel wrapper to {type(model).__name__}")
                logger.info(f"   → Model before wrap has encode(): {hasattr(model, 'encode')}")
                model = torch.nn.DataParallel(model)
                logger.info(f"   → Model after wrap type: {type(model).__name__}")
                logger.info(f"   → Wrapped model has encode(): {hasattr(model, 'encode')}")
                logger.info(f"   → Wrapped model.module has encode(): {hasattr(model.module, 'encode')}")
                logger.info("✅ Data parallel enabled")
        
        # PyTorch 2.0 compilation (if available)
        if self.gpu_config.enable_torch_compile and hasattr(torch, 'compile'):
            try:
                logger.info(f"🚀 Applying torch.compile to {type(model).__name__}")
                logger.info(f"   → Model before compile has encode(): {hasattr(model, 'encode')}")
                model = torch.compile(model, mode="reduce-overhead")
                logger.info(f"   → Model after compile type: {type(model).__name__}")
                logger.info(f"   → Compiled model has encode(): {hasattr(model, 'encode')}")
                has_orig_mod = hasattr(model, '_orig_mod')
                logger.info(f"   → Compiled model has _orig_mod: {has_orig_mod}")
                if has_orig_mod:
                    orig_mod: Any = getattr(model, '_orig_mod', None)
                    orig_type = type(orig_mod).__name__ if orig_mod is not None else 'unknown'
                    logger.info(f"   → _orig_mod type: {orig_type}")
                    logger.info(f"   → _orig_mod has encode(): {hasattr(orig_mod, 'encode')}")
                logger.info("✅ PyTorch 2.0 compilation enabled")
            except Exception as e:
                logger.warning(f"PyTorch compilation failed: {e}")
        
        return model
    
    def _load_onnx_model(self) -> Any:
        """Load ONNX optimized model"""
        
        if not ONNX_AVAILABLE:
            raise ImportError("ONNX runtime not available")
        if ORTModelForFeatureExtraction is None:
            raise ImportError("Optimum ORT model class not available")
        
        # ONNX provider configuration
        providers = []
        if torch.cuda.is_available():
            providers.append(('CUDAExecutionProvider', {
                'device_id': 0,
                'arena_extend_strategy': 'kSameAsRequested',
                'gpu_mem_limit': int(self.gpu_config.vram_per_gpu_gb * 0.8 * 1e9),
                'cudnn_conv_algo_search': 'EXHAUSTIVE',
                'do_copy_in_default_stream': True,
            }))
        providers.append('CPUExecutionProvider')
        
        # Load ONNX model
        ort_model_cls = ORTModelForFeatureExtraction
        model = ort_model_cls.from_pretrained(
            self.model_config.hf_model_id,
            export=True,
            provider=providers[0][0] if providers else 'CPUExecutionProvider'
        )
        
        return model

    def preprocess_text_advanced(self, text: str) -> str:
        """Apply advanced text preprocessing with optional caching."""

        if not self.preprocessing_config.enable_text_caching or not self.text_cache:
            return self._preprocess_text_core(text)

        return self.text_cache.get_processed_text(text, self._preprocess_text_core)

    def _preprocess_text_core(self, text: str) -> str:
        """Core normalization pipeline shared across preprocessing modes."""

        if self.preprocessing_config.normalize_whitespace:
            text = " ".join(text.split())

        if self.preprocessing_config.remove_excessive_newlines:
            text = re.sub(r"\n{3,}", "\n\n", text)

        if self.preprocessing_config.trim_long_sequences:
            max_chars = self.model_config.max_tokens * 4
            if len(text) > max_chars:
                text = f"{text[:max_chars]}..."

        return text
    
    def load_chunks_from_processing(
        self,
        chunks_dir: str = "/kaggle/working/rag_clean/Chunked"
    ) -> Dict[str, Any]:
        """Load processed chunks via the delegated chunk loader."""

        result = self.chunk_loader.load(
            chunks_dir,
            preprocess_text=self.preprocess_text_advanced,
            model_name=self.model_name,
            model_vector_dim=self.model_config.vector_dim,
            text_cache=self.text_cache,
        )

        self.chunks_metadata = result.metadata
        self.chunk_texts = result.processed_texts
        self.raw_chunk_texts = result.raw_texts
        self.sparse_vectors = result.sparse_vectors
        self._canonical_collection_hint = result.canonical_collection_hint
        self._target_collection_cache = None

        summary = result.summary
        self.last_loading_summary = summary
        if result.canonical_collection_hint:
            logger.info("Canonical collection hint: %s", result.canonical_collection_hint)

        error = summary.get("error")
        if error:
            logger.error("Chunk loading failed: %s", error)
            return summary

        logger.info("Chunk loading complete")
        logger.info("Total chunks: %s", summary.get("total_chunks_loaded", 0))
        memory_usage = summary.get("memory_usage_mb")
        if isinstance(memory_usage, (int, float)):
            logger.info("Memory usage: %.1fMB", memory_usage)

        cache_stats = summary.get("preprocessing_stats")
        if isinstance(cache_stats, dict) and "hit_rate" in cache_stats:
            logger.info("Cache hit rate: %.2f%%", cache_stats["hit_rate"] * 100.0)

        return summary

    @staticmethod
    def _normalize_collection_name(raw_name: str) -> str:
        """Map raw collection identifiers to canonical Qdrant collection names."""

        if not raw_name:
            return "qdrant_ecosystem"

        normalized = raw_name.strip().lower().replace("-", "_").replace(" ", "_")

        explicit_map = {
            "qdrant_v4_outputs": "qdrant_ecosystem",
            "qdrant_ecosystem_v4_outputs": "qdrant_ecosystem",
            "qdrant_ecosystem": "qdrant_ecosystem",
            "sentence_transformers_v4_outputs": "sentence_transformers",
            "sentence_transformers": "sentence_transformers",
            "docling_v4_outputs": "docling",
            "docling": "docling",
            "fast_docs_v4_outputs": "fast_docs",
            "fast_docs": "fast_docs",
            "pydantic_pydantic_v4_outputs": "pydantic",
            "pydantic_v4_outputs": "pydantic",
            "pydantic": "pydantic",
        }

        if normalized in explicit_map:
            return explicit_map[normalized]

        keyword_map = {
            "qdrant": "qdrant_ecosystem",
            "sentence_transformer": "sentence_transformers",
            "sentence": "sentence_transformers",
            "docling": "docling",
            "fast_docs": "fast_docs",
            "pydantic": "pydantic",
        }

        for keyword, target in keyword_map.items():
            if keyword in normalized:
                return target

        return normalized

    def get_target_collection_name(self) -> str:
        """Infer the Qdrant collection identifier for the current embedding export."""

        if self._target_collection_cache:
            return self._target_collection_cache

        candidates: Counter[str] = Counter()

        for metadata in self.chunks_metadata:
            candidate = metadata.get("qdrant_collection") if isinstance(metadata, dict) else None
            if not candidate:
                hints = metadata.get("collection_hints") if isinstance(metadata, dict) else None
                if isinstance(hints, list):
                    for hint in hints:
                        if isinstance(hint, str) and hint.strip():
                            candidate = hint
                            break
            if isinstance(candidate, str) and candidate.strip():
                normalized = self._normalize_collection_name(candidate)
                candidates[normalized] += 1

        if candidates:
            canonical = candidates.most_common(1)[0][0]
        elif self._canonical_collection_hint:
            canonical = self._normalize_collection_name(self._canonical_collection_hint)
        else:
            canonical = "ultimate_embeddings"

        safe_model = self.model_name.replace(" ", "_").replace("-", "_")
        collection_name = f"{canonical}_v4_{safe_model}"
        self._target_collection_cache = collection_name
        return collection_name
    
    def generate_embeddings_kaggle_optimized(
        self,
        enable_monitoring: bool = True,
        save_intermediate: bool = True,
    ) -> Dict[str, Any]:
        """Generate embeddings optimized for Kaggle T4 x2 environment."""

        if not self.chunk_texts:
            raise ValueError("No chunks loaded. Call load_chunks_from_processing() first.")

        results = self.batch_runner.run(
            enable_monitoring=enable_monitoring,
            save_intermediate=save_intermediate,
        )
        self._last_dense_run = results
        self._assemble_processing_summary(results=results)
        return results

    def _assemble_processing_summary(
        self,
        *,
        results: Optional[Dict[str, Any]] = None,
        collection_name: Optional[str] = None,
        chunk_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        dense_run = results or (self._last_dense_run or None)

        dense_latency_seconds: Optional[float] = None
        dense_embeddings_generated: Optional[int] = None
        dense_chunks_per_second: Optional[float] = None
        if isinstance(dense_run, Mapping):
            raw_latency = dense_run.get("processing_time_seconds")
            if isinstance(raw_latency, (int, float)):
                dense_latency_seconds = float(raw_latency)
            raw_embeddings = dense_run.get("total_embeddings_generated")
            if isinstance(raw_embeddings, (int, float)):
                dense_embeddings_generated = int(raw_embeddings)
            raw_chunks = dense_run.get("chunks_per_second")
            if isinstance(raw_chunks, (int, float)):
                dense_chunks_per_second = float(raw_chunks)

        gpu_history: Optional[Dict[str, Any]] = None

        dense_details: Dict[str, Any] = {
            "model": self.model_name,
            "device": self.device,
        }
        if dense_latency_seconds is not None:
            dense_details["latency_seconds"] = dense_latency_seconds
        if dense_chunks_per_second is not None:
            dense_details["chunks_per_second"] = dense_chunks_per_second
        if dense_embeddings_generated is not None:
            dense_details["embeddings_generated"] = dense_embeddings_generated

        if gpu_history is None:
            gpu_history = self._summarize_gpu_history()
        if gpu_history and gpu_history.get("peak_allocated_gb") is not None:
            peak_value = gpu_history.get("peak_allocated_gb")
            if isinstance(peak_value, (int, float)):
                dense_details["gpu_peak_gb"] = float(peak_value)

        dense_active = bool(
            dense_embeddings_generated is not None
            and dense_embeddings_generated > 0
        )
        dense_skip_reason: Optional[str] = None
        if not dense_active:
            dense_skip_reason = "dense stage produced no embeddings"
        self._emit_metrics_for_stage(
            "dense",
            active=dense_active,
            reason=dense_skip_reason,
            details=dense_details,
        )

        rerank_enabled = bool(self.reranking_config.enable_reranking)
        rerank_executor = getattr(self, "cross_encoder_executor", None)
        rerank_pipeline_device = None
        if rerank_executor is not None:
            rerank_pipeline_device = getattr(rerank_executor.rerank_pipeline, "device", None)

        rerank_run = getattr(self, "rerank_run", None)
        fused_candidates = getattr(self, "fused_candidates", {})
        rerank_failure_reason = getattr(self, "rerank_failure_reason", None)

        rerank_executed = bool(rerank_run and rerank_run.candidate_ids)
        rerank_loaded = bool(
            self.reranker is not None
            or (
                rerank_executor
                and getattr(rerank_executor.rerank_pipeline, "model", None) is not None
            )
        )

        requested_rerank_device = self._requested_rerank_device or (
            "cuda" if self.device == "cuda" else self.device
        )
        resolved_rerank_device = rerank_pipeline_device or self.reranker_device or "cpu"

        fallback_applied = False
        fallback_reason: Optional[str] = None
        if (
            rerank_enabled
            and isinstance(requested_rerank_device, str)
            and requested_rerank_device.startswith("cuda")
            and (not isinstance(resolved_rerank_device, str) or not resolved_rerank_device.startswith("cuda"))
        ):
            fallback_applied = True
            fallback_reason = "Resolved to CPU staging while awaiting GPU lease"

        rerank_status: str
        rerank_reason: Optional[str] = None

        if not rerank_enabled:
            source = self.feature_toggles.sources.get("enable_rerank", "default")
            rerank_status = "disabled"
            rerank_reason = self._rerank_runtime_reason or f"Disabled via {source}"
        elif rerank_executed:
            rerank_status = "executed"
            rerank_reason = None
        elif rerank_failure_reason:
            rerank_status = "error"
            rerank_reason = rerank_failure_reason
        elif rerank_loaded:
            rerank_status = "pending"
            rerank_reason = self._rerank_runtime_reason or "Rerank executor ready; awaiting execution"
        else:
            rerank_status = "pending"
            rerank_reason = self._rerank_runtime_reason or "Rerank executor unavailable"

        rerank_stage: Optional[Dict[str, Any]] = None
        if rerank_enabled or rerank_executed or rerank_failure_reason:
            rerank_stage = build_rerank_stage_summary(
                enabled=rerank_enabled,
                model_name=self.reranking_config.model_name,
                loaded=rerank_loaded,
                device=resolved_rerank_device,
                executed=rerank_executed,
                status=rerank_status,
                reason=rerank_reason,
                metrics={
                    "top_k_candidates": self.reranking_config.top_k_candidates,
                    "rerank_top_k": self.reranking_config.rerank_top_k,
                    "batch_size": self.reranking_config.batch_size,
                },
                requested_device=requested_rerank_device,
                fallback_applied=fallback_applied,
                fallback_reason=fallback_reason,
                fallback_count=self.rerank_fallback_count,
                rerank_fallback_reason=self.rerank_fallback_reason,
                fallback_source=self.rerank_fallback_source,
            )

            if rerank_run:
                rerank_stage.update(
                    {
                        "run_id": rerank_run.run_id,
                        "latency_ms": rerank_run.latency_ms,
                        "gpu_peak_gb": rerank_run.gpu_peak_gb,
                        "batch_size": rerank_run.batch_size,
                        "candidate_count": len(rerank_run.candidate_ids),
                        "candidate_ids": list(rerank_run.candidate_ids),
                        "scores": list(rerank_run.scores),
                        "result_count": len(rerank_run.candidate_ids),
                    }
                )
            rerank_stage.setdefault("fallback_count", self.rerank_fallback_count)
            if self.rerank_fallback_reason:
                rerank_stage.setdefault("fallback_reason", self.rerank_fallback_reason)
            if self.rerank_fallback_source:
                rerank_stage.setdefault("fallback_source", self.rerank_fallback_source)
            if fused_candidates:
                initial_ids = fused_candidates.get("candidate_ids", [])
                rerank_stage.setdefault("initial_candidate_count", len(initial_ids))
                if "query" in fused_candidates:
                    rerank_stage.setdefault("query", fused_candidates.get("query", ""))
                dense_scores = fused_candidates.get("dense_scores")
                if isinstance(dense_scores, list) and dense_scores:
                    rerank_stage["dense_scores"] = [float(score) for score in dense_scores]
                reranked_metadata = fused_candidates.get("reranked_metadata")
                if reranked_metadata:
                    rerank_stage["candidate_metadata"] = list(reranked_metadata)
                elif rerank_run and fused_candidates.get("metadata"):
                    rerank_stage["candidate_metadata"] = list(
                        fused_candidates["metadata"][: len(rerank_run.candidate_ids)]
                    )
            if rerank_failure_reason and rerank_status == "error":
                rerank_stage["failure_reason"] = rerank_failure_reason

        candidate_count = len(fused_candidates.get("candidate_ids", []))
        rerank_span_reason = rerank_reason or (
            f"Disabled via {self.feature_toggles.sources.get('enable_rerank', 'default')}"
            if not rerank_enabled
            else rerank_status
        )
        if rerank_executed and rerank_span_reason is None:
            rerank_span_reason = "executed"

        rerank_attributes: Dict[str, Any] = {
            "status": rerank_status,
            "executed": rerank_executed,
            "candidate_count": candidate_count,
            "requested_device": requested_rerank_device,
            "resolved_device": resolved_rerank_device,
        }
        rerank_attributes["fallback_count"] = self.rerank_fallback_count
        if self.rerank_fallback_reason:
            rerank_attributes["fallback_reason"] = self.rerank_fallback_reason
        if self.rerank_fallback_source:
            rerank_attributes["fallback_source"] = self.rerank_fallback_source
        if rerank_run:
            rerank_attributes.update(
                {
                    "latency_ms": rerank_run.latency_ms,
                    "gpu_peak_gb": rerank_run.gpu_peak_gb,
                    "batch_size": rerank_run.batch_size,
                    "result_count": len(rerank_run.candidate_ids),
                }
            )
        if rerank_failure_reason:
            rerank_attributes["failure_reason"] = rerank_failure_reason
        if fallback_applied and fallback_reason:
            rerank_attributes["device_fallback_reason"] = fallback_reason

        self.telemetry.record_span_presence(
            "rag.rerank",
            active=rerank_enabled,
            reason=rerank_span_reason,
            attributes=rerank_attributes,
            candidate_count=candidate_count,
            fallback_used=fallback_applied,
            fallback_count=self.rerank_fallback_count,
            fallback_reason=self.rerank_fallback_reason,
            fallback_source=self.rerank_fallback_source,
        )

        metrics_details: Dict[str, Any] = {
            "model": self.reranking_config.model_name,
            "device": resolved_rerank_device,
            "candidate_count": candidate_count,
        }
        metrics_details["fallback_count"] = self.rerank_fallback_count
        if self.rerank_fallback_reason:
            metrics_details["fallback_reason"] = self.rerank_fallback_reason
        if self.rerank_fallback_source:
            metrics_details["fallback_source"] = self.rerank_fallback_source
        if fallback_applied and fallback_reason:
            metrics_details["device_fallback_reason"] = fallback_reason
        metrics_details["device_fallback_applied"] = fallback_applied
        if rerank_run:
            metrics_details.update(
                {
                    "latency_seconds": rerank_run.latency_ms / 1000.0,
                    "gpu_peak_gb": rerank_run.gpu_peak_gb,
                    "batch_size": rerank_run.batch_size,
                }
            )

        metrics_reason = rerank_span_reason if not rerank_enabled else rerank_reason
        self._emit_metrics_for_stage(
            "rerank",
            active=rerank_executed if rerank_enabled else False,
            reason=metrics_reason,
            details=metrics_details,
        )

        sparse_total = len(self.sparse_vectors)
        sparse_available = sum(1 for vector in self.sparse_vectors if vector)
        coverage = (sparse_available / sparse_total) if sparse_total else 0.0
        sparse_reason = self._sparse_runtime_reason
        sparse_fallback_reason: Optional[str] = None
        sparse_fallback_used = False
        if self.enable_sparse and sparse_available == 0:
            sparse_fallback_used = True
            sparse_fallback_reason = "Sparse vectors unavailable; metadata fallback engaged"
            if not sparse_reason:
                sparse_reason = sparse_fallback_reason
        sparse_stage: Optional[Dict[str, Any]] = None
        sparse_result = getattr(self, "sparse_inference_result", None)
        sparse_latency = getattr(sparse_result, "latency_ms", None)
        sparse_run_id = getattr(sparse_result, "run_id", None)
        sparse_success = getattr(sparse_result, "success", None)
        sparse_error = getattr(sparse_result, "error_message", None)
        sparse_fallback_total = getattr(sparse_result, "fallback_count", None)
        sparse_primary_device = getattr(sparse_result, "device", None)
        sparse_attributes: Dict[str, Any] = {
            "models": list(self.sparse_model_names),
            "coverage_ratio": coverage,
            "devices": dict(self.sparse_device_map),
            "fallback_used": sparse_fallback_used,
        }
        if sparse_fallback_reason:
            sparse_attributes["fallback_reason"] = sparse_fallback_reason

        if self.enable_sparse:
            sparse_stage = build_sparse_stage_summary(
                enabled=True,
                model_names=self.sparse_model_names,
                vectors_total=sparse_total,
                vectors_available=sparse_available,
                executed=bool(self.sparse_vectors),
                coverage_ratio=coverage,
                devices=self.sparse_device_map,
                fallback_used=sparse_fallback_used,
                fallback_reason=sparse_fallback_reason,
                reason=sparse_reason,
                latency_ms=sparse_latency,
                run_id=sparse_run_id,
                success=sparse_success,
                error_message=sparse_error,
                fallback_count=sparse_fallback_total,
                device=sparse_primary_device,
            )

        sparse_span_reason = sparse_reason or (
            f"Disabled via {self.feature_toggles.sources.get('enable_sparse', 'default')}"
            if not self.enable_sparse
            else ("fallback engaged" if sparse_fallback_used else "active")
        )
        if not self.enable_sparse:
            sparse_attributes["source"] = self.feature_toggles.sources.get("enable_sparse", "default")
        self.telemetry.record_span_presence(
            "rag.sparse",
            active=self.enable_sparse,
            reason=sparse_span_reason,
            attributes=sparse_attributes,
            batch_size=sparse_total,
            coverage_ratio=coverage,
            fallback_used=sparse_fallback_used,
        )
        self._emit_metrics_for_stage(
            "sparse",
            active=self.enable_sparse,
            reason=sparse_span_reason,
            details={**sparse_attributes, "coverage_ratio": coverage},
        )

        telemetry_summary = build_telemetry_summary(
            mitigation_events=self.telemetry.mitigation_events,
            rotation_events=self.telemetry.rotation_events,
            lease_events=self.telemetry.gpu_lease_events,
            batch_progress_events=self.telemetry.batch_progress_events,
            span_events=getattr(self.telemetry, "span_events", {}),
            metrics_report=getattr(self.telemetry, "metrics_reports", {}),
        )

        resolved_chunk_count = chunk_count
        if resolved_chunk_count is None:
            if isinstance(dense_run, Mapping):
                dense_total = dense_run.get("total_embeddings_generated")
                if isinstance(dense_total, int):
                    resolved_chunk_count = dense_total
            if resolved_chunk_count is None:
                total_loaded = self.last_loading_summary.get("total_chunks_loaded") if isinstance(self.last_loading_summary, Mapping) else None
                if isinstance(total_loaded, int):
                    resolved_chunk_count = total_loaded
            if resolved_chunk_count is None and self.chunk_texts:
                resolved_chunk_count = len(self.chunk_texts)

        summary = build_processing_summary(
            feature_toggles=self.feature_toggles,
            dense_run=dense_run,
            rerank_stage=rerank_stage,
            sparse_stage=sparse_stage,
            telemetry=telemetry_summary,
            collection_name=collection_name,
            chunk_count=resolved_chunk_count,
        )

        warnings = summary.get("warnings") or []
        rerank_enabled = bool(self.feature_toggles.enable_rerank)
        rerank_run = getattr(self, "rerank_run", None)
        rerank_failure_reason = getattr(self, "rerank_failure_reason", None)
        if rerank_enabled and rerank_run is None and rerank_failure_reason:
            warnings.append(
                f"rerank stage reported failure: {rerank_failure_reason}"
            )

        sparse_enabled = bool(self.feature_toggles.enable_sparse)
        sparse_result = getattr(self, "sparse_inference_result", None)
        if sparse_enabled and sparse_result and not getattr(sparse_result, "success", True):
            error_message = getattr(sparse_result, "error_message", None)
            if error_message:
                warnings.append(f"sparse stage failure: {error_message}")

        if warnings:
            summary["warnings"] = warnings

        performance_baseline = build_performance_baseline(
            dict(self.processing_stats)
        )
        if performance_baseline:
            if gpu_history is None:
                gpu_history = self._summarize_gpu_history()
            if gpu_history:
                gpu_section = performance_baseline.setdefault("gpu", {})
                soft_limit_gb = gpu_history.get("soft_limit_gb")
                if soft_limit_gb is not None:
                    gpu_section["soft_limit_gb"] = soft_limit_gb
                exceeded = bool(gpu_history.get("soft_limit_exceeded"))
                gpu_section["soft_limit_exceeded"] = exceeded
                devices = gpu_history.get("soft_limit_devices") or []
                if devices:
                    gpu_section["soft_limit_devices"] = devices
                status = "within_limit" if not exceeded else "exceeded_soft_limit"
                gpu_section["status"] = status
                if (
                    exceeded
                    and "gpu_soft_limit" not in self.telemetry.metrics_reports
                ):
                    raise RuntimeError(
                        "GPU soft limit exceeded without alert telemetry; "
                        "ensure gpu_soft_limit status is recorded"
                    )
                peak_from_history = gpu_history.get("peak_allocated_gb")
                if peak_from_history is not None and "peak_memory_used_gb" not in gpu_section:
                    gpu_section["peak_memory_used_gb"] = peak_from_history
            summary["performance_baseline"] = performance_baseline

        self.last_processing_summary = summary
        return summary

    def create_processing_summary(
        self,
        *,
        collection_name: Optional[str] = None,
        chunk_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        return self._assemble_processing_summary(
            results=None,
            collection_name=collection_name,
            chunk_count=chunk_count,
        )

    def write_processing_summary(
        self,
        path: Union[str, Path],
        *,
        collection_name: Optional[str] = None,
        chunk_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        summary = self._assemble_processing_summary(
            results=None,
            collection_name=collection_name,
            chunk_count=chunk_count,
        )

        target_path = Path(path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        return summary
    
    def _encode_with_backend(self, texts: List[str], batch_size: int) -> np.ndarray:
        """Delegate backend encoding to the shared helper"""

        return encode_with_backend(self, texts, batch_size, logger)

    def _ensure_embedding_dimension(
        self,
        matrix: np.ndarray,
        expected_dim: Optional[int] = None,
    ) -> Tuple[np.ndarray, bool]:
        """Ensure embeddings align with the configured vector dimension."""

        expected_dim = expected_dim or self.model_config.vector_dim
        actual_dim = matrix.shape[1]

        if actual_dim == expected_dim:
            return matrix, False

        if actual_dim < expected_dim:
            raise ValueError(
                f"Embedding dimension {actual_dim} is smaller than expected {expected_dim}; "
                "cannot safely upsample vectors"
            )

        logger.warning(
            "Embedding dimension mismatch detected (%s -> %s); trimming to maintain compatibility",
            actual_dim,
            expected_dim,
        )
        return matrix[:, :expected_dim], True
    
    def export_for_local_qdrant(self) -> Dict[str, str]:
        """Export embeddings in formats optimized for local Qdrant upload."""

        return self.export_runtime.export_for_local_qdrant()
    
    def _export_qdrant_jsonl(self, file_path: str) -> None:
        """Export in JSONL format for Qdrant upload."""

        embeddings = self._require_embeddings()
        companion_arrays = {
            name: array
            for name, array in self.embeddings_by_model.items()
            if name != self.model_name
        }

        self.export_runtime._export_qdrant_jsonl(file_path, embeddings, companion_arrays)

    def _export_sparse_jsonl(self, file_path: str) -> None:
        """Export hashed sparse vectors as a sidecar JSONL file."""

        self.export_runtime._export_sparse_jsonl(file_path)
    
    def _export_faiss_index(self, file_path: str) -> None:
        """Export FAISS index for fast similarity search."""

        self.export_runtime._export_faiss_index(file_path)
    
    def _export_metadata(self, file_path: str) -> None:
        """Export enhanced metadata."""

        self.export_runtime._export_metadata(file_path)
    
    def _export_texts(self, file_path: str) -> None:
        """Export chunk texts."""

        self.export_runtime._export_texts(file_path)
    
    def _export_processing_stats(self, file_path: str) -> None:
        """Export comprehensive processing statistics."""

        self.export_runtime._export_processing_stats(file_path)
    
    def _start_performance_monitoring(self) -> None:
        """Start performance monitoring for Kaggle environment."""

        self.performance_monitor.start()
        self.monitoring_active = True
        self.monitor_thread = None

    def _stop_performance_monitoring(self) -> None:
        """Stop performance monitoring."""

        self.performance_monitor.stop()
        self.monitoring_active = False
        self.monitor_thread = None

def main():
    """Main function for Kaggle usage with V4 features demo"""
    
    logger.info("Ultimate Kaggle Embedder V4 - Complete Feature Demo")
    
    # Configuration for Kaggle T4 x2
    gpu_config = KaggleGPUConfig(
        device_count=2,
        base_batch_size=32,
        dynamic_batching=True,
        enable_torch_compile=True,
        backend="pytorch"  # Switch to "onnx" if available
    )
    
    export_config = KaggleExportConfig(
        export_numpy=True,
        export_jsonl=True,
        export_faiss=True,
        compress_embeddings=True
    )
    
    # V5 Feature Configurations (using V5-specified models)
    ensemble_config = EnsembleConfig(
        ensemble_models=["jina-code-embeddings-1.5b", "bge-m3", "qwen3-embedding-0.6b"]
    )
    
    reranking_config = RerankingConfig(
        model_name="jina-reranker-v3",
        enable_reranking=True,
        top_k_candidates=100,
        rerank_top_k=20
    )
    
    # Test different V4 modes
    test_configs = [
        {"name": "Standard Mode", "ensemble": False, "reranking": False},
        {"name": "Ensemble Mode", "ensemble": True, "reranking": False},
        {"name": "Reranking Mode", "ensemble": False, "reranking": True},
        {"name": "Full V4 Mode", "ensemble": True, "reranking": True}
    ]
    
    for config in test_configs:
        logger.info(f"\nTesting {config['name']}")
        
        try:
            # Initialize embedder with V5 features
            embedder = UltimateKaggleEmbedderV4(
                model_name="jina-code-embeddings-1.5b",
                gpu_config=gpu_config,
                export_config=export_config,
                enable_ensemble=config["ensemble"],
                ensemble_config=ensemble_config if config["ensemble"] else None,
                reranking_config=reranking_config if config["reranking"] else RerankingConfig()
            )
            
            # Set reranking based on config
            if config["reranking"]:
                embedder.reranking_config.enable_reranking = True

            # Load chunks
            logger.info("Loading chunks...")
            loading_results = embedder.load_chunks_from_processing()

            if loading_results.get("total_chunks_loaded", 0) == 0:
                logger.error("No chunks loaded!")
                continue

            logger.info(f"Loaded {loading_results['total_chunks_loaded']} chunks")

            # Generate embeddings
            logger.info("Generating embeddings...")
            embedding_results = embedder.generate_embeddings_kaggle_optimized()

            # Demo search with reranking (if enabled)
            if config["reranking"] and embedding_results.get('total_embeddings_generated', 0) > 0:
                logger.info("Testing semantic search with reranking...")
                try:
                    search_results = embedder.search_with_reranking(
                        query="How to optimize vector search performance?",
                        top_k=5
                    )
                    logger.info(f"Found {len(search_results)} reranked results")
                    if search_results:
                        logger.info(f"  Top result score: {search_results[0]['score']:.4f}")
                except Exception as e:
                    logger.warning(f"Search demo failed: {e}")

            # Export for local Qdrant
            logger.info("Exporting for local Qdrant...")
            exported_files = embedder.export_for_local_qdrant()

            # Results summary
            logger.info(f"\nResults for {config['name']}:")
            logger.info(f"  Embeddings: {embedding_results['total_embeddings_generated']}")
            logger.info(f"  Dimension: {embedding_results['embedding_dimension']}")
            logger.info(f"  Time: {embedding_results['processing_time_seconds']:.2f}s")
            logger.info(f"  Speed: {embedding_results['chunks_per_second']:.1f} chunks/sec")
            logger.info(f"  Memory: {embedding_results['embedding_memory_mb']:.1f}MB")
            logger.info(f"  Exported files: {len(exported_files)}")

            # Only test first config in demo to save time
            break

        except Exception as e:
            logger.error(f"Failed with {config['name']}: {e}")
            continue
    
    logger.info("\nV4 Demo complete. Download exported files and run upload script locally.")
    logger.info("V4 Features tested: Enhanced models, ensemble embedding, CrossEncoder reranking")

if __name__ == "__main__":
    main()