"""Configuration dataclasses and registries for the ultimate embedder."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence


@dataclass
class ModelConfig:
    """Kaggle T4 x2 optimized model configuration."""

    name: str
    hf_model_id: str
    vector_dim: int
    max_tokens: int
    trust_remote_code: bool = True
    query_prefix: str = ""
    doc_prefix: str = ""
    recommended_batch_size: int = 32
    memory_efficient: bool = True
    supports_flash_attention: bool = True


# Registry of dense models tuned for Kaggle usage.
KAGGLE_OPTIMIZED_MODELS: Dict[str, ModelConfig] = {
    "jina-code-embeddings-1.5b": ModelConfig(
        name="jina-code-embeddings-1.5b",
        hf_model_id="jinaai/jina-code-embeddings-1.5b",
        vector_dim=1024,
        max_tokens=32768,
        query_prefix="Encode this code snippet for semantic retrieval: ",
        recommended_batch_size=16,
        memory_efficient=True,
    ),
    "bge-m3": ModelConfig(
        name="bge-m3",
        hf_model_id="BAAI/bge-m3",
        vector_dim=1024,
        max_tokens=8192,
        recommended_batch_size=32,
        memory_efficient=True,
    ),
    "jina-embeddings-v4": ModelConfig(
        name="jina-embeddings-v4",
        hf_model_id="jinaai/jina-embeddings-v4",
        vector_dim=1024,
        max_tokens=32768,
        query_prefix="",
        recommended_batch_size=16,
        memory_efficient=True,
    ),
    "qwen3-embedding-0.6b": ModelConfig(
        name="qwen3-embedding-0.6b",
        hf_model_id="Qwen/Qwen3-Embedding-0.6B",
        vector_dim=1024,
        max_tokens=32768,
        recommended_batch_size=12,
        memory_efficient=True,
        supports_flash_attention=False,
    ),
    "nomic-coderank": ModelConfig(
        name="nomic-coderank",
        hf_model_id="nomic-ai/CodeRankEmbed",
        vector_dim=768,
        max_tokens=2048,
        recommended_batch_size=64,
        memory_efficient=True,
        supports_flash_attention=False,
    ),
    "qdrant-minilm-onnx": ModelConfig(
        name="qdrant-minilm-onnx",
        hf_model_id="Qdrant/all-MiniLM-L6-v2-onnx",
        vector_dim=384,
        max_tokens=256,
        recommended_batch_size=128,
        memory_efficient=True,
    ),
    "all-miniLM-l6": ModelConfig(
        name="all-miniLM-l6",
        hf_model_id="sentence-transformers/all-MiniLM-L6-v2",
        vector_dim=384,
        max_tokens=256,
        recommended_batch_size=128,
        memory_efficient=True,
    ),
}


def resolve_kaggle_model_key(model_name: str) -> str:
    """Resolve a user-provided model identifier to the canonical registry key."""

    if model_name is None:
        raise ValueError("Model name cannot be None")

    normalized = model_name.strip()
    if not normalized:
        raise ValueError("Model name cannot be empty")

    if normalized in KAGGLE_OPTIMIZED_MODELS:
        return normalized

    lookup = normalized.lower()
    for key, config in KAGGLE_OPTIMIZED_MODELS.items():
        if config.hf_model_id.lower() == lookup:
            return key

    valid = ", ".join(sorted(KAGGLE_OPTIMIZED_MODELS.keys()))
    raise ValueError(f"Unknown dense model '{model_name}'. Valid options: {valid}")


def normalize_kaggle_model_names(model_names: Sequence[str]) -> List[str]:
    """Normalize a sequence of model identifiers to canonical registry keys."""

    return [resolve_kaggle_model_key(name) for name in model_names]


def get_kaggle_model_config(model_name: str) -> ModelConfig:
    """Fetch a dense model configuration using any supported identifier."""

    canonical_key = resolve_kaggle_model_key(model_name)
    return KAGGLE_OPTIMIZED_MODELS[canonical_key]


# Sparse embedding model registry for hybrid retrieval.
SPARSE_MODELS: Dict[str, Dict[str, Any]] = {
    "splade": {
        "name": "splade",
        "hf_model_id": "naver/splade_v2_distil",
        "type": "splade",
        "description": "SPLADE learned sparse representation model (works with SentenceTransformer)",
        "recommended_batch_size": 64,
    },
    "qdrant-bm25": {
        "name": "qdrant-bm25",
        "hf_model_id": "Qdrant/bm25",
        "type": "bm25",
        "description": "DEPRECATED: BM25-style term frequency sparse vectors (not compatible with SentenceTransformer - use 'splade' instead)",
        "recommended_batch_size": 64,
        "deprecated": True,
    },
    "qdrant-minilm-attention": {
        "name": "qdrant-minilm-attention",
        "hf_model_id": "Qdrant/all_miniLM_L6_v2_with_attentions",
        "type": "attention",
        "description": "Attention-based sparse vectors from MiniLM",
        "recommended_batch_size": 64,
    },
}


# Reranking model registry used by the pipeline.
RERANKING_MODELS: Dict[str, str] = {
    "jina-reranker-v3": "jinaai/jina-reranker-v3",
}


@dataclass
class KaggleGPUConfig:
    """Kaggle T4 x2 specific GPU configuration."""

    device_count: int = 2
    vram_per_gpu_gb: float = 15.83
    total_vram_gb: float = 31.66
    max_memory_per_gpu: float = 0.8
    enable_memory_efficient_attention: bool = True
    gradient_checkpointing: bool = True
    precision: str = "fp16"
    enable_mixed_precision: bool = True
    use_amp: bool = True
    base_batch_size: int = 32
    dynamic_batching: bool = True
    max_sequence_length: int = 2048
    backend: str = "pytorch"
    enable_torch_compile: bool = True
    strategy: str = "data_parallel"
    enable_gradient_accumulation: bool = True
    accumulation_steps: int = 2
    kaggle_environment: bool = True
    output_path: str = "/kaggle/working"

    def get_optimal_batch_size(self, model_config: ModelConfig) -> int:
        """Calculate an optimal batch size for the provided model."""

        if not self.dynamic_batching:
            return model_config.recommended_batch_size

        memory_per_token = 4
        tokens_per_sample = min(model_config.max_tokens, self.max_sequence_length)
        model_params = {
            768: 137e6,
            1024: 350e6,
            1536: 1.5e9,
            4096: 7e9,
        }.get(model_config.vector_dim, 350e6)

        memory_per_sample = tokens_per_sample * memory_per_token + model_params * 2 / max(1, self.device_count)
        available_memory = self.vram_per_gpu_gb * self.max_memory_per_gpu * 1e9
        optimal_batch = int(available_memory / memory_per_sample * 0.7)
        return max(1, min(optimal_batch, model_config.recommended_batch_size))


@dataclass
class KaggleExportConfig:
    """Export configuration for local Qdrant integration."""

    export_numpy: bool = True
    export_jsonl: bool = True
    export_faiss: bool = True
    export_pickle: bool = False
    export_sparse_jsonl: bool = True
    compress_embeddings: bool = True
    quantize_int8: bool = False
    include_full_metadata: bool = True
    include_processing_stats: bool = True
    include_model_info: bool = True
    working_dir: str = "/kaggle/working"
    output_prefix: str = "ultimate_embeddings_v4"

    def get_output_path(self, suffix: str = "") -> str:
        base = f"{self.output_prefix}{suffix}"
        return os.path.join(self.working_dir, base)


@dataclass
class EnsembleConfig:
    """Multi-model ensemble configuration."""

    ensemble_models: List[str] = field(
        default_factory=lambda: [
            "jina-code-embeddings-1.5b",
            "bge-m3",
            "qwen3-embedding-0.6b",
        ]
    )
    model_weights: Optional[Dict[str, float]] = None
    sequential_data_parallel: bool = True
    exclusive_mode: bool = True  # Lease both GPUs exclusively per model (DEFAULT)

    def __post_init__(self) -> None:
        self.ensemble_models = normalize_kaggle_model_names(self.ensemble_models)

        if self.model_weights is not None:
            self.model_weights = {
                resolve_kaggle_model_key(model_name): weight
                for model_name, weight in self.model_weights.items()
            }


@dataclass
class RerankingConfig:
    """CrossEncoder reranking configuration."""

    model_name: str = "jina-reranker-v3"
    enable_reranking: bool = True
    top_k_candidates: int = 100
    rerank_top_k: int = 20
    batch_size: int = 32
    enable_caching: bool = True
    cache_size: int = 1000


@dataclass
class AdvancedPreprocessingConfig:
    """Advanced document preprocessing with caching."""

    enable_text_caching: bool = True
    normalize_whitespace: bool = True
    remove_excessive_newlines: bool = True
    trim_long_sequences: bool = True
    enable_tokenizer_caching: bool = True
    max_cache_size: int = 10000
    cache_hit_threshold: float = 0.8
    enable_memory_scaling: bool = True
    memory_scale_factor: float = 0.8
    adaptive_batch_sizing: bool = True


class AdvancedTextCache:
    """Intelligent text preprocessing cache."""

    def __init__(self, max_size: int = 10000) -> None:
        self.cache: Dict[str, str] = {}
        self.max_size = max_size
        self.hit_count = 0
        self.miss_count = 0

    def _get_text_hash(self, text: str) -> str:
        return hashlib.md5(text.encode("utf-8")).hexdigest()[:16]

    def get_processed_text(self, text: str, processor_func) -> str:
        text_hash = self._get_text_hash(text)
        if text_hash in self.cache:
            self.hit_count += 1
            return self.cache[text_hash]

        processed = processor_func(text)
        if len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

        self.cache[text_hash] = processed
        self.miss_count += 1
        return processed

    def get_stats(self) -> Dict[str, Any]:
        total = self.hit_count + self.miss_count
        hit_rate = self.hit_count / total if total else 0
        return {
            "cache_size": len(self.cache),
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate,
            "memory_mb": len(str(self.cache).encode("utf-8")) / 1024 / 1024,
        }


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
]
