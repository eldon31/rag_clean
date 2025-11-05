"""Throughput monitoring and logging for embedding operations with comprehensive error tracking."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

import torch


@dataclass
class ErrorRecord:
    """Record of an error that occurred during processing."""
    
    timestamp: str
    stage: str
    error_type: str
    error_message: str
    context: Dict[str, Any]
    severity: str = "error"  # error, warning, critical


@dataclass
class StageMetrics:
    """Metrics for a specific processing stage (dense, sparse, rerank)."""
    
    stage_name: str
    chunk_count: int
    duration: float
    chunks_per_sec: float
    success: bool
    error_count: int = 0
    warning_count: int = 0
    errors: List[ErrorRecord] = field(default_factory=list)
    model_name: Optional[str] = None
    device: Optional[str] = None
    batch_size: Optional[int] = None
    gpu_metrics: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ThroughputMetrics:
    """Container for throughput measurement results with comprehensive error tracking."""
    
    chunk_count: int
    duration: float
    chunks_per_sec: float
    timestamp_start: str
    timestamp_end: str
    gpu_metrics: List[Dict[str, Any]]
    stages: List[StageMetrics] = field(default_factory=list)
    total_errors: int = 0
    total_warnings: int = 0
    all_errors: List[ErrorRecord] = field(default_factory=list)
    has_failures: bool = False


class ThroughputMonitor:
    """Monitors and logs throughput metrics for embedding generation with full error visibility."""
    
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
        self._batch_size: int = 0
        self._is_data_parallel: bool = False
        self._current_stage: Optional[str] = None
        self._stage_start_time: Optional[float] = None
        self._stage_metrics: List[StageMetrics] = []
        self._errors: List[ErrorRecord] = []
        self._warnings: List[ErrorRecord] = []

    def _format_event(self, event: str, *fields: tuple[str, Any]) -> str:
        parts = [f"[throughput] {event}"]
        for key, value in fields:
            if isinstance(value, bool):
                normalized = "true" if value else "false"
            else:
                normalized = str(value)
            parts.append(f"{key}={normalized}")
        return " | ".join(parts)
        
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
        self._batch_size = batch_size
        self._is_data_parallel = is_data_parallel
        self._errors = []
        self._warnings = []
        self._stage_metrics = []
        
        device_normalized = device or ""
        gpu_count = torch.cuda.device_count() if device_normalized.startswith("cuda") else 0
        
        self.logger.info("=" * 60)
        self.logger.info("THROUGHPUT START:")
        self.logger.info(f"  Model: {model_name}")
        self.logger.info(f"  Chunks: {chunk_count}")
        self.logger.info(f"  Timestamp: {self._timestamp_start}")
        self.logger.info(f"  GPUs: {gpu_count}")
        self.logger.info(f"  Batch size/GPU: {batch_size}")
        self.logger.info(f"  DataParallel: {is_data_parallel}")

        print(
            self._format_event(
                "start",
                ("model", model_name),
                ("device", device),
                ("chunks", chunk_count),
                ("batch", batch_size),
                ("data_parallel", is_data_parallel),
            ),
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
                    self._format_event(
                        f"gpu{gpu_id}",
                        ("allocated", f"{mem_allocated:.2f}GB"),
                        ("reserved", f"{mem_reserved:.2f}GB"),
                    ),
                    flush=True,
                )
        
        self.logger.info("=" * 60)
    
    def start_stage(self, stage_name: str, model_name: Optional[str] = None, device: Optional[str] = None) -> None:
        """Start monitoring a specific stage (dense, sparse, rerank).
        
        Args:
            stage_name: Name of the stage (e.g., 'dense', 'sparse', 'rerank')
            model_name: Name of the model used in this stage
            device: Device used for this stage
        """
        self._current_stage = stage_name
        self._stage_start_time = time.time()
        
        self.logger.info(f"[throughput] Starting stage: {stage_name}" + (f" (model={model_name})" if model_name else ""))
        print(
            self._format_event(
                "stage_start",
                ("stage", stage_name),
                ("model", model_name or "N/A"),
                ("device", device or "N/A"),
            ),
            flush=True,
        )
    
    def end_stage(
        self,
        success: bool = True,
        chunks_processed: Optional[int] = None,
        batch_size: Optional[int] = None,
    ) -> None:
        """End monitoring for the current stage.
        
        Args:
            success: Whether the stage completed successfully
            chunks_processed: Number of chunks processed in this stage (defaults to total)
            batch_size: Batch size used in this stage
        """
        if self._current_stage is None or self._stage_start_time is None:
            return
        
        elapsed = time.time() - self._stage_start_time
        chunks = chunks_processed if chunks_processed is not None else self._chunk_count
        chunks_per_sec = chunks / elapsed if elapsed > 0 else 0.0
        
        # Collect GPU metrics for this stage
        gpu_metrics = []
        device_normalized = self._device or ""
        if device_normalized.startswith("cuda"):
            gpu_count = torch.cuda.device_count()
            for gpu_id in range(gpu_count):
                mem_allocated = torch.cuda.memory_allocated(gpu_id) / (1024**3)
                mem_reserved = torch.cuda.memory_reserved(gpu_id) / (1024**3)
                gpu_metrics.append({
                    "gpu_id": gpu_id,
                    "allocated_gb": round(mem_allocated, 2),
                    "reserved_gb": round(mem_reserved, 2),
                })
        
        # Count errors/warnings for this stage
        stage_errors = [e for e in self._errors if e.stage == self._current_stage]
        stage_warnings = [w for w in self._warnings if w.stage == self._current_stage]
        
        stage_metric = StageMetrics(
            stage_name=self._current_stage,
            chunk_count=chunks,
            duration=elapsed,
            chunks_per_sec=chunks_per_sec,
            success=success and len(stage_errors) == 0,
            error_count=len(stage_errors),
            warning_count=len(stage_warnings),
            errors=stage_errors + stage_warnings,
            model_name=self._model_name,
            device=self._device,
            batch_size=batch_size or self._batch_size,
            gpu_metrics=gpu_metrics,
        )
        
        self._stage_metrics.append(stage_metric)
        
        status = "✓ success" if stage_metric.success else "✗ failed"
        if stage_warnings and success:
            status = "⚠ warnings"
        
        self.logger.info(
            f"[throughput] Stage completed: {self._current_stage} | "
            f"status={status} | "
            f"duration={elapsed:.2f}s | "
            f"rate={chunks_per_sec:.2f}/s | "
            f"errors={len(stage_errors)} | "
            f"warnings={len(stage_warnings)}"
        )
        
        print(
            self._format_event(
                "stage_end",
                ("stage", self._current_stage),
                ("status", status),
                ("duration", f"{elapsed:.2f}s"),
                ("rate", f"{chunks_per_sec:.2f}/s"),
                ("errors", len(stage_errors)),
                ("warnings", len(stage_warnings)),
            ),
            flush=True,
        )
        
        # Log stage-specific errors
        if stage_errors or stage_warnings:
            self.logger.warning(f"[throughput] Stage '{self._current_stage}' had {len(stage_errors)} errors and {len(stage_warnings)} warnings")
            for error in stage_errors[:5]:  # Show first 5
                self.logger.error(f"  [{error.error_type}] {error.error_message}")
        
        self._current_stage = None
        self._stage_start_time = None
        
    def record_error(
        self,
        error: Exception,
        stage: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        severity: str = "error",
    ) -> None:
        """Record an error that occurred during processing.
        
        Args:
            error: The exception that occurred
            stage: Stage where error occurred (defaults to current stage)
            context: Additional context about the error
            severity: 'error', 'warning', or 'critical'
        """
        error_record = ErrorRecord(
            timestamp=datetime.now().isoformat(),
            stage=stage or self._current_stage or "unknown",
            error_type=type(error).__name__,
            error_message=str(error),
            context=context or {},
            severity=severity,
        )
        
        if severity == "warning":
            self._warnings.append(error_record)
        else:
            self._errors.append(error_record)
        
        log_func = self.logger.error if severity != "warning" else self.logger.warning
        log_func(
            f"[throughput] {severity.upper()} in {error_record.stage}: "
            f"{error_record.error_type}: {error_record.error_message}"
        )
        
        print(
            self._format_event(
                severity,
                ("stage", error_record.stage),
                ("type", error_record.error_type),
                ("message", error_record.error_message[:100]),
            ),
            flush=True,
        )
        
    def end(self) -> ThroughputMetrics:
        """End monitoring and return metrics.
        
        Returns:
            ThroughputMetrics object with measured data including all stages and errors
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
        
        total_errors = len(self._errors)
        total_warnings = len(self._warnings)
        has_failures = total_errors > 0
        
        self.logger.info("=" * 60)
        self.logger.info("THROUGHPUT END:")
        self.logger.info(f"  Chunks processed: {self._chunk_count}")
        self.logger.info(f"  Duration: {elapsed:.2f}s")
        self.logger.info(f"  Rate: {chunks_per_sec:.2f} chunks/sec")
        self.logger.info(f"  Stages completed: {len(self._stage_metrics)}")
        self.logger.info(f"  Total errors: {total_errors}")
        self.logger.info(f"  Total warnings: {total_warnings}")

        print(
            self._format_event(
                "done",
                ("model", self._model_name),
                ("chunks", self._chunk_count),
                ("duration", f"{elapsed:.2f}s"),
                ("rate", f"{chunks_per_sec:.2f}/s"),
                ("stages", len(self._stage_metrics)),
                ("errors", total_errors),
                ("warnings", total_warnings),
            ),
            flush=True,
        )
        
        # Log stage summary
        for stage in self._stage_metrics:
            status_symbol = "✓" if stage.success else "✗"
            self.logger.info(
                f"  {status_symbol} {stage.stage_name}: "
                f"{stage.chunks_per_sec:.2f} chunks/s, "
                f"{stage.error_count} errors, "
                f"{stage.warning_count} warnings"
            )
        
        for metric in gpu_metrics:
            self.logger.info(
                f"  GPU {metric['gpu_id']} peak: "
                f"{metric['allocated_gb']:.2f}GB allocated, "
                f"{metric['reserved_gb']:.2f}GB reserved"
            )
            print(
                self._format_event(
                    f"gpu{metric['gpu_id']}_peak",
                    ("allocated", f"{metric['allocated_gb']:.2f}GB"),
                    ("reserved", f"{metric['reserved_gb']:.2f}GB"),
                ),
                flush=True,
            )
        
        # Print error summary if any errors occurred
        if total_errors > 0 or total_warnings > 0:
            self.logger.warning("=" * 60)
            self.logger.warning("ERROR SUMMARY:")
            for error in self._errors[:10]:  # Show first 10 errors
                self.logger.error(
                    f"  [{error.stage}] {error.error_type}: {error.error_message}"
                )
            if len(self._errors) > 10:
                self.logger.error(f"  ... and {len(self._errors) - 10} more errors")
            
            if total_warnings > 0:
                self.logger.warning(f"  {total_warnings} warnings occurred (see logs for details)")
            
            print(
                self._format_event(
                    "error_summary",
                    ("total_errors", total_errors),
                    ("total_warnings", total_warnings),
                    ("has_failures", has_failures),
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
            stages=self._stage_metrics,
            total_errors=total_errors,
            total_warnings=total_warnings,
            all_errors=self._errors + self._warnings,
            has_failures=has_failures,
        )
    
    def log_error(self, error: Optional[BaseException] = None) -> None:
        """Log throughput failure after an exception."""
        if self._start_time is None:
            return

        elapsed = time.time() - self._start_time
        message = f"THROUGHPUT FAILED after {elapsed:.2f}s"
        if error is not None:
            message = f"{message} ({type(error).__name__}: {error})"
            self.record_error(error, severity="critical")

        self.logger.error(message)
        print(
            self._format_event("error", ("message", message)),
            flush=True,
        )


__all__ = ["ThroughputMonitor", "ThroughputMetrics", "StageMetrics", "ErrorRecord"]
