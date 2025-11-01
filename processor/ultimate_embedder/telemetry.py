"""Telemetry helpers for the Ultimate Embedder package."""

from __future__ import annotations

import logging
import os
import time
from typing import Callable
import uuid
from typing import Any, Dict, List, Mapping, Optional, Sequence

from .controllers import GPUMemorySnapshot


logger = logging.getLogger(__name__)


def resolve_rotation_payload_limit(
    default: int = 500,
    env_var: str = "EMBEDDER_ROTATION_LIMIT",
    *,
    log: Optional[logging.Logger] = None,
) -> int:
    """Resolve rotation payload limit from environment with validation."""

    active_logger = log or logger
    env_value = os.environ.get(env_var)
    if not env_value:
        return default

    try:
        candidate = int(env_value)
    except (TypeError, ValueError):
        active_logger.warning(
            "Invalid %s=%s, falling back to default %d",
            env_var,
            env_value,
            default,
        )
        return default

    if candidate <= 0:
        active_logger.warning(
            "Non-positive %s=%s, falling back to default %d",
            env_var,
            env_value,
            default,
        )
        return default

    return candidate


class TelemetryTracker:
    """Stateful recorder for mitigation, rotation, and GPU telemetry."""

    def __init__(
        self,
        *,
        rotation_sample_limit: int = 5,
        rotation_payload_limit: int = 500,
        batch_progress_limit: int = 1000,
        history_limit: int = 50,
        logger: Optional[logging.Logger] = None,
        time_provider: Optional[Callable[[], float]] = None,
    ) -> None:
        self._logger = logger or logging.getLogger(__name__)
        self.rotation_sample_limit = rotation_sample_limit
        self.rotation_payload_limit = rotation_payload_limit
        self.batch_progress_limit = max(1, batch_progress_limit)
        self.history_limit = max(1, history_limit)
        self.rotation_overflow_count = 0
        self._progress_label_limit = 96
        # Allow injection of a time provider for deterministic testing.
        self._time_provider = time_provider or time.time

        self.mitigation_events: List[Dict[str, Any]] = []
        self.rotation_events: List[Dict[str, Any]] = []
        self.cache_events: List[Dict[str, Any]] = []
        self.batch_progress_events: List[Dict[str, Any]] = []
        self.gpu_snapshot_history: List[Dict[str, Any]] = []
        self.latest_gpu_snapshots: Dict[int, GPUMemorySnapshot] = {}
        self.gpu_lease_events: List[Dict[str, Any]] = []
        self.span_events: Dict[str, Dict[str, Any]] = {}
        self.metrics_reports: Dict[str, Dict[str, Any]] = {}

    def record_mitigation(self, event_type: str, **details: Any) -> None:
        """Track mitigation events for diagnostics."""
        record = {"type": event_type, "timestamp": self._time_provider(), **details}
        self.mitigation_events.append(record)
        self._logger.info("Mitigation event captured: %s", record)

    def record_rotation_event(self, event: Dict[str, Any]) -> None:
        """Capture per-batch ensemble rotation telemetry with bounded detail."""
        samples = event.get("chunk_samples")
        if isinstance(samples, list) and len(samples) > self.rotation_sample_limit:
            event["chunk_samples"] = samples[: self.rotation_sample_limit]

        event.setdefault("timestamp", self._time_provider())
        if len(self.rotation_events) >= self.rotation_payload_limit:
            self.rotation_overflow_count += 1
            if event.get("status") != "completed":
                for idx in range(len(self.rotation_events) - 1, -1, -1):
                    if self.rotation_events[idx].get("status") == "completed":
                        self.rotation_events[idx] = event
                        break
                else:
                    self.rotation_events[-1] = event
            self._logger.debug(
                "Rotation telemetry overflow; limit=%d, discarded=%d",
                self.rotation_payload_limit,
                self.rotation_overflow_count,
            )
            return

        self.rotation_events.append(event)
        self._logger.debug("Rotation telemetry captured: %s", event)

    def record_cache_event(self, event: Dict[str, Any]) -> None:
        """Append cache hit/miss telemetry."""
        event.setdefault("timestamp", self._time_provider())
        self.cache_events.append(event)

    def record_batch_progress(
        self,
        *,
        batch_index: int,
        total_batches: int,
        label: Optional[str] = None,
        status: str = "completed",
        model: Optional[str] = None,
        device: Optional[str] = None,
        attempt: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Capture batch-level progress telemetry with bounded payload."""

        if len(self.batch_progress_events) >= self.batch_progress_limit:
            return

        payload: Dict[str, Any] = {
            "timestamp": self._time_provider(),
            "batch_index": max(0, batch_index),
            "total_batches": max(1, total_batches),
            "status": status,
        }

        if label:
            payload["label"] = label[: self._progress_label_limit]
        if model:
            payload["model"] = model
        if device:
            payload["device"] = device
        if attempt is not None:
            payload["attempt"] = attempt
        if metadata:
            payload["metadata"] = metadata

        self.batch_progress_events.append(payload)
        self._logger.debug("Batch progress captured: %s", payload)

    def record_span_presence(
        self,
        span_name: str,
        *,
        active: bool,
        reason: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        **extra_fields: Any,
    ) -> Dict[str, Any]:
        """Record the presence of an observability span for summary reporting."""

        existing = self.span_events.get(span_name, {})
        span_id = existing.get("span_id") or uuid.uuid4().hex
        record: Dict[str, Any] = {
            "span_id": span_id,
            "status": "active" if active else "skipped",
            "timestamp": self._time_provider(),
        }
        if reason:
            record["reason"] = reason

        merged_attributes: Dict[str, Any] = {}
        existing_attributes = existing.get("attributes")
        if isinstance(existing_attributes, Mapping):
            merged_attributes.update(existing_attributes)
        if attributes:
            merged_attributes.update(attributes)
        if extra_fields:
            merged_attributes.update(extra_fields)
        if merged_attributes:
            record["attributes"] = merged_attributes

        self.span_events[span_name] = record
        return record

    def record_metrics_status(
        self,
        stage: str,
        *,
        emitted: bool,
        reason: Optional[str] = None,
        metrics: Optional[Sequence[str]] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Capture metrics emission status for a pipeline stage."""

        record: Dict[str, Any] = {
            "status": "emitted" if emitted else "skipped",
            "timestamp": self._time_provider(),
        }
        if reason:
            record["reason"] = reason
        if metrics:
            record["metrics"] = list(metrics)
        if details:
            record["details"] = dict(details)
        self.metrics_reports[stage] = record
        return record

    def _record_gpu_soft_limit_status(
        self,
        *,
        exceeded: bool,
        soft_limit_gb: float,
        devices: Sequence[int],
        peak_allocated_gb: float,
    ) -> None:
        """Record whether the GPU soft limit has been breached."""

        status = "alert" if exceeded else "within_limit"
        record: Dict[str, Any] = {
            "status": status,
            "timestamp": self._time_provider(),
            "details": {
                "soft_limit_gb": round(soft_limit_gb, 2),
                "peak_allocated_gb": round(peak_allocated_gb, 2),
                "devices": [int(device) for device in devices],
            },
        }
        if exceeded:
            record["reason"] = "soft_limit_exceeded"
        self.metrics_reports["gpu_soft_limit"] = record
        log_level = logging.WARNING if exceeded else logging.INFO
        self._logger.log(
            log_level,
            "GPU soft limit status updated: status=%s limit=%.2fGB peak=%.2fGB devices=%s",
            status,
            record["details"]["soft_limit_gb"],
            record["details"]["peak_allocated_gb"],
            record["details"]["devices"],
        )

    def record_gpu_snapshot(
        self,
        snapshots: Dict[int, GPUMemorySnapshot],
        *,
        gpu0_soft_limit_bytes: int,
    ) -> None:
        """Persist GPU memory snapshots and enforce history limits."""

        if not snapshots:
            return

        limit_gb = gpu0_soft_limit_bytes / (1024 ** 3)
        payload = {
            "timestamp": self._time_provider(),
            "soft_limit_gb": round(limit_gb, 2),
            "devices": {
                device: snapshot.to_dict(gpu0_soft_limit_bytes if device == 0 else None)
                for device, snapshot in snapshots.items()
            },
        }
        payload["low_memory_devices"] = [
            device
            for device, snapshot in snapshots.items()
            if device == 0 and snapshot.allocated_bytes >= gpu0_soft_limit_bytes
        ]
        allocated_gb = [
            snapshot.allocated_bytes / (1024 ** 3)
            for snapshot in snapshots.values()
        ]
        peak_allocated_gb = max(allocated_gb) if allocated_gb else 0.0
        self._record_gpu_soft_limit_status(
            exceeded=bool(payload["low_memory_devices"]),
            soft_limit_gb=limit_gb,
            devices=payload["low_memory_devices"],
            peak_allocated_gb=peak_allocated_gb,
        )

        self.gpu_snapshot_history.append(payload)
        if len(self.gpu_snapshot_history) > self.history_limit:
            self.gpu_snapshot_history = self.gpu_snapshot_history[-self.history_limit :]

        self.latest_gpu_snapshots = snapshots

    def record_gpu_lease_event(
        self,
        *,
        event_type: str,
        model: str,
        device_ids: List[int],
        vram_snapshots: Dict[int, GPUMemorySnapshot],
    ) -> None:
        """Record GPU lease lifecycle events (acquire/release)."""

        payload: Dict[str, Any] = {
            "timestamp": self._time_provider(),
            "event_type": event_type,
            "model": model,
            "device_ids": device_ids,
            "vram": {
                device_id: snapshot.to_dict()
                for device_id, snapshot in vram_snapshots.items()
            },
        }

        self.gpu_lease_events.append(payload)
        self._logger.debug("GPU lease event captured: %s", payload)

    def summarize_gpu_history(self) -> Dict[str, Any]:
        """Return a condensed view of recent GPU telemetry."""

        if not self.gpu_snapshot_history:
            return {}

        latest = self.gpu_snapshot_history[-1]
        peak_alloc_gb = 0.0
        peak_device: Optional[int] = None
        for device_id, snapshot in latest["devices"].items():
            allocated = snapshot.get("allocated_gb", 0.0)
            if allocated > peak_alloc_gb:
                peak_alloc_gb = allocated
                peak_device = device_id

        soft_limit_gb = latest.get("soft_limit_gb")
        low_memory_devices = latest.get("low_memory_devices", [])
        soft_limit_exceeded = bool(low_memory_devices)

        return {
            "latest": latest,
            "peak_device": peak_device,
            "peak_allocated_gb": round(peak_alloc_gb, 2),
            "events_recorded": len(self.gpu_snapshot_history),
            "soft_limit_gb": soft_limit_gb,
            "soft_limit_exceeded": soft_limit_exceeded,
            "soft_limit_devices": low_memory_devices if soft_limit_exceeded else [],
        }

    def reset_runtime_state(self) -> None:
        """Clear per-run telemetry buffers."""
        self.mitigation_events.clear()
        self.rotation_events.clear()
        self.batch_progress_events.clear()
        self.gpu_lease_events.clear()
        self.span_events.clear()
        self.metrics_reports.clear()
        self.rotation_overflow_count = 0


__all__ = ["TelemetryTracker", "resolve_rotation_payload_limit"]
