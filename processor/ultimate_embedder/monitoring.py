"""Runtime performance monitoring helpers for the Ultimate Embedder."""

from __future__ import annotations

import logging
import threading
import time
from typing import TYPE_CHECKING, Optional

import torch

try:  # pragma: no cover - defensive import guard
    import psutil  # type: ignore
except Exception:  # pragma: no cover - psutil optional or partially available
    psutil = None  # type: ignore


PSUTIL_CPU_PERCENT_AVAILABLE = bool(psutil and hasattr(psutil, "cpu_percent"))
PSUTIL_VIRTUAL_MEMORY_AVAILABLE = bool(psutil and hasattr(psutil, "virtual_memory"))
PSUTIL_SUPPORTS_SYSTEM_METRICS = PSUTIL_CPU_PERCENT_AVAILABLE and PSUTIL_VIRTUAL_MEMORY_AVAILABLE

if TYPE_CHECKING:  # pragma: no cover
    from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4


class PerformanceMonitor:
    """Observe GPU and system metrics during embedding runs."""

    def __init__(self, embedder: "UltimateKaggleEmbedderV4", logger: logging.Logger) -> None:
        self.embedder = embedder
        self.logger = logger
        self._thread: Optional[threading.Thread] = None
        self._active = False
        self._psutil_warning_logged = False

    def start(self) -> None:
        """Begin the monitoring loop if it is not already running."""

        if self._active:
            return

        self._active = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        self.logger.info("Performance monitoring started")

    def stop(self) -> None:
        """Stop the monitoring loop and join the background thread."""

        if not self._active:
            return

        self._active = False
        if self._thread:
            self._thread.join(timeout=3)
            self._thread = None
        telemetry = getattr(self.embedder, "telemetry", None)
        if telemetry and getattr(telemetry, "batch_progress_events", None):
            self.embedder.processing_stats["batch_progress"] = list(telemetry.batch_progress_events)
        self.logger.info("Performance monitoring stopped")

    def _monitor_loop(self) -> None:
        """Collect GPU and system metrics until monitoring is disabled."""

        embedder = self.embedder

        while self._active:
            try:
                if torch.cuda.is_available() and embedder.device_count > 0:
                    for idx in range(embedder.device_count):
                        memory_used = torch.cuda.memory_allocated(idx) / 1e9
                        memory_reserved = torch.cuda.memory_reserved(idx) / 1e9
                        properties = torch.cuda.get_device_properties(idx)
                        memory_total = properties.total_memory / 1e9 if properties else 0.0
                        utilization = (memory_used / memory_total * 100) if memory_total else 0.0

                        embedder.processing_stats["gpu_memory"].append(
                            {
                                "gpu_id": idx,
                                "memory_used_gb": memory_used,
                                "memory_reserved_gb": memory_reserved,
                                "memory_total_gb": memory_total,
                                "utilization_percent": utilization,
                                "timestamp": time.time(),
                            }
                        )

                if PSUTIL_SUPPORTS_SYSTEM_METRICS:
                    cpu_percent = psutil.cpu_percent()  # type: ignore[union-attr]
                    memory_info = psutil.virtual_memory()  # type: ignore[union-attr]
                    embedder.processing_stats["system_metrics"].append(
                        {
                            "cpu_percent": cpu_percent,
                            "memory_used_gb": memory_info.used / 1e9,
                            "memory_percent": memory_info.percent,
                            "timestamp": time.time(),
                        }
                    )
                elif not self._psutil_warning_logged:
                    self.logger.warning(
                        "psutil missing cpu_percent/virtual_memory; skipping system metrics collection"
                    )
                    self._psutil_warning_logged = True

                time.sleep(2)
            except Exception as exc:  # pragma: no cover - defensive logging
                self.logger.error("Monitoring error: %s", exc)
                self._active = False
                break
