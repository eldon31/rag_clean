"""Sparse vector generator for live SPLADE-style inference with fallback handling.

This module executes sparse inference, returning vectors per chunk with metadata on
fallback usage. GPU leasing support mirrors existing dense passes, including telemetry
of device usage.
"""

from __future__ import annotations

import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence

import numpy as np
import torch

from processor.ultimate_embedder.gpu_lease import GPULease, lease_gpus
from processor.ultimate_embedder.sparse_pipeline import (
    build_sparse_vector_from_metadata,
)

if TYPE_CHECKING:  # pragma: no cover - typing only
    from sentence_transformers import SentenceTransformer
else:
    from .compat import SentenceTransformer

if TYPE_CHECKING:  # pragma: no cover
    from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4
    from processor.ultimate_embedder.model_manager import ModelManager


@dataclass
class ChunkRecord:
    """Lightweight chunk record for sparse inference."""

    text: str
    metadata: Dict[str, Any]
    chunk_id: Optional[str] = None


@dataclass
class SparseInferenceResult:
    """Result of sparse vector generation for a batch of chunks.

    Contains per-chunk sparse vectors, fallback metadata, and telemetry attributes.
    """

    vectors: List[Optional[Dict[str, Any]]]
    fallback_count: int
    fallback_indices: List[int]
    latency_ms: float
    device: str
    model_name: str
    success: bool
    error_message: Optional[str] = None
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex)


