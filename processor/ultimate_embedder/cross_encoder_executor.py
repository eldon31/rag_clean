"""CrossEncoder batch executor with GPU leasing and adaptive batching.

Provides rerank execution with memory-aware batching, OOM recovery,
and telemetry integration for the Ultimate Embedder ensemble pipeline.
"""

from __future__ import annotations

import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import torch

from processor.ultimate_embedder.config import KaggleGPUConfig, RerankingConfig
from processor.ultimate_embedder.gpu_lease import lease_gpus
from processor.ultimate_embedder.rerank_pipeline import RerankPipeline

if TYPE_CHECKING:  # pragma: no cover
    from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4


@dataclass
class CrossEncoderRerankRun:
    """Telemetry and export payload for a single rerank batch execution."""

    query: str
    candidate_ids: List[str] = field(default_factory=list)
    scores: List[float] = field(default_factory=list)
    latency_ms: float = 0.0
    gpu_peak_gb: float = 0.0
    batch_size: int = 0
    throughput_cands_per_sec: float = 0.0
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self) -> None:
        """Validate and truncate query string for privacy."""
        if len(self.query) > 100:
            self.query = self.query[:100]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary for JSON export."""
        return {
            "run_id": self.run_id,
            "query": self.query,
            "candidate_ids": self.candidate_ids,
            "scores": self.scores,
            "latency_ms": self.latency_ms,
            "gpu_peak_gb": self.gpu_peak_gb,
            "batch_size": self.batch_size,
            "throughput_cands_per_sec": self.throughput_cands_per_sec,
        }


class CrossEncoderBatchExecutor:
    """Execute CrossEncoder reranking with GPU leasing and dynamic batching.
    
    Orchestrates rerank inference with:
    - Adaptive batch sizing respecting 12 GB VRAM ceiling
    - Exclusive GPU leasing via context manager
    - OOM recovery with exponential backoff
    - Telemetry capture (latency, VRAM peak, lease events)
    """

    def __init__(
        self,
        config: RerankingConfig,
        gpu_config: KaggleGPUConfig,
        logger: logging.Logger,
        embedder: "UltimateKaggleEmbedderV4",
    ) -> None:
        """Initialize executor with configuration and embedder reference.
        
        Args:
            config: Reranking configuration with model name and top_k settings
            gpu_config: GPU configuration for memory ceiling calculations
            logger: Logger instance for diagnostic output
            embedder: Reference to embedder instance for telemetry access
        """
        self.config = config
        self.gpu_config = gpu_config
        self.logger = logger
        self.embedder = embedder
        self.rerank_pipeline = RerankPipeline(config, logger)

    def ensure_model(self, device: str) -> None:
        """Load CrossEncoder model via RerankPipeline if enabled.
        
        Args:
            device: Target device (e.g., 'cuda:0', 'cpu')
        """
        if not self.config.enable_reranking:
            self.logger.info("Reranking disabled, skipping model load")
            return

        self.logger.debug("Ensuring CrossEncoder model loaded on %s", device)
        self.rerank_pipeline.ensure_model(device=device)
        if self.rerank_pipeline.model is not None:
            self.embedder.reranker = self.rerank_pipeline.model
            self.embedder.reranker_device = getattr(self.rerank_pipeline, "device", device)

    def _calculate_optimal_batch_size(self) -> int:
        """Compute safe batch size respecting 12 GB memory ceiling.
        
        Uses GPU config parameters (vram_per_gpu_gb, max_memory_per_gpu)
        to estimate maximum batch size with 0.8 safety factor.
        
        Returns:
            Optimal batch size for rerank inference
        """
        # Default batch size from config
        base_batch_size = self.config.batch_size

        # Calculate available memory per GPU
        vram_gb = self.gpu_config.vram_per_gpu_gb
        max_memory_factor = self.gpu_config.max_memory_per_gpu
        safety_factor = 0.8

        # Available memory after safety margin
        available_gb = vram_gb * max_memory_factor * safety_factor

        # Estimate memory per candidate pair (heuristic: ~50 MB per pair for large models)
        memory_per_pair_gb = 0.05

        # Calculate optimal batch size
        optimal_batch = int(available_gb / memory_per_pair_gb)

        # Clamp to reasonable range
        optimal_batch = max(1, min(optimal_batch, base_batch_size))

        self.logger.info(
            "Rerank batch size: %d (max_memory=%.2f, vram=%.2fGB, safety=%.2f)",
            optimal_batch,
            max_memory_factor,
            vram_gb,
            safety_factor,
        )

        return optimal_batch

    def execute_rerank(
        self,
        query: str,
        candidate_ids: List[str],
        candidate_texts: List[str],
        top_k: int,
    ) -> CrossEncoderRerankRun:
        """Execute rerank with GPU leasing, adaptive batching, and telemetry.
        
        Args:
            query: Search query string
            candidate_ids: List of candidate document IDs
            candidate_texts: List of candidate document texts
            top_k: Number of top results to return
            
        Returns:
            CrossEncoderRerankRun payload with scores and telemetry
        """
        # Truncate query for privacy (early for all code paths)
        truncated_query = query[:100]
        
        # Handle empty candidate list
        if not candidate_ids or not candidate_texts:
            self.logger.warning("Empty candidate list, returning empty result")
            return CrossEncoderRerankRun(
                query=truncated_query,
                candidate_ids=[],
                scores=[],
                batch_size=0,
            )

        # Check if reranking enabled - clamp to top_k for contract compliance
        if not self.config.enable_reranking:
            clamped_ids = candidate_ids[:top_k]
            self.logger.warning(
                "Reranking disabled, returning top_k=%d results (out of %d candidates)",
                top_k,
                len(candidate_ids),
            )
            return CrossEncoderRerankRun(
                query=truncated_query,
                candidate_ids=clamped_ids,
                scores=[0.0] * len(clamped_ids),
                batch_size=0,
            )

        # Calculate optimal batch size
        batch_size = self._calculate_optimal_batch_size()

        # Determine execution path based on GPU availability
        use_gpu = (
            self.embedder.device == "cuda"
            and torch.cuda.is_available()
            and getattr(self.embedder, "device_count", 0) > 0
        )

        # Execute rerank with appropriate device handling
        start_time = time.time()
        gpu_peak_gb = 0.0
        throughput_cands_per_sec = 0.0

        try:
            if use_gpu:
                with lease_gpus(
                    self.embedder,
                    f"rerank-{self.config.model_name}",
                    self.logger,
                ) as lease:
                    device_index = lease.device_ids[0] if lease.device_ids else 0
                    target_device = f"cuda:{device_index}"
                    self.ensure_model(device=target_device)

                    # Execute rerank with OOM recovery on GPU
                    scores = self._execute_rerank_with_retry(
                        query=query,
                        candidate_texts=candidate_texts,
                        batch_size=batch_size,
                    )

                    if torch.cuda.is_available():
                        torch.cuda.synchronize(device_index)
                        gpu_peak_bytes = torch.cuda.max_memory_allocated(device_index)
                        gpu_peak_gb = gpu_peak_bytes / (1024 ** 3)
                        self.logger.debug("Peak GPU memory: %.2f GB", gpu_peak_gb)
            else:
                self.logger.info("GPU unavailable; running CrossEncoder rerank on CPU")
                self.ensure_model(device="cpu")
                scores = self._execute_rerank_with_retry(
                    query=query,
                    candidate_texts=candidate_texts,
                    batch_size=batch_size,
                )

        except Exception as exc:  # pragma: no cover
            self.logger.error("Rerank execution failed: %s", exc)
            # Return fallback result with zero scores
            latency_ms = (time.time() - start_time) * 1000
            if latency_ms > 0 and candidate_texts:
                throughput_cands_per_sec = len(candidate_texts) / (latency_ms / 1000.0)
                self.logger.info(
                    "Rerank throughput: %.2f candidates/sec",
                    throughput_cands_per_sec,
                )
            return CrossEncoderRerankRun(
                query=truncated_query,
                candidate_ids=candidate_ids[:top_k],
                scores=[0.0] * min(top_k, len(candidate_ids)),
                latency_ms=latency_ms,
                gpu_peak_gb=gpu_peak_gb,
                batch_size=batch_size,
                throughput_cands_per_sec=throughput_cands_per_sec,
            )

        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        if latency_ms > 0 and candidate_texts:
            throughput_cands_per_sec = len(candidate_texts) / (latency_ms / 1000.0)
        else:
            throughput_cands_per_sec = 0.0

        if throughput_cands_per_sec > 0.0:
            self.logger.info(
                "Rerank throughput: %.2f candidates/sec",
                throughput_cands_per_sec,
            )

        # Rank candidates by score and return top_k
        import numpy as np
        ranked_indices = np.argsort(scores)[::-1][:top_k]
        
        top_candidate_ids = [candidate_ids[idx] for idx in ranked_indices]
        top_scores = [float(scores[idx]) for idx in ranked_indices]

        self.logger.info(
            "Rerank complete: top_k=%d, latency=%.2fms, peak_gpu=%.2fGB",
            len(top_candidate_ids),
            latency_ms,
            gpu_peak_gb,
        )

        return CrossEncoderRerankRun(
            query=truncated_query,
            candidate_ids=top_candidate_ids,
            scores=top_scores,
            latency_ms=latency_ms,
            gpu_peak_gb=gpu_peak_gb,
            batch_size=batch_size,
            throughput_cands_per_sec=throughput_cands_per_sec,
        )

    def _execute_rerank_with_retry(
        self,
        query: str,
        candidate_texts: List[str],
        batch_size: int,
        max_retries: int = 3,
    ) -> List[float]:
        """Execute rerank with OOM recovery via batch halving.
        
        Args:
            query: Search query string
            candidate_texts: List of candidate document texts
            batch_size: Initial batch size
            max_retries: Maximum retry attempts on OOM
            
        Returns:
            List of rerank scores for all candidates
            
        Raises:
            RuntimeError: If rerank fails after max retries
        """
        if self.rerank_pipeline.model is None:
            raise RuntimeError("CrossEncoder model not loaded")

        current_batch_size = batch_size
        attempt = 0

        while attempt < max_retries:
            try:
                # Prepare query-document pairs
                query_doc_pairs = [[query, text] for text in candidate_texts]

                # Execute rerank in batches if needed
                if len(query_doc_pairs) <= current_batch_size:
                    # Single batch
                    scores = self.rerank_pipeline.model.predict(query_doc_pairs)
                else:
                    # Multiple batches
                    scores = []
                    for i in range(0, len(query_doc_pairs), current_batch_size):
                        batch = query_doc_pairs[i:i + current_batch_size]
                        batch_scores = self.rerank_pipeline.model.predict(batch)
                        scores.extend(batch_scores)

                # Success - return scores
                return list(scores)

            except torch.cuda.OutOfMemoryError as oom_error:
                attempt += 1
                if attempt >= max_retries:
                    self.logger.error(
                        "OOM after %d attempts, raising exception",
                        max_retries,
                    )
                    raise RuntimeError(
                        f"Rerank failed after {max_retries} OOM recovery attempts"
                    ) from oom_error

                # Halve batch size and retry
                new_batch_size = max(1, current_batch_size // 2)
                self.logger.warning(
                    "OOM during rerank, reducing batch size: %d -> %d (attempt %d/%d)",
                    current_batch_size,
                    new_batch_size,
                    attempt,
                    max_retries,
                )

                # Clear cache before retry
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

                current_batch_size = new_batch_size

            except Exception as exc:  # pragma: no cover
                self.logger.error("Rerank inference failed: %s", exc)
                raise RuntimeError(f"Rerank inference failed: {exc}") from exc

        # Should not reach here
        raise RuntimeError("Rerank failed: unexpected error")  # pragma: no cover


__all__ = ["CrossEncoderBatchExecutor", "CrossEncoderRerankRun"]
