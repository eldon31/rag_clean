"""Telemetry helpers for the Ultimate Embedder package."""

from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, List, Optional

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
		history_limit: int = 50,
		logger: Optional[logging.Logger] = None,
	) -> None:
		self._logger = logger or logging.getLogger(__name__)
		self.rotation_sample_limit = rotation_sample_limit
		self.rotation_payload_limit = rotation_payload_limit
		self.history_limit = max(1, history_limit)
		self.rotation_overflow_count = 0

		self.mitigation_events: List[Dict[str, Any]] = []
		self.rotation_events: List[Dict[str, Any]] = []
		self.cache_events: List[Dict[str, Any]] = []
		self.gpu_snapshot_history: List[Dict[str, Any]] = []
		self.latest_gpu_snapshots: Dict[int, GPUMemorySnapshot] = {}

	def record_mitigation(self, event_type: str, **details: Any) -> None:
		"""Track mitigation events for diagnostics."""

		record = {"type": event_type, "timestamp": time.time(), **details}
		self.mitigation_events.append(record)
		self._logger.info("Mitigation event captured: %s", record)

	def record_rotation_event(self, event: Dict[str, Any]) -> None:
		"""Capture per-batch ensemble rotation telemetry with bounded detail."""

		samples = event.get("chunk_samples")
		if isinstance(samples, list) and len(samples) > self.rotation_sample_limit:
			event["chunk_samples"] = samples[: self.rotation_sample_limit]

		event.setdefault("timestamp", time.time())
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

		event.setdefault("timestamp", time.time())
		self.cache_events.append(event)

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
			"timestamp": time.time(),
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

		self.gpu_snapshot_history.append(payload)
		if len(self.gpu_snapshot_history) > self.history_limit:
			self.gpu_snapshot_history = self.gpu_snapshot_history[-self.history_limit :]

		self.latest_gpu_snapshots = snapshots

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

		return {
			"latest": latest,
			"peak_device": peak_device,
			"peak_allocated_gb": round(peak_alloc_gb, 2),
			"events_recorded": len(self.gpu_snapshot_history),
		}

	def reset_runtime_state(self) -> None:
		"""Clear per-run telemetry buffers."""

		self.mitigation_events.clear()
		self.rotation_events.clear()
		self.rotation_overflow_count = 0


__all__ = ["TelemetryTracker", "resolve_rotation_payload_limit"]