class SparseVectorGenerator:
    """Executes live SPLADE-style sparse inference with GPU leasing and fallback.

    This generator routes between CPU and GPU while handling metadata fallback when
    models fail or leasing is unavailable.
    """

    def __init__(
        self,
        embedder: "UltimateKaggleEmbedderV4",
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """Initialize the sparse vector generator.

        Args:
            embedder: Reference to the UltimateKaggleEmbedderV4 instance for model
                      access and configuration.
            logger: Optional logger instance. If None, uses module logger.
        """
        self.embedder = embedder
        self.logger = logger or logging.getLogger(__name__)
        self._vram_cap_gb = 12.0  # 12 GB VRAM cap per story constraints
        self._vram_soft_limit_gb = 10.0  # Soft limit for early warning
        self._adaptive_batch_size = 32  # Initial batch size
        self._min_batch_size = 4  # Minimum batch size before abort

    def generate(
        self,
        chunks: Sequence[ChunkRecord],
        model_name: str,
        use_gpu: bool = False,
        device_ids: Optional[List[int]] = None,
    ) -> SparseInferenceResult:
        """Generate sparse vectors for a sequence of chunks.

        Args:
            chunks: Sequence of chunk records to process.
            model_name: Name of the sparse model to use.
            use_gpu: Whether to attempt GPU-accelerated inference.
            device_ids: Optional list of GPU device IDs for leasing.

        Returns:
            SparseInferenceResult containing vectors and metadata.
        """
        start_time = time.perf_counter()
        vectors: List[Optional[Dict[str, Any]]] = []
        fallback_indices: List[int] = []
        device = "cpu"
        success = True
        error_message: Optional[str] = None

        try:
            # Retrieve the sparse model from the embedder's registry
            sparse_model = self.embedder.sparse_models.get(model_name)
            if sparse_model is None:
                self.logger.warning(
                    "Sparse model %s not loaded; using metadata fallback for all chunks",
                    model_name,
                )
                vectors, fallback_indices = self._fallback_to_metadata(chunks)
                success = False
                error_message = f"Model {model_name} not loaded"
            elif use_gpu and self.embedder.device == "cuda":
                # GPU-accelerated inference with leasing
                vectors, fallback_indices, device = self._generate_with_gpu(
                    chunks,
                    sparse_model,
                    model_name,
                    device_ids,
                )
            else:
                # CPU-based inference
                vectors, fallback_indices, device = self._generate_with_cpu(
                    chunks,
                    sparse_model,
                    model_name,
                )

        except Exception as exc:  # pragma: no cover
            self.logger.error(
                "Sparse inference failed for model %s: %s",
                model_name,
                exc,
                exc_info=True,
            )
            vectors, fallback_indices = self._fallback_to_metadata(chunks)
            success = False
            error_message = str(exc)[:200]

        latency_ms = (time.perf_counter() - start_time) * 1000.0

        result = SparseInferenceResult(
            vectors=vectors,
            fallback_count=len(fallback_indices),
            fallback_indices=fallback_indices,
            latency_ms=round(latency_ms, 2),
            device=device,
            model_name=model_name,
            success=success,
            error_message=error_message,
        )

        # Emit telemetry for this sparse inference run
        self._record_telemetry(result, len(chunks))

        return result

    def _generate_with_cpu(
        self,
        chunks: Sequence[ChunkRecord],
        sparse_model: SentenceTransformer,
        model_name: str,
    ) -> tuple[List[Optional[Dict[str, Any]]], List[int], str]:
        """Execute sparse inference on CPU.

        Args:
            chunks: Sequence of chunk records.
            sparse_model: Loaded sparse model instance.
            model_name: Name of the sparse model.

        Returns:
            Tuple of (vectors, fallback_indices, device).
        """
        self.logger.debug(
            "Running sparse inference on CPU for %d chunks with model %s",
            len(chunks),
            model_name,
        )

        vectors: List[Optional[Dict[str, Any]]] = []
        fallback_indices: List[int] = []

        texts = [chunk.text for chunk in chunks]

        try:
            # Encode texts to produce sparse vectors
            # Note: Actual SPLADE-style models return token-level weights
            embeddings = sparse_model.encode(
                texts,
                convert_to_tensor=False,
                show_progress_bar=False,
            )

            for idx, embedding in enumerate(embeddings):
                vector = self._convert_embedding_to_sparse_vector(embedding)
                if vector is None:
                    # Fallback to metadata-derived vector
                    fallback_vector = build_sparse_vector_from_metadata(
                        chunks[idx].metadata
                    )
                    vectors.append(fallback_vector)
                    fallback_indices.append(idx)
                else:
                    vectors.append(vector)

        except Exception as exc:  # pragma: no cover
            self.logger.warning(
                "CPU sparse inference failed for model %s: %s; falling back to metadata",
                model_name,
                exc,
            )
            # Full fallback to metadata
            for idx, chunk in enumerate(chunks):
                fallback_vector = build_sparse_vector_from_metadata(chunk.metadata)
                vectors.append(fallback_vector)
                fallback_indices.append(idx)

        return vectors, fallback_indices, "cpu"

    def _generate_with_gpu(
        self,
        chunks: Sequence[ChunkRecord],
        sparse_model: SentenceTransformer,
        model_name: str,
        device_ids: Optional[List[int]],
    ) -> tuple[List[Optional[Dict[str, Any]]], List[int], str]:
        """Execute sparse inference on GPU with leasing and VRAM enforcement.

        Args:
            chunks: Sequence of chunk records.
            sparse_model: Loaded sparse model instance.
            model_name: Name of the sparse model.
            device_ids: Optional list of GPU device IDs for leasing.

        Returns:
            Tuple of (vectors, fallback_indices, device).
        """
        self.logger.debug(
            "Running sparse inference on GPU for %d chunks with model %s",
            len(chunks),
            model_name,
        )

        vectors: List[Optional[Dict[str, Any]]] = []
        fallback_indices: List[int] = []
        device = "cpu"

        try:
            # Lease GPUs for exclusive sparse inference
            with lease_gpus(
                self.embedder,
                model_name,
                self.logger,
                device_ids=device_ids,
            ) as lease:
                # Hydrate model to GPU
                hydrated_model = self.embedder.model_manager.hydrate_model_to_gpus(
                    model_name,
                    device_ids=lease.device_ids,
                )

                if hydrated_model is None:
                    self.logger.warning(
                        "Failed to hydrate sparse model %s to GPU; falling back to CPU",
                        model_name,
                    )
                    return self._generate_with_cpu(chunks, sparse_model, model_name)

                device_id = lease.device_ids[0] if lease.device_ids else 0
                device = f"cuda:{device_id}"

                # Enforce VRAM cap before processing
                can_proceed, suggested_batch_size = self._enforce_vram_cap(
                    device_id,
                    len(chunks),
                )

                if not can_proceed:
                    self.logger.error(
                        "VRAM cap violation detected; falling back to CPU inference"
                    )
                    self.embedder.model_manager.stage_model_to_cpu(model_name)
                    return self._generate_with_cpu(chunks, sparse_model, model_name)

                # Use adaptive batch size if suggested
                batch_size = suggested_batch_size or len(chunks)
                if suggested_batch_size:
                    self.logger.info(
                        "Using adaptive batch size %d (original: %d) due to VRAM constraints",
                        batch_size,
                        len(chunks),
                    )

                texts = [chunk.text for chunk in chunks]

                # Process in batches if adaptive sizing is active
                if batch_size < len(chunks):
                    embeddings_list = []
                    for i in range(0, len(chunks), batch_size):
                        batch_texts = texts[i : i + batch_size]
                        
                        # Check VRAM before each batch
                        can_proceed, _ = self._enforce_vram_cap(device_id, batch_size)
                        if not can_proceed:
                            self.logger.error(
                                "VRAM cap violation during batch %d; aborting GPU inference",
                                i // batch_size,
                            )
                            self.embedder.model_manager.stage_model_to_cpu(model_name)
                            return self._generate_with_cpu(chunks, sparse_model, model_name)
                        
                        batch_embeddings = hydrated_model.encode(
                            batch_texts,
                            convert_to_tensor=True,
                            device=device,
                            show_progress_bar=False,
                        )
                        embeddings_list.append(batch_embeddings)
                    
                    # Concatenate all batch results
                    embeddings = torch.cat(embeddings_list, dim=0)
                else:
                    # Process all at once
                    embeddings = hydrated_model.encode(
                        texts,
                        convert_to_tensor=True,
                        device=device,
                        show_progress_bar=False,
                    )

                # Convert tensor embeddings to sparse vectors
                if isinstance(embeddings, torch.Tensor):
                    embeddings = embeddings.cpu().numpy()

                for idx, embedding in enumerate(embeddings):
                    vector = self._convert_embedding_to_sparse_vector(embedding)
                    if vector is None:
                        fallback_vector = build_sparse_vector_from_metadata(
                            chunks[idx].metadata
                        )
                        vectors.append(fallback_vector)
                        fallback_indices.append(idx)
                    else:
                        vectors.append(vector)

                # Record peak VRAM usage in telemetry
                final_vram_stats = self._check_vram_usage(device_id)
                self.embedder.telemetry.record_metrics_status(
                    "sparse_vram_usage",
                    emitted=True,
                    reason=None,
                    metrics=["peak_vram_gb", "utilization_ratio"],
                    details={
                        "peak_vram_gb": final_vram_stats["used_gb"],
                        "utilization_ratio": final_vram_stats["utilization_ratio"],
                        "batch_size": batch_size,
                        "chunks_processed": len(chunks),
                    },
                )

                # Stage model back to CPU after inference
                self.embedder.model_manager.stage_model_to_cpu(model_name)

        except Exception as exc:  # pragma: no cover
            self.logger.warning(
                "GPU sparse inference failed for model %s: %s; falling back to CPU",
                model_name,
                exc,
            )
            return self._generate_with_cpu(chunks, sparse_model, model_name)

        return vectors, fallback_indices, device

    def _convert_embedding_to_sparse_vector(
        self,
        embedding: Any,
    ) -> Optional[Dict[str, Any]]:
        """Convert a dense embedding to a sparse vector structure.

        For SPLADE-style models, this extracts non-zero token weights.
        For dense embeddings, we simulate sparsity by keeping top-k values.

        Args:
            embedding: Embedding array (numpy or torch).

        Returns:
            Sparse vector dict with indices, values, tokens, and stats, or None.
        """
        if embedding is None:
            return None

        try:
            if isinstance(embedding, torch.Tensor):
                embedding = embedding.cpu().numpy()

            if not isinstance(embedding, np.ndarray):
                embedding = np.array(embedding)

            # For SPLADE-style sparse models, keep non-zero weights
            # For dense models, simulate sparsity by keeping top-k values
            nonzero_indices = np.where(np.abs(embedding) > 1e-6)[0]

            if len(nonzero_indices) == 0:
                # No significant values
                return None

            indices = nonzero_indices.tolist()
            values = embedding[nonzero_indices].tolist()

            # Normalize values
            vector = np.array(values, dtype=np.float32)
            norm = float(np.linalg.norm(vector))
            if norm > 0:
                normalized_values = (vector / norm).tolist()
            else:
                normalized_values = vector.tolist()

            # Generate token placeholders (actual tokens would come from tokenizer)
            tokens = [f"token_{idx}" for idx in indices]

            return {
                "indices": indices,
                "values": normalized_values,
                "tokens": tokens,
                "stats": {
                    "weight_norm": norm,
                    "unique_terms": len(indices),
                    "total_terms": len(embedding),
                    "weighting": "normalized",
                },
            }

        except Exception as exc:  # pragma: no cover
            self.logger.debug(
                "Failed to convert embedding to sparse vector: %s",
                exc,
            )
            return None

    def _check_vram_usage(self, device_id: int = 0) -> Dict[str, float]:
        """Check current VRAM usage on specified GPU device.

        Args:
            device_id: GPU device ID to check.

        Returns:
            Dict with 'used_gb', 'total_gb', and 'utilization_ratio'.
        """
        if not torch.cuda.is_available():
            return {"used_gb": 0.0, "total_gb": 0.0, "utilization_ratio": 0.0}

        try:
            torch.cuda.synchronize(device_id)
            used_bytes = torch.cuda.memory_allocated(device_id)
            total_bytes = torch.cuda.get_device_properties(device_id).total_memory
            used_gb = used_bytes / (1024**3)
            total_gb = total_bytes / (1024**3)
            return {
                "used_gb": round(used_gb, 2),
                "total_gb": round(total_gb, 2),
                "utilization_ratio": round(used_gb / total_gb, 3) if total_gb > 0 else 0.0,
            }
        except Exception as exc:  # pragma: no cover
            self.logger.warning("Failed to check VRAM usage: %s", exc)
            return {"used_gb": 0.0, "total_gb": 0.0, "utilization_ratio": 0.0}

    def _enforce_vram_cap(
        self,
        device_id: int,
        current_batch_size: int,
    ) -> tuple[bool, Optional[int]]:
        """Enforce VRAM cap by checking usage and suggesting adaptive batch size.

        Args:
            device_id: GPU device ID to monitor.
            current_batch_size: Current batch size being processed.

        Returns:
            Tuple of (can_proceed, suggested_batch_size).
            If can_proceed is False, must abort or fallback to CPU.
            If suggested_batch_size is provided, retry with smaller batch.
        """
        vram_stats = self._check_vram_usage(device_id)
        used_gb = vram_stats["used_gb"]
        utilization = vram_stats["utilization_ratio"]

        # Hard cap violation - must abort
        if used_gb > self._vram_cap_gb:
            self.logger.error(
                "VRAM usage %.2f GB exceeds hard cap %.2f GB on device %d; aborting GPU inference",
                used_gb,
                self._vram_cap_gb,
                device_id,
            )
            # Record telemetry for VRAM violation
            self.embedder.telemetry.record_metrics_status(
                "sparse_vram_violation",
                emitted=True,
                reason=f"VRAM usage {used_gb:.2f}GB exceeded cap {self._vram_cap_gb:.2f}GB",
                metrics=["vram_used_gb", "vram_cap_gb", "batch_size"],
                details={
                    "vram_used_gb": used_gb,
                    "vram_cap_gb": self._vram_cap_gb,
                    "batch_size": current_batch_size,
                },
            )
            return False, None

        # Soft limit warning - reduce batch size adaptively
        if used_gb > self._vram_soft_limit_gb:
            suggested_batch_size = max(
                self._min_batch_size,
                int(current_batch_size * 0.5),
            )
            self.logger.warning(
                "VRAM usage %.2f GB exceeds soft limit %.2f GB on device %d; "
                "suggesting batch size reduction from %d to %d",
                used_gb,
                self._vram_soft_limit_gb,
                device_id,
                current_batch_size,
                suggested_batch_size,
            )
            return True, suggested_batch_size

        return True, None

    def _fallback_to_metadata(
        self,
        chunks: Sequence[ChunkRecord],
    ) -> tuple[List[Optional[Dict[str, Any]]], List[int]]:
        """Fallback to metadata-derived sparse vectors for all chunks.

        Args:
            chunks: Sequence of chunk records.

        Returns:
            Tuple of (vectors, fallback_indices).
        """
        vectors: List[Optional[Dict[str, Any]]] = []
        fallback_indices = list(range(len(chunks)))

        for chunk in chunks:
            fallback_vector = build_sparse_vector_from_metadata(chunk.metadata)
            vectors.append(fallback_vector)

        self.logger.info(
            "Applied metadata fallback for %d chunks",
            len(chunks),
        )

        return vectors, fallback_indices

    def _record_telemetry(
        self,
        result: SparseInferenceResult,
        chunk_count: int,
    ) -> None:
        """Record telemetry for sparse inference run.

        Args:
            result: Sparse inference result.
            chunk_count: Number of chunks processed.
        """
        telemetry = self.embedder.telemetry

        # Record span presence for sparse stage
        telemetry.record_span_presence(
            "sparse_inference",
            active=result.success,
            reason=result.error_message if not result.success else None,
            attributes={
                "model": result.model_name,
                "device": result.device,
                "latency_ms": result.latency_ms,
                "fallback_count": result.fallback_count,
                "chunk_count": chunk_count,
                "fallback_ratio": round(result.fallback_count / max(1, chunk_count), 4),
            },
        )

        # Record metrics status for sparse stage
        telemetry.record_metrics_status(
            "sparse",
            emitted=result.success,
            reason=result.error_message if not result.success else None,
            metrics=["latency_ms", "fallback_count", "device"],
            details={
                "latency_ms": result.latency_ms,
                "fallback_count": result.fallback_count,
                "device": result.device,
            },
        )

        self.logger.debug(
            "Sparse inference telemetry recorded: model=%s device=%s latency=%.2fms fallback=%d/%d",
            result.model_name,
            result.device,
            result.latency_ms,
            result.fallback_count,
            chunk_count,
        )


__all__ = ["SparseVectorGenerator", "ChunkRecord", "SparseInferenceResult"]
