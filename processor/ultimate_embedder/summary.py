"""Helper utilities for building processing summary payloads."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional, Sequence, List

from .runtime_config import FeatureToggleConfig


SCHEMA_VERSION = "v4.1"


def _mean(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _round_metric(value: float) -> float:
    return round(value, 4)


def _copy_mapping(mapping: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    if not mapping:
        return {}
    return {key: mapping[key] for key in mapping}


def _format_provenance_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        joined = ", ".join(str(item) for item in value)
        return joined if joined else "[]"
    return str(value)


def _build_activation_provenance_lines(
    events: Sequence[Mapping[str, Any]],
) -> List[str]:
    grouped: Dict[str, List[Mapping[str, Any]]] = {}
    order: List[str] = []

    for event in events:
        key = str(event.get("key", ""))
        if not key:
            continue
        if key not in grouped:
            grouped[key] = []
            order.append(key)
        grouped[key].append(event)

    lines: List[str] = []
    for key in order:
        key_events = grouped.get(key, [])
        if not key_events:
            continue

        default_event = next(
            (item for item in key_events if item.get("layer") == "default"),
            key_events[0],
        )
        final_event = key_events[-1]

        default_value = default_event.get("value")
        final_value = final_event.get("value")
        default_display = _format_provenance_value(default_value)
        final_display = _format_provenance_value(final_value)
        final_source = str(final_event.get("source", "default"))

        if final_event is default_event or final_source == "default":
            descriptor = "default"
        else:
            descriptor = f"override via {final_source}"
            if final_value == default_value:
                descriptor = f"{descriptor}; matched default"
            else:
                descriptor = f"{descriptor}; default {default_display}"

        lines.append(f"{key}: {final_display} ({descriptor})")

    return lines


def _extract_rerank_payload(stage: Mapping[str, Any]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}

    for key in ("run_id", "query"):
        value = stage.get(key)
        if value:
            payload[key] = value

    for key in (
        "candidate_ids",
        "scores",
        "dense_scores",
        "candidate_metadata",
    ):
        value = stage.get(key)
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            payload[key] = list(value)

    for key in (
        "latency_ms",
        "gpu_peak_gb",
        "batch_size",
        "result_count",
        "initial_candidate_count",
    ):
        value = stage.get(key)
        if value is not None:
            payload[key] = value

    device_state = stage.get("device_state")
    if isinstance(device_state, Mapping):
        payload["device_state"] = _copy_mapping(device_state)

    for key in ("fallback_count", "fallback_reason", "fallback_source"):
        if key in stage:
            payload[key] = stage[key]

    if stage.get("status"):
        payload["status"] = stage["status"]

    return payload


def _extract_sparse_payload(stage: Mapping[str, Any]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}

    if stage.get("run_id"):
        payload["run_id"] = stage["run_id"]

    models = stage.get("models")
    if isinstance(models, Sequence) and not isinstance(models, (str, bytes, bytearray)):
        payload["models"] = list(models)

    vectors = stage.get("vectors")
    if isinstance(vectors, Mapping):
        payload["vectors"] = {
            "total": vectors.get("total"),
            "available": vectors.get("available"),
            "coverage_ratio": vectors.get("coverage_ratio"),
        }

    for key in (
        "fallback_used",
        "fallback_reason",
        "fallback_count",
        "latency_ms",
        "device",
        "success",
    ):
        if key in stage:
            payload[key] = stage[key]

    devices = stage.get("devices")
    if isinstance(devices, Mapping):
        payload["devices"] = _copy_mapping(devices)

    error_message = stage.get("error_message")
    if error_message:
        payload["error_message"] = error_message

    reason = stage.get("reason")
    if reason:
        payload["reason"] = reason

    return payload


def build_rerank_stage_summary(
    *,
    enabled: bool,
    model_name: Optional[str],
    loaded: bool,
    device: Optional[str],
    executed: bool,
    status: Optional[str] = None,
    reason: Optional[str] = None,
    metrics: Optional[Mapping[str, Any]] = None,
    requested_device: Optional[str] = None,
    fallback_applied: bool = False,
    fallback_reason: Optional[str] = None,
    fallback_count: int = 0,
    rerank_fallback_reason: Optional[str] = None,
    fallback_source: Optional[str] = None,
) -> Dict[str, Any]:
    summary: Dict[str, Any] = {
        "enabled": bool(enabled),
        "model_name": model_name or "",
        "loaded": bool(loaded),
        "device": device or "cpu",
        "executed": bool(executed),
    }

    if status:
        summary["status"] = status
    if reason:
        summary["reason"] = reason
    if metrics:
        summary["metrics"] = _copy_mapping(metrics)
    summary["device_state"] = {
        "requested": requested_device or "",
        "resolved": device or "",
        "fallback_applied": bool(fallback_applied),
    }
    if fallback_reason:
        summary["device_state"]["fallback_reason"] = fallback_reason

    summary["fallback_count"] = max(0, fallback_count)
    if rerank_fallback_reason is not None:
        summary["fallback_reason"] = rerank_fallback_reason
    if fallback_source:
        summary["fallback_source"] = fallback_source

    return summary


def build_sparse_stage_summary(
    *,
    enabled: bool,
    model_names: Sequence[str],
    vectors_total: int,
    vectors_available: int,
    executed: bool,
    coverage_ratio: float,
    devices: Optional[Mapping[str, str]] = None,
    fallback_used: bool = False,
    fallback_reason: Optional[str] = None,
    reason: Optional[str] = None,
    latency_ms: Optional[float] = None,
    run_id: Optional[str] = None,
    success: Optional[bool] = None,
    error_message: Optional[str] = None,
    fallback_count: Optional[int] = None,
    device: Optional[str] = None,
) -> Dict[str, Any]:
    summary: Dict[str, Any] = {
        "enabled": bool(enabled),
        "models": list(model_names),
        "executed": bool(executed),
        "vectors": {
            "total": int(max(0, vectors_total)),
            "available": int(max(0, vectors_available)),
            "coverage_ratio": round(max(0.0, coverage_ratio), 4),
        },
    }

    summary["devices"] = dict(devices) if devices else {}
    summary["fallback_used"] = bool(fallback_used)
    if fallback_reason:
        summary["fallback_reason"] = fallback_reason
    if reason:
        summary["reason"] = reason
    if latency_ms is not None:
        summary["latency_ms"] = round(float(latency_ms), 2)
    if run_id:
        summary["run_id"] = run_id
    if success is not None:
        summary["success"] = bool(success)
    if error_message:
        summary["error_message"] = error_message
    if fallback_count is not None:
        summary["fallback_count"] = max(0, int(fallback_count))
    if device:
        summary["device"] = device

    return summary


def build_telemetry_summary(
    *,
    mitigation_events: Sequence[Mapping[str, Any]],
    rotation_events: Sequence[Mapping[str, Any]],
    lease_events: Sequence[Mapping[str, Any]],
    batch_progress_events: Sequence[Mapping[str, Any]],
    span_events: Optional[Mapping[str, Mapping[str, Any]]] = None,
    metrics_report: Optional[Mapping[str, Mapping[str, Any]]] = None,
) -> Dict[str, Any]:
    summary: Dict[str, Any] = {
        "mitigation_events_recorded": len(mitigation_events),
        "rotation_events_recorded": len(rotation_events),
        "lease_events_recorded": len(lease_events),
        "batch_progress_events_recorded": len(batch_progress_events),
    }

    summary["spans"] = {
        name: {
            key: value
            for key, value in event.items()
            if key in {"span_id", "status", "reason", "attributes", "timestamp"}
        }
        for name, event in (span_events or {}).items()
    }
    summary["metrics"] = {
        stage: {
            key: value
            for key, value in report.items()
            if key in {"status", "reason", "metrics", "details", "timestamp"}
        }
        for stage, report in (metrics_report or {}).items()
    }

    return summary


def build_processing_summary(
    *,
    feature_toggles: FeatureToggleConfig,
    dense_run: Optional[Mapping[str, Any]],
    rerank_stage: Optional[Mapping[str, Any]],
    sparse_stage: Optional[Mapping[str, Any]],
    telemetry: Mapping[str, Any],
    collection_name: Optional[str] = None,
    chunk_count: Optional[int] = None,
) -> Dict[str, Any]:
    """Build processing summary manifest with optional stage payloads."""

    schema_version = SCHEMA_VERSION
    
    summary: Dict[str, Any] = {
        "schema_version": schema_version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "feature_toggles": {
            "enable_rerank": feature_toggles.enable_rerank,
            "enable_sparse": feature_toggles.enable_sparse,
            "sparse_models": list(feature_toggles.sparse_models),
            "sources": dict(feature_toggles.sources),
        },
        "telemetry": dict(telemetry),
    }

    summary["compatibility"] = {
    "current": SCHEMA_VERSION,
        "legacy": ["v4.0"],
    }

    if rerank_stage is not None:
        rerank_entry = {key: rerank_stage[key] for key in rerank_stage}
        payload = _extract_rerank_payload(rerank_entry)
        if payload:
            rerank_entry["payload"] = payload
        summary["rerank_run"] = rerank_entry
    if sparse_stage is not None:
        sparse_entry = {key: sparse_stage[key] for key in sparse_stage}
        payload = _extract_sparse_payload(sparse_entry)
        if payload:
            sparse_entry["payload"] = payload
        summary["sparse_run"] = sparse_entry

    provenance_events = list(feature_toggles.resolution_events)
    if not provenance_events:
        fallback_keys = set(feature_toggles.sources.keys()) or {
            "enable_rerank",
            "enable_sparse",
            "sparse_models",
        }
        for key in fallback_keys:
            source = feature_toggles.sources.get(key, "default")
            value = getattr(feature_toggles, key, None)
            provenance_events.append(
                {
                    "key": key,
                    "value": value,
                    "source": source,
                    "layer": "unspecified",
                }
            )

    sanitized_provenance = [
        {
            "key": event.get("key"),
            "value": event.get("value"),
            "source": event.get("source"),
            "layer": event.get("layer"),
        }
        for event in provenance_events
    ]
    activation_lines = _build_activation_provenance_lines(provenance_events)
    summary["feature_toggles"]["provenance"] = sanitized_provenance
    summary["feature_toggles"]["provenance_lines"] = list(activation_lines)
    summary["activation_provenance"] = list(sanitized_provenance)
    summary["activation_provenance_lines"] = list(activation_lines)

    if collection_name:
        summary["collection"] = collection_name
    if chunk_count is not None:
        summary["chunk_count"] = int(max(0, chunk_count))

    if dense_run is not None:
        summary["dense_run"] = {
            key: dense_run[key] for key in dense_run
        }

    warnings: List[str] = []

    if feature_toggles.enable_rerank and rerank_stage is None:
        rerank_source = feature_toggles.sources.get("enable_rerank", "default")
        warnings.append(
            "rerank stage enabled (source=%s) but rerank_run payload is missing; "
            "verify rerank execution logs." % rerank_source
        )

    if feature_toggles.enable_sparse and sparse_stage is None:
        sparse_source = feature_toggles.sources.get("enable_sparse", "default")
        warnings.append(
            "sparse stage enabled (source=%s) but sparse_run payload is missing; "
            "verify sparse generator execution." % sparse_source
        )

    if warnings:
        summary["warnings"] = warnings

    return summary


def build_performance_baseline(
    performance_stats: Mapping[str, Sequence[Mapping[str, Any]]],
) -> Dict[str, Any]:
    baseline: Dict[str, Any] = {}

    gpu_samples_raw = performance_stats.get("gpu_memory", [])
    gpu_samples = [
        sample
        for sample in gpu_samples_raw
        if isinstance(sample, Mapping)
    ]

    if gpu_samples:
        by_gpu: Dict[str, list[Mapping[str, Any]]] = {}
        for sample in gpu_samples:
            gpu_id = str(sample.get("gpu_id", "0"))
            by_gpu.setdefault(gpu_id, []).append(sample)

        overall_max_used = 0.0
        overall_max_reserved = 0.0
        overall_max_util = 0.0
        peak_device: Optional[str] = None
        per_gpu: Dict[str, Dict[str, Any]] = {}

        for gpu_id, entries in by_gpu.items():
            used = [float(entry.get("memory_used_gb", 0.0)) for entry in entries]
            reserved = [
                float(entry.get("memory_reserved_gb", 0.0))
                for entry in entries
            ]
            utilization = [
                float(entry.get("utilization_percent", 0.0))
                for entry in entries
            ]
            memory_total = next(
                (
                    float(entry.get("memory_total_gb", 0.0))
                    for entry in entries
                    if entry.get("memory_total_gb") is not None
                ),
                0.0,
            )

            gpu_summary = {
                "samples": len(entries),
                "peak_memory_used_gb": _round_metric(max(used) if used else 0.0),
                "peak_memory_reserved_gb": _round_metric(
                    max(reserved) if reserved else 0.0
                ),
                "average_utilization_percent": _round_metric(_mean(utilization)),
                "peak_utilization_percent": _round_metric(
                    max(utilization) if utilization else 0.0
                ),
                "memory_total_gb": _round_metric(memory_total),
            }

            per_gpu[gpu_id] = gpu_summary

            overall_max_used = max(overall_max_used, gpu_summary["peak_memory_used_gb"])
            overall_max_reserved = max(
                overall_max_reserved,
                gpu_summary["peak_memory_reserved_gb"],
            )
            overall_max_util = max(
                overall_max_util,
                gpu_summary["peak_utilization_percent"],
            )
            if (
                peak_device is None
                or gpu_summary["peak_memory_used_gb"] >= overall_max_used
            ):
                peak_device = gpu_id

        utilization_values = [
            float(sample.get("utilization_percent", 0.0))
            for sample in gpu_samples
        ]
        baseline["gpu"] = {
            "samples": len(gpu_samples),
            "peak_memory_used_gb": _round_metric(overall_max_used),
            "peak_memory_reserved_gb": _round_metric(overall_max_reserved),
            "peak_utilization_percent": _round_metric(overall_max_util),
            "average_utilization_percent": _round_metric(
                _mean(utilization_values)
            ),
            "per_gpu": per_gpu,
            "peak_device": peak_device,
        }

    system_samples_raw = performance_stats.get("system_metrics", [])
    system_samples = [
        sample
        for sample in system_samples_raw
        if isinstance(sample, Mapping)
    ]

    if system_samples:
        cpu_percent = [
            float(sample.get("cpu_percent", 0.0))
            for sample in system_samples
        ]
        memory_gb = [
            float(sample.get("memory_used_gb", 0.0))
            for sample in system_samples
        ]
        memory_percent = [
            float(sample.get("memory_percent", 0.0))
            for sample in system_samples
        ]

        baseline["system"] = {
            "samples": len(system_samples),
            "average_cpu_percent": _round_metric(_mean(cpu_percent)),
            "peak_cpu_percent": _round_metric(
                max(cpu_percent) if cpu_percent else 0.0
            ),
            "average_memory_gb": _round_metric(_mean(memory_gb)),
            "peak_memory_gb": _round_metric(max(memory_gb) if memory_gb else 0.0),
            "average_memory_percent": _round_metric(_mean(memory_percent)),
            "peak_memory_percent": _round_metric(
                max(memory_percent) if memory_percent else 0.0
            ),
        }

    hydration_events_raw = performance_stats.get("hydration_events", [])
    hydration_events = [
        sample
        for sample in hydration_events_raw
        if isinstance(sample, Mapping)
        and sample.get("duration_seconds") is not None
    ]

    if hydration_events:
        durations = [
            float(sample.get("duration_seconds", 0.0))
            for sample in hydration_events
        ]
        per_model: Dict[str, Dict[str, Any]] = {}
        success_count = 0
        failure_count = 0

        for sample in hydration_events:
            model_name = str(sample.get("model", "unknown"))
            duration = float(sample.get("duration_seconds", 0.0))
            status = str(sample.get("status", "hydrated"))
            success = bool(sample.get("success", status == "hydrated"))
            device_ids = sample.get("device_ids")

            model_entry = per_model.setdefault(
                model_name,
                {
                    "samples": 0,
                    "successes": 0,
                    "failures": 0,
                    "total_duration_seconds": 0.0,
                    "peak_duration_seconds": 0.0,
                    "last_device_ids": [],
                },
            )

            model_entry["samples"] += 1
            if success:
                model_entry["successes"] += 1
            else:
                model_entry["failures"] += 1
            model_entry["total_duration_seconds"] += duration
            model_entry["peak_duration_seconds"] = max(
                model_entry["peak_duration_seconds"],
                duration,
            )
            if isinstance(device_ids, (list, tuple)):
                model_entry["last_device_ids"] = [
                    str(device) for device in device_ids
                ]

            if success:
                success_count += 1
            else:
                failure_count += 1

        for entry in per_model.values():
            samples = entry["samples"] or 1
            entry["average_duration_seconds"] = _round_metric(
                entry["total_duration_seconds"] / samples
            )
            entry["total_duration_seconds"] = _round_metric(
                entry["total_duration_seconds"]
            )
            entry["peak_duration_seconds"] = _round_metric(
                entry["peak_duration_seconds"]
            )

        baseline["hydration"] = {
            "samples": len(hydration_events),
            "successes": success_count,
            "failures": failure_count,
            "average_duration_seconds": _round_metric(_mean(durations)),
            "peak_duration_seconds": _round_metric(max(durations)),
            "total_duration_seconds": _round_metric(sum(durations)),
            "per_model": per_model,
        }

    return baseline


def normalize_processing_summary(
    summary: Mapping[str, Any],
) -> Dict[str, Any]:
    """Return a safe copy of a processing summary for consumer parsing.

    Ensures schema_version is populated and critical sections exist even when
    reading legacy (v4.0) manifests.
    """

    normalized: Dict[str, Any] = {}
    for key, value in summary.items():
        if isinstance(value, Mapping):
            normalized[key] = _copy_mapping(value)
        elif isinstance(value, list):
            normalized[key] = list(value)
        else:
            normalized[key] = value

    schema_version = str(normalized.get("schema_version") or "v4.0")
    normalized["schema_version"] = schema_version

    if not isinstance(normalized.get("telemetry"), Mapping):
        normalized["telemetry"] = {}
    if not isinstance(normalized.get("feature_toggles"), Mapping):
        normalized["feature_toggles"] = {}
    if not isinstance(normalized.get("warnings"), list):
        normalized["warnings"] = []

    compatibility = normalized.get("compatibility")
    if not isinstance(compatibility, Mapping):
        legacy = ["v4.0"] if schema_version != "v4.0" else []
        normalized["compatibility"] = {
            "current": schema_version,
            "legacy": legacy,
        }

    return normalized


__all__ = [
    "SCHEMA_VERSION",
    "build_processing_summary",
    "build_rerank_stage_summary",
    "build_sparse_stage_summary",
    "build_telemetry_summary",
    "build_performance_baseline",
    "normalize_processing_summary",
]