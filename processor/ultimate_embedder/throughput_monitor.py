"""Throughput monitoring and logging for embedding operations."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

import torch


@dataclass
class ThroughputMetrics:
    """Container for throughput measurement results."""
    
    chunk_count: int
    duration: float
    chunks_per_sec: float
    timestamp_start: str
    timestamp_end: str
    gpu_metrics: list[dict[str, Any]]


class ThroughputMonitor:
    """Monitors and logs throughput metrics for embedding generation."""
    
    def __init__(self, logger: logging.Logger):
        """Initialize throughput monitor.
        
        Args:
            logger: Logger instance for output
        """
        self.logger = logger
        self._start_time: Optional[float] = None
        self._timestamp_start: Optional[str] = None
        self._chunk_count: int = 0
        self._model_name: str = ""
        self._device: str = ""
        
    def start(
        self,
        chunk_count: int,
        model_name: str,
        device: str,
        batch_size: int,
        is_data_parallel: bool,
    ) -> None:
        """Start monitoring throughput for a batch.
        
        Args:
            chunk_count: Number of chunks being processed
            model_name: Name of the model
            device: Device type ('cuda' or 'cpu')
            batch_size: Batch size per GPU
            is_data_parallel: Whether DataParallel is enabled
        """
        self._start_time = time.time()
        self._timestamp_start = datetime.now().isoformat()
        self._chunk_count = chunk_count
        self._model_name = model_name
        self._device = device
        
        gpu_count = torch.cuda.device_count() if device == "cuda" else 0
        
        self.logger.info("=" * 60)
        self.logger.info("THROUGHPUT START:")
        self.logger.info(f"  Model: {model_name}")
        self.logger.info(f"  Chunks: {chunk_count}")
        self.logger.info(f"  Timestamp: {self._timestamp_start}")
        self.logger.info(f"  GPUs: {gpu_count}")
        self.logger.info(f"  Batch size/GPU: {batch_size}")
        self.logger.info(f"  DataParallel: {is_data_parallel}")

        print(
            "[throughput] start | chunks=%s | model=%s | device=%s | batch=%s | data_parallel=%s"
            % (chunk_count, model_name, device, batch_size, is_data_parallel),
            flush=True,
        )
        
        if gpu_count > 0:
            for gpu_id in range(gpu_count):
                mem_allocated = torch.cuda.memory_allocated(gpu_id) / (1024**3)
                mem_reserved = torch.cuda.memory_reserved(gpu_id) / (1024**3)
                self.logger.info(
                    f"  GPU {gpu_id}: {mem_allocated:.2f}GB allocated, {mem_reserved:.2f}GB reserved"
                )
                print(
                    "[throughput] gpu%d | allocated=%.2fGB | reserved=%.2fGB"
                    % (gpu_id, mem_allocated, mem_reserved),
                    flush=True,
                )
        
        self.logger.info("=" * 60)
        
    def end(self) -> ThroughputMetrics:
        """End monitoring and return metrics.
        
        Returns:
            ThroughputMetrics object with measured data
        """
        if self._start_time is None:
            raise RuntimeError("ThroughputMonitor.start() must be called before end()")
            
        elapsed = time.time() - self._start_time
        timestamp_end = datetime.now().isoformat()
        chunks_per_sec = self._chunk_count / elapsed if elapsed > 0 else 0.0
        
        gpu_count = torch.cuda.device_count() if self._device == "cuda" else 0
        gpu_metrics = []
        
        if gpu_count > 0:
            for gpu_id in range(gpu_count):
                mem_allocated = torch.cuda.memory_allocated(gpu_id) / (1024**3)
                mem_reserved = torch.cuda.memory_reserved(gpu_id) / (1024**3)
                gpu_metrics.append({
                    "gpu_id": gpu_id,
                    "allocated_gb": round(mem_allocated, 2),
                    "reserved_gb": round(mem_reserved, 2),
                })
        
        self.logger.info("=" * 60)
        self.logger.info("THROUGHPUT END:")
        self.logger.info(f"  Chunks processed: {self._chunk_count}")
        self.logger.info(f"  Duration: {elapsed:.2f}s")
        self.logger.info(f"  Rate: {chunks_per_sec:.2f} chunks/sec")

        print(
            "[throughput] end | chunks=%s | duration=%.2fs | rate=%.2f chunks/sec"
            % (self._chunk_count, elapsed, chunks_per_sec),
            flush=True,
        )
        
        for metric in gpu_metrics:
            self.logger.info(
                f"  GPU {metric['gpu_id']} peak: "
                f"{metric['allocated_gb']:.2f}GB allocated, "
                f"{metric['reserved_gb']:.2f}GB reserved"
            )
            print(
                "[throughput] gpu%d_peak | allocated=%.2fGB | reserved=%.2fGB"
                % (
                    metric["gpu_id"],
                    metric["allocated_gb"],
                    metric["reserved_gb"],
                ),
                flush=True,
            )
        
        self.logger.info(f"  Timestamp: {timestamp_end}")
        self.logger.info("=" * 60)
        
        return ThroughputMetrics(
            chunk_count=self._chunk_count,
            duration=elapsed,
            chunks_per_sec=chunks_per_sec,
            timestamp_start=self._timestamp_start or "",
            timestamp_end=timestamp_end,
            gpu_metrics=gpu_metrics,
        )
    
    def log_error(self, error: Optional[BaseException] = None) -> None:
        """Log throughput failure after an exception."""
        if self._start_time is None:
            return

        elapsed = time.time() - self._start_time
        message = f"THROUGHPUT FAILED after {elapsed:.2f}s"
        if error is not None:
            message = f"{message} ({type(error).__name__}: {error})"

        self.logger.error(message)
        print(f"[throughput] error | {message}", flush=True)


__all__ = ["ThroughputMonitor", "ThroughputMetrics"]
