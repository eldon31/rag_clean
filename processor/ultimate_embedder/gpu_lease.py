"""GPU lease helper for exclusive ensemble mode.

Coordinates device acquisition, release, cache eviction, VRAM sampling,
and telemetry hooks to enable one-model-at-a-time GPU occupancy.
"""

from __future__ import annotations

import gc
import logging
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Optional

import torch

from processor.ultimate_embedder.controllers import GPUMemorySnapshot, collect_gpu_snapshots

if TYPE_CHECKING:  # pragma: no cover
    from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4


class GPULease:
    """Manage exclusive GPU access for a single model during ensemble passes."""

    def __init__(
        self,
        embedder: "UltimateKaggleEmbedderV4",
        model_name: str,
        logger: logging.Logger,
    ) -> None:
        self.embedder = embedder
        self.model_name = model_name
        self.logger = logger
        self.device_ids: List[int] = []
        self.leased_device_ids: List[int] = []  # Preserved for summary
        self.active = False
        self.vram_before: Dict[int, GPUMemorySnapshot] = {}
        self.vram_after: Dict[int, GPUMemorySnapshot] = {}

    def acquire(self, device_ids: Optional[List[int]] = None) -> None:
        """Lease GPU devices for exclusive use, evicting other models."""
        if self.active:
            self.logger.warning("Lease already active for %s", self.model_name)
            return

        # Default to all available CUDA devices
        if device_ids is None:
            device_ids = list(range(self.embedder.device_count))

        self.device_ids = device_ids
        self.leased_device_ids = list(device_ids)  # Preserve for summary

        if self.embedder.device != "cuda":
            # CPU execution path skips GPU telemetry while maintaining logs
            self.logger.debug(
                "CPU execution detected; skipping GPU lease for %s",
                self.model_name,
            )
            self.vram_before = {}
            self.active = True
            self.embedder.telemetry.record_gpu_lease_event(
                event_type="acquire",
                model=self.model_name,
                device_ids=[],
                vram_snapshots={},
            )
            return

        self.logger.debug(
            "Acquiring GPU lease for %s on devices %s",
            self.model_name,
            self.device_ids,
        )

        # Capture VRAM state before acquisition
        self.vram_before = collect_gpu_snapshots(
            self.embedder.device,
            self.embedder.device_count,
        )

        # Evict cache and trigger garbage collection
        torch.cuda.empty_cache()
        gc.collect()
        torch.cuda.empty_cache()

        self.active = True

        # Record lease acquisition telemetry
        self.embedder.telemetry.record_gpu_lease_event(
            event_type="acquire",
            model=self.model_name,
            device_ids=self.device_ids,
            vram_snapshots=self.vram_before,
        )

        self.logger.info("✓ GPU lease acquired for %s", self.model_name)

    def release(self) -> None:
        """Release GPU devices, capturing final VRAM state."""
        if not self.active:
            self.logger.debug("No active lease to release for %s", self.model_name)
            return

        self.logger.debug("Releasing GPU lease for %s", self.model_name)

        if self.embedder.device != "cuda":
            self.vram_after = {}
            self.active = False
            self.embedder.telemetry.record_gpu_lease_event(
                event_type="release",
                model=self.model_name,
                device_ids=[],
                vram_snapshots={},
            )
            self.device_ids = []
            return

        # Capture VRAM state after release
        self.vram_after = collect_gpu_snapshots(
            self.embedder.device,
            self.embedder.device_count,
        )

        # Aggressive cache eviction
        torch.cuda.empty_cache()
        gc.collect()
        torch.cuda.synchronize()
        torch.cuda.empty_cache()

        self.active = False

        # Record lease release telemetry
        self.embedder.telemetry.record_gpu_lease_event(
            event_type="release",
            model=self.model_name,
            device_ids=self.device_ids,
            vram_snapshots=self.vram_after,
        )

        self.logger.info("✓ GPU lease released for %s", self.model_name)
        self.device_ids = []

    def get_vram_delta_gb(self, device_id: int) -> Optional[float]:
        """Return VRAM delta in GB between acquisition and release."""
        before = self.vram_before.get(device_id)
        after = self.vram_after.get(device_id)

        if before is None or after is None:
            return None

        before_gb = before.allocated_bytes / 1e9
        after_gb = after.allocated_bytes / 1e9
        return after_gb - before_gb

    def summarize(self) -> Dict[str, Any]:
        """Return a summary of lease lifecycle and VRAM metrics."""
        vram_deltas = {}
        for device_id in self.leased_device_ids:  # Use preserved list
            delta = self.get_vram_delta_gb(device_id)
            if delta is not None:
                vram_deltas[f"gpu_{device_id}"] = round(delta, 2)

        return {
            "model": self.model_name,
            "device_ids": self.leased_device_ids,  # Show originally leased devices
            "vram_deltas_gb": vram_deltas,
            "active": self.active,
        }


@contextmanager
def lease_gpus(
    embedder: "UltimateKaggleEmbedderV4",
    model_name: str,
    logger: logging.Logger,
    device_ids: Optional[List[int]] = None,
) -> Generator[GPULease, None, None]:
    """Context manager for exclusive GPU leasing during ensemble passes.

    Usage:
        with lease_gpus(embedder, "bge-m3", logger) as lease:
            # GPUs are exclusively leased
            model = load_model_onto_device(...)
            embeddings = encode(...)
        # GPUs are released, cache evicted
    """
    lease = GPULease(embedder, model_name, logger)
    try:
        lease.acquire(device_ids=device_ids)
        yield lease
    finally:
        lease.release()
