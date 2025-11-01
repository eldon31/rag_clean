import logging
import sys
from pathlib import Path

import pytest

from processor.ultimate_embedder.runtime_config import FeatureToggleConfig
import scripts.embed_collections_v6 as cli


def _make_toggles():
    return FeatureToggleConfig(
        enable_rerank=True,
        enable_sparse=True,
        sparse_models=["splade"],
        sources={
            "enable_rerank": "default",
            "enable_sparse": "default",
            "sparse_models": "default",
        },
    )


def test_help_mentions_sparse_default(monkeypatch, capsys):
    toggles = _make_toggles()
    monkeypatch.setattr(cli, "load_feature_toggles", lambda: toggles)
    monkeypatch.setattr(cli, "KAGGLE_ENV", False)
    monkeypatch.setattr(sys, "argv", ["embed_collections_v6.py", "--help"])

    with pytest.raises(SystemExit):
        cli.parse_arguments()

    captured = capsys.readouterr()
    assert "default: splade" in captured.out


def test_parse_arguments_defaults(monkeypatch):
    toggles = _make_toggles()
    monkeypatch.setattr(cli, "load_feature_toggles", lambda: toggles)
    monkeypatch.setattr(cli, "KAGGLE_ENV", False)
    monkeypatch.setattr(sys, "argv", ["embed_collections_v6.py"])

    args = cli.parse_arguments()

    assert args.enable_rerank is True
    assert args.enable_sparse is True
    assert args.sparse_models == ["splade"]
    assert args.toggle_sources["enable_rerank"] == "default"
    assert args.toggle_sources["enable_sparse"] == "default"
    assert args.toggle_sources["sparse_models"] == "default"


def test_parse_arguments_disable_flags(monkeypatch):
    toggles = _make_toggles()
    monkeypatch.setattr(cli, "load_feature_toggles", lambda: toggles)
    monkeypatch.setattr(cli, "KAGGLE_ENV", False)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "embed_collections_v6.py",
            "--disable-rerank",
            "--disable-sparse",
            "--sparse-models",
            "custom-one",
            "custom-two",
        ],
    )

    args = cli.parse_arguments()

    assert args.enable_rerank is False
    assert args.enable_sparse is False
    assert args.sparse_models == []
    assert args.toggle_sources["enable_rerank"] == "cli"
    assert args.toggle_sources["enable_sparse"] == "cli"
    assert args.toggle_sources["sparse_models"] == "cli:disable-sparse-trim"


def test_parse_arguments_disable_sparse_records_provenance(monkeypatch):
    toggles = _make_toggles()
    monkeypatch.setattr(cli, "load_feature_toggles", lambda: toggles)
    monkeypatch.setattr(cli, "KAGGLE_ENV", False)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "embed_collections_v6.py",
            "--disable-sparse",
        ],
    )

    args = cli.parse_arguments()

    assert args.enable_sparse is False
    assert args.sparse_models == []
    assert args.toggle_sources["sparse_models"] == "cli:disable-sparse-trim"


def test_parse_arguments_cli_overrides_env(monkeypatch):
    env_toggles = FeatureToggleConfig(
        enable_rerank=False,
        enable_sparse=True,
        sparse_models=["env-model"],
        sources={
            "enable_rerank": "env",
            "enable_sparse": "env",
            "sparse_models": "env",
        },
        resolution_events=(
            {
                "key": "enable_rerank",
                "value": True,
                "source": "default",
                "layer": "default",
            },
            {
                "key": "enable_rerank",
                "value": False,
                "source": "env",
                "layer": "environment",
            },
            {
                "key": "enable_sparse",
                "value": True,
                "source": "env",
                "layer": "environment",
            },
            {
                "key": "sparse_models",
                "value": ["env-model"],
                "source": "env",
                "layer": "environment",
            },
        ),
    )

    monkeypatch.setattr(cli, "load_feature_toggles", lambda: env_toggles)
    monkeypatch.setattr(cli, "KAGGLE_ENV", False)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "embed_collections_v6.py",
            "--enable-rerank",
            "--sparse-models",
            "cli-model",
        ],
    )

    args = cli.parse_arguments()

    assert args.enable_rerank is True
    assert args.toggle_sources["enable_rerank"] == "cli"
    assert args.enable_sparse is True
    assert args.toggle_sources["enable_sparse"] == "env"
    assert args.sparse_models == ["cli-model"]
    assert args.toggle_sources["sparse_models"] == "cli"

    events = list(args.toggle_resolution_events)
    assert any(event.get("source") == "env" for event in events)
    assert events[-1]["source"] == "cli:--sparse-models"
    assert events[-2]["source"] == "cli:--enable-rerank"


def test_parse_arguments_enable_sparse_flag(monkeypatch):
    """Test --enable-sparse flag explicitly enables sparse embeddings"""
    toggles = FeatureToggleConfig(
        enable_rerank=True,
        enable_sparse=False,  # Disabled by default in this scenario
        sparse_models=["splade"],
        sources={
            "enable_rerank": "default",
            "enable_sparse": "default",
            "sparse_models": "default",
        },
    )

    monkeypatch.setattr(cli, "load_feature_toggles", lambda: toggles)
    monkeypatch.setattr(cli, "KAGGLE_ENV", False)
    monkeypatch.setattr(
        sys,
        "argv",
        ["embed_collections_v6.py", "--enable-sparse"],
    )

    args = cli.parse_arguments()

    assert args.enable_sparse is True
    assert args.toggle_sources["enable_sparse"] == "cli"


