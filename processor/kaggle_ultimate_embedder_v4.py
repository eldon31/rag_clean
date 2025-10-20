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

import os
import sys

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

import json
import logging
import math
import numpy as np
import pickle
import torch
import gc
import warnings
from contextlib import nullcontext
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union, Set, Type, cast
from datetime import datetime
from collections import defaultdict, Counter
import time
import psutil
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import hashlib
from functools import lru_cache
import math
import textwrap

from huggingface_hub import snapshot_download

try:
    from huggingface_hub import LocalEntryNotFoundError  # type: ignore[attr-defined]
except ImportError:
    try:
        from huggingface_hub.utils import LocalEntryNotFoundError  # type: ignore[attr-defined]
    except ImportError:  # pragma: no cover - legacy hub versions
        LocalEntryNotFoundError = FileNotFoundError  # type: ignore[assignment]

LocalEntryNotFoundErrorType = cast(Type[Exception], LocalEntryNotFoundError)

# Core ML libraries
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import faiss

# Advanced optimization libraries (optional on Kaggle)
try:
    import onnxruntime as ort  # type: ignore[import-not-found]
    from optimum.onnxruntime import ORTModelForFeatureExtraction  # type: ignore[import-not-found]
    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False
    ORTModelForFeatureExtraction = None  # type: ignore[assignment]

try:
    import tensorrt  # type: ignore[import-not-found]
    TENSORRT_AVAILABLE = True
except ImportError:
    TENSORRT_AVAILABLE = False

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


# ============================================================================
# SOTA MODEL CONFIGURATIONS (Kaggle T4 x2 Optimized)
# ============================================================================

@dataclass
class ModelConfig:
    """Kaggle T4 x2 optimized model configurations"""
    name: str
    hf_model_id: str
    vector_dim: int
    max_tokens: int
    trust_remote_code: bool = True
    query_prefix: str = ""
    doc_prefix: str = ""
    # Kaggle T4 specific optimizations
    recommended_batch_size: int = 32
    memory_efficient: bool = True
    supports_flash_attention: bool = True  # ENABLED: Install with !pip install flash-attn --no-build-isolation
    
# V5 Model Registry - Qdrant-Optimized Models ONLY
# Based on notes/V5_MODEL_CONFIGURATIONS.md
KAGGLE_OPTIMIZED_MODELS = {
    # PRIMARY: Code-optimized (Main model for code embedding)
    # ENSEMBLE MODE: Using 1024D Matryoshka for compatibility
    "jina-code-embeddings-1.5b": ModelConfig(
        name="jina-code-embeddings-1.5b",
        hf_model_id="jinaai/jina-code-embeddings-1.5b",
        vector_dim=1024,  # Ensemble dimension (native: 1536D, Matryoshka: 1024D)
        max_tokens=32768,
        query_prefix="Encode this code snippet for semantic retrieval: ",
        recommended_batch_size=16,
        memory_efficient=True
    ),
    
    # SECONDARY: Multi-modal retrieval
    # ENSEMBLE MODE: Native 1024D (perfect for ensemble)
    "bge-m3": ModelConfig(
        name="bge-m3",
        hf_model_id="BAAI/bge-m3",
        vector_dim=1024,  # Native 1024D (ensemble-ready)
        max_tokens=8192,
        recommended_batch_size=32,
        memory_efficient=True
    ),
    
    # TERTIARY: Jina Embeddings V4 (Multi-vector + Matryoshka support)
    # ENSEMBLE MODE: Using 1024D Matryoshka for compatibility
    "jina-embeddings-v4": ModelConfig(
        name="jina-embeddings-v4",
        hf_model_id="jinaai/jina-embeddings-v4",
        vector_dim=1024,  # Ensemble dimension (native: 2048D, Matryoshka: 1024D)
        max_tokens=32768,
        query_prefix="",
        recommended_batch_size=16,
        memory_efficient=True
    ),

    # QUINARY: Qwen3 instruction-aware encoder (balanced quality vs params)
    "qwen3-embedding-0.6b": ModelConfig(
        name="qwen3-embedding-0.6b",
        hf_model_id="Qwen/Qwen3-Embedding-0.6B",
        vector_dim=1024,
        max_tokens=32768,
        recommended_batch_size=12,
        memory_efficient=True,
        supports_flash_attention=False
    ),
    
    # QUATERNARY: Qdrant ONNX-optimized (Ultra-fast inference)
    "qdrant-minilm-onnx": ModelConfig(
        name="qdrant-minilm-onnx",
        hf_model_id="Qdrant/all-MiniLM-L6-v2-onnx",
        vector_dim=384,
        max_tokens=256,
        recommended_batch_size=128,  # Large batch for tiny model
        memory_efficient=True
    ),
    
    # ALTERNATIVE: Regular MiniLM (fallback if ONNX unavailable)
    "all-miniLM-l6": ModelConfig(
        name="all-miniLM-l6",
        hf_model_id="sentence-transformers/all-MiniLM-L6-v2",
        vector_dim=384,
        max_tokens=256,
        recommended_batch_size=128,
        memory_efficient=True
    ),
}

# SPARSE EMBEDDING MODELS (V5)
SPARSE_MODELS = {
    # Qdrant BM25 model (term frequency-based)
    "qdrant-bm25": {
        "name": "qdrant-bm25",
        "hf_model_id": "Qdrant/bm25",
        "type": "bm25",
        "description": "BM25-style term frequency sparse vectors",
        "recommended_batch_size": 64
    },
    
    # Qdrant attention-based sparse model
    "qdrant-minilm-attention": {
        "name": "qdrant-minilm-attention",
        "hf_model_id": "Qdrant/all_miniLM_L6_v2_with_attentions",
        "type": "attention",
        "description": "Attention-based sparse vectors from MiniLM",
        "recommended_batch_size": 64
    }
}

# V5 RERANKING MODEL (From V5_MODEL_CONFIGURATIONS.md)
RERANKING_MODELS = {
    # QUATERNARY: Jina Reranker V3 (0.6B params, 131K token context, 256D output)
    # Listwise reranking with multilingual support and code search capability
    "jina-reranker-v3": "jinaai/jina-reranker-v3",
}

@dataclass
class KaggleGPUConfig:
    """Kaggle T4 x2 specific GPU configuration"""
    # Hardware specs
    device_count: int = 2  # T4 x2
    vram_per_gpu_gb: float = 15.83
    total_vram_gb: float = 31.66
    
    # Memory management (reserve 20% for system)
    max_memory_per_gpu: float = 0.8  # 12.66GB usable per GPU
    enable_memory_efficient_attention: bool = True
    gradient_checkpointing: bool = True
    
    # Precision optimization
    precision: str = "fp16"  # Half precision for T4
    enable_mixed_precision: bool = True
    use_amp: bool = True  # Automatic Mixed Precision
    
    # Batch optimization (dynamic based on model)
    base_batch_size: int = 32
    dynamic_batching: bool = True
    max_sequence_length: int = 2048
    
    # Backend optimization
    backend: str = "pytorch"  # pytorch, onnx, tensorrt
    enable_torch_compile: bool = True  # PyTorch 2.0+ optimization
    
    # Multi-GPU strategy
    strategy: str = "data_parallel"  # data_parallel, model_parallel
    enable_gradient_accumulation: bool = True
    accumulation_steps: int = 2
    
    # Kaggle specific
    kaggle_environment: bool = True
    output_path: str = "/kaggle/working"
    
    def get_optimal_batch_size(self, model_config: ModelConfig) -> int:
        """Calculate optimal batch size for model and GPU memory"""
        if not self.dynamic_batching:
            return model_config.recommended_batch_size
        
        # Estimate memory per sample (rough calculation)
        memory_per_token = 4  # bytes for fp16
        tokens_per_sample = min(model_config.max_tokens, self.max_sequence_length)
        model_params = {
            768: 137e6,    # CodeRankEmbed
            1024: 350e6,   # BGE-M3, GTE-Large  
            1536: 1.5e9,   # GTE-Qwen2-1.5B
            4096: 7e9      # E5-Mistral-7B
        }.get(model_config.vector_dim, 350e6)
        
        # Memory estimation
        memory_per_sample = (tokens_per_sample * memory_per_token + 
                           model_params * 2 / self.device_count)  # Split across GPUs
        
        available_memory = self.vram_per_gpu_gb * self.max_memory_per_gpu * 1e9
        optimal_batch = int(available_memory / memory_per_sample * 0.7)  # Safety margin
        
        return max(1, min(optimal_batch, model_config.recommended_batch_size))

@dataclass
class KaggleExportConfig:
    """Export configuration for local Qdrant integration"""
    # Output formats
    export_numpy: bool = True           # .npy files
    export_jsonl: bool = True          # JSONL for Qdrant upload
    export_faiss: bool = True          # FAISS index for fast search
    export_pickle: bool = False        # Pickle for Python compatibility
    export_sparse_jsonl: bool = True   # Sparse vector sidecar JSONL
    
    # Compression
    compress_embeddings: bool = True    # Use float32 instead of float64
    quantize_int8: bool = False        # Int8 quantization for huge collections
    
    # Metadata enrichment
    include_full_metadata: bool = True
    include_processing_stats: bool = True
    include_model_info: bool = True
    
    # Kaggle specific paths
    working_dir: str = "/kaggle/working"
    output_prefix: str = "ultimate_embeddings_v4"
    
    def get_output_path(self, suffix: str = "") -> str:
        """Get full output path for Kaggle"""
        base = f"{self.output_prefix}{suffix}"
        return os.path.join(self.working_dir, base)

@dataclass
class EnsembleConfig:
    """Multi-model ensemble configuration"""
    # Ensemble models: Both support 1024D (Jina Code via Matryoshka, Jina V4 native)
    ensemble_models: List[str] = field(default_factory=lambda: ["jina-code-embeddings-1.5b", "bge-m3", "qwen3-embedding-0.6b"])

    # Ensemble weighting strategy
    weighting_strategy: str = "equal"  # equal, performance_based, adaptive
    model_weights: Optional[Dict[str, float]] = None

    # Ensemble aggregation
    aggregation_method: str = "weighted_average"  # weighted_average, max_pooling, concat

    # Performance optimization
    parallel_encoding: bool = True
    memory_efficient: bool = True

    # Sequential execution toggles
    sequential_passes: bool = False
    sequential_data_parallel: bool = True
    preferred_devices: Optional[List[str]] = None

@dataclass
class RerankingConfig:
    """CrossEncoder reranking configuration"""
    # Reranking model (Jina V3: 0.6B params, 131K context, 256D output)
    model_name: str = "jina-reranker-v3"  # Default: Best quality, long context
    enable_reranking: bool = False
    
    # Reranking parameters
    top_k_candidates: int = 100  # Initial retrieval candidates
    rerank_top_k: int = 20      # Final reranked results
    batch_size: int = 32        # Reranking batch size
    
    # Performance optimization
    enable_caching: bool = True
    cache_size: int = 1000

@dataclass
class AdvancedPreprocessingConfig:
    """Advanced document preprocessing with caching"""
    # Text preprocessing
    enable_text_caching: bool = True
    normalize_whitespace: bool = True
    remove_excessive_newlines: bool = True
    trim_long_sequences: bool = True
    
    # Token optimization
    enable_tokenizer_caching: bool = True
    max_cache_size: int = 10000
    cache_hit_threshold: float = 0.8
    
    # Memory scaling
    enable_memory_scaling: bool = True
    memory_scale_factor: float = 0.8
    adaptive_batch_sizing: bool = True

