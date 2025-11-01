"""Prometheus metrics emission for Ultimate Embedder pipeline stages."""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional, Sequence

logger = logging.getLogger(__name__)


class PrometheusMetricsEmitter:
    """
    Manages Prometheus metrics for rerank, sparse, and other pipeline stages.
    
    Metrics are recorded as structured payloads for export to Prometheus
    push gateway or pull endpoint. When metrics emission is disabled,
    status is logged with explicit reason codes.
    """

    def __init__(
        self,
        *,
        enabled: bool = False,
        namespace: str = "rag",
        logger_instance: Optional[logging.Logger] = None,
    ) -> None:
        self.enabled = enabled
        self.namespace = namespace
        self._logger = logger_instance or logger
        self._metric_buffer: list[Dict[str, Any]] = []

    def emit_latency_metric(
        self,
        *,
        stage: str,
        latency_seconds: float,
        labels: Optional[Dict[str, str]] = None,
    ) -> bool:
        """
        Record a latency histogram/summary metric for a pipeline stage.
        
        Args:
            stage: Stage name (dense, rerank, sparse, export)
            latency_seconds: Execution time in seconds
            labels: Optional Prometheus labels (device, model, etc.)
            
        Returns:
            True if metric was emitted, False otherwise
        """
        if not self.enabled:
            return False

        metric_name = f"{self.namespace}_{stage}_latency_seconds"
        payload = {
            "metric": metric_name,
            "type": "histogram",
            "value": latency_seconds,
            "labels": labels or {},
        }
        
        self._metric_buffer.append(payload)
        self._logger.debug(
            "Emitted %s = %.3fs with labels %s",
            metric_name,
            latency_seconds,
            labels or {}
        )
        return True

    def emit_gpu_peak_metric(
        self,
        *,
        stage: str,
        peak_bytes: int,
        labels: Optional[Dict[str, str]] = None,
    ) -> bool:
        """
        Record GPU peak memory usage gauge metric.
        
        Args:
            stage: Stage name (dense, rerank, sparse, export)
            peak_bytes: Peak GPU memory in bytes
            labels: Optional Prometheus labels (device, stage, etc.)
            
        Returns:
            True if metric was emitted, False otherwise
        """
        if not self.enabled:
            return False

        metric_name = f"{self.namespace}_gpu_peak_bytes"
        full_labels = {**(labels or {}), "stage": stage}
        payload = {
            "metric": metric_name,
            "type": "gauge",
            "value": peak_bytes,
            "labels": full_labels,
        }
        
        self._metric_buffer.append(payload)
        self._logger.debug(
            "Emitted %s{stage=%s} = %d bytes with labels %s",
            metric_name,
            stage,
            peak_bytes,
            full_labels
        )
        return True

    def emit_counter(
        self,
        *,
        metric_name: str,
        value: float = 1.0,
        labels: Optional[Dict[str, str]] = None,
    ) -> bool:
        """
        Record a counter metric (e.g., rerank_executions_total).
        
        Args:
            metric_name: Full metric name (without namespace prefix)
            value: Counter increment value
            labels: Optional Prometheus labels
            
        Returns:
            True if metric was emitted, False otherwise
        """
        if not self.enabled:
            return False

        full_name = f"{self.namespace}_{metric_name}"
        payload = {
            "metric": full_name,
            "type": "counter",
            "value": value,
            "labels": labels or {},
        }
        
        self._metric_buffer.append(payload)
        self._logger.debug(
            "Emitted counter %s = %.1f with labels %s",
            full_name,
            value,
            labels or {}
        )
        return True

    def get_buffered_metrics(self) -> Sequence[Dict[str, Any]]:
        """Return all buffered metrics and clear the buffer."""
        metrics = list(self._metric_buffer)
        self._metric_buffer.clear()
        return metrics

    def clear_buffer(self) -> None:
        """Clear all buffered metrics without returning them."""
        self._metric_buffer.clear()

    def check_gpu_alert_threshold(
        self, *, peak_bytes: int
    ) -> tuple[str, bool]:
        """
        Check GPU peak memory against alert thresholds.

        Args:
            peak_bytes: GPU peak memory in bytes

        Returns:
            Tuple of (alert_level, threshold_exceeded)
            - alert_level: "none", "warning", or "critical"
            - threshold_exceeded: True if any threshold exceeded
        """
        CRITICAL_THRESHOLD_GB = 12.0
        WARNING_THRESHOLD_GB = 11.5

        peak_gb = peak_bytes / (1024**3)

        if peak_gb >= CRITICAL_THRESHOLD_GB:
            return ("critical", True)
        elif peak_gb >= WARNING_THRESHOLD_GB:
            return ("warning", True)
        else:
            return ("none", False)

    def get_alert_thresholds_gb(self) -> dict[str, float]:
        """
        Return configured alert thresholds in GB.

        Returns:
            Dictionary with warning and critical thresholds
        """
        return {
            "soft_limit": 10.0,
            "warning": 11.5,
            "critical": 12.0,
        }


def create_prometheus_emitter(
    *,
    env_var: str = "EMBEDDER_METRICS_ENABLED",
    namespace_var: str = "EMBEDDER_METRICS_NAMESPACE",
    logger_instance: Optional[logging.Logger] = None,
) -> PrometheusMetricsEmitter:
    """
    Factory to create a PrometheusMetricsEmitter from environment configuration.
    
    Args:
        env_var: Environment variable name for enable/disable flag
        namespace_var: Environment variable for metrics namespace
        logger_instance: Optional logger for emission logging
        
    Returns:
        Configured PrometheusMetricsEmitter instance
    """
    metrics_flag = os.environ.get(env_var, "")
    enabled = metrics_flag.strip().lower() in {"1", "true", "yes", "on"}
    
    namespace = os.environ.get(namespace_var, "rag").strip() or "rag"
    
    return PrometheusMetricsEmitter(
        enabled=enabled,
        namespace=namespace,
        logger_instance=logger_instance,
    )


__all__ = ["PrometheusMetricsEmitter", "create_prometheus_emitter"]