def test_parse_arguments_enable_rerank_and_sparse_flags(monkeypatch):
    """Test both --enable-rerank and --enable-sparse flags together"""
    toggles = FeatureToggleConfig(
        enable_rerank=False,
        enable_sparse=False,
        sparse_models=["splade"],
        sources={
            "enable_rerank": "default",
            "enable_sparse": "default",
            "sparse_models": "default",
        },
    )

    monkeypatch.setattr(cli, "load_feature_toggles", lambda: toggles)
    monkeypatch.setattr(cli, "KAGGLE_ENV", False)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "embed_collections_v6.py",
            "--enable-rerank",
            "--enable-sparse",
        ],
    )

    args = cli.parse_arguments()

    assert args.enable_rerank is True
    assert args.enable_sparse is True
    assert args.toggle_sources["enable_rerank"] == "cli"
    assert args.toggle_sources["enable_sparse"] == "cli"


def test_parse_arguments_enable_and_disable_conflict_precedence(monkeypatch):
    """Test that disable flags take precedence when both enable/disable specified (safety first)"""
    toggles = _make_toggles()
    monkeypatch.setattr(cli, "load_feature_toggles", lambda: toggles)
    monkeypatch.setattr(cli, "KAGGLE_ENV", False)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "embed_collections_v6.py",
            "--enable-rerank",
            "--disable-rerank",  # Disable takes precedence
        ],
    )

    args = cli.parse_arguments()

    # Disable should win for safety (explicit disablement overrides enable)
    assert args.enable_rerank is False
    assert args.toggle_sources["enable_rerank"] == "cli"


def test_log_collection_completion_includes_candidate_count(caplog):
    summary_payload = {
        "feature_toggles": {
            "enable_rerank": True,
            "enable_sparse": True,
            "sparse_models": [],
            "sources": {
                "enable_rerank": "default",
                "enable_sparse": "default",
            },
        },
        "rerank_run": {
            "enabled": True,
            "executed": True,
            "model_name": "cross-encoder",
            "status": "executed",
            "latency_ms": 42.5,
            "gpu_peak_gb": 1.5,
            "batch_size": 8,
            "candidate_count": 3,
            "fallback_count": 2,
            "fallback_reason": "execution_failed",
            "fallback_source": "runtime",
            "device_state": {
                "requested": "cuda",
                "resolved": "cuda",
                "fallback_applied": False,
            },
        },
    }

    caplog.set_level(logging.INFO, logger=cli.LOGGER.name)

    cli._log_collection_completion(
        collection_name="demo",
        models_executed=["model-a"],
        lease_events=[],
        elapsed_seconds=1.23,
        summary_path=None,
        summary_payload=summary_payload,
        metrics_report=None,
    )

    assert any("candidates=3" in message for message in caplog.messages)
    assert any(
        "fallback counter: count=2" in message and "reason=execution_failed" in message
        for message in caplog.messages
    )


def test_log_collection_completion_logs_warnings(caplog):
    summary_payload = {
        "feature_toggles": {
            "enable_rerank": True,
            "enable_sparse": True,
            "sparse_models": [],
            "sources": {
                "enable_rerank": "default",
                "enable_sparse": "default",
            },
            "provenance_lines": [],
        },
        "telemetry": {
            "spans": {},
        },
        "performance_baseline": {},
        "warnings": [
            "rerank stage enabled (source=default) but rerank_run payload is missing; verify rerank execution logs.",
        ],
    }

    caplog.set_level(logging.WARNING, logger=cli.LOGGER.name)

    cli._log_collection_completion(
        collection_name="demo",
        models_executed=["model-a"],
        lease_events=[],
        elapsed_seconds=2.5,
        summary_path="/tmp/summary.json",
        summary_payload=summary_payload,
        metrics_report=None,
    )

    assert any("Stage warnings detected" in message for message in caplog.messages)
    assert any("verify rerank execution logs" in message for message in caplog.messages)


def test_runbook_sparse_default_matches_feature_toggle():
    toggles = cli.load_feature_toggles(env={})
    if toggles.enable_sparse and toggles.sparse_models:
        default_label = ", ".join(toggles.sparse_models)
    elif toggles.enable_sparse:
        default_label = "none"
    else:
        default_label = "disabled (FeatureToggleConfig)"

    doc_path = Path(__file__).resolve().parents[1] / "docs" / "telemetry" / "rerank_sparse_signals.md"
    content = doc_path.read_text(encoding="utf-8")

    assert f"(default: {default_label})" in content


@pytest.mark.regression_harness
def test_regression_harness_cli_args_format(regression_harness_config):
    chunked_dir = regression_harness_config["chunked_dir"]
    collections = regression_harness_config["collections"]
    assert collections, "Collections list must not be empty"
    collection = collections[0]

    for scenario, config_entry in regression_harness_config["scenarios"].items():
        args = list(config_entry.get("args", []))
        assert "--chunked-dir" in args
        assert args[args.index("--chunked-dir") + 1] == chunked_dir
        assert "--collections" in args
        assert args[args.index("--collections") + 1] == collection
        if scenario == "fallback_force":
            assert "--disable-rerank" in args
            assert "--disable-sparse" in args


@pytest.mark.regression_harness
@pytest.mark.parametrize(
    "scenario",
    ["default_on", "rerank_disabled", "sparse_disabled", "fallback_force"],
)
def test_regression_cli_scenarios_align_with_summary(
    regression_harness_config,
    regression_summary_runner,
    scenario,
):
    summary, _ = regression_summary_runner(scenario)
    args = regression_harness_config["scenarios"][scenario]["args"]
    rerank_disabled = "--disable-rerank" in args
    sparse_disabled = "--disable-sparse" in args

    assert summary["feature_toggles"]["enable_rerank"] is (not rerank_disabled)
    assert summary["feature_toggles"]["enable_sparse"] is (not sparse_disabled)
