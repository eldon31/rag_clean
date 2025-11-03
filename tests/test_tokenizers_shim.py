"""Tests for the tokenizers/transformers compatibility shim."""

from __future__ import annotations

import types

import importlib.metadata as stdlib_metadata
import pkg_resources

from processor.ultimate_embedder import compat


def test_tokenizers_version_guard_relaxes_version_checks(monkeypatch):
    """Ensure the shim overrides pkg_resources and importlib metadata lookups."""

    dummy_distribution = types.SimpleNamespace(project_name="tokenizers", key="tokenizers", version="0.21.2")

    def fake_get_distribution(dist):
        assert dist == "tokenizers"
        return dummy_distribution

    def fake_metadata_version(name):
        assert compat._normalize_package_name(name) == "tokenizers"  # type: ignore[attr-defined]
        return "0.21.2"

    monkeypatch.setattr(pkg_resources, "get_distribution", fake_get_distribution, raising=False)
    monkeypatch.setattr(compat.importlib_metadata, "version", fake_metadata_version, raising=False)
    monkeypatch.setattr(stdlib_metadata, "version", fake_metadata_version, raising=False)

    compat.TOKENIZERS_COMPAT_PATCHED_FROM = None

    with compat._tokenizers_version_guard("0.21.2"):  # type: ignore[attr-defined]
        patched_dist = pkg_resources.get_distribution("tokenizers")
        assert patched_dist.version == compat.TOKENIZERS_REPORTED_VERSION
        assert compat.importlib_metadata.version("tokenizers") == compat.TOKENIZERS_REPORTED_VERSION
        assert stdlib_metadata.version("tokenizers") == compat.TOKENIZERS_REPORTED_VERSION

    assert pkg_resources.get_distribution is fake_get_distribution
    assert compat.importlib_metadata.version("tokenizers") == "0.21.2"
    assert stdlib_metadata.version("tokenizers") == "0.21.2"
    assert compat.TOKENIZERS_COMPAT_PATCHED_FROM == "0.21.2"
    compat.TOKENIZERS_COMPAT_PATCHED_FROM = None
