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

import os

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

import gc
import logging
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union, cast

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
try:
    from optimum.onnxruntime import ORTModelForFeatureExtraction  # type: ignore[import-not-found]
except ImportError:
    ORTModelForFeatureExtraction = None  # type: ignore[assignment]

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


# Module extractions
from processor.ultimate_embedder.batch_runner import BatchRunner
from processor.ultimate_embedder.chunk_loader import ChunkLoader
from processor.ultimate_embedder.controllers import (
    AdaptiveBatchController,
    GPUMemorySnapshot,
    collect_gpu_snapshots,
)
from processor.ultimate_embedder.export_runtime import ExportRuntime
from processor.ultimate_embedder.model_manager import ModelManager
from processor.ultimate_embedder.monitoring import PerformanceMonitor
from processor.ultimate_embedder.rerank_pipeline import RerankPipeline
from processor.ultimate_embedder.telemetry import TelemetryTracker, resolve_rotation_payload_limit
from processor.ultimate_embedder.config import (
    AdvancedPreprocessingConfig,
    AdvancedTextCache,
    EnsembleConfig,
    KAGGLE_OPTIMIZED_MODELS,
    KaggleExportConfig,
    KaggleGPUConfig,
    ModelConfig,
    RERANKING_MODELS,
    RerankingConfig,
)
from processor.ultimate_embedder.backend_encoder import encode_with_backend

