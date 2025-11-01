"""Adaptive batch processing pipeline for Ultimate Embedder."""

from __future__ import annotations

import gc
import logging
import math
import time
from contextlib import nullcontext
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, cast

import numpy as np
import torch
from tqdm import tqdm

from processor.ultimate_embedder.config import EnsembleConfig
from processor.ultimate_embedder.controllers import AdaptiveBatchController
from processor.ultimate_embedder.progress import BatchProgressContext
from processor.ultimate_embedder.sparse_generator import SparseVectorGenerator, ChunkRecord, SparseInferenceResult
from sklearn.preprocessing import normalize

if TYPE_CHECKING:  # pragma: no cover
    from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4


class _BatchProgressTracker:
    """Track batch progress indices and total counts for a run."""

    def __init__(self, total_chunks: int, initial_total_batch: int) -> None:
        estimate = 1
        if total_chunks > 0 and initial_total_batch > 0:
            estimate = max(1, math.ceil(total_chunks / initial_total_batch))
        self.completed: int = 0
        self.total_batches: int = estimate

    def ensure_capacity(self, pending_batches: int) -> None:
        required_total = self.completed + max(1, pending_batches)
        if required_total > self.total_batches:
            self.total_batches = required_total

    def build_context(self, label: Optional[str], model_name: Optional[str] = None) -> BatchProgressContext:
        return BatchProgressContext(
            batch_index=self.completed,
            total_batches=self.total_batches,
            label=label,
            model_name=model_name,
        )

    def mark_completed(self) -> None:
        self.completed += 1


