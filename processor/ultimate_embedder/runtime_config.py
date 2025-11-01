"""Runtime configuration helpers for the Ultimate Embedder feature toggles."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"0", "false", "no", "off"}


@dataclass(frozen=True)
class FeatureToggleConfig:
    """Resolved feature toggles for rerank and sparse activation."""

    enable_rerank: bool = True
    enable_sparse: bool = True
    sparse_models: List[str] = field(default_factory=list)
    sources: Dict[str, str] = field(default_factory=dict)
    resolution_events: Tuple[Dict[str, Any], ...] = field(default_factory=tuple)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _parse_bool(raw: Optional[str]) -> Optional[bool]:
    if raw is None:
        return None
    value = raw.strip().lower()
    if value in _TRUE_VALUES:
        return True
    if value in _FALSE_VALUES:
        return False
    return None


def _parse_list(raw: Optional[str]) -> List[str]:
    if raw is None:
        return []
    items = [item.strip() for item in raw.split(",")]
    return [item for item in items if item]


def _load_env_file(path: Path) -> Dict[str, str]:
    data: Dict[str, str] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    except FileNotFoundError:
        return {}
    except OSError:
        return {}
    return data


def _load_json_file(path: Path) -> Dict[str, object]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if isinstance(payload, dict):
            return payload
    except FileNotFoundError:
        return {}
    except OSError:
        return {}
    except json.JSONDecodeError:
        return {}
    return {}


def _deduplicate(items: Iterable[str]) -> List[str]:
    seen: Dict[str, None] = {}
    for item in items:
        if item not in seen:
            seen[item] = None
    return list(seen.keys())


def load_feature_toggles(env: Optional[Mapping[str, str]] = None) -> FeatureToggleConfig:
    """Resolve feature toggles from defaults, config files, and environment."""

    effective_env: Mapping[str, str] = env or os.environ
    project_root = _project_root()

    enable_rerank = True
    enable_sparse = True
    sparse_models: List[str] = ["splade"]  # Changed from qdrant-bm25 to working SPLADE model
    sources: Dict[str, str] = {
        "enable_rerank": "default",
        "enable_sparse": "default",
        "sparse_models": "default",
    }
    resolution_events: List[Dict[str, Any]] = []

    def _record_event(key: str, value: Any, source: str, layer: str) -> None:
        resolution_events.append(
            {
                "key": key,
                "value": value,
                "source": source,
                "layer": layer,
            }
        )

    _record_event("enable_rerank", enable_rerank, "default", "default")
    _record_event("enable_sparse", enable_sparse, "default", "default")
    _record_event("sparse_models", list(sparse_models), "default", "default")

    config_dir = project_root / "config"
    config_candidates = [
        config_dir / "embedder.json",
        config_dir / "embedder.config.json",
    ]

    for config_path in config_candidates:
        payload = _load_json_file(config_path)
        if not payload:
            continue
        if "enable_rerank" in payload:
            bool_value = _parse_bool(str(payload.get("enable_rerank")))
            if bool_value is not None:
                enable_rerank = bool_value
                sources["enable_rerank"] = f"config:{config_path.name}"
                _record_event("enable_rerank", enable_rerank, sources["enable_rerank"], "config")

        if "enable_sparse" in payload:
            bool_value = _parse_bool(str(payload.get("enable_sparse")))
            if bool_value is not None:
                enable_sparse = bool_value
                sources["enable_sparse"] = f"config:{config_path.name}"
                _record_event("enable_sparse", enable_sparse, sources["enable_sparse"], "config")

        raw_models = payload.get("sparse_models")
        if isinstance(raw_models, list):
            models = [str(item).strip() for item in raw_models if str(item).strip()]
            if models:
                sparse_models = models
                sources["sparse_models"] = f"config:{config_path.name}"
                _record_event("sparse_models", list(sparse_models), sources["sparse_models"], "config")

    env_file_values = _load_env_file(project_root / ".env")
    env_layers = [env_file_values, effective_env]

    for layer in env_layers:
        raw_rerank = layer.get("EMBEDDER_ENABLE_RERANK")
        parsed = _parse_bool(raw_rerank)
        if parsed is not None:
            enable_rerank = parsed
            source_key = "env-file" if layer is env_file_values else "env"
            sources["enable_rerank"] = source_key
            _record_event("enable_rerank", enable_rerank, source_key, "environment")

        raw_sparse = layer.get("EMBEDDER_ENABLE_SPARSE")
        parsed = _parse_bool(raw_sparse)
        if parsed is not None:
            enable_sparse = parsed
            source_key = "env-file" if layer is env_file_values else "env"
            sources["enable_sparse"] = source_key
            _record_event("enable_sparse", enable_sparse, source_key, "environment")

        raw_models = layer.get("EMBEDDER_SPARSE_MODELS")
        if raw_models:
            models = _parse_list(raw_models)
            if models:
                sparse_models = models
                source_key = "env-file" if layer is env_file_values else "env"
                sources["sparse_models"] = source_key
                _record_event("sparse_models", list(sparse_models), source_key, "environment")

    if not enable_sparse:
        sparse_models = []
        _record_event("sparse_models", list(sparse_models), "normalization", "post-processing")

    sparse_models = _deduplicate(model for model in sparse_models if model)

    return FeatureToggleConfig(
        enable_rerank=enable_rerank,
        enable_sparse=enable_sparse,
        sparse_models=sparse_models,
        sources=sources,
        resolution_events=tuple(resolution_events),
    )


__all__ = ["FeatureToggleConfig", "load_feature_toggles"]