class AdvancedTextCache:
    """Intelligent text preprocessing cache"""
    
    def __init__(self, max_size: int = 10000):
        self.cache = {}
        self.max_size = max_size
        self.hit_count = 0
        self.miss_count = 0
    
    def _get_text_hash(self, text: str) -> str:
        """Get deterministic hash for text"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()[:16]
    
    def get_processed_text(self, text: str, processor_func) -> str:
        """Get processed text with caching"""
        text_hash = self._get_text_hash(text)
        
        if text_hash in self.cache:
            self.hit_count += 1
            return self.cache[text_hash]
        
        # Process and cache
        processed = processor_func(text)
        
        # Manage cache size
        if len(self.cache) >= self.max_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[text_hash] = processed
        self.miss_count += 1
        return processed
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total = self.hit_count + self.miss_count
        hit_rate = self.hit_count / total if total > 0 else 0
        
        return {
            "cache_size": len(self.cache),
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate,
            "memory_mb": len(str(self.cache).encode('utf-8')) / 1024 / 1024
        }


@dataclass
class GPUMemorySnapshot:
    """Point-in-time view of GPU memory usage."""

    device_id: int
    total_bytes: int
    free_bytes: int
    allocated_bytes: int
    reserved_bytes: int
    timestamp: float = field(default_factory=time.time)

    @property
    def used_bytes(self) -> int:
        return self.total_bytes - self.free_bytes

    @property
    def utilization_ratio(self) -> float:
        return self.used_bytes / max(1, self.total_bytes)

    @property
    def free_gb(self) -> float:
        return self.free_bytes / (1024 ** 3)

    @property
    def total_gb(self) -> float:
        return self.total_bytes / (1024 ** 3)

    def to_dict(self, soft_limit_bytes: Optional[int] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "device_id": self.device_id,
            "total_gb": round(self.total_gb, 2),
            "free_gb": round(self.free_gb, 2),
            "allocated_gb": round(self.allocated_bytes / (1024 ** 3), 2),
            "reserved_gb": round(self.reserved_bytes / (1024 ** 3), 2),
            "utilization": round(self.utilization_ratio, 3),
            "timestamp": self.timestamp,
        }
        if soft_limit_bytes is not None:
            payload["below_soft_limit"] = self.allocated_bytes >= soft_limit_bytes
        return payload


class AdaptiveBatchController:
    """Heuristics for adjusting batch sizes during embedding generation."""

    def __init__(
        self,
        primary_batch: int,
        device_count: int,
        gpu0_soft_limit_bytes: int,
        companion_enabled: bool,
    ) -> None:
        self.device_count = max(1, device_count)
        self.gpu0_soft_limit_bytes = max(0, gpu0_soft_limit_bytes)
        self.primary_batch = max(1, primary_batch)
        self.companion_enabled = companion_enabled
        self._oom_events = 0
        self._updates = 0
        self.total_batch = self._calculate_total_batch()

    def _calculate_total_batch(self) -> int:
        multiplier = max(1, self.device_count)
        return max(1, self.primary_batch * multiplier)

    def _apply_reduction(self, factor: float) -> bool:
        new_batch = max(1, int(self.primary_batch * factor))
        if new_batch < self.primary_batch:
            self.primary_batch = new_batch
            self.total_batch = self._calculate_total_batch()
            self._updates += 1
            return True
        return False

    def register_oom(self, companion_active: bool) -> Optional[Dict[str, Any]]:
        """Handle CUDA out-of-memory by shrinking batch sizes or disabling companions."""

        self._oom_events += 1

        if self.primary_batch > 1:
            self.primary_batch = max(1, self.primary_batch // 2)
            self.total_batch = self._calculate_total_batch()
            return {
                "type": "adaptive_batch_reduce_after_oom",
                "primary_batch": self.primary_batch,
                "total_batch": self.total_batch,
                "oom_events": self._oom_events,
                "companion_disabled": False,
            }

        if companion_active and self.companion_enabled:
            self.companion_enabled = False
            self.total_batch = self._calculate_total_batch()
            return {
                "type": "adaptive_companion_disabled_after_oom",
                "primary_batch": self.primary_batch,
                "total_batch": self.total_batch,
                "oom_events": self._oom_events,
                "companion_disabled": True,
            }

        return None

    def register_snapshot(self, snapshots: Dict[int, GPUMemorySnapshot]) -> Optional[Dict[str, Any]]:
        """Adjust batch sizes when telemetry indicates memory pressure."""

        if not snapshots:
            return None

        primary_snapshot = snapshots.get(0)
        if primary_snapshot is None:
            return None

        free_threshold = max(0, primary_snapshot.total_bytes - self.gpu0_soft_limit_bytes)
        low_memory = (
            primary_snapshot.allocated_bytes >= self.gpu0_soft_limit_bytes
            or primary_snapshot.free_bytes <= free_threshold
        )

        if low_memory:
            if self._apply_reduction(0.75):
                return {
                    "type": "adaptive_batch_reduce_after_snapshot",
                    "primary_batch": self.primary_batch,
                    "total_batch": self.total_batch,
                    "reserved_bytes": primary_snapshot.reserved_bytes,
                    "allocated_bytes": primary_snapshot.allocated_bytes,
                    "free_bytes": primary_snapshot.free_bytes,
                    "companion_disabled": False,
                }

            if self.companion_enabled:
                self.companion_enabled = False
                self.total_batch = self._calculate_total_batch()
                return {
                    "type": "adaptive_companion_disabled_after_snapshot",
                    "primary_batch": self.primary_batch,
                    "total_batch": self.total_batch,
                    "reserved_bytes": primary_snapshot.reserved_bytes,
                    "allocated_bytes": primary_snapshot.allocated_bytes,
                    "free_bytes": primary_snapshot.free_bytes,
                    "companion_disabled": True,
                }

        return None


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
            # Default sparse models
            self.sparse_model_names = ["qdrant-bm25"]
        
        # V5 ENSEMBLE MODE: Default to registry dimension (1024D for ensemble models)
        # matryoshka_dim parameter allows override if needed
        self.matryoshka_dim = matryoshka_dim if matryoshka_dim else self.model_config.vector_dim
        
        # Validate if override is provided
        if matryoshka_dim and matryoshka_dim != self.model_config.vector_dim:
            supported_dims = {128, 256, 512, 1024, 1536, 2048}
            if matryoshka_dim not in supported_dims:
                logger.warning(
                    f"⚠️  Non-standard Matryoshka dimension: {matryoshka_dim}D "
                    f"(registry default: {self.model_config.vector_dim}D)"
                )
            if matryoshka_dim > self.model_config.vector_dim:
                raise ValueError(
                    f"Matryoshka dimension ({matryoshka_dim}) cannot exceed "
                    f"registry dimension ({self.model_config.vector_dim})"
                )
        
        logger.info(
            f"Embedding dimension: {self.matryoshka_dim}D "
            f"(registry: {self.model_config.vector_dim}D, ensemble-ready)"
        )
        
        # Kaggle environment detection
        self.is_kaggle = '/kaggle' in os.getcwd() or os.path.exists('/kaggle')
        if self.is_kaggle:
            logger.info("Kaggle environment detected - optimizing for T4 x2")
            self.gpu_config.kaggle_environment = True
            if not export_config or not self.export_config.working_dir:
                self.export_config.working_dir = "/kaggle/working"
            else:
                working_path = Path(self.export_config.working_dir)
                if not working_path.is_absolute():
                    self.export_config.working_dir = str(Path("/kaggle/working") / working_path)
        
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
            # Adjust Kaggle-specific defaults so CPU execution remains stable
            self.gpu_config.device_count = 1
            self.gpu_config.precision = "fp32"
            self.gpu_config.enable_memory_efficient_attention = False
            self.gpu_config.enable_torch_compile = False
            self.gpu_config.enable_mixed_precision = False
            self.gpu_config.base_batch_size = 8
            self.gpu_config.dynamic_batching = False
        else:
            self.device = "cuda"
            logger.info(f"Detected {self.device_count} GPU(s)")

            # Log GPU information
            for i in range(self.device_count):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1e9
                logger.info(f"  GPU {i}: {gpu_name} ({gpu_memory:.1f}GB)")
        
        # Advanced preprocessing with caching
        self.text_cache = AdvancedTextCache() if self.preprocessing_config.enable_text_caching else None

        # Initialize models
        self.models: Dict[str, Any] = {}  # For ensemble support
        self.primary_model: Optional[SentenceTransformer] = None
        self.reranker = None  # CrossEncoder reranking model

        # V5: Dense companion models (auto-configure based on V5_MODEL_CONFIGURATIONS.md)
        self.companion_dense_model_names: List[str] = companion_dense_models or []
        self.companion_models: Dict[str, SentenceTransformer] = {}
        self.companion_model_configs: Dict[str, ModelConfig] = {}
        self.companion_batch_sizes: Dict[str, int] = {}
        self.companion_device_map: Dict[str, str] = {}
        self.failed_ensemble_models: Set[str] = set()
        self.ensemble_device_map: Dict[str, str] = {}

        # Telemetry & adaptive batching
        self.mitigation_events: List[Dict[str, Any]] = []
        self.cache_events: List[Dict[str, Any]] = []
        self.adaptive_controller: Optional[AdaptiveBatchController] = None
        self.gpu_snapshot_history: List[Dict[str, Any]] = []
        self.latest_gpu_snapshots: Dict[int, GPUMemorySnapshot] = {}
        self.gradient_checkpoint_evaluated: bool = False

        # Sequential ensemble preferences
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
                preferred = [d.strip() for d in device_override.split(",") if d.strip()]
                if preferred:
                    self.ensemble_config.preferred_devices = preferred
            if self.ensemble_config.preferred_devices:
                unique_order: List[str] = []
                for device_candidate in self.ensemble_config.preferred_devices:
                    if device_candidate and device_candidate not in unique_order:
                        unique_order.append(device_candidate)
                for fallback in self.sequential_device_order:
                    if fallback not in unique_order:
                        unique_order.append(fallback)
                self.sequential_device_order = unique_order

        sequential_dp_env = os.environ.get("EMBEDDER_SEQUENTIAL_DATA_PARALLEL")
        if sequential_dp_env and self.ensemble_config:
            self.ensemble_config.sequential_data_parallel = sequential_dp_env.strip().lower() in {"1", "true", "yes", "on"}

        self._initialize_embedding_models()
        self._initialize_companion_models()
        
        # V5: Initialize sparse models if enabled
        if self.enable_sparse:
            self._initialize_sparse_models()
        
        # Initialize reranker if enabled
        if self.reranking_config.enable_reranking:
            self._initialize_reranking_model()
        
        # Storage
        self.embeddings: Optional[np.ndarray] = None
        self.embeddings_by_model: Dict[str, np.ndarray] = {}
        self.chunks_metadata: List[Dict[str, Any]] = []
        self.chunk_texts: List[str] = []
        self.raw_chunk_texts: List[str] = []
        self.sparse_vectors: List[Optional[Dict[str, Any]]] = []
        self.processing_stats: defaultdict[str, List[Any]] = defaultdict(list)
        
        # Performance monitoring
        self.monitor_thread = None
        self.monitoring_active = False

        # Log model availability for debugging
        logger.info("="*70)
        logger.info("MODEL AVAILABILITY CHECK")
        logger.info("="*70)
        logger.info(f"Primary model loaded: {self.primary_model is not None}")
        if self.primary_model:
            model_type = type(self.primary_model).__name__
            logger.info(f"  Model type: {model_type}")
            logger.info(f"  Is DataParallel: {isinstance(self.primary_model, torch.nn.DataParallel)}")
            if hasattr(self.primary_model, 'encode'):
                logger.info(f"  ✓ Has encode() method")
            elif hasattr(self.primary_model, 'module') and hasattr(self.primary_model.module, 'encode'):
                logger.info(f"  ✓ Has encode() method via .module")
            else:
                logger.warning(f"  ✗ No encode() method found!")
        
        if self.companion_models:
            logger.info(f"Companion models loaded: {len(self.companion_models)}")
            for name, model in self.companion_models.items():
                model_type = type(model).__name__
                has_encode = hasattr(model, 'encode') or (hasattr(model, 'module') and hasattr(model.module, 'encode'))
                logger.info(f"  {name}: {model_type}, encode={'✓' if has_encode else '✗'}")
        else:
            logger.info("No companion models loaded")
        
        logger.info("="*70)
        logger.info("Ultimate Kaggle Embedder V4 initialized successfully")
        logger.info("="*70)
    
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

    def _require_embeddings(self) -> np.ndarray:
        """Return embeddings array, raising if it has not been generated."""
        if self.embeddings is None:
            raise RuntimeError("Embeddings have not been generated yet")
        return self.embeddings

    def _record_mitigation(self, event_type: str, **details: Any) -> None:
        """Track mitigation events for telemetry and diagnostics."""

        record = {"type": event_type, "timestamp": time.time(), **details}
        self.mitigation_events.append(record)
        logger.info("Mitigation event captured: %s", record)

    def _ensure_model_snapshot(self, repo_id: str) -> Path:
        """Ensure the Hugging Face snapshot for a model is cached locally."""

        repo_cache_dir = self.hf_cache_dir / f"models--{repo_id.replace('/', '--')}"
        if repo_cache_dir.exists() and not self.force_cache_refresh:
            snapshot_root = next(repo_cache_dir.glob("snapshots/*"), repo_cache_dir)
            event = {
                "model_id": repo_id,
                "path": str(snapshot_root),
                "status": "cache_hit",
            }
            self.cache_events.append(event)
            logger.debug("Cache hit for %s at %s", repo_id, snapshot_root)
            return snapshot_root

        try:
            snapshot_path = snapshot_download(
                repo_id=repo_id,
                cache_dir=str(self.hf_cache_dir),
                local_files_only=self.local_files_only,
                resume_download=not self.force_cache_refresh,
                force_download=self.force_cache_refresh and not self.local_files_only,
            )
        except Exception as exc:  # pragma: no cover - defensive logging
            if isinstance(exc, LocalEntryNotFoundErrorType):
                message = (
                    f"Model {repo_id} not present in local cache and offline mode is enabled."
                )
                logger.error(message)
                raise FileNotFoundError(message) from exc

            logger.error("Snapshot download failed for %s: %s", repo_id, exc)
            raise

        event = {
            "model_id": repo_id,
            "path": snapshot_path,
            "status": "downloaded" if not self.force_cache_refresh else "refreshed",
        }
        self.cache_events.append(event)
        logger.info("Cache ready for %s -> %s", repo_id, snapshot_path)
        return Path(snapshot_path)

    def _build_sentence_transformer_kwargs(
        self,
        device: Optional[str] = None,
        **overrides: Any,
    ) -> Dict[str, Any]:
        """Construct keyword arguments for SentenceTransformer initialization."""

        kwargs: Dict[str, Any] = {
            "device": device or self.device,
            "cache_folder": str(self.hf_cache_dir),
        }
        if self.local_files_only:
            kwargs["local_files_only"] = True
        kwargs.update(overrides)
        return kwargs

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

        return encode_callable(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
            normalize_embeddings=True,
            device=device,
        )

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
        if not snapshots:
            return

        limit_gb = self.gpu0_soft_limit_bytes / (1024 ** 3)
        snapshot_payload = {
            "timestamp": time.time(),
            "soft_limit_gb": round(limit_gb, 2),
            "devices": {device: snap.to_dict(self.gpu0_soft_limit_bytes if device == 0 else None) for device, snap in snapshots.items()},
        }
        snapshot_payload["low_memory_devices"] = [
            device
            for device, snap in snapshots.items()
            if (device == 0 and snap.allocated_bytes >= self.gpu0_soft_limit_bytes)
        ]

        self.gpu_snapshot_history.append(snapshot_payload)
        # Keep last 50 snapshots to bound memory usage
        if len(self.gpu_snapshot_history) > 50:
            self.gpu_snapshot_history = self.gpu_snapshot_history[-50:]

        self.latest_gpu_snapshots = snapshots

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
        if not self.gpu_snapshot_history:
            return {}

        latest = self.gpu_snapshot_history[-1]
        peak_alloc_gb = 0.0
        peak_device = None
        for device_id, snapshot in latest["devices"].items():
            allocated = snapshot.get("allocated_gb", 0.0)
            if allocated > peak_alloc_gb:
                peak_alloc_gb = allocated
                peak_device = device_id

        return {
            "latest": latest,
            "peak_device": peak_device,
            "peak_allocated_gb": round(peak_alloc_gb, 2),
            "events_recorded": len(self.gpu_snapshot_history),
        }

    def _maybe_enable_transformer_checkpointing(self, model: SentenceTransformer) -> None:
        """Enable gradient checkpointing when supported and requested."""

        if not self.gpu_config.gradient_checkpointing:
            return

        target = None
        if hasattr(model, "model"):
            target = model.model
        elif hasattr(model, "_model"):
            target = model._model

        if target is None:
            return

        try:
            if hasattr(target, "gradient_checkpointing_enable"):
                target.gradient_checkpointing_enable()  # type: ignore[attr-defined]
                self._record_mitigation(
                    "gradient_checkpointing_enabled",
                    model=getattr(model, "name_or_path", self.model_name),
                )
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.debug("Gradient checkpointing enable failed: %s", exc)

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

        if self.device != "cuda" or not torch.cuda.is_available():
            return {}

        snapshots: Dict[int, GPUMemorySnapshot] = {}

        for device_id in range(self.device_count):
            try:
                free_bytes, total_bytes = torch.cuda.mem_get_info(device_id)
            except RuntimeError:
                total_bytes = torch.cuda.get_device_properties(device_id).total_memory
                free_bytes = max(0, total_bytes - torch.cuda.memory_allocated(device_id))

            allocated_bytes = torch.cuda.memory_allocated(device_id)
            reserved_bytes = torch.cuda.memory_reserved(device_id)

            snapshots[device_id] = GPUMemorySnapshot(
                device_id=device_id,
                total_bytes=int(total_bytes),
                free_bytes=int(free_bytes),
                allocated_bytes=int(allocated_bytes),
                reserved_bytes=int(reserved_bytes),
            )

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
        
    def _initialize_embedding_models(self):
        """Initialize embedding models with advanced optimization"""

        logger.info(f"Loading embedding model: {self.model_config.hf_model_id}")

        # Optimal batch size for this model
        optimal_batch = self.gpu_config.get_optimal_batch_size(self.model_config)
        logger.info(f"Optimal batch size: {optimal_batch}")

        # Model loading configuration
        model_kwargs = self._build_sentence_transformer_kwargs()
        model_kwargs["trust_remote_code"] = self.model_config.trust_remote_code
        
        # Precision optimization for T4
        if self.gpu_config.precision == "fp16" and self.device == "cuda":
            model_kwargs["torch_dtype"] = torch.float16
            logger.info("Using FP16 precision for T4 optimization")
        
        # Flash Attention for supported models
        # NOTE: Flash Attention 2 requires sentence-transformers >= 3.0.0 and flash-attn package
        # However, attn_implementation is NOT a SentenceTransformer parameter - it's for the underlying model
        # sentence-transformers 3.0+ will automatically use Flash Attention if available
        if (self.model_config.supports_flash_attention and
            self.gpu_config.enable_memory_efficient_attention):
            try:
                import sentence_transformers
                st_version = tuple(map(int, sentence_transformers.__version__.split('.')[:2]))
                if st_version >= (3, 0):
                    logger.info("Flash Attention 2 will be used automatically (sentence-transformers >= 3.0)")
                else:
                    logger.info(f"Flash Attention requires sentence-transformers >= 3.0.0 (current: {sentence_transformers.__version__})")
            except Exception as e:
                logger.debug(f"Flash Attention check failed: {e}")
        
        # Ensure model artifacts are available locally
        try:
            self._ensure_model_snapshot(self.model_config.hf_model_id)
        except Exception as exc:
            logger.warning("Snapshot preparation failed for %s: %s", self.model_config.hf_model_id, exc)

        # Backend optimization
        if self.gpu_config.backend == "onnx" and ONNX_AVAILABLE:
            logger.info("Attempting ONNX backend optimization...")
            try:
                self.primary_model = self._load_onnx_model()
                logger.info("ONNX backend loaded successfully")
            except Exception as e:
                logger.warning(f"ONNX backend failed, using PyTorch: {e}")
                self.primary_model = self._load_pytorch_model(model_kwargs, optimal_batch)
        else:
            self.primary_model = self._load_pytorch_model(model_kwargs, optimal_batch)

        if isinstance(self.primary_model, SentenceTransformer):
            self._maybe_enable_transformer_checkpointing(self.primary_model)
        
        # Store for ensemble if needed
        self.models[self.model_name] = self.primary_model
        
        # Initialize ensemble models if enabled
        if self.enable_ensemble:
            self._initialize_ensemble_models()
        
        # Memory optimization
        if self.device == "cuda":
            torch.cuda.empty_cache()
            logger.info("GPU memory cache cleared")
    
    def _initialize_companion_models(self) -> None:
        """Load additional dense encoders that accompany the primary model."""

        if not self.companion_dense_model_names:
            return

        for companion_name in self.companion_dense_model_names:
            if companion_name == self.model_name:
                logger.debug("Skipping companion %s because it matches the primary model", companion_name)
                continue

            config = KAGGLE_OPTIMIZED_MODELS.get(companion_name)
            if config is None:
                logger.warning("Companion model %s not found in registry; skipping", companion_name)
                continue

            if companion_name in self.companion_models:
                continue

            try:
                logger.info("Loading companion dense model: %s (%sD)", config.hf_model_id, config.vector_dim)

                target_device = "cpu"
                if self.device == "cuda":
                    if self.device_count > 1:
                        target_device = "cuda:1"
                        self.companion_device_map[companion_name] = target_device
                        self._record_mitigation("companion_gpu_routed", companion=companion_name, device=target_device)
                    else:
                        target_device = "cuda:0"
                        self.companion_device_map[companion_name] = target_device
                        self._record_mitigation("companion_gpu_shared", companion=companion_name, device=target_device)
                else:
                    self.companion_device_map[companion_name] = target_device
                    self._record_mitigation("companion_cpu_fallback", companion=companion_name)

                self._ensure_model_snapshot(config.hf_model_id)
                companion_kwargs = self._build_sentence_transformer_kwargs(device=target_device)
                companion_kwargs["trust_remote_code"] = config.trust_remote_code

                model = SentenceTransformer(
                    config.hf_model_id,
                    **companion_kwargs,
                )

                if self.gpu_config.precision == "fp16" and target_device.startswith("cuda"):
                    model = model.half()

                if self.gpu_config.gradient_checkpointing:
                    self._maybe_enable_transformer_checkpointing(model)

                self.companion_models[companion_name] = model
                self.companion_model_configs[companion_name] = config
                batch_size = self.gpu_config.get_optimal_batch_size(config)
                if target_device == "cpu":
                    batch_size = max(1, min(batch_size, 4))
                self.companion_batch_sizes[companion_name] = batch_size
                self.models.setdefault(companion_name, model)
                logger.info("Companion model %s ready (batch size %s, device %s)", companion_name, batch_size, target_device)
            except Exception as exc:
                logger.error("Failed to load companion model %s: %s", companion_name, exc)
                self._record_mitigation("companion_missing", companion=companion_name, error=str(exc))

        if self.device == "cuda" and self.companion_models:
            torch.cuda.empty_cache()
    
    def _initialize_sparse_models(self) -> None:
        """
        Initialize sparse embedding models (V5 feature).
        
        Sparse models generate BM25-style or attention-based sparse vectors
        for hybrid search in Qdrant.
        """
        
        if not self.sparse_model_names:
            logger.info("No sparse models specified")
            return
        
        logger.info(f"Loading sparse models: {self.sparse_model_names}")
        
        for sparse_name in self.sparse_model_names:
            if sparse_name not in SPARSE_MODELS:
                logger.warning(f"Unknown sparse model: {sparse_name}, skipping")
                continue
            
            sparse_config = SPARSE_MODELS[sparse_name]
            
            try:
                logger.info(f"Loading sparse model: {sparse_config['hf_model_id']}")
                
                # Load sparse model using SentenceTransformer
                # Note: Actual implementation depends on model type
                sparse_model = SentenceTransformer(
                    sparse_config["hf_model_id"],
                    trust_remote_code=True,
                    device=self.device
                )
                
                self.sparse_models[sparse_name] = sparse_model
                logger.info(f"✓ Sparse model {sparse_name} loaded successfully")
                
            except Exception as e:
                logger.error(f"Failed to load sparse model {sparse_name}: {e}")
        
        if self.sparse_models:
            logger.info(f"Loaded {len(self.sparse_models)} sparse models")
        else:
            logger.warning("No sparse models loaded successfully")
            self.enable_sparse = False

    def _initialize_reranking_model(self):
        """Initialize CrossEncoder for reranking"""
        
        if not self.reranking_config.model_name in RERANKING_MODELS:
            logger.warning(f"Unknown reranker {self.reranking_config.model_name}, defaulting to jina-reranker-v3")
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
    
    def _initialize_ensemble_models(self):
        """Initialize multiple models for ensemble embedding"""
        
        if not self.enable_ensemble or not self.ensemble_config:
            return

        if self.embedding_backend != "local":
            logger.info("Companion models are unavailable for API-backed embeddings")
            return
        
        logger.info(f"Loading ensemble models: {self.ensemble_config.ensemble_models}")
        
        for model_name in self.ensemble_config.ensemble_models:
            if model_name not in KAGGLE_OPTIMIZED_MODELS:
                logger.warning(f"Unknown ensemble model {model_name}, skipping")
                continue
            
            if model_name == self.model_name:
                # Primary model already loaded
                continue
            
            try:
                model_config = KAGGLE_OPTIMIZED_MODELS[model_name]
                logger.info(f"Loading ensemble model: {model_config.hf_model_id}")
                
                # Load with minimal configuration for ensemble
                ensemble_model = SentenceTransformer(
                    model_config.hf_model_id,
                    trust_remote_code=model_config.trust_remote_code,
                    device=self.device
                )
                
                # Apply FP16 if needed
                if self.gpu_config.precision == "fp16" and self.device == "cuda":
                    ensemble_model = ensemble_model.half()
                
                self.models[model_name] = ensemble_model
                logger.info(f"Ensemble model {model_name} loaded")
                
            except Exception as e:
                logger.error(f"Failed to load ensemble model {model_name}: {e}")
    
    def generate_ensemble_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings using ensemble of models"""
        
        if not self.enable_ensemble or not self.ensemble_config:
            logger.debug("Ensemble not enabled, using primary model only")
            primary_model = self._get_primary_model()
            primary_batch = self._get_batch_hint_for_model(self.model_name)

            self._log_gpu_memory("Primary encode (non-ensemble) - before")
            result = self._call_encode(
                primary_model,
                texts,
                batch_size=primary_batch,
                device=self.device,
            )
            result = self._normalize_embedding_matrix(result, self.model_name)
            self._log_gpu_memory("Primary encode (non-ensemble) - after")

            if self.device == "cuda":
                torch.cuda.empty_cache()

            return result

        sequential_mode = bool(self.ensemble_config.sequential_passes)
        model_weights: Dict[str, float] = {}
        all_embeddings: List[np.ndarray] = []
        successful_models: List[str] = []

        ordered_models: List[str] = []
        seen: Set[str] = set()
        for candidate in [self.model_name, *self.ensemble_config.ensemble_models]:
            if candidate not in seen:
                ordered_models.append(candidate)
                seen.add(candidate)

        if not sequential_mode:
            for model_name in ordered_models:
                model = self._get_or_load_ensemble_model(model_name)
                if model is None:
                    continue
                batch_hint = self._get_batch_hint_for_model(model_name)

                try:
                    logger.debug("[ENSEMBLE] Parallel encode with %s", model_name)
                    self._log_gpu_memory(f"Ensemble encode before {model_name}")
                    embeddings = self._call_encode(
                        model,
                        texts,
                        batch_size=batch_hint,
                        device=self.device,
                    )
                    embeddings = self._normalize_embedding_matrix(embeddings, model_name)
                    self._log_gpu_memory(f"Ensemble encode after {model_name}")
                except Exception as exc:
                    logger.warning("Failed to generate embeddings with %s: %s", model_name, exc)
                    continue

                all_embeddings.append(embeddings)
                successful_models.append(model_name)
                model_weights[model_name] = (
                    self.ensemble_config.model_weights.get(model_name, 1.0)
                    if self.ensemble_config.model_weights
                    else 1.0
                )

        else:
            for model_name in ordered_models:
                model = self._get_or_load_ensemble_model(model_name)
                if model is None:
                    continue
                batch_hint = self._get_batch_hint_for_model(model_name)
                target_device = self._select_sequential_device(model_name)
                current_device = target_device
                current_batch_hint = batch_hint
                pass_start = time.time()
                embeddings: Optional[np.ndarray] = None

                try:
                    if hasattr(model, "to"):
                        model = model.to(target_device)
                        self.models[model_name] = model
                except Exception as exc:
                    logger.warning("Failed to move model %s to %s: %s", model_name, target_device, exc)
                    self._record_mitigation(
                        "ensemble_move_failed",
                        model=model_name,
                        device=target_device,
                        error=str(exc)[:300],
                    )
                    base_model = self._unwrap_model(model)
                    if hasattr(base_model, "to"):
                        try:
                            base_model = cast(Any, base_model.to("cpu"))
                        except Exception as move_exc:
                            logger.warning("CPU fallback conversion failed for %s: %s", model_name, move_exc)
                        else:
                            model = base_model
                    current_device = "cpu"
                    self.models[model_name] = model

                self._record_mitigation(
                    "ensemble_pass_started",
                    model=model_name,
                    device=current_device,
                    batch_size=current_batch_hint,
                )

                success = False
                retries = 0
                max_retries = 3

                while retries <= max_retries:
                    try:
                        self._log_gpu_memory(f"Sequential ensemble encode before {model_name} @ {current_device}")
                        embeddings = self._call_encode(
                            model,
                            texts,
                            batch_size=current_batch_hint,
                            device=current_device,
                        )
                        embeddings = self._normalize_embedding_matrix(embeddings, model_name)
                        self._log_gpu_memory(f"Sequential ensemble encode after {model_name} @ {current_device}")
                        success = True
                        break
                    except RuntimeError as exc:
                        message = str(exc)
                        if "out of memory" in message.lower():
                            self._record_mitigation(
                                "ensemble_pass_oom",
                                model=model_name,
                                device=current_device,
                                batch_size=current_batch_hint,
                                retry=retries,
                            )
                            if torch.cuda.is_available() and current_device.startswith("cuda"):
                                torch.cuda.empty_cache()
                                gc.collect()
                                if current_batch_hint > 1:
                                    current_batch_hint = max(1, current_batch_hint // 2)
                                    retries += 1
                                    self._record_mitigation(
                                        "ensemble_pass_batch_reduced",
                                        model=model_name,
                                        batch_size=current_batch_hint,
                                    )
                                    continue
                                base_model = self._unwrap_model(model)
                                if hasattr(base_model, "to"):
                                    try:
                                        base_model = cast(Any, base_model.to("cpu"))
                                    except Exception as move_exc:
                                        logger.warning("Failed to move model %s to CPU fallback: %s", model_name, move_exc)
                                    else:
                                        model = base_model
                                        self.models[model_name] = model
                                current_device = "cpu"
                                retries += 1
                                self._record_mitigation(
                                    "ensemble_pass_cpu_fallback",
                                    model=model_name,
                                )
                                continue
                        self._record_mitigation(
                            "ensemble_pass_failed",
                            model=model_name,
                            device=current_device,
                            error=message[:500],
                        )
                        logger.warning("Sequential ensemble pass failed for %s: %s", model_name, message)
                        break
                    except Exception as exc:
                        message = str(exc)
                        self._record_mitigation(
                            "ensemble_pass_failed",
                            model=model_name,
                            device=current_device,
                            error=message[:500],
                        )
                        logger.warning("Sequential ensemble pass failed for %s: %s", model_name, message)
                        break

                if not success or embeddings is None:
                    self.failed_ensemble_models.add(model_name)
                    continue

                pass_duration = time.time() - pass_start
                self._record_mitigation(
                    "ensemble_pass_completed",
                    model=model_name,
                    device=current_device,
                    duration=pass_duration,
                    batch_size=current_batch_hint,
                )
                self.ensemble_device_map[model_name] = current_device

                all_embeddings.append(embeddings)
                successful_models.append(model_name)
                model_weights[model_name] = (
                    self.ensemble_config.model_weights.get(model_name, 1.0)
                    if self.ensemble_config.model_weights
                    else 1.0
                )

                if current_device.startswith("cuda"):
                    torch.cuda.synchronize()
                    torch.cuda.empty_cache()

                if current_device.startswith("cuda") and model_name != self.model_name:
                    try:
                        if hasattr(model, "to"):
                            model = cast(Any, model.to("cpu"))
                            self.models[model_name] = model
                    except Exception as exc:
                        logger.warning("Failed to move model %s to CPU post-pass: %s", model_name, exc)
                    gc.collect()

        if not all_embeddings:
            logger.error(
                "No ensemble models generated embeddings successfully - falling back to primary model"
            )
            primary_model = self._get_primary_model()
            fallback_embeddings = self._call_encode(
                primary_model,
                texts,
                batch_size=self._get_batch_hint_for_model(self.model_name),
                device=self.device,
            )
            return self._normalize_embedding_matrix(fallback_embeddings, self.model_name)

        row_counts = [emb.shape[0] for emb in all_embeddings]
        min_rows = min(row_counts)
        if max(row_counts) != min_rows:
            self._record_mitigation(
                "ensemble_row_mismatch",
                models=successful_models,
                row_counts=row_counts[:5],
                min_rows=min_rows,
            )
        trimmed_rows = [emb[:min_rows] for emb in all_embeddings]

        if min_rows == 0:
            if self.ensemble_config.aggregation_method == "concat":
                total_dim = sum(emb.shape[1] for emb in trimmed_rows)
                return np.empty((0, total_dim), dtype=np.float32)
            base_dim = trimmed_rows[0].shape[1] if trimmed_rows else 0
            return np.empty((0, base_dim), dtype=np.float32)

        final_embeddings: np.ndarray

        if self.ensemble_config.aggregation_method == "concat":
            final_embeddings = np.concatenate(trimmed_rows, axis=1)
        else:
            dims = [emb.shape[1] for emb in trimmed_rows]
            min_dim = min(dims)
            if max(dims) != min_dim:
                self._record_mitigation(
                    "ensemble_dim_mismatch",
                    models=successful_models,
                    min_dim=min_dim,
                    max_dim=max(dims),
                    sample_dims=dims[:5],
                )
            aligned = [emb[:, :min_dim] for emb in trimmed_rows]
            stacked = np.stack(aligned, axis=0)

            method = self.ensemble_config.aggregation_method
            if method == "weighted_average":
                weights = np.array([model_weights.get(name, 1.0) for name in successful_models], dtype=np.float32)
                weight_sum = float(weights.sum())
                if not np.isfinite(weight_sum) or weight_sum <= 0:
                    weights = np.ones_like(weights) / len(weights)
                else:
                    weights = weights / weight_sum
                final_embeddings = np.tensordot(weights, stacked, axes=(0, 0))
            elif method == "max_pooling":
                final_embeddings = stacked.max(axis=0)
            else:
                final_embeddings = stacked.mean(axis=0)

        final_embeddings = normalize(final_embeddings, norm="l2", axis=1)
        return final_embeddings
    
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
        """Advanced text preprocessing with caching"""
        
        if not self.preprocessing_config.enable_text_caching or not self.text_cache:
            return self._preprocess_text_core(text)
        
        return self.text_cache.get_processed_text(text, self._preprocess_text_core)
    
    def _preprocess_text_core(self, text: str) -> str:
        """Core text preprocessing logic"""
        
        if self.preprocessing_config.normalize_whitespace:
            # Normalize whitespace
            text = ' '.join(text.split())
        
        if self.preprocessing_config.remove_excessive_newlines:
            # Remove excessive newlines (keep max 2)
            import re
            text = re.sub(r'\n{3,}', '\n\n', text)
        
        if self.preprocessing_config.trim_long_sequences:
            # Trim to model's max tokens (rough estimation)
            max_chars = self.model_config.max_tokens * 4  # ~4 chars per token
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
        
        return text

    @staticmethod
    def _build_hierarchy_path(section_path: Optional[List[str]]) -> str:
        """Format hierarchical section path for display/search."""

        if not section_path:
            return ""
        return " > ".join(part.strip() for part in section_path if isinstance(part, str) and part.strip())

    @staticmethod
    def _normalize_collection_name(raw_name: str) -> str:
        """Map raw collection folder names to canonical Qdrant collections."""

        if not raw_name:
            return "qdrant_ecosystem"

        normalized = raw_name.strip().lower().replace('-', '_').replace(' ', '_')

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
        """Infer the Qdrant collection name that should receive the current export."""

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

        canonical = None
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

    @staticmethod
    def _ensure_document_id(metadata: Dict[str, Any]) -> None:
        """Ensure metadata contains a stable document identifier."""

        if metadata.get("document_id"):
            return

        source_hint = metadata.get("source_path") or metadata.get("source_file") or metadata.get("filename")
        if not source_hint:
            return

        normalized = Path(str(source_hint)).as_posix().lower()
        metadata["document_id"] = hashlib.md5(normalized.encode("utf-8")).hexdigest()[:12]
        metadata.setdefault("document_name", Path(str(source_hint)).stem)

    @staticmethod
    def _stable_term_index(term: str) -> int:
        """Deterministically map a token string to a 32-bit integer index."""

        digest = hashlib.sha1(term.encode("utf-8")).hexdigest()[:8]
        return int(digest, 16)

    def _build_sparse_vector_from_metadata(self, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform sparse term statistics into a hashed sparse vector payload."""

        sparse = metadata.get("sparse_features")
        if not isinstance(sparse, dict):
            return None

        term_weights = sparse.get("term_weights")
        if not isinstance(term_weights, list):
            return None

        indices: List[int] = []
        values: List[float] = []
        tokens: List[str] = []

        for entry in term_weights:
            term = entry.get("term")
            weight = entry.get("weight")
            if not isinstance(term, str):
                continue
            if not isinstance(weight, (int, float)):
                continue
            index = self._stable_term_index(term)
            indices.append(index)
            values.append(float(weight))
            tokens.append(term)

        if not indices:
            return None

        vector = np.array(values, dtype=np.float32)
        norm = float(np.linalg.norm(vector))
        if norm > 0:
            normalized_values = (vector / norm).tolist()
        else:
            normalized_values = vector.tolist()

        return {
            "indices": indices,
            "values": normalized_values,
            "tokens": tokens,
            "stats": {
                "weight_norm": norm,
                "unique_terms": sparse.get("unique_terms", len(tokens)),
                "total_terms": sparse.get("total_terms", 0),
                "weighting": sparse.get("weighting", "tf-normalized"),
            }
        }

    @staticmethod
    def _infer_modal_hint(text: str, metadata: Dict[str, Any]) -> Optional[str]:
        """Infer a modal hint, favouring metadata from the chunker when available."""

        hint = metadata.get("modal_hint")
        if isinstance(hint, str) and hint.strip():
            return hint.strip()

        flags = metadata.get("content_flags") or {}
        if isinstance(flags, dict):
            if flags.get("has_table"):
                return "table"
            if flags.get("has_code_block"):
                return "code"
            if flags.get("has_list"):
                return "list"
            if flags.get("has_json"):
                return "json"

        sample = text.strip().lower()[:400]
        if "```" in text or "def " in sample or "class " in sample:
            return "code"
        if "|" in text and "\n|" in text:
            return "table"
        if sample.startswith("{") or sample.startswith("["):
            return "json"

        return "prose" if text.strip() else None
    
    def _resolve_chunks_directory(self, preferred_dir: str) -> Tuple[Optional[Path], List[Path]]:
        """Resolve the most likely chunks directory, mirroring Kaggle input layout."""

        attempted: List[Path] = []
        candidates: List[Path] = []
        project_root = Path(__file__).resolve().parents[1]

        preferred_path = Path(preferred_dir)
        candidates.extend([
            preferred_path,
            preferred_path / "Chunked",
            preferred_path / "chunked",
        ])

        if self.is_kaggle:
            # Prefer the working directory used by the notebook runtime
            candidates.extend([
                Path("/kaggle/working/rag_clean/Chunked"),
                Path("/kaggle/working/Chunked"),
            ])

            # Mirror Kaggle's /kaggle/input/<dataset>/Chunked structure
            kaggle_root = Path("/kaggle/input")
            if kaggle_root.exists():
                for dataset_dir in sorted(kaggle_root.iterdir()):
                    if not dataset_dir.is_dir():
                        continue
                    candidates.extend([
                        dataset_dir / "Chunked",
                        dataset_dir / "chunked",
                        dataset_dir,
                    ])

            # Common fallback names from upload script
            candidates.extend([
                Path("/kaggle/input/docs-chunks-output"),
                Path("/kaggle/input/docs-chunks-output/Chunked"),
            ])
        else:
            local_root = project_root / "DOCS_CHUNKS_OUTPUT"
            candidates.extend([
                project_root / "Chunked",
                project_root / "chunked",
                project_root / "output" / "Chunked",
                local_root,
                local_root / "Chunked",
                local_root / "chunked",
                Path(r"C:\Users\raze0\Documents\LLM_KNOWLEDGE_CREATOR\RAG\RAG_CLEAN\DOCS_CHUNKS_OUTPUT"),
            ])

        seen: Set[Path] = set()

        def looks_like_chunk_dir(path: Path) -> bool:
            if not path.exists() or path.is_file():
                return False
            try:
                for entry in path.iterdir():
                    if entry.is_dir():
                        return True
                    if entry.suffix.lower() == ".json":
                        return True
            except Exception:
                return False
            return False

        for candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)
            attempted.append(candidate)
            if looks_like_chunk_dir(candidate):
                logger.info(f"Resolved chunks directory to {candidate}")
                return candidate, attempted

        return None, attempted
    
    def load_chunks_from_processing(
        self,
        chunks_dir: str = "/kaggle/working/rag_clean/Chunked"
    ) -> Dict[str, Any]:
        """Load processed chunks, preferring Kaggle's working `Chunked` folder when present."""
        
        preferred_dir = chunks_dir
        if not self.is_kaggle:
            preferred_dir = r"C:\Users\raze0\Documents\LLM_KNOWLEDGE_CREATOR\RAG\RAG_CLEAN\DOCS_CHUNKS_OUTPUT"

        chunks_path, attempted_paths = self._resolve_chunks_directory(preferred_dir)

        if chunks_path is None:
            logger.error("Chunks directory not found. Tried: %s", ", ".join(str(p) for p in attempted_paths))
            if self.is_kaggle:
                logger.info("On Kaggle: ensure the uploaded dataset contains a Chunked/ directory")
            return {"error": "Chunks directory not found"}

        logger.info(f"Loading chunks from {chunks_path}")
        
        results = {
            "collections_loaded": 0,
            "total_chunks_loaded": 0,
            "chunks_by_collection": {},
            "loading_errors": [],
            "memory_usage_mb": 0,
            "preprocessing_stats": {},
            "sparse_vectors_generated": 0,
            "modal_hint_counts": {}
        }
        
        # Reset storage
        self.chunks_metadata = []
        self.chunk_texts = []
        self.raw_chunk_texts = []
        self.sparse_vectors = []
        self._canonical_collection_hint = None
        self._target_collection_cache = None

        modal_hint_distribution: defaultdict[str, int] = defaultdict(int)
        
        # Collection priorities (Qdrant knowledge base insights)
        collection_priorities = {
            "qdrant_ecosystem": 1.0,
            "sentence_transformers": 0.9,
            "docling": 0.8,
            "fast_docs": 0.7,
            "pydantic": 0.6
        }
        
        # Detect if we're loading a single collection or multiple
        # Ignore processing summary files when detecting structure
        has_json_files = any(
            f.suffix == '.json' and not f.name.endswith('_processing_summary.json') 
            for f in chunks_path.iterdir() if f.is_file()
        )
        
        if has_json_files:
            # Single collection mode: load JSON files directly from this path
            collection_name = chunks_path.name
            canonical_collection = self._normalize_collection_name(collection_name)
            collection_chunks = 0
            priority = collection_priorities.get(canonical_collection, 0.5)
            
            logger.info(f"Loading single collection: {collection_name} -> {canonical_collection}")
            self._canonical_collection_hint = canonical_collection
            
            # Enhanced glob patterns to catch all chunk file variations
            chunk_file_patterns = [
                "*_chunks.json",    # Standard pattern
                "*chunks.json",     # Without underscore
                "*.json"            # Any JSON file
            ]
            
            chunk_files_found = []
            for pattern in chunk_file_patterns:
                chunk_files_found.extend(list(chunks_path.glob(pattern)))
            
            # Remove duplicates
            chunk_files_found = list(set(chunk_files_found))
            
            logger.info(f"Found {len(chunk_files_found)} JSON files matching patterns")
            
            if not chunk_files_found:
                # List all files in directory for debugging
                all_files = list(chunks_path.iterdir())
                logger.warning(f"No chunk files found; directory contains {len(all_files)} items:")
                for f in all_files[:10]:  # Show first 10 items
                    logger.warning(f"   - {f.name} ({'file' if f.is_file() else 'dir'})")
            
            for chunk_file in chunk_files_found:
                try:
                    with open(chunk_file, 'r', encoding='utf-8') as f:
                        file_chunks = json.load(f)
                    
                    for chunk in file_chunks:
                        metadata = chunk.get("metadata", {}) or {}

                        # Quality filtering
                        token_count = metadata.get("token_count", 0)
                        if token_count < 50:  # Skip very small chunks
                            continue

                        # Advanced text preprocessing
                        original_text = chunk["text"]
                        processed_text = self.preprocess_text_advanced(original_text)

                        # Enhanced metadata harmonised with MCP/Qdrant server
                        chunk_id = len(self.chunks_metadata)
                        hierarchy_path = metadata.get("hierarchy_path") or self._build_hierarchy_path(metadata.get("section_path"))

                        collection_hints_raw = metadata.get("collection_hints") or metadata.get("qdrant_collection_hint")
                        if isinstance(collection_hints_raw, str):
                            collection_hints = [collection_hints_raw]
                        elif collection_hints_raw:
                            # Preserve order while deduplicating
                            seen = set()
                            collection_hints = [hint for hint in collection_hints_raw if not (hint in seen or seen.add(hint))]
                        else:
                            collection_hints = [canonical_collection]

                        metadata_updates = {
                            "global_chunk_id": chunk_id,
                            "collection_priority": priority,
                            "quality_score": min(1.0, token_count / 1000),
                            "text_preprocessing_applied": True,
                            "original_length": len(original_text),
                            "processed_length": len(processed_text),
                            "full_text_length": len(original_text),
                            "kaggle_processing_timestamp": datetime.now().isoformat(),
                            "model_target": self.model_name,
                            "embedding_dimension": self.model_config.vector_dim,
                            "qdrant_collection": canonical_collection,
                            "collection_alias": collection_name,
                            "collection_hints": collection_hints,
                            "hierarchy_path": hierarchy_path,
                        }

                        metadata.update(metadata_updates)
                        metadata["qdrant_collection_hint"] = metadata["collection_hints"]
                        metadata.setdefault("payload_version", "1.2")
                        metadata.setdefault("source_path", metadata.get("source_file") or metadata.get("filename") or str(chunk_file))
                        metadata.setdefault("source_file", metadata["source_path"])
                        metadata.setdefault("source_filename", Path(str(metadata["source_file"])).name)
                        metadata.setdefault("document_name", Path(str(metadata["source_file"])).stem)
                        metadata.setdefault("chunk_hash", metadata.get("chunk_hash") or hashlib.sha1(original_text.encode("utf-8")).hexdigest()[:16])
                        metadata.setdefault("content_digest", metadata["chunk_hash"])
                        metadata.setdefault("content_type", metadata.get("content_type", "hierarchical_section"))

                        keywords = set(k for k in metadata.get("search_keywords", []) if isinstance(k, str))
                        if hierarchy_path:
                            keywords.update(part.strip() for part in hierarchy_path.split(" > ") if part.strip())
                        if metadata.get("heading_text"):
                            keywords.add(metadata["heading_text"])
                        metadata["search_keywords"] = sorted(k for k in keywords if k)

                        modal_hint = self._infer_modal_hint(original_text, metadata)
                        if modal_hint:
                            metadata["modal_hint"] = modal_hint
                            metadata.setdefault("embedding_modal_hint", modal_hint)
                            modal_hint_distribution[modal_hint] += 1

                        sparse_vector = self._build_sparse_vector_from_metadata(metadata)
                        self.sparse_vectors.append(sparse_vector)
                        if sparse_vector:
                            results["sparse_vectors_generated"] += 1
                            metadata["sparse_vector"] = sparse_vector
                        else:
                            metadata.pop("sparse_vector", None)

                        metadata["sparse_vector_tokens"] = sparse_vector.get("tokens") if sparse_vector else []
                        metadata["sparse_vector_weight_norm"] = sparse_vector.get("stats", {}).get("weight_norm") if sparse_vector else 0.0

                        self._ensure_document_id(metadata)

                        chunk["metadata"] = metadata
                        self.chunks_metadata.append(metadata)
                        self.chunk_texts.append(processed_text)
                        self.raw_chunk_texts.append(original_text)
                        collection_chunks += 1
                    
                    logger.debug(f"  Loaded {len(file_chunks)} chunks from {chunk_file.name}")
                    
                except Exception as e:
                    error_msg = f"Error loading {chunk_file}: {e}"
                    logger.error(f"Error: {error_msg}")
                    results["loading_errors"].append(error_msg)
            
            results["chunks_by_collection"][collection_name] = collection_chunks
            results["collections_loaded"] += 1
            logger.info(f"Collection '{collection_name}': {collection_chunks} chunks (priority: {priority})")
        
        else:
            # Multi-collection mode: iterate through subdirectories
            logger.info(f"Multi-collection mode: scanning subdirectories in {chunks_path}")
            subdirs = [d for d in chunks_path.iterdir() if d.is_dir() and d.name != "__pycache__"]
            logger.info(f"Found {len(subdirs)} subdirectories: {[d.name for d in subdirs]}")
            
            for collection_dir in subdirs:
                collection_name = collection_dir.name
                collection_chunks = 0
                
                logger.info(f"Processing subdirectory: {collection_name}")
                priority = collection_priorities.get(collection_name, 0.5)
                canonical_collection = self._normalize_collection_name(collection_name)
                
                # Enhanced debugging for multi-collection mode
                chunk_files_found = list(collection_dir.rglob("*_chunks.json"))
                logger.info(f"   Pattern *_chunks.json: Found {len(chunk_files_found)} files")
                
                if not chunk_files_found:
                    # Debug: Try other patterns
                    all_json = list(collection_dir.rglob("*.json"))
                    logger.warning(f"   No *_chunks.json found, but found {len(all_json)} total JSON files")
                    if all_json:
                        logger.warning(f"      Example files: {[f.name for f in all_json[:5]]}")
                        # Try loading all JSON files as fallback
                        chunk_files_found = all_json
                
                for chunk_file in chunk_files_found:
                    try:
                        with open(chunk_file, 'r', encoding='utf-8') as f:
                            file_chunks = json.load(f)
                        
                        for chunk in file_chunks:
                            metadata = chunk.get("metadata", {}) or {}

                            # Quality filtering
                            token_count = metadata.get("token_count", 0)
                            if token_count < 50:  # Skip very small chunks
                                continue
                            
                            # Advanced text preprocessing
                            original_text = chunk["text"]
                            processed_text = self.preprocess_text_advanced(original_text)
                            
                            chunk_id = len(self.chunks_metadata)
                            hierarchy_path = metadata.get("hierarchy_path") or self._build_hierarchy_path(metadata.get("section_path"))

                            collection_hints_raw = metadata.get("collection_hints") or metadata.get("qdrant_collection_hint")
                            if isinstance(collection_hints_raw, str):
                                collection_hints = [collection_hints_raw]
                            elif collection_hints_raw:
                                seen = set()
                                collection_hints = [hint for hint in collection_hints_raw if not (hint in seen or seen.add(hint))]
                            else:
                                collection_hints = [canonical_collection]

                            metadata_updates = {
                                "global_chunk_id": chunk_id,
                                "collection_priority": priority,
                                "quality_score": min(1.0, token_count / 1000),
                                "text_preprocessing_applied": True,
                                "original_length": len(original_text),
                                "processed_length": len(processed_text),
                                "kaggle_processing_timestamp": datetime.now().isoformat(),
                                "model_target": self.model_name,
                                "embedding_dimension": self.model_config.vector_dim,
                                "qdrant_collection": canonical_collection,
                                "collection_alias": collection_name,
                                "collection_hints": collection_hints,
                                "hierarchy_path": hierarchy_path,
                            }

                            metadata.update(metadata_updates)
                            metadata["qdrant_collection_hint"] = metadata["collection_hints"]
                            metadata.setdefault("payload_version", "1.2")
                            metadata.setdefault("source_path", metadata.get("source_file") or metadata.get("filename") or str(chunk_file))
                            metadata.setdefault("source_file", metadata["source_path"])
                            metadata.setdefault("source_filename", Path(str(metadata["source_file"])).name)
                            metadata.setdefault("document_name", Path(str(metadata["source_file"])).stem)
                            metadata.setdefault("chunk_hash", metadata.get("chunk_hash") or hashlib.sha1(original_text.encode("utf-8")).hexdigest()[:16])
                            metadata.setdefault("content_digest", metadata["chunk_hash"])
                            metadata.setdefault("content_type", metadata.get("content_type", "hierarchical_section"))

                            keywords = set(k for k in metadata.get("search_keywords", []) if isinstance(k, str))
                            if hierarchy_path:
                                keywords.update(part.strip() for part in hierarchy_path.split(" > ") if part.strip())
                            if metadata.get("heading_text"):
                                keywords.add(metadata["heading_text"])
                            metadata["search_keywords"] = sorted(k for k in keywords if k)

                            sparse_vector = self._build_sparse_vector_from_metadata(metadata)
                            self.sparse_vectors.append(sparse_vector)
                            if sparse_vector:
                                results["sparse_vectors_generated"] += 1
                                metadata["sparse_vector"] = sparse_vector
                            else:
                                metadata.pop("sparse_vector", None)

                            metadata["sparse_vector_tokens"] = sparse_vector.get("tokens", []) if sparse_vector else []
                            metadata["sparse_vector_weight_norm"] = sparse_vector.get("stats", {}).get("weight_norm") if sparse_vector else 0.0

                            modal_hint = self._infer_modal_hint(original_text, metadata)
                            if modal_hint:
                                metadata["modal_hint"] = modal_hint
                                metadata.setdefault("embedding_modal_hint", modal_hint)
                                modal_hint_distribution[modal_hint] += 1

                            self._ensure_document_id(metadata)

                            chunk["metadata"] = metadata
                            self.chunks_metadata.append(metadata)
                            self.chunk_texts.append(processed_text)
                            self.raw_chunk_texts.append(original_text)
                            collection_chunks += 1
                        
                        logger.debug(f"  Loaded {len(file_chunks)} chunks from {chunk_file.name}")
                        
                    except Exception as e:
                        error_msg = f"Error loading {chunk_file}: {e}"
                        logger.error(f"Error: {error_msg}")
                        results["loading_errors"].append(error_msg)
                
                results["chunks_by_collection"][collection_name] = collection_chunks
                results["collections_loaded"] += 1
                logger.info(f"Collection '{collection_name}': {collection_chunks} chunks (priority: {priority})")
        
        results["total_chunks_loaded"] = len(self.chunks_metadata)
        results["memory_usage_mb"] = psutil.Process().memory_info().rss / 1024 / 1024

        # Preprocessing statistics
        if self.text_cache:
            results["preprocessing_stats"] = self.text_cache.get_stats()

        logger.info("Chunk loading complete")
        logger.info(f"Total chunks: {results['total_chunks_loaded']}")
        logger.info(f"Memory usage: {results['memory_usage_mb']:.1f}MB")

        if self.text_cache:
            cache_stats = results["preprocessing_stats"]
            logger.info(f"Cache hit rate: {cache_stats['hit_rate']:.2%}")

        results["modal_hint_counts"] = dict(sorted(modal_hint_distribution.items()))

        return results
    
    def generate_embeddings_kaggle_optimized(
        self,
        enable_monitoring: bool = True,
        save_intermediate: bool = True
    ) -> Dict[str, Any]:
        """
        Generate embeddings optimized for Kaggle T4 x2 environment
        """
        
        if not self.chunk_texts:
            raise ValueError("No chunks loaded. Call load_chunks_from_processing() first.")
        
        total_chunks = len(self.chunk_texts)
        logger.info("Starting Kaggle T4 x2 optimized embedding generation")
        logger.info(f"Total chunks: {total_chunks}")
        logger.info(f"Model: {self.model_name} ({self.model_config.vector_dim}D)")
        if self.device == "cuda":
            logger.info(f"GPUs: {self.device_count}x T4")
        else:
            logger.info("Running in CPU fallback mode")

        self.embeddings_by_model = {}
        self.multivectors_by_model = {}
        self.multivector_dimensions = {}
        self.multivector_comparators = {}
        self.mitigation_events.clear()
        self.processing_stats.clear()

        if self.gpu_config.gradient_checkpointing and not self.gradient_checkpoint_evaluated:
            self._record_mitigation(
                "gradient_checkpointing_active",
                model=self.model_name,
                enabled=True,
            )
            self.gradient_checkpoint_evaluated = True
        
        # Start monitoring
        if enable_monitoring:
            self._start_performance_monitoring()
        
        start_time = time.time()
        
        # Dynamic batch size optimization
        initial_primary_batch = self.gpu_config.get_optimal_batch_size(self.model_config)
        if self.device == "cpu":
            initial_primary_batch = max(1, min(initial_primary_batch, 8))
        base_total_batch_size = initial_primary_batch * self.device_count if self.device_count > 1 else initial_primary_batch

        batch_unit = "per GPU" if self.device == "cuda" else "per device"
        logger.info(f"Initial primary batch size: {initial_primary_batch} ({batch_unit}), total {base_total_batch_size}")

        controller: Optional[AdaptiveBatchController] = None
        if self.device == "cuda":
            controller = AdaptiveBatchController(
                primary_batch=initial_primary_batch,
                device_count=self.device_count,
                gpu0_soft_limit_bytes=self.gpu0_soft_limit_bytes,
                companion_enabled=bool(self.companion_models),
            )
            self.adaptive_controller = controller
            logger.info(
                "Adaptive batch controller enabled (GPU0 soft limit %.2f GB)",
                self.gpu0_soft_limit_bytes / (1024 ** 3),
            )
        else:
            self.adaptive_controller = None

        # Process in optimized batches
        all_embeddings: List[np.ndarray] = []
        companion_batches: Dict[str, List[np.ndarray]] = {
            name: [] for name in self.companion_models
        }
        companion_adjustments: Dict[str, int] = {
            name: 0 for name in self.companion_models
        }
        active_companion_names: List[str] = list(self.companion_models.keys())
        dimension_adjustments = 0
        executed_batches = 0
        batch_index = 0

        try:
            while batch_index < total_chunks:
                batch_start = time.time()
                companion_outputs: Dict[str, np.ndarray] = {}
                batch_embeddings: Optional[np.ndarray] = None
                companion_devices_used: Set[str] = set()

                while True:
                    if controller:
                        primary_batch = controller.primary_batch
                        current_total_batch = max(1, controller.total_batch)
                    else:
                        primary_batch = initial_primary_batch
                        current_total_batch = max(1, base_total_batch_size)

                    batch_end = min(batch_index + current_total_batch, total_chunks)
                    batch_texts = self.chunk_texts[batch_index:batch_end]

                    if not batch_texts:
                        break

                    if controller and self.device == "cuda":
                        snapshots = self._collect_gpu_snapshots()
                        mitigation = controller.register_snapshot(snapshots)
                        if mitigation:
                            event_type = mitigation.pop("type", "adaptive_action")
                            self._record_mitigation(event_type, **mitigation)
                            if mitigation.get("companion_disabled"):
                                active_companion_names = []
                                self._deactivate_companions()
                            torch.cuda.empty_cache()
                            gc.collect()
                            continue

                    autocast_ctx = (
                        torch.autocast(
                            device_type="cuda",
                            enabled=self.gpu_config.enable_mixed_precision,
                        )
                        if self.device == "cuda"
                        else nullcontext()
                    )

                    try:
                        with autocast_ctx:
                            if self.enable_ensemble:
                                logger.debug(f"Batch {executed_batches + 1}: Using ensemble mode")
                                batch_embeddings = self.generate_ensemble_embeddings(batch_texts)
                            elif self.primary_model is not None:
                                logger.debug(f"Batch {executed_batches + 1}: Using primary model")
                                primary_model = self._get_primary_model()
                                logger.debug(f"Primary model type: {type(primary_model).__name__}")
                                batch_embeddings = self._call_encode(
                                    primary_model,
                                    batch_texts,
                                    batch_size=primary_batch,
                                    device=self.device,
                                )
                                batch_embeddings = self._normalize_embedding_matrix(
                                    batch_embeddings,
                                    self.model_name,
                                )
                            else:
                                logger.debug(f"Batch {executed_batches + 1}: Using backend")
                                batch_embeddings = self._encode_with_backend(batch_texts, primary_batch)
                                batch_embeddings = self._normalize_embedding_matrix(
                                    batch_embeddings,
                                    self.model_name,
                                )

                            temp_outputs: Dict[str, np.ndarray] = {}
                            for companion_name in active_companion_names:
                                companion_model = self.companion_models.get(companion_name)
                                if companion_model is None:
                                    continue
                                comp_batch_size = self.companion_batch_sizes.get(companion_name, primary_batch)
                                companion_device = self.companion_device_map.get(companion_name, self.device)
                                companion_matrix = self._call_encode(
                                    companion_model,
                                    batch_texts,
                                    batch_size=comp_batch_size,
                                    device=companion_device,
                                )
                                temp_outputs[companion_name] = self._normalize_embedding_matrix(
                                    companion_matrix,
                                    companion_name,
                                )
                                companion_devices_used.add(companion_device)

                            companion_outputs = temp_outputs

                        break
                    except RuntimeError as exc:
                        if (
                            self.device == "cuda"
                            and controller
                            and "out of memory" in str(exc).lower()
                        ):
                            mitigation = controller.register_oom(companion_active=bool(active_companion_names))
                            if mitigation:
                                event_type = mitigation.pop("type", "adaptive_oom")
                                self._record_mitigation(event_type, **mitigation)
                                if mitigation.get("companion_disabled"):
                                    active_companion_names = []
                                    self._deactivate_companions()
                                torch.cuda.empty_cache()
                                gc.collect()
                                continue
                        raise

                if not batch_texts:
                    break

                if batch_embeddings is None:
                    logger.debug("No embeddings produced for current batch; retrying next batch")
                    continue

                executed_batches += 1
                progress = (batch_end / total_chunks) * 100
                remaining_chunks = max(0, total_chunks - batch_end)
                est_remaining_batches = math.ceil(remaining_chunks / max(1, current_total_batch))

                batch_embeddings, adjusted = self._ensure_embedding_dimension(batch_embeddings)
                if adjusted:
                    dimension_adjustments += 1

                if self.matryoshka_dim and batch_embeddings.shape[1] > self.matryoshka_dim:
                    batch_embeddings = batch_embeddings[:, :self.matryoshka_dim]
                    logger.debug(
                        f"Applied Matryoshka truncation: {batch_embeddings.shape[1]}D -> {self.matryoshka_dim}D"
                    )

                all_embeddings.append(batch_embeddings)

                for companion_name, companion_matrix in companion_outputs.items():
                    config = self.companion_model_configs.get(companion_name)
                    expected_dim = config.vector_dim if config else None
                    adjusted_companion = False
                    companion_matrix, adjusted_companion = self._ensure_embedding_dimension(
                        companion_matrix,
                        expected_dim=expected_dim,
                    )
                    if adjusted_companion:
                        companion_adjustments[companion_name] += 1

                    if self.matryoshka_dim and companion_matrix.shape[1] > self.matryoshka_dim:
                        companion_matrix = companion_matrix[:, :self.matryoshka_dim]
                        logger.debug(
                            f"Applied Matryoshka truncation to {companion_name}: {companion_matrix.shape[1]}D -> {self.matryoshka_dim}D"
                        )

                    companion_batches[companion_name].append(companion_matrix)

                batch_time = time.time() - batch_start
                chunks_per_second = len(batch_texts) / batch_time if batch_time > 0 else 0.0
                logger.info(
                    "Batch %s: %.1f chunks/sec, Progress: %.1f%%, Remaining batches ≈ %s",
                    executed_batches,
                    chunks_per_second,
                    progress,
                    est_remaining_batches,
                )

                if save_intermediate and executed_batches % 10 == 0:
                    self._save_intermediate_results(all_embeddings, executed_batches)

                if self.device == "cuda":
                    torch.cuda.synchronize()
                for companion_device in companion_devices_used:
                    if isinstance(companion_device, str) and companion_device.startswith("cuda"):
                        with torch.cuda.device(companion_device):
                            torch.cuda.synchronize()
                            torch.cuda.empty_cache()

                batch_index = batch_end

            # Combine all embeddings
            self.embeddings = np.vstack(all_embeddings)

            # V5: Check against either Matryoshka dimension or full model dimension
            expected_dim = self.matryoshka_dim if self.matryoshka_dim else self.model_config.vector_dim
            if self.embeddings.shape[1] != expected_dim:
                raise ValueError(
                    f"Embedding dimension mismatch after aggregation: expected {expected_dim}D "
                    f"(Matryoshka: {self.matryoshka_dim}, Model: {self.model_config.vector_dim}), "
                    f"got {self.embeddings.shape[1]}D"
                )

            if self.export_config.compress_embeddings:
                self.embeddings = self.embeddings.astype(np.float32)
                logger.info("Embeddings compressed to float32")

            self.embeddings_by_model = {self.model_name: self.embeddings}

            for companion_name, batch_list in companion_batches.items():
                if not batch_list:
                    continue
                companion_full = np.vstack(batch_list)
                if self.export_config.compress_embeddings:
                    companion_full = companion_full.astype(np.float32)
                self.embeddings_by_model[companion_name] = companion_full
            
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise
        finally:
            # Stop monitoring
            if enable_monitoring:
                self._stop_performance_monitoring()
        
        # Calculate final statistics
        total_time = time.time() - start_time
        chunks_per_second = total_chunks / total_time
        
        # Calculate memory efficiency
        embeddings = self._require_embeddings()
        embedding_memory_mb = embeddings.nbytes / 1024 / 1024
        memory_per_chunk_kb = (embedding_memory_mb * 1024) / total_chunks

        companion_memory_mb = {}
        companion_dimensions = {}
        for companion_name, companion_array in self.embeddings_by_model.items():
            if companion_name == self.model_name:
                continue
            companion_memory_mb[companion_name] = companion_array.nbytes / 1024 / 1024
            companion_dimensions[companion_name] = companion_array.shape[1]
        
        final_primary_batch = controller.primary_batch if controller else initial_primary_batch
        final_total_batch_size = controller.total_batch if controller else base_total_batch_size

        results = {
            "total_embeddings_generated": len(embeddings),
            "embedding_dimension": embeddings.shape[1],
            "processing_time_seconds": total_time,
            "chunks_per_second": chunks_per_second,
            "gpu_count": self.device_count,
            "optimal_batch_size": final_primary_batch,
            "effective_total_batch_size": final_total_batch_size,
            "total_batches": executed_batches,
            "model_used": self.model_name,
            "backend": self.gpu_config.backend,
            "precision": self.gpu_config.precision,
            "embedding_memory_mb": embedding_memory_mb,
            "memory_per_chunk_kb": memory_per_chunk_kb,
            "kaggle_optimized": True,
            "performance_stats": dict(self.processing_stats),
            "dimension_adjustments": dimension_adjustments,
            "mitigation_events": list(self.mitigation_events),
            "gpu_snapshot_summary": self._summarize_gpu_history(),
            "cache_events": list(self.cache_events),
        }

        if self.multivectors_by_model:
            multivector_stats: Dict[str, Dict[str, Any]] = {}
            for name, channel_vectors in self.multivectors_by_model.items():
                total_vectors = sum(len(vectors) for vectors in channel_vectors)
                average_vectors = total_vectors / len(channel_vectors) if channel_vectors else 0.0
                dimension = self.multivector_dimensions.get(name)
                multivector_stats[name] = {
                    "dimension": dimension,
                    "comparator": self.multivector_comparators.get(name, "max_sim"),
                    "average_vectors_per_point": average_vectors,
                }
            results["multivector_channels"] = multivector_stats

        if companion_memory_mb:
            results["companion_models"] = {
                name: {
                    "embedding_dimension": companion_dimensions.get(name),
                    "memory_mb": companion_memory_mb.get(name),
                    "batch_size": self.companion_batch_sizes.get(name),
                    "dimension_adjustments": companion_adjustments.get(name, 0),
                }
                for name in companion_memory_mb
            }

        if controller:
            results["adaptive_controller"] = {
                "primary_batch": controller.primary_batch,
                "total_batch": controller.total_batch,
                "oom_events": controller._oom_events,
                "updates": controller._updates,
                "companions_enabled": controller.companion_enabled,
            }

        logger.info("Kaggle embedding generation complete")
        logger.info(f"Generated {results['total_embeddings_generated']} embeddings")
        logger.info(f"Dimension: {results['embedding_dimension']}")
        logger.info(f"Total time: {results['processing_time_seconds']:.2f}s")
        logger.info(f"Speed: {results['chunks_per_second']:.1f} chunks/second")
        logger.info(f"Memory: {results['embedding_memory_mb']:.1f}MB ({results['memory_per_chunk_kb']:.2f}KB per chunk)")

        if companion_memory_mb:
            formatted = ", ".join(
                f"{name}={memory:.1f}MB/{companion_dimensions.get(name)}D"
                for name, memory in companion_memory_mb.items()
            )
            logger.info("Companion dense embeddings: %s", formatted)

        return results
    
    def _encode_with_backend(self, texts: List[str], batch_size: int) -> np.ndarray:
        """Encode with alternative backend (ONNX/TensorRT)"""
        
        if self.primary_model is None:
            raise RuntimeError("No backend model loaded")
        
        # Unwrap all wrappers (torch.compile + DataParallel)
        encode_model = self._unwrap_model(self.primary_model)
        
        if hasattr(encode_model, 'encode'):
            try:
                logger.debug(f"Encoding {len(texts)} texts with ONNX backend (batch_size={batch_size})")
                
                embeddings = encode_model.encode(
                    texts,
                    batch_size=batch_size,
                    show_progress_bar=False,
                    convert_to_numpy=True,
                    normalize_embeddings=True,
                )
                
                # Ensure correct dtype
                if embeddings.dtype != np.float32:
                    embeddings = embeddings.astype(np.float32)
                
                logger.debug(f"ONNX encoding complete: shape={embeddings.shape}")
                return embeddings
                
            except Exception as e:
                logger.error(f"ONNX encoding failed: {e}")
                raise RuntimeError(f"Backend encoding failed: {e}")
        
        # If no encode method, try direct inference (for pure ONNX models)
        elif hasattr(self.primary_model, 'forward') or hasattr(self.primary_model, '__call__'):
            try:
                logger.debug(f"Encoding {len(texts)} texts with direct ONNX inference")
                
                # Tokenize inputs
                from transformers import AutoTokenizer
                tokenizer = AutoTokenizer.from_pretrained(self.model_config.hf_model_id)
                
                all_embeddings = []
                for i in range(0, len(texts), batch_size):
                    batch_texts = texts[i:i + batch_size]
                    
                    # Tokenize
                    inputs = tokenizer(
                        batch_texts,
                        padding=True,
                        truncation=True,
                        max_length=self.model_config.max_tokens,
                        return_tensors="pt"
                    )
                    
                    # Forward pass
                    if hasattr(self.primary_model, 'forward'):
                        outputs = self.primary_model.forward(**inputs)
                    else:
                        outputs = self.primary_model(**inputs)

                    token_embeddings = None
                    if isinstance(outputs, dict):
                        token_embeddings = outputs.get("last_hidden_state")
                    elif hasattr(outputs, "last_hidden_state"):
                        token_embeddings = getattr(outputs, "last_hidden_state")

                    if token_embeddings is not None:
                        attention_mask = inputs["attention_mask"]
                        token_embeddings = torch.as_tensor(token_embeddings)
                        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
                        embeddings_tensor = torch.sum(token_embeddings * input_mask_expanded, dim=1) / torch.clamp(
                            input_mask_expanded.sum(dim=1), min=1e-9
                        )
                    else:
                        candidate = outputs[0] if isinstance(outputs, tuple) else outputs
                        embeddings_tensor = torch.as_tensor(candidate)

                    embeddings_tensor = torch.nn.functional.normalize(embeddings_tensor, p=2, dim=1)
                    
                    # Convert to numpy
                    batch_embeddings = (
                        embeddings_tensor.detach().cpu().numpy().astype(np.float32)
                    )
                    all_embeddings.append(batch_embeddings)
                
                final_embeddings = np.vstack(all_embeddings)
                logger.debug(f"ONNX direct inference complete: shape={final_embeddings.shape}")
                return final_embeddings
                
            except Exception as e:
                logger.error(f"ONNX direct inference failed: {e}")
                raise RuntimeError(f"Backend encoding failed: {e}")
        
        else:
            raise RuntimeError(
                "Backend model does not support encoding. "
                "Model must have either 'encode()' method or 'forward()' method."
            )

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
        """
        Export embeddings in formats optimized for local Qdrant upload
        """
        
        if self.embeddings is None:
            raise ValueError("No embeddings to export. Generate embeddings first.")
        embeddings = self._require_embeddings()
        companion_arrays = {
            name: array
            for name, array in self.embeddings_by_model.items()
            if name != self.model_name
        }

        logger.info("Exporting embeddings for local Qdrant integration...")

        exported_files = {}
        base_path = self.export_config.get_output_path()
        
        # 1. NumPy format (for fast loading)
        if self.export_config.export_numpy:
            numpy_path = f"{base_path}_embeddings.npy"
            np.save(numpy_path, embeddings)
            exported_files["numpy"] = numpy_path
            logger.info(f"NumPy embeddings: {numpy_path}")

            for companion_name, companion_array in companion_arrays.items():
                safe_name = companion_name.replace("-", "_")
                companion_path = f"{base_path}_{safe_name}_embeddings.npy"
                np.save(companion_path, companion_array)
                exported_files[f"numpy_{safe_name}"] = companion_path
                logger.info(f"NumPy embeddings ({companion_name}): {companion_path}")
        
        # 2. JSONL format (for Qdrant upload)
        if self.export_config.export_jsonl:
            jsonl_path = f"{base_path}_qdrant.jsonl"
            self._export_qdrant_jsonl(jsonl_path)
            exported_files["jsonl"] = jsonl_path
            logger.info(f"Qdrant JSONL: {jsonl_path}")

        if self.multivectors_by_model:
            multivector_path = f"{base_path}_multivectors.json"
            multivector_payload = {
                "channels": self.multivectors_by_model,
                "dimensions": self.multivector_dimensions,
                "comparators": self.multivector_comparators,
            }
            with open(multivector_path, "w", encoding="utf-8") as handle:
                json.dump(multivector_payload, handle, ensure_ascii=False)
            exported_files["multivectors"] = multivector_path
            logger.info(f"Multivector JSON: {multivector_path}")

        # 2b. Sparse JSONL sidecar
        if self.export_config.export_sparse_jsonl and any(self.sparse_vectors):
            sparse_path = f"{base_path}_sparse.jsonl"
            self._export_sparse_jsonl(sparse_path)
            exported_files["sparse_jsonl"] = sparse_path
            logger.info(f"Sparse JSONL: {sparse_path}")
        
        # 3. FAISS index (for fast similarity search)
        if self.export_config.export_faiss:
            faiss_path = f"{base_path}_index.faiss"
            self._export_faiss_index(faiss_path)
            exported_files["faiss"] = faiss_path
            logger.info(f"FAISS index: {faiss_path}")
        
        # 4. Metadata files
        metadata_path = f"{base_path}_metadata.json"
        self._export_metadata(metadata_path)
        exported_files["metadata"] = metadata_path
        
        texts_path = f"{base_path}_texts.json"
        self._export_texts(texts_path)
        exported_files["texts"] = texts_path
        
        # 5. Processing statistics
        stats_path = f"{base_path}_stats.json"
        self._export_processing_stats(stats_path)
        exported_files["stats"] = stats_path
        
        # 6. Upload script for local machine
        script_path = f"{base_path}_upload_script.py"
        self._generate_upload_script(script_path, exported_files)
        exported_files["upload_script"] = script_path
        exported_files["qdrant_collection"] = self.get_target_collection_name()
        
        logger.info("Export complete; files ready for download:")
        for file_type, file_path in exported_files.items():
            if file_type == "qdrant_collection":
                logger.info("  %s: %s", file_type, file_path)
                continue

            if not os.path.exists(file_path):
                logger.warning("  %s: expected export missing at %s", file_type, file_path)
                continue

            file_size_mb = os.path.getsize(file_path) / 1024 / 1024
            logger.info(f"  {file_type}: {os.path.basename(file_path)} ({file_size_mb:.1f}MB)")
        
        return exported_files
    
    def _export_qdrant_jsonl(self, file_path: str):
        """Export in JSONL format for Qdrant upload"""
        embeddings = self._require_embeddings()
        companion_arrays = {
            name: array
            for name, array in self.embeddings_by_model.items()
            if name != self.model_name
        }

        dense_vector_names = [self.model_name, *companion_arrays.keys()]

        with open(file_path, 'w', encoding='utf-8') as f:
            total = len(embeddings)
            for i in range(total):
                metadata = self.chunks_metadata[i]
                text = self.chunk_texts[i]
                sparse_vector = self.sparse_vectors[i] if i < len(self.sparse_vectors) else None

                payload_model_info = {
                    "name": self.model_name,
                    "hf_model_id": self.model_config.hf_model_id,
                    "dimension": self.model_config.vector_dim,
                    "version": "v4",
                }

                companion_payload = {}
                vector_payload: Dict[str, Any] = {
                    self.model_name: embeddings[i].tolist()
                }

                for companion_name, companion_array in companion_arrays.items():
                    vector_payload[companion_name] = companion_array[i].tolist()
                    config = self.companion_model_configs.get(companion_name)
                    companion_payload[companion_name] = {
                        "dimension": companion_array.shape[1],
                        "hf_model_id": config.hf_model_id if config else None,
                    }

                if companion_payload:
                    payload_model_info["companions"] = companion_payload

                multivector_channel_counts: Dict[str, int] = {}
                if self.multivectors_by_model:
                    multivector_meta = {}
                    for channel_name, channel_vectors in self.multivectors_by_model.items():
                        channel_dimension = self.multivector_dimensions.get(channel_name)
                        comparator = self.multivector_comparators.get(channel_name, "max_sim")
                        multivector_meta[channel_name] = {
                            "dimension": channel_dimension,
                            "comparator": comparator,
                        }

                        point_vectors = channel_vectors[i] if i < len(channel_vectors) else []
                        multivector_channel_counts[channel_name] = len(point_vectors)
                        vector_payload[channel_name] = {"vectors": point_vectors}

                    payload_model_info["multivectors"] = multivector_meta

                payload = {
                    **metadata,
                    "text_preview": text[:500],
                    "full_text_length": len(text),
                    "kaggle_export_timestamp": datetime.now().isoformat(),
                    "model_info": payload_model_info,
                    "primary_vector_name": self.model_name,
                    "dense_vector_names": dense_vector_names,
                }

                if companion_arrays:
                    payload["companion_vector_dimensions"] = {
                        name: info["dimension"] for name, info in companion_payload.items()
                    }

                if sparse_vector:
                    payload["sparse_vector"] = {
                        "indices": sparse_vector.get("indices", []),
                        "values": sparse_vector.get("values", []),
                        "tokens": sparse_vector.get("tokens", []),
                        "stats": sparse_vector.get("stats", {})
                    }

                if multivector_channel_counts:
                    payload["multivector_counts"] = multivector_channel_counts
                    payload["multivector_channels"] = list(multivector_channel_counts.keys())

                qdrant_point: Dict[str, Any] = {"id": i, "payload": payload}
                qdrant_point["vectors"] = vector_payload

                f.write(json.dumps(qdrant_point, ensure_ascii=False) + '\n')

    def _export_sparse_jsonl(self, file_path: str) -> None:
        """Export hashed sparse vectors as a sidecar JSONL file."""

        if not self.sparse_vectors or not any(self.sparse_vectors):
            logger.info("No sparse vectors available for export; skipping sparse JSONL generation.")
            return

        with open(file_path, 'w', encoding='utf-8') as f:
            for i, sparse_vector in enumerate(self.sparse_vectors):
                if sparse_vector:
                    record = {
                        "id": i,
                        "sparse_vector": {
                            "indices": sparse_vector.get("indices", []),
                            "values": sparse_vector.get("values", [])
                        },
                        "tokens": sparse_vector.get("tokens", []),
                        "stats": sparse_vector.get("stats", {})
                    }
                else:
                    record = {
                        "id": i,
                        "sparse_vector": {
                            "indices": [],
                            "values": []
                        },
                        "tokens": [],
                        "stats": {}
                    }

                f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    def _export_faiss_index(self, file_path: str):
        """Export FAISS index for fast similarity search"""
        embeddings = self._require_embeddings()
        dimension = embeddings.shape[1]
        
        # Use Inner Product for cosine similarity (embeddings are normalized)
        index = faiss.IndexFlatIP(dimension)
        
        # Add vectors
        embeddings_float32 = embeddings.astype(np.float32)
        index.add(embeddings_float32)  # type: ignore[arg-type]
        
        # Save index
        faiss.write_index(index, file_path)
    
    def _export_metadata(self, file_path: str):
        """Export enhanced metadata"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.chunks_metadata, f, indent=2, ensure_ascii=False)
    
    def _export_texts(self, file_path: str):
        """Export chunk texts"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.chunk_texts, f, indent=2, ensure_ascii=False)
    
    def _export_processing_stats(self, file_path: str):
        """Export comprehensive processing statistics"""
        embeddings = self.embeddings
        stats = {
            "kaggle_environment": self.is_kaggle,
            "model_config": {
                "name": self.model_name,
                "hf_model_id": self.model_config.hf_model_id,
                "vector_dimension": self.model_config.vector_dim,
                "max_tokens": self.model_config.max_tokens
            },
            "gpu_config": {
                "device_count": self.device_count,
                "backend": self.gpu_config.backend,
                "precision": self.gpu_config.precision,
                "total_vram_gb": self.gpu_config.total_vram_gb
            },
            "embedding_stats": {
                "total_embeddings": len(embeddings) if embeddings is not None else 0,
                "embedding_dimension": embeddings.shape[1] if embeddings is not None else 0,
                "memory_usage_mb": embeddings.nbytes / 1024 / 1024 if embeddings is not None else 0
            },
            "processing_performance": dict(self.processing_stats),
            "export_timestamp": datetime.now().isoformat()
        }

        if self.sparse_vectors:
            available = sum(1 for vec in self.sparse_vectors if vec)
            stats["sparse_vector_stats"] = {
                "total_chunks": len(self.sparse_vectors),
                "sparse_vectors_available": available,
                "coverage_ratio": available / len(self.sparse_vectors) if self.sparse_vectors else 0.0
            }
        
        if self.embeddings_by_model:
            stats["dense_vector_layout"] = {
                name: {
                    "dimension": array.shape[1],
                    "memory_mb": array.nbytes / 1024 / 1024,
                    "is_primary": name == self.model_name,
                }
                for name, array in self.embeddings_by_model.items()
            }

        if self.multivectors_by_model:
            stats["multivector_layout"] = {
                name: {
                    "dimension": self.multivector_dimensions.get(name),
                    "comparator": self.multivector_comparators.get(name, "max_sim"),
                    "average_vectors_per_point": (
                        sum(len(vectors) for vectors in channel) / len(channel)
                        if channel
                        else 0.0
                    ),
                }
                for name, channel in self.multivectors_by_model.items()
            }

        if self.text_cache:
            stats["preprocessing_cache"] = self.text_cache.get_stats()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    
    def _generate_upload_script(self, file_path: str, exported_files: Dict[str, str]):
        """Generate Python script for local Qdrant upload"""

        collection_name = self.get_target_collection_name()

        vector_files_map: Dict[str, str] = {}
        vector_dimensions_map: Dict[str, int] = {}

        primary_numpy_filename = ""
        if "numpy" in exported_files:
            primary_numpy_filename = os.path.basename(exported_files["numpy"])
            vector_files_map[self.model_name] = primary_numpy_filename
            vector_dimensions_map[self.model_name] = self.model_config.vector_dim
        else:
            logger.warning("Primary NumPy embeddings file missing; upload script will have limited functionality")

        for model_name, array in self.embeddings_by_model.items():
            if model_name == self.model_name:
                continue
            safe_name = model_name.replace("-", "_")
            numpy_key = f"numpy_{safe_name}"
            companion_path = exported_files.get(numpy_key)
            if not companion_path:
                logger.warning("Companion embeddings for %s not exported; skipping in upload script", model_name)
                continue
            vector_files_map[model_name] = os.path.basename(companion_path)
            vector_dimensions_map[model_name] = array.shape[1]

        dense_vector_names = list(vector_files_map.keys())

        vector_files_json = json.dumps(vector_files_map)
        vector_dimensions_json = json.dumps(vector_dimensions_map)
        dense_vector_names_json = json.dumps(dense_vector_names)
        primary_vector_name = self.model_name

        script_content = textwrap.dedent(f'''#!/usr/bin/env python3
"""
Auto-generated Qdrant upload script for Ultimate Kaggle Embedder V4
Generated on: {datetime.now().isoformat()}

USAGE:
1. Download all exported files to your local machine
2. Make sure Qdrant is running locally (docker-compose up -d)
3. Install requirements: pip install qdrant-client numpy
4. Run this script: python {os.path.basename(file_path)}
"""

import json
import logging
from datetime import datetime

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    MultiVectorConfig,
    MultiVectorComparator,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upload_to_qdrant():
    """Upload embeddings to local Qdrant instance."""

    # Configuration
    qdrant_host = "localhost"
    qdrant_port = 6333
    collection_name = "{collection_name}"

    # File paths (adjust if needed)
    files = {{
        "embeddings": "{primary_numpy_filename}",
        "metadata": "{os.path.basename(exported_files.get('metadata', ''))}",
        "texts": "{os.path.basename(exported_files.get('texts', ''))}",
        "stats": "{os.path.basename(exported_files.get('stats', ''))}",
        "jsonl": "{os.path.basename(exported_files.get('jsonl', ''))}",
        "sparse": "{os.path.basename(exported_files.get('sparse_jsonl', ''))}",
        "multivectors": "{os.path.basename(exported_files.get('multivectors', ''))}"
    }}

    vector_files = json.loads("""{vector_files_json}""")
    vector_dimensions = json.loads("""{vector_dimensions_json}""")
    dense_vector_names = json.loads("""{dense_vector_names_json}""")
    primary_vector_name = "{primary_vector_name}"

    vector_files = {{name: path for name, path in vector_files.items() if path}}
    dense_vector_names = [name for name in dense_vector_names if name in vector_files]

    try:
        client = QdrantClient(host=qdrant_host, port=qdrant_port)
        logger.info(f"Connected to Qdrant at {{qdrant_host}}:{{qdrant_port}}")

        logger.info("Loading exported data...")
        dense_vectors = {{name: np.load(path) for name, path in vector_files.items()}}

        with open(files["metadata"], "r", encoding="utf-8") as handle:
            metadata_list = json.load(handle)

        with open(files["texts"], "r", encoding="utf-8") as handle:
            texts_list = json.load(handle)

        multivector_channels = {{}}
        multivector_dimensions = {{}}
        multivector_comparators = {{}}

        if files.get("multivectors"):
            with open(files["multivectors"], "r", encoding="utf-8") as handle:
                multivector_blob = json.load(handle)
            multivector_channels = multivector_blob.get("channels", {{}})
            multivector_dimensions = multivector_blob.get("dimensions", {{}})
            multivector_comparators = multivector_blob.get("comparators", {{}})

        if not dense_vectors:
            raise RuntimeError("No dense embedding files were found; cannot proceed with upload")

        point_count = len(metadata_list)

        for name in dense_vector_names:
            vectors = dense_vectors.get(name)
            if vectors is None:
                raise RuntimeError(f"Missing dense vectors for {{name}}")
            if len(vectors) != point_count:
                raise ValueError(
                    f"Vector count mismatch for {{name}}: expected {{point_count}}, got {{len(vectors)}}"
                )
            vector_dim = vector_dimensions.get(name, vectors.shape[1])
            logger.info("Loaded %s embeddings for %s (%sD)", len(vectors), name, vector_dim)

        if files.get("sparse"):
            logger.info(f"Sparse sidecar detected: {{files['sparse']}}")

        multivector_names = list(multivector_channels.keys())
        for name in multivector_names:
            channel_vectors = multivector_channels.get(name, [])
            if len(channel_vectors) != point_count:
                raise ValueError(
                    f"Multivector count mismatch for {{name}}: expected {{point_count}}, got {{len(channel_vectors)}}"
                )
        if multivector_names:
            logger.info("Multivector channels detected: %s", ", ".join(multivector_names))

        try:
            client.get_collection(collection_name)
            logger.info(f"Collection '{{collection_name}}' already exists")
        except Exception:
            logger.info(f"Creating collection: {{collection_name}}")
            vector_params = {{
                name: VectorParams(size=vector_dimensions.get(name, dense_vectors[name].shape[1]), distance=Distance.COSINE)
                for name in dense_vector_names
            }}
            for name in multivector_names:
                dimension = multivector_dimensions.get(name)
                if dimension is None:
                    channel_vectors = multivector_channels.get(name, [])
                    first_non_empty = next((vec for vec in channel_vectors if vec), [])
                    if first_non_empty:
                        dimension = len(first_non_empty[0])
                if dimension is None:
                    raise RuntimeError(f"Could not determine dimension for multivector channel {{name}}")
                comparator_value = multivector_comparators.get(name, "max_sim")
                try:
                    comparator_enum = MultiVectorComparator(comparator_value)
                except ValueError:
                    logger.warning(
                        "Unknown comparator '%s' for multivector channel %s; defaulting to max_sim",
                        comparator_value,
                        name,
                    )
                    comparator_enum = MultiVectorComparator.MAX_SIM
                multivector_dimensions[name] = dimension
                vector_params[name] = VectorParams(
                    size=dimension,
                    distance=Distance.COSINE,
                    multivector_config=MultiVectorConfig(
                        comparator=comparator_enum
                    ),
                )
            if len(vector_params) == 1:
                vectors_config = next(iter(vector_params.values()))
            else:
                vectors_config = vector_params

            client.create_collection(
                collection_name=collection_name,
                vectors_config=vectors_config,
                hnsw_config={{
                    "m": 48,
                    "ef_construct": 512,
                    "full_scan_threshold": 50000,
                }},
                quantization_config={{
                    "scalar": {{
                        "type": "int8",
                        "quantile": 0.99,
                        "always_ram": True,
                    }}
                }},
            )

        logger.info("Preparing points for upload...")
        points = []

        for i in range(point_count):
            metadata = metadata_list[i]
            text = texts_list[i]
            vector_payload = {{
                name: dense_vectors[name][i].tolist()
                for name in dense_vector_names
            }}
            for name in multivector_names:
                channel_data = multivector_channels[name][i]
                if channel_data is None:
                    channel_data = []
                if channel_data and isinstance(channel_data[0], (list, tuple)):
                    channel_data = [list(vec) for vec in channel_data]
                vector_payload[name] = {{"vectors": channel_data}}
            payload_data = {{
                **metadata,
                "text_preview": text[:500],
                "full_text_length": len(text),
                "local_upload_timestamp": datetime.now().isoformat(),
                "primary_vector_name": primary_vector_name,
                "dense_vector_names": dense_vector_names,
            }}
            if multivector_names:
                payload_data.setdefault("multivector_channels", multivector_names)
                if multivector_dimensions:
                    payload_data.setdefault("multivector_dimensions", multivector_dimensions)
                if multivector_comparators:
                    payload_data.setdefault("multivector_comparators", multivector_comparators)
            point = PointStruct(
                id=i,
                vectors=vector_payload,
                payload=payload_data,
            )
            points.append(point)

        batch_size = 1000
        total_batches = (len(points) + batch_size - 1) // batch_size
        logger.info(f"Uploading {{len(points)}} points in {{total_batches}} batches...")

        for start in range(0, len(points), batch_size):
            batch = points[start:start + batch_size]
            batch_num = (start // batch_size) + 1

            client.upsert(collection_name=collection_name, points=batch, wait=True)
            logger.info(f"Uploaded batch {{batch_num}}/{{total_batches}} ({{len(batch)}} points)")

        collection_info = client.get_collection(collection_name)
        logger.info(f"Upload complete; collection has {{collection_info.points_count}} points")

        logger.info("Testing search...")
        test_results = client.search(
            collection_name=collection_name,
            query_vector=(
                primary_vector_name,
                dense_vectors[primary_vector_name][0].tolist(),
            ),
            limit=5,
        )

        logger.info(f"Search test successful; found {{len(test_results)}} results")
        logger.info(f"Embeddings are ready for use in collection: {{collection_name}}")

    except Exception as exc:
        logger.error(f"Upload failed: {{exc}}")
        raise


if __name__ == "__main__":
    upload_to_qdrant()
''')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
    
    def _start_performance_monitoring(self):
        """Start performance monitoring for Kaggle environment"""
        
        def monitor():
            while self.monitoring_active:
                try:
                    # GPU monitoring
                    if torch.cuda.is_available():
                        for i in range(self.device_count):
                            memory_used = torch.cuda.memory_allocated(i) / 1e9
                            memory_reserved = torch.cuda.memory_reserved(i) / 1e9
                            memory_total = torch.cuda.get_device_properties(i).total_memory / 1e9
                            utilization = memory_used / memory_total * 100
                            
                            self.processing_stats["gpu_memory"].append({
                                "gpu_id": i,
                                "memory_used_gb": memory_used,
                                "memory_reserved_gb": memory_reserved,
                                "memory_total_gb": memory_total,
                                "utilization_percent": utilization,
                                "timestamp": time.time()
                            })
                    
                    # System monitoring
                    cpu_percent = psutil.cpu_percent()
                    memory_info = psutil.virtual_memory()
                    
                    self.processing_stats["system_metrics"].append({
                        "cpu_percent": cpu_percent,
                        "memory_used_gb": memory_info.used / 1e9,
                        "memory_percent": memory_info.percent,
                        "timestamp": time.time()
                    })
                    
                    time.sleep(2)  # Monitor every 2 seconds
                    
                except Exception as e:
                    logger.error(f"Monitoring error: {e}")
                    break
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=monitor, daemon=True)
        self.monitor_thread.start()
        logger.info("Performance monitoring started")
    
    def _stop_performance_monitoring(self):
        """Stop performance monitoring"""
        
        if self.monitoring_active:
            self.monitoring_active = False
            if self.monitor_thread:
                self.monitor_thread.join(timeout=3)
            logger.info("Performance monitoring stopped")

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