class BatchRunner:
    """Coordinate adaptive batch embedding generation for the facade."""

    def __init__(self, embedder: "UltimateKaggleEmbedderV4", logger: logging.Logger) -> None:
        self.embedder = embedder
        self.logger = logger

    def _prepare_chunk_records(self, embedder: "UltimateKaggleEmbedderV4") -> List[ChunkRecord]:
        """Prepare ChunkRecord instances from embedder state.
        
        Args:
            embedder: The embedder instance with chunk_texts and chunks_metadata
            
        Returns:
            List of ChunkRecord instances ready for sparse inference
        """
        chunk_records: List[ChunkRecord] = []
        for idx, text in enumerate(embedder.chunk_texts):
            metadata = (
                embedder.chunks_metadata[idx]
                if embedder.chunks_metadata and idx < len(embedder.chunks_metadata)
                else {}
            )
            chunk_records.append(
                ChunkRecord(
                    text=text,
                    metadata=metadata or {},
                    chunk_id=str(idx),
                )
            )
        return chunk_records

    def _store_sparse_results(
        self,
        embedder: "UltimateKaggleEmbedderV4",
        sparse_result: SparseInferenceResult,
        logger: logging.Logger,
    ) -> None:
        """Store sparse inference results on embedder for export runtime.
        
        Args:
            embedder: The embedder instance to populate with sparse results
            sparse_result: The sparse inference result to store
            logger: Logger for status messages
        """
        logger.info(
            f"[SPARSE] Inference complete: model={sparse_result.model_name} "
            f"device={sparse_result.device} latency={sparse_result.latency_ms:.2f}ms "
            f"fallback={sparse_result.fallback_count}/{len(sparse_result.vectors)}"
        )
        
        # Store sparse result on embedder for export runtime
        embedder.sparse_inference_result = sparse_result
        
        # Populate sparse_vectors for export and processing summary
        embedder.sparse_vectors = sparse_result.vectors
        
        # Populate sparse model tracking
        if sparse_result.model_name not in embedder.sparse_model_names:
            embedder.sparse_model_names.append(sparse_result.model_name)
        embedder.sparse_device_map[sparse_result.model_name] = sparse_result.device

    def _record_progress_event(
        self,
        context: Optional[BatchProgressContext],
        *,
        status: str,
        model: str,
        device: Optional[str] = None,
        attempt: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        if context is None:
            return

        telemetry = self.embedder.telemetry
        telemetry.record_batch_progress(
            batch_index=context.batch_index,
            total_batches=context.total_batches,
            label=context.label,
            status=status,
            model=model,
            device=device,
            attempt=attempt,
            metadata=metadata,
        )

    def _build_rerank_query(self, embedder: "UltimateKaggleEmbedderV4") -> str:
        """Construct a synthetic query string for rerank telemetry."""

        try:
            collection_name = embedder.get_target_collection_name()
        except Exception:  # pragma: no cover - defensive path
            collection_name = "collection"

        sample_text = ""
        if embedder.chunk_texts:
            first_chunk = embedder.chunk_texts[0]
            if isinstance(first_chunk, str):
                sample_text = first_chunk.strip().splitlines()[0][:80]

        if sample_text:
            return f"Summarize {collection_name}: {sample_text}"

        return f"Summarize collection {collection_name}"

    def _assemble_fused_candidates(
        self,
        embedder: "UltimateKaggleEmbedderV4",
        embeddings: np.ndarray,
    ) -> Dict[str, Any]:
        """Build fused candidate payload mirroring dense similarity retrieval."""

        if embeddings.size == 0:
            return {}

        total_points = embeddings.shape[0]
        candidate_limit = embedder.reranking_config.top_k_candidates
        if candidate_limit <= 0 or candidate_limit > total_points:
            candidate_limit = total_points

        query_vector = embeddings.mean(axis=0)
        if np.ndim(query_vector) != 1:
            query_vector = np.reshape(query_vector, (-1,))

        norm = float(np.linalg.norm(query_vector))
        if norm > 0.0:
            query_vector = query_vector / norm

        similarity_scores = embeddings @ query_vector
        top_indices = np.argsort(similarity_scores)[::-1][:candidate_limit]

        candidate_ids: List[str] = []
        candidate_texts: List[str] = []
        candidate_metadata: List[Dict[str, Any]] = []
        dense_scores: List[float] = []

        for idx in top_indices:
            candidate_ids.append(str(int(idx)))
            if idx < len(embedder.chunk_texts):
                text_value = embedder.chunk_texts[idx]
            else:
                text_value = ""
            if not isinstance(text_value, str):
                text_value = str(text_value)
            candidate_texts.append(text_value)

            metadata_value: Dict[str, Any] = {}
            if idx < len(embedder.chunks_metadata):
                raw_meta = embedder.chunks_metadata[idx]
                if isinstance(raw_meta, dict):
                    metadata_value = dict(raw_meta)
            candidate_metadata.append(metadata_value)

            dense_scores.append(float(similarity_scores[idx]))

        return {
            "query": self._build_rerank_query(embedder),
            "candidate_ids": candidate_ids,
            "candidate_texts": candidate_texts,
            "metadata": candidate_metadata,
            "dense_scores": dense_scores,
            "indices": [int(idx) for idx in top_indices],
            "total_candidates": candidate_limit,
        }

    def _run_rerank_stage(
        self,
        embedder: "UltimateKaggleEmbedderV4",
        embeddings: np.ndarray,
    ) -> None:
        """Execute CrossEncoder-based reranking after dense+sparse fusion."""

        logger = self.logger

        embedder.fused_candidates = {}
        embedder.rerank_run = None
        embedder.rerank_candidate_scores = {}
        embedder.rerank_failure_reason = None
        embedder.rerank_fallback_count = 0
        embedder.rerank_fallback_reason = None
        embedder.rerank_fallback_source = None

        fused_candidates = self._assemble_fused_candidates(embedder, embeddings)
        if not fused_candidates:
            logger.warning("[RERANK] No candidates available for rerank stage; skipping execution")
            embedder.rerank_failure_reason = "No candidates available"
            embedder._rerank_runtime_reason = embedder.rerank_failure_reason
            embedder.rerank_fallback_count = 1
            embedder.rerank_fallback_reason = "no_candidates"
            embedder.rerank_fallback_source = "runtime"
            return

        embedder.fused_candidates = fused_candidates

        if not embedder.reranking_config.enable_reranking:
            logger.info("[RERANK] Rerank stage disabled; fused candidates persisted for telemetry")
            embedder.rerank_failure_reason = "Rerank disabled via feature toggles"
            embedder._rerank_runtime_reason = embedder.rerank_failure_reason
            source = embedder.feature_toggles.sources.get("enable_rerank", "default")
            embedder.rerank_fallback_count = 1
            embedder.rerank_fallback_reason = "feature_disabled"
            embedder.rerank_fallback_source = source
            return

        executor = embedder.cross_encoder_executor
        if executor is None:
            logger.warning("[RERANK] CrossEncoder executor unavailable; skipping execution")
            embedder.rerank_failure_reason = "CrossEncoder executor unavailable"
            embedder._rerank_runtime_reason = embedder.rerank_failure_reason
            embedder.rerank_fallback_count = 1
            embedder.rerank_fallback_reason = "executor_unavailable"
            embedder.rerank_fallback_source = "runtime"
            return

        candidate_ids = fused_candidates.get("candidate_ids", [])
        candidate_texts = fused_candidates.get("candidate_texts", [])
        if not candidate_ids or not candidate_texts:
            logger.warning("[RERANK] Candidate payload empty; skipping execution")
            embedder.rerank_failure_reason = "Candidate payload empty"
            embedder._rerank_runtime_reason = embedder.rerank_failure_reason
            embedder.rerank_fallback_count = 1
            embedder.rerank_fallback_reason = "candidate_payload_empty"
            embedder.rerank_fallback_source = "runtime"
            return

        top_k = embedder.reranking_config.rerank_top_k
        if top_k <= 0:
            top_k = len(candidate_ids)
        top_k = min(top_k, len(candidate_ids))

        try:
            rerank_run = executor.execute_rerank(
                query=fused_candidates.get("query", ""),
                candidate_ids=candidate_ids,
                candidate_texts=candidate_texts,
                top_k=top_k,
            )
        except Exception as exc:  # pragma: no cover - defensive fallback
            logger.warning("[RERANK] Execution failed: %s", exc)
            embedder.rerank_failure_reason = str(exc)[:160]
            embedder._rerank_runtime_reason = embedder.rerank_failure_reason
            embedder.rerank_run = None
            embedder.rerank_candidate_scores = {}
            embedder.rerank_fallback_count = 1
            embedder.rerank_fallback_reason = "execution_failed"
            embedder.rerank_fallback_source = "runtime"
            return

        embedder.rerank_run = rerank_run
        embedder.rerank_candidate_scores = {
            candidate_id: score
            for candidate_id, score in zip(rerank_run.candidate_ids, rerank_run.scores)
        }
        embedder.rerank_failure_reason = None
        embedder._rerank_runtime_reason = None
        embedder.rerank_fallback_count = 0
        embedder.rerank_fallback_reason = None
        embedder.rerank_fallback_source = None

        candidate_metadata = fused_candidates.get("metadata", [])
        candidate_lookup = {
            cid: meta for cid, meta in zip(candidate_ids, candidate_metadata)
        }
        reranked_metadata = [candidate_lookup.get(cid, {}) for cid in rerank_run.candidate_ids]
        embedder.fused_candidates["reranked_metadata"] = reranked_metadata
        embedder.fused_candidates["reranked_candidate_ids"] = list(rerank_run.candidate_ids)
        embedder.fused_candidates["reranked_scores"] = list(rerank_run.scores)

        logger.info(
            "[RERANK] CrossEncoder stage completed: %s candidates → %s top results (latency=%.2fms, peak=%.2fGB)",
            len(candidate_ids),
            len(rerank_run.candidate_ids),
            rerank_run.latency_ms,
            rerank_run.gpu_peak_gb,
        )

    def generate_ensemble_embeddings(
        self,
        texts: List[str],
        batch_slice: Optional[slice] = None,
        batch_index: Optional[int] = None,
        progress_context: Optional[BatchProgressContext] = None,
    ) -> np.ndarray:
        """Generate embeddings using the configured ensemble pipeline."""

        embedder = self.embedder
        logger = self.logger

        if not embedder.enable_ensemble or not embedder.ensemble_config:
            logger.debug("Ensemble not enabled, using primary model only")
            primary_model = embedder._get_primary_model()
            primary_batch = embedder._get_batch_hint_for_model(embedder.model_name)

            embedder._log_gpu_memory("Primary encode (non-ensemble) - before")
            try:
                result = embedder._call_encode(
                    primary_model,
                    texts,
                    batch_size=primary_batch,
                    device=embedder.device,
                    progress_context=progress_context,
                )
                result = embedder._normalize_embedding_matrix(result, embedder.model_name)
            except Exception as exc:
                self._record_progress_event(
                    progress_context,
                    status="failed",
                    model=embedder.model_name,
                    device=embedder.device,
                    metadata={"error": str(exc)[:200]},
                )
                embedder._log_gpu_memory("Primary encode (non-ensemble) - after")
                raise
            else:
                embedder._log_gpu_memory("Primary encode (non-ensemble) - after")
                self._record_progress_event(
                    progress_context,
                    status="completed",
                    model=embedder.model_name,
                    device=embedder.device,
                )

            if embedder.device == "cuda":
                torch.cuda.empty_cache()

            return result

        if not embedder.ensemble_config.exclusive_mode:
            logger.info("Forcing exclusive_mode=True (legacy ensemble paths removed)")
            embedder.ensemble_config.exclusive_mode = True

        slice_info = embedder._describe_batch_slice(batch_slice)
        slice_summary = embedder._format_batch_slice_info(slice_info)

        ordered_models: List[str] = []
        seen: Set[str] = set()
        for candidate in [embedder.model_name, *embedder.ensemble_config.ensemble_models]:
            if candidate not in seen:
                ordered_models.append(candidate)
                seen.add(candidate)

        target_dim = embedder.matryoshka_dim or embedder.model_config.vector_dim
        model_weights: Dict[str, float] = {}
        all_embeddings: List[np.ndarray] = []
        successful_models: List[str] = []

        from processor.ultimate_embedder.gpu_lease import lease_gpus

        chunk_start = slice_info.get("start") if slice_info else None
        chunk_end = slice_info.get("end") if slice_info else None
        chunk_count = slice_info.get("count") if slice_info else len(texts)
        chunk_samples = slice_info.get("samples") if slice_info else []

        previous_model: Optional[str] = None

        for model_idx, model_name in enumerate(ordered_models):
            weight = (
                embedder.ensemble_config.model_weights.get(model_name, 1.0)
                if embedder.ensemble_config.model_weights
                else 1.0
            )

            base_rotation_event: Dict[str, Any] = {
                "batch_index": batch_index,
                "model": model_name,
                "aggregation_weight": weight,
                "chunk_start": chunk_start,
                "chunk_end": chunk_end,
                "chunk_count": chunk_count,
                "chunk_samples": [dict(sample) for sample in chunk_samples] if chunk_samples else [],
                "mode": "exclusive",
            }

            if previous_model:
                if embedder.device == "cuda":
                    embedder.model_manager.stage_model_to_cpu(previous_model)
                else:
                    embedder.model_manager.dispose_model(previous_model)

            embedder._record_rotation_event({**base_rotation_event, "status": "acquiring_lease"})

            with lease_gpus(embedder, model_name, logger) as lease:
                embedder._record_rotation_event({**base_rotation_event, "status": "lease_acquired"})

                model = embedder.model_manager.hydrate_model_to_gpus(
                    model_name,
                    device_ids=lease.device_ids,
                )

                if model is None:
                    embedder._record_rotation_event({**base_rotation_event, "status": "missing_model"})
                    self._record_progress_event(
                        progress_context,
                        status="failed",
                        model=model_name,
                        device=None,
                        metadata={"mode": "exclusive", "reason": "hydrate_failed"},
                    )
                    raise RuntimeError(f"Exclusive ensemble model '{model_name}' could not be hydrated")

                batch_hint = embedder._get_batch_hint_for_model(model_name)
                target_device = (
                    f"cuda:{lease.device_ids[0]}"
                    if embedder.device == "cuda" and lease.device_ids
                    else embedder.device
                )

                logger.info(
                    "[ENSEMBLE] %s exclusive pass starting | device=%s | batch_hint=%d | chunks=%s",
                    model_name,
                    target_device,
                    batch_hint,
                    slice_summary,
                )

                try:
                    embeddings = embedder._call_encode(
                        model,
                        texts,
                        batch_size=batch_hint,
                        device=target_device,
                        progress_context=progress_context,
                    )
                    embeddings = embedder._normalize_embedding_matrix(embeddings, model_name)
                    embeddings, adjusted = embedder._ensure_embedding_dimension(
                        embeddings,
                        expected_dim=target_dim,
                    )
                    if adjusted:
                        logger.debug(
                            "[ENSEMBLE] %s embedding trimmed to %sD for aggregation",
                            model_name,
                            embeddings.shape[1],
                        )

                    all_embeddings.append(embeddings)
                    successful_models.append(model_name)
                    model_weights[model_name] = weight

                    lease_summary = lease.summarize()
                    logger.info("[ENSEMBLE] %s lease summary: %s", model_name, lease_summary)

                    embedder._record_rotation_event({**base_rotation_event, "status": "completed"})
                    self._record_progress_event(
                        progress_context,
                        status="completed",
                        model=model_name,
                        device=target_device,
                        metadata={
                            "mode": "exclusive",
                            "model_pass": model_idx + 1,
                            "total_passes": len(ordered_models),
                        },
                    )
                except Exception as exc:
                    embedder.failed_ensemble_models.add(model_name)
                    embedder._record_rotation_event(
                        {**base_rotation_event, "status": "failed", "error": str(exc)[:200]}
                    )
                    self._record_progress_event(
                        progress_context,
                        status="failed",
                        model=model_name,
                        device=target_device,
                        metadata={"mode": "exclusive", "error": str(exc)[:200]},
                    )
                    logger.error("[ENSEMBLE] %s exclusive pass failed: %s", model_name, exc)
                    raise
                finally:
                    if embedder.device == "cuda":
                        torch.cuda.empty_cache()
                        gc.collect()

            previous_model = model_name

        if previous_model:
            if embedder.device == "cuda":
                embedder.model_manager.stage_model_to_cpu(previous_model)
            else:
                embedder.model_manager.dispose_model(previous_model)

        if not all_embeddings:
            raise RuntimeError("Ensemble generation produced no embeddings")

        if len(all_embeddings) == 1:
            final_embeddings = all_embeddings[0]
        else:
            weight_values = np.array(
                [model_weights.get(model_name, 1.0) for model_name in successful_models],
                dtype=np.float32,
            )

            if not np.isfinite(weight_values).all() or np.all(weight_values == 0):
                weight_values = np.ones(len(all_embeddings), dtype=np.float32)

            weight_values = weight_values / weight_values.sum()
            stacked = np.stack(all_embeddings, axis=0)
            final_embeddings = np.tensordot(weight_values, stacked, axes=1)

        if not all_embeddings:
            raise RuntimeError("Ensemble generation produced no embeddings")

        if len(all_embeddings) == 1:
            final_embeddings = all_embeddings[0]
        else:
            weight_values = np.array(
                [model_weights.get(model_name, 1.0) for model_name in successful_models],
                dtype=np.float32,
            )

            if not np.isfinite(weight_values).all() or np.all(weight_values == 0):
                weight_values = np.ones(len(all_embeddings), dtype=np.float32)

            weight_values = weight_values / weight_values.sum()
            stacked = np.stack(all_embeddings, axis=0)
            final_embeddings = np.tensordot(weight_values, stacked, axes=1)

        final_embeddings = normalize(final_embeddings, norm="l2", axis=1)
        return final_embeddings

    def run(self, enable_monitoring: bool, save_intermediate: bool) -> Dict[str, Any]:
        """Run embedding generation using exclusive ensemble mode.
        
        Exclusive mode is now the ONLY supported mode. All execution paths use
        model-first iteration with GPU leasing for optimal VRAM management.
        
        For single model (non-ensemble) scenarios, a minimal ensemble config
        is auto-created to unify the code path.
        """
        embedder = self.embedder
        logger = self.logger

        # Ensure ensemble config exists (even for single model)
        if not embedder.ensemble_config:
            logger.info("Creating ensemble config for single model mode")
            embedder.ensemble_config = EnsembleConfig(
                ensemble_models=[],  # Empty list = primary model only
                exclusive_mode=True
            )
        
        # Force exclusive mode (it's the only mode now)
        if not embedder.ensemble_config.exclusive_mode:
            logger.info("Forcing exclusive_mode=True (parallel mode removed)")
            embedder.ensemble_config.exclusive_mode = True
        
        # Always use exclusive ensemble mode
        return self.run_exclusive_ensemble(enable_monitoring, save_intermediate)

    def run_exclusive_ensemble(
        self,
        enable_monitoring: bool,
        save_intermediate: bool,
    ) -> Dict[str, Any]:
        """Run exclusive ensemble mode: iterate by model, leasing GPUs for each pass."""
        embedder = self.embedder
        logger = self.logger

        # Validate ensemble config (required for exclusive mode)
        if not embedder.ensemble_config:
            raise ValueError("Ensemble config required for exclusive ensemble mode")
        
        total_chunks = len(embedder.chunk_texts)
        logger.info("Starting EXCLUSIVE ensemble embedding generation")
        logger.info("Total chunks: %s", total_chunks)
        logger.info("Models: %s", embedder.ensemble_config.ensemble_models)

        # Prepare ordered model list
        ordered_models: List[str] = []
        seen: Set[str] = set()
        for candidate in [embedder.model_name, *embedder.ensemble_config.ensemble_models]:
            if candidate not in seen:
                ordered_models.append(candidate)
                seen.add(candidate)

        logger.info("Model execution order: %s", ordered_models)

        embedder.embeddings_by_model = {}
        embedder.telemetry.reset_runtime_state()
        embedder.processing_stats.clear()

        if enable_monitoring:
            embedder._start_performance_monitoring()

        start_time = time.time()
        per_model_embeddings: Dict[str, np.ndarray] = {}
        model_weights: Dict[str, float] = {}

        target_dim = embedder.matryoshka_dim or embedder.model_config.vector_dim

        try:
            # Import lease helper
            from processor.ultimate_embedder.gpu_lease import lease_gpus

            for model_idx, model_name in enumerate(ordered_models):
                model_start = time.time()
                
                logger.info(
                    "=" * 70
                )
                logger.info(
                    "MODEL PASS %d/%d: %s",
                    model_idx + 1,
                    len(ordered_models),
                    model_name,
                )
                logger.info("=" * 70)

                # Stage previous models to CPU if not the first model
                if model_idx > 0:
                    prev_model = ordered_models[model_idx - 1]
                    embedder.model_manager.stage_model_to_cpu(prev_model)
                    logger.info("Staged %s to CPU", prev_model)

                # Acquire GPU lease
                with lease_gpus(embedder, model_name, logger) as lease:
                    # Hydrate model onto leased GPUs
                    model = embedder.model_manager.hydrate_model_to_gpus(
                        model_name,
                        device_ids=lease.device_ids,
                    )

                    if model is None:
                        logger.warning("Failed to hydrate %s, skipping", model_name)
                        continue

                    # Reset adaptive controller for this model pass
                    batch_hint = embedder._get_batch_hint_for_model(model_name)
                    controller: Optional[AdaptiveBatchController] = None
                    if embedder.device == "cuda":
                        controller = AdaptiveBatchController(
                            primary_batch=batch_hint,
                            device_count=len(lease.device_ids),
                            gpu0_soft_limit_bytes=embedder.gpu0_soft_limit_bytes,
                            companion_enabled=False,  # No companions in exclusive mode
                        )
                        logger.info(
                            "Adaptive batch controller enabled for %s (initial batch: %d)",
                            model_name,
                            batch_hint,
                        )

                    # Progress tracker for this model
                    est_batches = max(1, math.ceil(total_chunks / batch_hint))
                    progress_tracker = _BatchProgressTracker(total_chunks, batch_hint)

                    # Create tqdm progress bar for batches (disabled on CPU)
                    show_batch_progress = embedder.device != "cpu"
                    pbar = tqdm(
                        total=total_chunks,
                        desc=f"Batches",
                        unit="chunk",
                        leave=False,
                        dynamic_ncols=True,
                        disable=not show_batch_progress
                    )
                    
                    # Update progress bar with chunk file name and model
                    chunk_file_name = "unknown"
                    if hasattr(embedder, 'chunks_metadata') and embedder.chunks_metadata and len(embedder.chunks_metadata) > 0:
                        first_metadata = embedder.chunks_metadata[0] or {}
                        chunk_file_name = first_metadata.get("chunk_file_name", "unknown")
                    pbar.set_description(f"Batches({chunk_file_name})")
                    pbar.set_postfix_str(model_name)

                    # Batch iteration for this model
                    model_embeddings: List[np.ndarray] = []
                    batch_index = 0
                    executed_batches = 0

                    while batch_index < total_chunks:
                        current_batch = controller.primary_batch if controller else batch_hint
                        batch_end = min(batch_index + current_batch, total_chunks)
                        batch_texts = embedder.chunk_texts[batch_index:batch_end]

                        if not batch_texts:
                            break

                        progress_label = embedder._get_batch_progress_label(batch_index, batch_end)
                        progress_context = progress_tracker.build_context(progress_label, model_name)

                        # Check memory and adapt
                        if controller and embedder.device == "cuda":
                            snapshots = embedder._collect_gpu_snapshots()
                            mitigation = controller.register_snapshot(snapshots)
                            if mitigation:
                                event_type = mitigation.pop("type", "adaptive_action")
                                embedder._record_mitigation(event_type, model=model_name, **mitigation)
                                torch.cuda.empty_cache()
                                gc.collect()
                                continue

                        # Encode batch
                        try:
                            target_device = (
                                f"cuda:{lease.device_ids[0]}"
                                if embedder.device == "cuda" and lease.device_ids
                                else embedder.device
                            )
                            batch_embeddings = embedder._call_encode(
                                model,
                                batch_texts,
                                batch_size=current_batch,
                                device=target_device,
                                progress_context=progress_context,
                            )
                            batch_embeddings = embedder._normalize_embedding_matrix(
                                batch_embeddings,
                                model_name,
                            )

                            # Ensure dimension and truncate if needed
                            batch_embeddings, _ = embedder._ensure_embedding_dimension(
                                batch_embeddings,
                                expected_dim=target_dim,
                            )

                            model_embeddings.append(batch_embeddings)
                            executed_batches += 1
                            progress_tracker.mark_completed()

                            self._record_progress_event(
                                progress_context,
                                status="completed",
                                model=model_name,
                                device=target_device,
                                metadata={
                                    "mode": "exclusive",
                                    "model_pass": model_idx + 1,
                                    "total_passes": len(ordered_models),
                                },
                            )

                            logger.info(
                                "[%s] Batch %d/%d completed (chunks %d-%d)",
                                model_name,
                                executed_batches,
                                est_batches,
                                batch_index,
                                batch_end,
                            )

                            # Update progress bar
                            pbar.update(batch_end - batch_index)
                            
                            batch_index = batch_end

                        except RuntimeError as exc:
                            if "out of memory" in str(exc).lower() and controller:
                                mitigation = controller.register_oom(companion_active=False)
                                if mitigation:
                                    event_type = mitigation.pop("type", "adaptive_oom")
                                    embedder._record_mitigation(event_type, model=model_name, **mitigation)
                                    torch.cuda.empty_cache()
                                    gc.collect()
                                    continue
                            raise

                    # Aggregate model embeddings
                    if model_embeddings:
                        full_embeddings = np.vstack(model_embeddings)
                        per_model_embeddings[model_name] = full_embeddings
                        model_weights[model_name] = (
                            embedder.ensemble_config.model_weights.get(model_name, 1.0)
                            if embedder.ensemble_config.model_weights
                            else 1.0
                        )

                        logger.info(
                            "[%s] Pass completed: %d embeddings, %.2fs",
                            model_name,
                            len(full_embeddings),
                            time.time() - model_start,
                        )

                        # Log lease summary
                        lease_summary = lease.summarize()
                        logger.info("[%s] GPU lease summary: %s", model_name, lease_summary)
                    else:
                        logger.warning("[%s] No embeddings generated", model_name)

                    # Close progress bar for this model pass
                    pbar.close()

                # Lease released automatically here

            # Aggregate across models
            if not per_model_embeddings:
                raise RuntimeError("No embeddings generated across all models")

            if len(per_model_embeddings) == 1:
                final_embeddings = list(per_model_embeddings.values())[0]
            else:
                weight_values = np.array(
                    [model_weights.get(name, 1.0) for name in per_model_embeddings.keys()],
                    dtype=np.float32,
                )
                weight_values = weight_values / weight_values.sum()
                stacked = np.stack(list(per_model_embeddings.values()), axis=0)
                final_embeddings = np.tensordot(weight_values, stacked, axes=1)

            # ================================================================
            # SPARSE VECTOR GENERATION STAGE
            # ================================================================
            # Execute sparse inference after dense aggregation but before
            # final normalization and fusion. This maintains the pipeline
            # sequence: dense -> sparse -> fusion/export.
            sparse_result: Optional[SparseInferenceResult] = None
            
            # Early return if sparse is not enabled
            if not embedder.enable_sparse or not embedder.sparse_models:
                logger.debug("Sparse inference disabled or no models available")
            else:
                logger.info("=" * 70)
                logger.info("SPARSE VECTOR GENERATION STAGE")
                logger.info("=" * 70)
                
                # Prepare ChunkRecord instances using helper method
                chunk_records = self._prepare_chunk_records(embedder)
                
                # Instantiate sparse generator
                sparse_generator = SparseVectorGenerator(embedder, logger)
                
                # Determine sparse model to use (first from sparse_models dict)
                sparse_model_name = (
                    next(iter(embedder.sparse_models.keys()), None)
                    if embedder.sparse_models
                    else None
                )
                
                if not sparse_model_name:
                    logger.warning("Sparse enabled but no sparse models configured")
                else:
                    # Execute sparse inference (CPU-first, optional GPU)
                    use_gpu = embedder.device == "cuda"
                    device_ids = (
                        list(range(embedder.device_count)) if use_gpu else None
                    )
                    
                    sparse_result = sparse_generator.generate(
                        chunks=chunk_records,
                        model_name=sparse_model_name,
                        use_gpu=use_gpu,
                        device_ids=device_ids,
                    )
                    
                    # Store results using helper method
                    self._store_sparse_results(embedder, sparse_result, logger)

            if not isinstance(final_embeddings, np.ndarray):
                final_embeddings = np.asarray(final_embeddings)
            if final_embeddings.dtype.kind not in {"f", "c"}:
                final_embeddings = final_embeddings.astype(np.float32, copy=False)

            final_embeddings = normalize(final_embeddings, norm="l2", axis=1)
            embedder.embeddings = final_embeddings
            embedder.embeddings_by_model[embedder.model_name] = final_embeddings

            self._run_rerank_stage(embedder, final_embeddings)

        except Exception as exc:
            logger.error("Exclusive ensemble generation failed: %s", exc)
            raise
        finally:
            if enable_monitoring:
                embedder._stop_performance_monitoring()

        total_time = time.time() - start_time
        chunks_per_second = total_chunks / total_time if total_time else 0.0

        embeddings = embedder._require_embeddings()
        embedding_memory_mb = embeddings.nbytes / 1024 / 1024
        memory_per_chunk_kb = (embedding_memory_mb * 1024) / total_chunks

        results: Dict[str, Any] = {
            "total_embeddings_generated": len(embeddings),
            "embedding_dimension": embeddings.shape[1],
            "processing_time_seconds": total_time,
            "chunks_per_second": chunks_per_second,
            "gpu_count": embedder.device_count,
            "model_used": embedder.model_name,
            "backend": embedder.gpu_config.backend,
            "precision": embedder.gpu_config.precision,
            "embedding_memory_mb": embedding_memory_mb,
            "memory_per_chunk_kb": memory_per_chunk_kb,
            "ensemble_mode": "exclusive",
            "models_executed": list(per_model_embeddings.keys()),
            "lease_events": embedder.telemetry.gpu_lease_events,
        }
        
        # Add sparse inference results if available
        if hasattr(embedder, 'sparse_inference_result') and embedder.sparse_inference_result:
            sparse_res = embedder.sparse_inference_result
            results["sparse_inference"] = {
                "model_name": sparse_res.model_name,
                "device": sparse_res.device,
                "latency_ms": sparse_res.latency_ms,
                "fallback_count": sparse_res.fallback_count,
                "success": sparse_res.success,
                "total_vectors": len(sparse_res.vectors),
            }

        logger.info("=" * 70)
        logger.info("EXCLUSIVE ENSEMBLE COMPLETE")
        logger.info("Generated %s embeddings", results["total_embeddings_generated"])
        logger.info("Dimension: %s", results["embedding_dimension"])
        logger.info("Total time: %.2fs", results["processing_time_seconds"])
        logger.info("Speed: %.1f chunks/second", results["chunks_per_second"])
        logger.info("Models executed: %s", results["models_executed"])
        logger.info("=" * 70)

        return results


__all__ = ["BatchRunner"]
