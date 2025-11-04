"""Shared regression harness fixtures for Story 4.3 tests."""

from __future__ import annotations

import importlib
import io
import json
import os
import shutil
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
from unittest import mock

import pytest
from _pytest.monkeypatch import MonkeyPatch

_REGRESSION_ROOT = (
    Path(__file__).resolve().parent.parent / "data" / "regression" / "docling-mini"
)


def _coerce_scalar(token: str) -> Any:
    lowered = token.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return None if lowered in {"null", "none"} else token


def _parse_minimal_yaml(text: str) -> Dict[str, Any]:
    lines = text.splitlines()
    root: Dict[str, Any] = {}
    stack: List[Tuple[int, Any]] = [(-1, root)]

    for idx, raw_line in enumerate(lines):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(raw_line) - len(stripped)
        while stack and indent <= stack[-1][0]:
            stack.pop()

        if not stack:
            raise ValueError("YAML parser stack underflow")

        parent = stack[-1][1]

        if stripped.startswith("- "):
            value = _coerce_scalar(stripped[2:].strip())
            if not isinstance(parent, list):
                raise ValueError("List item outside list context")
            parent.append(value)
            continue

        key, _, remainder = stripped.partition(":")
        key = key.strip()

        if remainder and (remainder := remainder.strip()):
            value = _coerce_scalar(remainder)
            if not isinstance(parent, dict):
                raise ValueError("Scalar assignment requires dict parent")
            parent[key] = value
            continue

        # Determine container type by peeking ahead.
        next_is_list = False
        for peek in lines[idx + 1 :]:
            look = peek.strip()
            if not look or look.startswith("#"):
                continue
            next_indent = len(peek) - len(look)
            if next_indent <= indent:
                break
            next_is_list = look.startswith("- ")
            break

        container: Any = [] if next_is_list else {}
        if not isinstance(parent, dict):
            raise ValueError("Nested container requires dict parent")
        parent[key] = container
        stack.append((indent, container))

    return root


