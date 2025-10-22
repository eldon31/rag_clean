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

from processor.ultimate_embedder.controllers import AdaptiveBatchController
from sklearn.preprocessing import normalize

if TYPE_CHECKING:  # pragma: no cover
    from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4


class BatchRunner:
    """Coordinate adaptive batch embedding generation for the facade."""

    def __init__(self, embedder: "UltimateKaggleEmbedderV4", logger: logging.Logger) -> None:
        self.embedder = embedder
        self.logger = logger

    def generate_ensemble_embeddings(
        self,
        texts: List[str],
        batch_slice: Optional[slice] = None,
        batch_index: Optional[int] = None,
    ) -> np.ndarray:
        """Generate embeddings using the configured ensemble pipeline."""

        embedder = self.embedder
        logger = self.logger

        if not embedder.enable_ensemble or not embedder.ensemble_config:
            logger.debug("Ensemble not enabled, using primary model only")
            primary_model = embedder._get_primary_model()
            primary_batch = embedder._get_batch_hint_for_model(embedder.model_name)

            embedder._log_gpu_memory("Primary encode (non-ensemble) - before")
            result = embedder._call_encode(
                primary_model,
                texts,
                batch_size=primary_batch,
                device=embedder.device,
            )
            result = embedder._normalize_embedding_matrix(result, embedder.model_name)
            embedder._log_gpu_memory("Primary encode (non-ensemble) - after")

            if embedder.device == "cuda":
                torch.cuda.empty_cache()

            return result

        sequential_mode = bool(embedder.ensemble_config.sequential_passes)
        slice_info = embedder._describe_batch_slice(batch_slice)
        slice_summary = embedder._format_batch_slice_info(slice_info)
        base_slice_mitigation: Dict[str, Any] = {}
        if slice_info:
            base_slice_mitigation = {
                "chunk_start": slice_info["start"],
                "chunk_end": slice_info["end"],
                "chunk_count": slice_info["count"],
                "chunk_samples": slice_info["samples"],
            }

        model_weights: Dict[str, float] = {}
        all_embeddings: List[np.ndarray] = []
        successful_models: List[str] = []

        ordered_models: List[str] = []
        seen: Set[str] = set()
        for candidate in [embedder.model_name, *embedder.ensemble_config.ensemble_models]:
            if candidate not in seen:
                ordered_models.append(candidate)
                seen.add(candidate)

        target_dim = embedder.matryoshka_dim or embedder.model_config.vector_dim

        if not sequential_mode:
            for model_name in ordered_models:
                model = embedder._get_or_load_ensemble_model(model_name)
                if model is None:
                    continue
                batch_hint = embedder._get_batch_hint_for_model(model_name)

                try:
                    logger.debug("[ENSEMBLE] Parallel encode with %s", model_name)
                    embedder._log_gpu_memory(
                        f"Ensemble encode before {model_name} | chunks={slice_summary}"
                    )
                    embeddings = embedder._call_encode(
                        model,
                        texts,
                        batch_size=batch_hint,
                        device=embedder.device,
                    )
                    embeddings = embedder._normalize_embedding_matrix(embeddings, model_name)
                    embedder._log_gpu_memory(
                        f"Ensemble encode after {model_name} | chunks={slice_summary}"
                    )
                except Exception as exc:
                    logger.warning("Failed to generate embeddings with %s: %s", model_name, exc)
                    continue

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
                model_weights[model_name] = (
                    embedder.ensemble_config.model_weights.get(model_name, 1.0)
                    if embedder.ensemble_config.model_weights
                    else 1.0
                )

        else:
            chunk_start = slice_info.get("start") if slice_info else None
            chunk_end = slice_info.get("end") if slice_info else None
            chunk_count = slice_info.get("count") if slice_info else len(texts)
            chunk_samples = slice_info.get("samples") if slice_info else []

            for model_name in ordered_models:
                model = embedder._get_or_load_ensemble_model(model_name)

                base_rotation_event: Dict[str, Any] = {
                    "batch_index": batch_index,
                    "model": model_name,
                    "aggregation_weight": (
                        embedder.ensemble_config.model_weights.get(model_name, 1.0)
                        if embedder.ensemble_config and embedder.ensemble_config.model_weights
                        else 1.0
                    ),
                    "chunk_start": chunk_start,
                    "chunk_end": chunk_end,
                    "chunk_count": chunk_count,
                    "chunk_samples": [dict(sample) for sample in chunk_samples] if chunk_samples else [],
                }

                if model is None:
                    embedder._record_rotation_event({**base_rotation_event, "status": "missing_model"})
                    raise RuntimeError(
                        f"Sequential ensemble model '{model_name}' is unavailable; rotation cannot continue"
                    )

                batch_hint = embedder._get_batch_hint_for_model(model_name)
                target_device = embedder._select_sequential_device(model_name)
                current_device = target_device
                current_batch_hint = batch_hint
                pass_start = time.time()
                embeddings: Optional[np.ndarray] = None
                mitigation_payload = dict(base_slice_mitigation)

                try:
                    if hasattr(model, "to"):
                        model = model.to(target_device)
                        embedder.models[model_name] = model
                except Exception as exc:
                    logger.warning("Failed to move model %s to %s: %s", model_name, target_device, exc)
                    embedder._record_mitigation(
                        "ensemble_move_failed",
                        model=model_name,
                        device=target_device,
                        error=str(exc)[:300],
                        **mitigation_payload,
                    )
                    base_model = embedder._unwrap_model(model)
                    if hasattr(base_model, "to"):
                        try:
                            base_model = cast(Any, base_model.to("cpu"))
                        except Exception as move_exc:
                            logger.warning("CPU fallback conversion failed for %s: %s", model_name, move_exc)
                        else:
                            model = base_model
                    current_device = "cpu"
                    embedder.models[model_name] = model

                logger.info(
                    "[ENSEMBLE] %s pass starting | device=%s | batch_hint=%d | chunks=%s",
                    model_name,
                    current_device,
                    current_batch_hint,
                    slice_summary,
                )
                if slice_info.get("samples"):
                    sample_summary = ", ".join(
                        f"{sample['index']}:{sample['source']}" for sample in slice_info["samples"]
                    )
                    logger.debug("[ENSEMBLE] %s chunk samples: %s", model_name, sample_summary)

                embedder._record_mitigation(
                    "ensemble_pass_started",
                    model=model_name,
                    device=current_device,
                    batch_size=current_batch_hint,
                    **mitigation_payload,
                )

                success = False
                retries = 0
                max_retries = 3

                while retries <= max_retries:
                    try:
                        embedder._log_gpu_memory(
                            f"Sequential ensemble encode before {model_name} @ {current_device} | chunks={slice_summary}"
                        )
                        embeddings = embedder._call_encode(
                            model,
                            texts,
                            batch_size=current_batch_hint,
                            device=current_device,
                        )
                        embeddings = embedder._normalize_embedding_matrix(embeddings, model_name)
                        embedder._log_gpu_memory(
                            f"Sequential ensemble encode after {model_name} @ {current_device} | chunks={slice_summary}"
                        )
                        success = True
                        break
                    except RuntimeError as exc:
                        message = str(exc)
                        if "out of memory" in message.lower():
                            embedder._record_mitigation(
                                "ensemble_pass_oom",
                                model=model_name,
                                device=current_device,
                                batch_size=current_batch_hint,
                                retry=retries,
                                **mitigation_payload,
                            )
                            logger.warning(
                                "[ENSEMBLE] OOM during %s pass @ %s | batch=%d | chunks=%s | retry=%d",
                                model_name,
                                current_device,
                                current_batch_hint,
                                slice_summary,
                                retries,
                            )
                            if torch.cuda.is_available() and current_device.startswith("cuda"):
                                torch.cuda.empty_cache()
                                gc.collect()
                                if current_batch_hint > 1:
                                    current_batch_hint = max(1, current_batch_hint // 2)
                                    retries += 1
                                    embedder._record_mitigation(
                                        "ensemble_pass_batch_reduced",
                                        model=model_name,
                                        batch_size=current_batch_hint,
                                        **mitigation_payload,
                                    )
                                    logger.info(
                                        "[ENSEMBLE] %s batch reduced to %d for chunks=%s",
                                        model_name,
                                        current_batch_hint,
                                        slice_summary,
                                    )
                                    continue
                                base_model = embedder._unwrap_model(model)
                                if hasattr(base_model, "to"):
                                    try:
                                        base_model = cast(Any, base_model.to("cpu"))
                                    except Exception as move_exc:
                                        logger.warning(
                                            "Failed to move model %s to CPU fallback: %s",
                                            model_name,
                                            move_exc,
                                        )
                                    else:
                                        model = base_model
                                        embedder.models[model_name] = model
                                current_device = "cpu"
                                retries += 1
                                embedder._record_mitigation(
                                    "ensemble_pass_cpu_fallback",
                                    model=model_name,
                                    **mitigation_payload,
                                )
                                logger.info(
                                    "[ENSEMBLE] %s falling back to CPU for chunks=%s",
                                    model_name,
                                    slice_summary,
                                )
                                continue
                        embedder._record_mitigation(
                            "ensemble_pass_failed",
                            model=model_name,
                            device=current_device,
                            error=message[:500],
                            **mitigation_payload,
                        )
                        logger.warning("Sequential ensemble pass failed for %s: %s", model_name, message)
                        break
                    except Exception as exc:
                        message = str(exc)
                        embedder._record_mitigation(
                            "ensemble_pass_failed",
                            model=model_name,
                            device=current_device,
                            error=message[:500],
                            **mitigation_payload,
                        )
                        logger.warning("Sequential ensemble pass failed for %s: %s", model_name, message)
                        break

                if not success or embeddings is None:
                    embedder.failed_ensemble_models.add(model_name)
                    failure_event = {
                        **base_rotation_event,
                        "status": "failed",
                        "device": current_device,
                        "batch_size": current_batch_hint,
                        "retries": retries,
                    }
                    embedder._record_rotation_event(failure_event)
                    logger.error(
                        "[ENSEMBLE] %s pass aborted | device=%s | chunks=%s",
                        model_name,
                        current_device,
                        slice_summary,
                    )
                    raise RuntimeError(
                        f"Sequential ensemble model '{model_name}' failed to encode batch {batch_index}"
                    )

                pass_duration = time.time() - pass_start
                embedder._record_mitigation(
                    "ensemble_pass_completed",
                    model=model_name,
                    device=current_device,
                    duration=pass_duration,
                    batch_size=current_batch_hint,
                    **mitigation_payload,
                )
                embedder.ensemble_device_map[model_name] = current_device

                logger.info(
                    "[ENSEMBLE] %s pass completed | device=%s | duration=%.2fs | chunks=%s",
                    model_name,
                    current_device,
                    pass_duration,
                    slice_summary,
                )

                completed_event = {
                    **base_rotation_event,
                    "status": "completed",
                    "device": current_device,
                    "batch_size": current_batch_hint,
                    "duration_seconds": pass_duration,
                    "retries": retries,
                }
                embedder._record_rotation_event(completed_event)

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
                model_weights[model_name] = (
                    embedder.ensemble_config.model_weights.get(model_name, 1.0)
                    if embedder.ensemble_config.model_weights
                    else 1.0
                )

                if current_device.startswith("cuda"):
                    torch.cuda.synchronize()
                    torch.cuda.empty_cache()

                if current_device.startswith("cuda") and model_name != embedder.model_name:
                    try:
                        if hasattr(model, "to"):
                            model = cast(Any, model.to("cpu"))
                            embedder.models[model_name] = model
                    except Exception as exc:
                        logger.warning("Failed to move model %s to CPU post-pass: %s", model_name, exc)
                    gc.collect()

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
        embedder = self.embedder
        logger = self.logger

        total_chunks = len(embedder.chunk_texts)
        logger.info("Starting Kaggle T4 x2 optimized embedding generation")
        logger.info("Total chunks: %s", total_chunks)
        logger.info("Model: %s (%sD)", embedder.model_name, embedder.model_config.vector_dim)
        if embedder.device == "cuda":
            logger.info("GPUs: %sx T4", embedder.device_count)
        else:
            logger.info("Running in CPU fallback mode")

        embedder.embeddings_by_model = {}
        embedder.multivectors_by_model = {}
        embedder.multivector_dimensions = {}
        embedder.multivector_comparators = {}
        embedder.telemetry.reset_runtime_state()
        embedder.processing_stats.clear()

        if embedder.gpu_config.gradient_checkpointing and not embedder.gradient_checkpoint_evaluated:
            embedder._record_mitigation(
                "gradient_checkpointing_active",
                model=embedder.model_name,
                enabled=True,
            )
            embedder.gradient_checkpoint_evaluated = True

        if enable_monitoring:
            embedder._start_performance_monitoring()

        start_time = time.time()

        initial_primary_batch = embedder.gpu_config.get_optimal_batch_size(embedder.model_config)
        if embedder.device == "cpu":
            initial_primary_batch = max(1, min(initial_primary_batch, 8))
        base_total_batch_size = (
            initial_primary_batch * embedder.device_count
            if embedder.device_count > 1
            else initial_primary_batch
        )

        batch_unit = "per GPU" if embedder.device == "cuda" else "per device"
        logger.info(
            "Initial primary batch size: %s (%s), total %s",
            initial_primary_batch,
            batch_unit,
            base_total_batch_size,
        )

        controller: Optional[AdaptiveBatchController] = None
        if embedder.device == "cuda":
            controller = AdaptiveBatchController(
                primary_batch=initial_primary_batch,
                device_count=embedder.device_count,
                gpu0_soft_limit_bytes=embedder.gpu0_soft_limit_bytes,
                companion_enabled=bool(embedder.companion_models),
            )
            embedder.adaptive_controller = controller
            logger.info(
                "Adaptive batch controller enabled (GPU0 soft limit %.2f GB)",
                embedder.gpu0_soft_limit_bytes / (1024 ** 3),
            )
        else:
            embedder.adaptive_controller = None

        all_embeddings: List[np.ndarray] = []
        companion_batches: Dict[str, List[np.ndarray]] = {name: [] for name in embedder.companion_models}
        companion_adjustments: Dict[str, int] = {name: 0 for name in embedder.companion_models}
        active_companions: List[str] = list(embedder.companion_models.keys())
        companion_devices_used: Set[str] = set()

        dimension_adjustments = 0
        executed_batches = 0
        batch_index = 0

        try:
            while batch_index < total_chunks:
                batch_start = time.time()
                companion_outputs: Dict[str, np.ndarray] = {}
                batch_embeddings: Optional[np.ndarray] = None

                while True:
                    if controller:
                        primary_batch = controller.primary_batch
                        current_total_batch = max(1, controller.total_batch)
                    else:
                        primary_batch = initial_primary_batch
                        current_total_batch = max(1, base_total_batch_size)

                    batch_end = min(batch_index + current_total_batch, total_chunks)
                    batch_texts = embedder.chunk_texts[batch_index:batch_end]

                    if not batch_texts:
                        break

                    if controller and embedder.device == "cuda":
                        snapshots = embedder._collect_gpu_snapshots()
                        mitigation = controller.register_snapshot(snapshots)
                        if mitigation:
                            event_type = mitigation.pop("type", "adaptive_action")
                            embedder._record_mitigation(event_type, **mitigation)
                            if mitigation.get("companion_disabled"):
                                active_companions = []
                                embedder._deactivate_companions()
                            torch.cuda.empty_cache()
                            gc.collect()
                            continue

                    autocast_ctx = (
                        torch.autocast(
                            device_type="cuda",
                            enabled=embedder.gpu_config.enable_mixed_precision,
                        )
                        if embedder.device == "cuda"
                        else nullcontext()
                    )

                    try:
                        batch_slice = slice(batch_index, batch_end)
                        with autocast_ctx:
                            if embedder.enable_ensemble:
                                logger.debug("Batch %s: Using ensemble mode", executed_batches + 1)
                                batch_embeddings = embedder.generate_ensemble_embeddings(
                                    batch_texts,
                                    batch_slice=batch_slice,
                                    batch_index=executed_batches,
                                )
                            elif embedder.primary_model is not None:
                                logger.debug("Batch %s: Using primary model", executed_batches + 1)
                                primary_model = embedder._get_primary_model()
                                batch_embeddings = embedder._call_encode(
                                    primary_model,
                                    batch_texts,
                                    batch_size=primary_batch,
                                    device=embedder.device,
                                )
                                batch_embeddings = embedder._normalize_embedding_matrix(
                                    batch_embeddings,
                                    embedder.model_name,
                                )
                            else:
                                logger.debug("Batch %s: Using backend", executed_batches + 1)
                                batch_embeddings = embedder._encode_with_backend(batch_texts, primary_batch)
                                batch_embeddings = embedder._normalize_embedding_matrix(
                                    batch_embeddings,
                                    embedder.model_name,
                                )

                            temp_outputs: Dict[str, np.ndarray] = {}
                            companion_devices_used.clear()
                            for companion_name in active_companions:
                                companion_model = embedder.companion_models.get(companion_name)
                                if companion_model is None:
                                    continue
                                comp_batch_size = embedder.companion_batch_sizes.get(companion_name, primary_batch)
                                companion_device = embedder.companion_device_map.get(companion_name, embedder.device)
                                companion_matrix = embedder._call_encode(
                                    companion_model,
                                    batch_texts,
                                    batch_size=comp_batch_size,
                                    device=companion_device,
                                )
                                temp_outputs[companion_name] = embedder._normalize_embedding_matrix(
                                    companion_matrix,
                                    companion_name,
                                )
                                if isinstance(companion_device, str) and companion_device.startswith("cuda"):
                                    companion_devices_used.add(companion_device)

                            companion_outputs = temp_outputs

                        break
                    except RuntimeError as exc:
                        if (
                            embedder.device == "cuda"
                            and controller
                            and "out of memory" in str(exc).lower()
                        ):
                            mitigation = controller.register_oom(companion_active=bool(active_companions))
                            if mitigation:
                                event_type = mitigation.pop("type", "adaptive_oom")
                                embedder._record_mitigation(event_type, **mitigation)
                                if mitigation.get("companion_disabled"):
                                    active_companions = []
                                    embedder._deactivate_companions()
                                torch.cuda.empty_cache()
                                gc.collect()
                                continue
                        raise

                if not batch_texts:
                    break

                if batch_embeddings is None:
                    logger.debug("No embeddings produced for current batch; retrying next batch")
                    continue

                embedder._log_batch_sources(executed_batches + 1, batch_index, batch_end)
                executed_batches += 1
                progress = (batch_end / total_chunks) * 100
                remaining_chunks = max(0, total_chunks - batch_end)
                est_remaining_batches = math.ceil(remaining_chunks / max(1, current_total_batch))

                batch_embeddings, adjusted = embedder._ensure_embedding_dimension(batch_embeddings)
                if adjusted:
                    dimension_adjustments += 1

                if embedder.matryoshka_dim and batch_embeddings.shape[1] > embedder.matryoshka_dim:
                    batch_embeddings = batch_embeddings[:, : embedder.matryoshka_dim]
                    logger.debug(
                        "Applied Matryoshka truncation: %sD -> %sD",
                        batch_embeddings.shape[1],
                        embedder.matryoshka_dim,
                    )

                all_embeddings.append(batch_embeddings)

                for companion_name, companion_matrix in companion_outputs.items():
                    config = embedder.companion_model_configs.get(companion_name)
                    expected_dim = config.vector_dim if config else None
                    companion_matrix, adjusted_companion = embedder._ensure_embedding_dimension(
                        companion_matrix,
                        expected_dim=expected_dim,
                    )
                    if adjusted_companion:
                        companion_adjustments[companion_name] += 1

                    if embedder.matryoshka_dim and companion_matrix.shape[1] > embedder.matryoshka_dim:
                        companion_matrix = companion_matrix[:, : embedder.matryoshka_dim]
                        logger.debug(
                            "Applied Matryoshka truncation to %s: %sD -> %sD",
                            companion_name,
                            companion_matrix.shape[1],
                            embedder.matryoshka_dim,
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
                    embedder._save_intermediate_results(all_embeddings, executed_batches)

                if embedder.device == "cuda":
                    torch.cuda.synchronize()
                for companion_device in companion_devices_used:
                    with torch.cuda.device(companion_device):
                        torch.cuda.synchronize()
                        torch.cuda.empty_cache()

                batch_index = batch_end

            embedder.embeddings = np.vstack(all_embeddings)

            expected_dim = embedder.matryoshka_dim or embedder.model_config.vector_dim
            if embedder.embeddings.shape[1] != expected_dim:
                raise ValueError(
                    "Embedding dimension mismatch after aggregation: expected %sD (Matryoshka: %s, Model: %s) got %sD",
                    expected_dim,
                    embedder.matryoshka_dim,
                    embedder.model_config.vector_dim,
                    embedder.embeddings.shape[1],
                )

            if embedder.export_config.compress_embeddings:
                embedder.embeddings = embedder.embeddings.astype(np.float32)
                logger.info("Embeddings compressed to float32")

            embedder.embeddings_by_model = {embedder.model_name: embedder.embeddings}

            for companion_name, batch_list in companion_batches.items():
                if not batch_list:
                    continue
                companion_full = np.vstack(batch_list)
                if embedder.export_config.compress_embeddings:
                    companion_full = companion_full.astype(np.float32)
                embedder.embeddings_by_model[companion_name] = companion_full

        except Exception as exc:
            logger.error("Embedding generation failed: %s", exc)
            raise
        finally:
            if enable_monitoring:
                embedder._stop_performance_monitoring()

        total_time = time.time() - start_time
        chunks_per_second = total_chunks / total_time if total_time else 0.0

        embeddings = embedder._require_embeddings()
        embedding_memory_mb = embeddings.nbytes / 1024 / 1024
        memory_per_chunk_kb = (embedding_memory_mb * 1024) / total_chunks

        companion_memory_mb: Dict[str, float] = {}
        companion_dimensions: Dict[str, int] = {}
        for companion_name, companion_array in embedder.embeddings_by_model.items():
            if companion_name == embedder.model_name:
                continue
            companion_memory_mb[companion_name] = companion_array.nbytes / 1024 / 1024
            companion_dimensions[companion_name] = companion_array.shape[1]

        final_primary_batch = controller.primary_batch if controller else initial_primary_batch
        final_total_batch_size = controller.total_batch if controller else base_total_batch_size

        results: Dict[str, Any] = {
            "total_embeddings_generated": len(embeddings),
            "embedding_dimension": embeddings.shape[1],
            "processing_time_seconds": total_time,
            "chunks_per_second": chunks_per_second,
            "gpu_count": embedder.device_count,
            "optimal_batch_size": final_primary_batch,
            "effective_total_batch_size": final_total_batch_size,
            "total_batches": executed_batches,
            "model_used": embedder.model_name,
            "backend": embedder.gpu_config.backend,
            "precision": embedder.gpu_config.precision,
            "embedding_memory_mb": embedding_memory_mb,
            "memory_per_chunk_kb": memory_per_chunk_kb,
            "kaggle_optimized": True,
            "performance_stats": dict(embedder.processing_stats),
            "dimension_adjustments": dimension_adjustments,
            "mitigation_events": list(embedder.telemetry.mitigation_events),
            "ensemble_rotation": list(embedder.telemetry.rotation_events),
            "ensemble_rotation_limit": embedder.telemetry.rotation_payload_limit,
            "gpu_snapshot_summary": embedder.telemetry.summarize_gpu_history(),
            "cache_events": list(embedder.telemetry.cache_events),
        }

        if embedder.telemetry.rotation_overflow_count:
            results["ensemble_rotation_overflow"] = embedder.telemetry.rotation_overflow_count

        if embedder.multivectors_by_model:
            multivector_stats: Dict[str, Dict[str, Any]] = {}
            for name, channel_vectors in embedder.multivectors_by_model.items():
                total_vectors = sum(len(vectors) for vectors in channel_vectors)
                average_vectors = total_vectors / len(channel_vectors) if channel_vectors else 0.0
                dimension = embedder.multivector_dimensions.get(name)
                multivector_stats[name] = {
                    "dimension": dimension,
                    "comparator": embedder.multivector_comparators.get(name, "max_sim"),
                    "average_vectors_per_point": average_vectors,
                }
            results["multivector_channels"] = multivector_stats

        if companion_memory_mb:
            results["companion_models"] = {
                name: {
                    "embedding_dimension": companion_dimensions.get(name),
                    "memory_mb": companion_memory_mb.get(name),
                    "batch_size": embedder.companion_batch_sizes.get(name),
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
        logger.info("Generated %s embeddings", results["total_embeddings_generated"])
        logger.info("Dimension: %s", results["embedding_dimension"])
        logger.info("Total time: %.2fs", results["processing_time_seconds"])
        logger.info("Speed: %.1f chunks/second", results["chunks_per_second"])
        logger.info(
            "Memory: %.1fMB (%.2fKB per chunk)",
            results["embedding_memory_mb"],
            results["memory_per_chunk_kb"],
        )

        if companion_memory_mb:
            formatted = ", ".join(
                f"{name}={memory:.1f}MB/{companion_dimensions.get(name)}D"
                for name, memory in companion_memory_mb.items()
            )
            logger.info("Companion dense embeddings: %s", formatted)

        return results


__all__ = ["BatchRunner"]
