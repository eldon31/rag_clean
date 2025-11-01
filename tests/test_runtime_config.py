import json
from typing import Dict

from processor.ultimate_embedder import runtime_config


def test_load_feature_toggles_defaults(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(runtime_config, "_project_root", lambda: tmp_path)

    cfg = runtime_config.load_feature_toggles(env={})

    assert cfg.enable_rerank is True
    assert cfg.enable_sparse is True
    assert cfg.sparse_models == ["splade"]  # Changed from qdrant-bm25 to working SPLADE model
    assert cfg.sources["enable_rerank"] == "default"
    assert cfg.sources["sparse_models"] == "default"


def test_env_overrides_disable_features(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(runtime_config, "_project_root", lambda: tmp_path)

    env: Dict[str, str] = {
        "EMBEDDER_ENABLE_RERANK": "0",
        "EMBEDDER_ENABLE_SPARSE": "off",
        "EMBEDDER_SPARSE_MODELS": "alt-one,alt-two",
    }

    cfg = runtime_config.load_feature_toggles(env=env)

    assert cfg.enable_rerank is False
    assert cfg.enable_sparse is False
    assert cfg.sparse_models == []
    assert cfg.sources["enable_rerank"] == "env"
    assert cfg.sources["enable_sparse"] == "env"


def test_config_file_overrides(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(runtime_config, "_project_root", lambda: tmp_path)

    config_dir = tmp_path / "config"
    config_dir.mkdir()
    payload = {
        "enable_rerank": False,
        "enable_sparse": True,
        "sparse_models": ["alpha", "beta"],
    }
    (config_dir / "embedder.json").write_text(json.dumps(payload), encoding="utf-8")

    cfg = runtime_config.load_feature_toggles(env={})

    assert cfg.enable_rerank is False
    assert cfg.enable_sparse is True
    assert cfg.sparse_models == ["alpha", "beta"]
    assert cfg.sources["enable_rerank"] == "config:embedder.json"
    assert cfg.sources["sparse_models"] == "config:embedder.json"


def test_env_file_precedence(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(runtime_config, "_project_root", lambda: tmp_path)

    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "embedder.json").write_text(
        json.dumps({"enable_sparse": True}),
        encoding="utf-8",
    )
    (tmp_path / ".env").write_text("EMBEDDER_ENABLE_SPARSE=0\n", encoding="utf-8")

    cfg = runtime_config.load_feature_toggles(env={})

    assert cfg.enable_sparse is False
    assert cfg.sources["enable_sparse"] == "env-file"
    assert cfg.sparse_models == []
