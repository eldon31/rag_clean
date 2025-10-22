"""Controllers for adaptive batching and GPU telemetry helpers."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

try:  # Optional dependency handling mirrors legacy module behaviour.
    import torch
except ImportError:  # pragma: no cover - torch not installed in minimal envs
    torch = None  # type: ignore[assignment]


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
        """Handle CUDA out-of-memory by shrinking batches or disabling companions."""

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


def collect_gpu_snapshots(device: str, device_count: int) -> Dict[int, GPUMemorySnapshot]:
    """Capture current GPU memory telemetry for adaptive batching."""

    if device != "cuda" or torch is None or not torch.cuda.is_available():
        return {}

    snapshots: Dict[int, GPUMemorySnapshot] = {}

    for device_id in range(device_count):
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

    return snapshots


__all__ = ["GPUMemorySnapshot", "AdaptiveBatchController", "collect_gpu_snapshots"]