def _load_harness_config(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        return dict(yaml.safe_load(text))  # pragma: no cover - prefers native loader
    except Exception:
        return _parse_minimal_yaml(text)


@pytest.fixture(scope="session")
def regression_data_root() -> Path:
    return _REGRESSION_ROOT


@pytest.fixture(scope="session")
def regression_corpus_dir(regression_data_root: Path) -> Path:
    return regression_data_root / "chunked"


@pytest.fixture(scope="session")
def regression_goldens(regression_data_root: Path) -> Dict[str, Path]:
    golden_dir = regression_data_root / "goldens"
    return {
        "processing_summary_default_on": golden_dir / "processing_summary_default_on.json",
        "qdrant_default_on": golden_dir / "qdrant_default_on.jsonl",
    }


@pytest.fixture(scope="session")
def regression_harness_config(regression_data_root: Path) -> Dict[str, Any]:
    config_path = regression_data_root / "harness_config.yaml"
    return _load_harness_config(config_path)


def _base_summary(goldens: Dict[str, Path]) -> Dict[str, Any]:
    path = goldens["processing_summary_default_on"]
    return json.loads(path.read_text(encoding="utf-8"))


def _load_qdrant_lines(goldens: Dict[str, Path]) -> List[str]:
    path = goldens["qdrant_default_on"]
    return path.read_text(encoding="utf-8").splitlines()


def _ensure_toggle(summary: Dict[str, Any], key: str, value: bool, source: str) -> None:
    toggles = summary.setdefault("feature_toggles", {})
    toggles[key] = value
    provenance = toggles.setdefault("provenance", {})
    provenance[key] = source
    lines = toggles.setdefault("provenance_lines", [])
    record = f"{source}: {key}={value}"
    if record not in lines:
        lines.append(record)


def _record_sparse_models(summary: Dict[str, Any], models: Iterable[str], source: str) -> None:
    toggles = summary.setdefault("feature_toggles", {})
    toggles["sparse_models"] = list(models)
    provenance = toggles.setdefault("provenance", {})
    provenance["sparse_models"] = source
    lines = toggles.setdefault("provenance_lines", [])
    record = f"{source}: sparse_models={list(models)}"
    if record not in lines:
        lines.append(record)


def _mark_span(summary: Dict[str, Any], span: str, status: str, reason: str) -> None:
    telemetry = summary.setdefault("telemetry", {})
    spans = telemetry.setdefault("spans", {})
    spans[span] = {
        "span_id": f"{span}-regression",
        "status": status,
        "reason": reason,
    }

    metrics = telemetry.setdefault("metrics", {})
    metrics[span.split(".")[-1]] = {
        "status": "skipped" if status != "active" else "emitted",
        "reason": reason,
    }


def _scenario_slug(name: str) -> str:
    mapping = {
        "default_on": "default-on",
        "rerank_disabled": "rerank-disabled",
        "sparse_disabled": "sparse-disabled",
        "fallback_force": "fallback",
    }
    return mapping.get(name, name.replace("_", "-"))


_STUB_BASE_SUMMARY: Dict[str, Any] | None = None
_STUB_QDRANT_LINES: List[str] = []

_RESULT_KEY_MODELS_EXECUTED = "models_executed"
_RESULT_KEY_LEASE_EVENTS = "lease_events"
_RESULT_KEY_TOTAL_EMBEDDINGS = "total_embeddings_generated"
_DEFAULT_GPU_PEAK_GB = 3.2


def _determine_scenario(enable_rerank: bool, enable_sparse: bool) -> str:
    if enable_rerank and enable_sparse:
        return "default_on"
    if not enable_rerank and enable_sparse:
        return "rerank_disabled"
    if enable_rerank and not enable_sparse:
        return "sparse_disabled"
    return "fallback_force"


class RegressionHarnessStubEmbedder:
    """Lightweight embedder that feeds CLI runs with golden fixtures."""

    def __init__(
        self,
        *_: Any,
        feature_toggles: Any,
        export_config: Any,
        **__: Any,
    ) -> None:
        if _STUB_BASE_SUMMARY is None:
            raise RuntimeError("Regression stub context not initialised.")
        self.feature_toggles = feature_toggles
        self.export_config = export_config
        self._base_summary = _STUB_BASE_SUMMARY
        self._qdrant_lines = list(_STUB_QDRANT_LINES)
        resolved = _determine_scenario(
            feature_toggles.enable_rerank,
            feature_toggles.enable_sparse,
        )
        self._scenario = os.environ.get(
            "REGRESSION_HARNESS_SCENARIO",
            resolved,
        )
        self._chunk_count = 0
        self._embedding_count = 0
        self.embeddings = None
        self.embeddings_by_model: Dict[str, Any] = {}
        self.chunk_texts: List[str] = []
        self.chunks_metadata: List[Dict[str, Any]] = []
        self.sparse_vectors: Dict[str, Any] = {}
        self.fused_candidates: Dict[str, Any] = {}
        self.rerank_run = None
        self.rerank_candidate_scores: Dict[str, float] = {}
        self.rerank_failure_reason: str | None = None
        self.prometheus_emitter = None
        self.metrics_enabled = False
        self._active_collection_name = None
        self._active_collection_safe_dir = None

    def load_chunks_from_processing(
        self,
        chunks_dir: str,
        *,
        collection_name: str | None = None,
        single_collection_mode: bool | None = None,
    ) -> Dict[str, Any]:
        del single_collection_mode
        directory = Path(chunks_dir)
        total = 0
        for path in directory.rglob("*.json"):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if isinstance(payload, list):
                total += len(payload)
        self._chunk_count = total
        alias = collection_name or directory.name or "collection"
        alias_str = str(alias)
        sanitized = "".join(
            character if character.isalnum() or character in {"-", "_"} else "_"
            for character in alias_str
        ).strip("_") or "collection"
        self._active_collection_name = alias_str
        self._active_collection_safe_dir = sanitized
        return {"total_chunks_loaded": total}

    def generate_embeddings_kaggle_optimized(
        self,
        *,
        enable_monitoring: bool = True,
        save_intermediate: bool = True,
    ) -> Dict[str, Any]:
        del enable_monitoring, save_intermediate
        self._embedding_count = self._chunk_count or len(self._qdrant_lines)
        return {
            _RESULT_KEY_MODELS_EXECUTED: ["stub-dense"],
            _RESULT_KEY_LEASE_EVENTS: [],
            _RESULT_KEY_TOTAL_EMBEDDINGS: self._embedding_count,
        }

    def export_for_local_qdrant(self) -> List[str]:
        safe_dir = self._active_collection_safe_dir or "collection"
        collection_dir = Path(self.export_config.working_dir) / safe_dir
        collection_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{self.export_config.output_prefix}_qdrant.jsonl"
        qdrant_path = collection_dir / filename
        qdrant_path.write_text(
            "\n".join(self._qdrant_lines) + "\n",
            encoding="utf-8",
        )
        self._qdrant_path = qdrant_path
        return [str(qdrant_path)]

    def get_active_collection_alias(self) -> str | None:
        return self._active_collection_name

    def get_active_collection_output_dir(self) -> str | None:
        return self._active_collection_safe_dir

    def write_processing_summary(
        self,
        summary_path: str | Path,
        collection_name: str,
        chunk_count: int | None,
    ) -> Dict[str, Any]:
        summary = self._build_summary(chunk_count)
        summary["collection"] = collection_name
        if chunk_count is not None:
            summary["chunk_count"] = chunk_count
        summary.setdefault("dense_run", {})
        summary["dense_run"]["total_embeddings_generated"] = (
            self._embedding_count
            or chunk_count
            or len(self._qdrant_lines)
        )
        path = Path(summary_path)
        path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        self._summary_path = path
        return summary

    def _build_summary(self, chunk_count: int | None) -> Dict[str, Any]:
        summary = deepcopy(self._base_summary)
        if chunk_count:
            summary["chunk_count"] = chunk_count
        toggles = summary.setdefault("feature_toggles", {})
        toggles["enable_rerank"] = self.feature_toggles.enable_rerank
        toggles["enable_sparse"] = self.feature_toggles.enable_sparse
        toggles["sparse_models"] = list(self.feature_toggles.sparse_models)
        baseline_section = summary.setdefault("performance_baseline", {})
        gpu_section = baseline_section.setdefault("gpu", {})
        gpu_section.setdefault("peak_memory_used_gb", _DEFAULT_GPU_PEAK_GB)
        gpu_section.setdefault("peak_device", "cpu")
        scenario = self._scenario
        if scenario == "default_on":
            return summary
        if scenario == "rerank_disabled":
            _ensure_toggle(summary, "enable_rerank", False, "cli")
            summary.pop("rerank_run", None)
            _mark_span(
                summary,
                "rag.rerank",
                "skipped",
                "Disabled via CLI flag",
            )
            return summary
        if scenario == "sparse_disabled":
            _ensure_toggle(summary, "enable_sparse", False, "cli")
            summary.pop("sparse_run", None)
            _record_sparse_models(summary, [], "cli")
            _mark_span(
                summary,
                "rag.sparse",
                "skipped",
                "Disabled via CLI flag",
            )
            return summary
        _ensure_toggle(summary, "enable_rerank", False, "cli")
        _ensure_toggle(summary, "enable_sparse", False, "cli")
        _record_sparse_models(summary, [], "cli")
        summary.pop("rerank_run", None)
        summary.pop("sparse_run", None)
        warnings = summary.setdefault("warnings", [])
        fallback_notes = (
            "Both rerank and sparse stages disabled; dense fallback executed.",
            "Verify rollback plan captured CLI overrides.",
        )
        for note in fallback_notes:
            if note not in warnings:
                warnings.append(note)
        _mark_span(summary, "rag.rerank", "skipped", "Dense fallback active")
        _mark_span(summary, "rag.sparse", "skipped", "Dense fallback active")
        return summary


@pytest.fixture(scope="session")
def regression_summary_runner(
    regression_goldens: Dict[str, Path],
    regression_harness_config: Dict[str, Any],
):
    base_summary = _base_summary(regression_goldens)
    qdrant_lines = _load_qdrant_lines(regression_goldens)
    cli_module = importlib.import_module("scripts.embed_collections_v6")

    def _runner(
        scenario: str,
        *,
        output_dir: Path | None = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Path]]:
        scenarios = regression_harness_config.get("scenarios", {})
        if scenario not in scenarios:
            raise ValueError(f"Unknown regression scenario: {scenario}")

        args = list(scenarios[scenario].get("args", []))

        run_root = Path(tempfile.mkdtemp(prefix=f"regression_cli_{scenario}_"))
        cli_output_dir = run_root / "cli"
        cli_output_dir.mkdir(parents=True, exist_ok=True)

        args_with_output = list(args)
        if "--output-dir" in args_with_output:
            idx = args_with_output.index("--output-dir")
            if idx + 1 < len(args_with_output):
                args_with_output[idx + 1] = str(cli_output_dir)
        else:
            args_with_output.extend(["--output-dir", str(cli_output_dir)])

        global _STUB_BASE_SUMMARY, _STUB_QDRANT_LINES
        _STUB_BASE_SUMMARY = base_summary
        _STUB_QDRANT_LINES = list(qdrant_lines)

        monkeypatch = MonkeyPatch()
        monkeypatch.setitem(os.environ, "REGRESSION_HARNESS_SCENARIO", scenario)

        def _discover_override(path: Path) -> Dict[str, Path]:
            return {"docling-mini": Path(path)}

        monkeypatch.setattr(
            cli_module,
            "UltimateKaggleEmbedderV4",
            RegressionHarnessStubEmbedder,
        )
        monkeypatch.setattr(cli_module, "discover_collections", _discover_override)

        argv = ["embed_collections_v6.py", *args_with_output]
        capture = io.StringIO()
        exit_code = 1

        try:
            with mock.patch.object(sys, "argv", argv):
                with redirect_stdout(capture), redirect_stderr(capture):
                    exit_code = cli_module.main()
        finally:
            monkeypatch.undo()

        log_text = capture.getvalue()
        if exit_code != 0:
            raise RuntimeError(
                f"CLI execution failed for scenario '{scenario}' with exit code {exit_code}."
            )

        collection_dir = cli_output_dir / "docling-mini"
        summary_source = collection_dir / "docling-mini_processing_summary.json"
        qdrant_source = collection_dir / "docling-mini_qdrant.jsonl"

        if not summary_source.exists() or not qdrant_source.exists():
            raise FileNotFoundError(
                "Regression CLI stub did not emit expected summary or qdrant artifacts."
            )

        summary_data = json.loads(summary_source.read_text(encoding="utf-8"))

        target_dir = output_dir
        if target_dir is None:
            env_root = os.environ.get("REGRESSION_HARNESS_OUTPUT_DIR")
            if env_root:
                target_dir = Path(env_root) / scenario

        if target_dir is None:
            target_dir = run_root / "artifacts"

        target_dir.mkdir(parents=True, exist_ok=True)

        timestamp = os.environ.get("REGRESSION_HARNESS_TIMESTAMP") or datetime.now(UTC).strftime(
            "%Y%m%d%H%M%S"
        )
        slug = _scenario_slug(scenario)

        summary_target = target_dir / f"processing_summary_{slug}_{timestamp}.json"
        qdrant_target = target_dir / f"qdrant_{slug}_{timestamp}.jsonl"
        shutil.copy2(summary_source, summary_target)
        shutil.copy2(qdrant_source, qdrant_target)

        cli_log_path = target_dir / f"cli_{slug}_{timestamp}.txt"
        if log_text.strip():
            cli_log_path.write_text(log_text, encoding="utf-8")
        else:
            feature_state = summary_data.get("feature_toggles", {})
            log_lines = [
                f"scenario: {slug}",
                f"timestamp: {timestamp}",
                f"enable_rerank: {feature_state.get('enable_rerank')}",
                f"enable_sparse: {feature_state.get('enable_sparse')}",
                f"sparse_models: {feature_state.get('sparse_models')}",
            ]
            cli_log_path.write_text(
                "\n".join(str(line) for line in log_lines) + "\n",
                encoding="utf-8",
            )

        artifacts: Dict[str, Path] = {
            "summary_path": summary_target,
            "qdrant_path": qdrant_target,
            "cli_log_path": cli_log_path,
        }

        if scenario == "default_on":
            expected = _base_summary(regression_goldens)
            assert summary_data == expected, "CLI summary diverged from default-on golden"

        if not str(target_dir).startswith(str(run_root)):
            shutil.rmtree(run_root, ignore_errors=True)

        return summary_data, artifacts

    return _runner