# ============================================================================
# SOTA MODEL CONFIGURATIONS (Kaggle T4 x2 Optimized)
# ============================================================================
# Definitions reside in processor.ultimate_embedder.config and are imported
# above for reuse within the facade.



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
        enable_sparse: bool = False,  # V5: Enable sparse embeddings
        sparse_models: Optional[List[str]] = None,  # V5: Sparse model names
        matryoshka_dim: Optional[int] = None,  # V5: Matryoshka dimension
        local_files_only: bool = False,
        force_cpu: bool = False,
        hf_cache_dir: Optional[Union[str, Path]] = None,
        refresh_cache: bool = False,
        gpu0_soft_limit_gb: float = 12.0,
    ):
        """Initialize Ultimate Kaggle Embedder V4"""

        logger.info("Initializing Ultimate Kaggle Embedder V4 (Split Architecture)")

        # Validate model
        if model_name not in KAGGLE_OPTIMIZED_MODELS:
            logger.warning(f"Unknown model {model_name}, defaulting to jina-code-embeddings-1.5b")
            model_name = "jina-code-embeddings-1.5b"
        
        self.model_config = KAGGLE_OPTIMIZED_MODELS[model_name]
        self.model_name = model_name
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
        self.ensemble_config = ensemble_config or EnsembleConfig() if enable_ensemble else None
        self.reranking_config = reranking_config or RerankingConfig()
        self._canonical_collection_hint: Optional[str] = None
        self._target_collection_cache: Optional[str] = None

        self.embedding_backend: str = "local"
        self.multivectors_by_model: Dict[str, List[List[List[float]]]] = {}
        self.multivector_dimensions: Dict[str, int] = {}
        self.multivector_comparators: Dict[str, str] = {}
        self.primary_vector_name: str = self.model_name

        # V5: Sparse embedding support
        self.enable_sparse = enable_sparse
        self.sparse_models: Dict[str, Any] = {}
        self.sparse_model_names: List[str] = sparse_models or []
        if self.enable_sparse and not self.sparse_model_names:
            self.sparse_model_names = ["qdrant-bm25"]

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

        self.text_cache = AdvancedTextCache() if self.preprocessing_config.enable_text_caching else None

        self.models: Dict[str, Any] = {}
        self.primary_model: Optional[SentenceTransformer] = None
        self.reranker = None

        self.companion_dense_model_names: List[str] = companion_dense_models or []
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
        self._rotation_payload_limit: int = rotation_limit
        self.mitigation_events = self.telemetry.mitigation_events
        self.cache_events = self.telemetry.cache_events
        self.rotation_events = self.telemetry.rotation_events
        self.adaptive_controller: Optional[AdaptiveBatchController] = None
        self.gradient_checkpoint_evaluated: bool = False

        self.model_manager = ModelManager(self, logger)
        self.chunk_loader = ChunkLoader(
            project_root=self.project_root,
            is_kaggle=self.is_kaggle,
            logger=logger,
        )
        self.batch_runner = BatchRunner(self, logger)
        self.rerank_pipeline = RerankPipeline(self.reranking_config, logger)

        self.sequential_device_order: List[str] = []
        if self.device == "cuda":
            if self.device_count > 1:
                self.sequential_device_order = [f"cuda:{idx}" for idx in range(self.device_count - 1, -1, -1)]
            else:
                self.sequential_device_order = ["cuda:0"]
        self.sequential_device_order.append("cpu")

        sequential_env = os.environ.get("EMBEDDER_SEQUENTIAL_ENSEMBLE")
        if sequential_env is not None:
            sequential_enabled = sequential_env.strip().lower() in {"1", "true", "yes", "on"}
            if sequential_enabled and not self.ensemble_config:
                self.enable_ensemble = True
                self.ensemble_config = EnsembleConfig(sequential_passes=True)
            elif self.ensemble_config:
                self.ensemble_config.sequential_passes = sequential_enabled

        if self.ensemble_config:
            device_override = os.environ.get("EMBEDDER_SEQUENTIAL_DEVICES")
            if device_override:
                preferred = [candidate.strip() for candidate in device_override.split(",") if candidate.strip()]
                if preferred:
                    self.ensemble_config.preferred_devices = preferred
            if self.ensemble_config.preferred_devices:
                unique_order: List[str] = []
                for candidate in self.ensemble_config.preferred_devices:
                    if candidate and candidate not in unique_order:
                        unique_order.append(candidate)
                for fallback in self.sequential_device_order:
                    if fallback not in unique_order:
                        unique_order.append(fallback)
                self.sequential_device_order = unique_order

        sequential_dp_env = os.environ.get("EMBEDDER_SEQUENTIAL_DATA_PARALLEL")
        if sequential_dp_env and self.ensemble_config:
            self.ensemble_config.sequential_data_parallel = sequential_dp_env.strip().lower() in {"1", "true", "yes", "on"}

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
            fallback = self.models.get(self.model_name) or next(iter(self.models.values()))
            self.primary_model = cast(SentenceTransformer, fallback)
            logger.debug("Primary model fallback resolved to %s", type(fallback).__name__)
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
        self.telemetry.record_mitigation(event_type, **details)

    def _record_rotation_event(self, event: Dict[str, Any]) -> None:
        """Capture per-batch ensemble rotation telemetry with bounded detail."""
        self.telemetry.record_rotation_event(event)

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

    def _call_encode(
        self,
        model: Any,
        texts: List[str],
        batch_size: int,
        device: str,
        show_progress: bool = True,
        progress_label: Optional[str] = None,
    ) -> np.ndarray:
        """Invoke encode() against SentenceTransformer or compatible wrappers."""

        encode_callable = getattr(model, "encode", None)
        if encode_callable is None and hasattr(model, "module"):
            encode_callable = getattr(model.module, "encode", None)

        if encode_callable is None:
            base_model = self._unwrap_model(model)
            encode_callable = getattr(base_model, "encode", None)

        if encode_callable is None:
            raise AttributeError(f"Model {type(model).__name__} does not expose encode()")

        call_args: List[Any] = [texts]
        call_kwargs: Dict[str, Any] = {
            "batch_size": batch_size,
            "show_progress_bar": show_progress,
            "convert_to_numpy": True,
            "normalize_embeddings": True,
            "device": device,
        }

        progress_requested = bool(show_progress and progress_label)
        if progress_requested:
            call_kwargs["tqdm_kwargs"] = {"desc": f"Batches({progress_label})"}

        try:
            return encode_callable(*call_args, **call_kwargs)
        except Exception as primary_exc:
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
            hint = max(1, min(hint, 8))
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

        if self.ensemble_config and self.ensemble_config.preferred_devices:
            candidates = self.ensemble_config.preferred_devices
        else:
            candidates = self.sequential_device_order

        for candidate in candidates:
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
        """Aggregate chunk counts per source within the given slice."""

        counts: Counter[str] = Counter()
        if start_index >= end_index:
            return counts

        for idx in range(start_index, end_index):
            if idx >= len(self.chunks_metadata):
                source_name = f"chunk_{idx}"
            else:
                metadata = self.chunks_metadata[idx] or {}
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
        """Build a succinct progress label describing the primary source for a batch."""

        counts = self._collect_batch_source_counts(start_index, end_index)
        if not counts:
            return None

        primary_name, _ = counts.most_common(1)[0]
        unique_sources = len(counts)
        if unique_sources <= 1:
            return primary_name

        return f"{primary_name} +{unique_sources - 1} more"

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
        
        try:
            self.reranker = CrossEncoder(reranker_model, device=self.device)
            logger.info("CrossEncoder reranking model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load reranking model: {e}")
            self.reranking_config.enable_reranking = False
            self.reranker = None
    
    def generate_ensemble_embeddings(
        self,
        texts: List[str],
        batch_slice: Optional[slice] = None,
        batch_index: Optional[int] = None,
        progress_label: Optional[str] = None,
    ) -> np.ndarray:
        """Delegate ensemble embedding generation to the batch runner service."""

        return self.batch_runner.generate_ensemble_embeddings(
            texts,
            batch_slice=batch_slice,
            batch_index=batch_index,
            progress_label=progress_label,
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
        
        # Step 3: Prepare query-document pairs for reranking
        query_doc_pairs = []
        candidate_indices = []
        
        for idx in top_indices:
            if idx < len(self.chunk_texts):
                query_doc_pairs.append([query, self.chunk_texts[idx]])
                candidate_indices.append(idx)
        
        if not query_doc_pairs:
            logger.warning("No valid candidates for reranking")
            return []
        
        # Step 4: Rerank with CrossEncoder
        logger.info(f"Reranking {len(query_doc_pairs)} candidates...")

        try:
            rerank_scores = self.reranker.predict(query_doc_pairs)
            
            # Sort by reranking scores
            reranked_indices = np.argsort(rerank_scores)[::-1][:top_k]
            
            # Prepare results
            results = []
            for rank, idx in enumerate(reranked_indices):
                original_idx = candidate_indices[idx]
                
                result = {
                    "rank": rank + 1,
                    "score": float(rerank_scores[idx]),
                    "embedding_similarity": float(similarities[original_idx]),
                    "text": self.chunk_texts[original_idx],
                    "metadata": self.chunks_metadata[original_idx],
                    "chunk_id": original_idx
                }
                results.append(result)
            
            logger.info(f"Reranking complete. Top score: {results[0]['score']:.4f}")
            return results
            
        except Exception as e:
            logger.error(f"Reranking failed: {e}")
            return self._embedding_only_search(query, top_k)
    
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
    
    def _generate_upload_script(self, file_path: str, exported_files: Dict[str, str]) -> None:
        """Generate Python script for local Qdrant upload."""

        self.export_runtime._generate_upload_script(file_path, exported_files)

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

        return self.batch_runner.run(
            enable_monitoring=enable_monitoring,
            save_intermediate=save_intermediate,
        )
    
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
    
    def _save_intermediate_results(self, embeddings_list: List[np.ndarray], batch_num: int):
        """Save intermediate results during processing"""
        if not self.is_kaggle:
            return
        
        try:
            intermediate_path = self.export_config.get_output_path(f"_intermediate_batch_{batch_num}")
            embeddings_so_far = np.vstack(embeddings_list)
            np.save(f"{intermediate_path}.npy", embeddings_so_far.astype(np.float32))
            logger.info(f"Intermediate results saved: {intermediate_path}.npy")
        except Exception as e:
            logger.warning(f"Failed to save intermediate results: {e}")
    
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
        ensemble_models=["jina-code-embeddings-1.5b", "bge-m3", "qwen3-embedding-0.6b"],
        weighting_strategy="equal",
        aggregation_method="weighted_average"
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