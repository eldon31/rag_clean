"""Compatibility utilities for external ML dependencies."""

from __future__ import annotations

import importlib
import importlib.metadata as importlib_metadata
from contextlib import contextmanager, nullcontext
from typing import Any, List, Optional, Tuple

TOKENIZERS_REPORTED_VERSION = "0.19.99"
_TOKENIZERS_INSTALLED_VERSION: Optional[str]
_TOKENIZERS_NEEDS_SHIM: bool
TOKENIZERS_COMPAT_PATCHED_FROM: Optional[str] = None


def _normalize_package_name(name: str) -> str:
    """Normalize package identifiers for consistent comparisons."""

    return name.replace("-", "_").lower()


def _transformers_caps_tokenizers_below_020() -> bool:
    """Return True if installed transformers limits tokenizers to <0.20."""

    try:
        requirements = importlib_metadata.requires("transformers")
    except importlib_metadata.PackageNotFoundError:
        return False
    except Exception:
        return False

    if not requirements:
        return False

    try:
        from packaging.requirements import Requirement
    except Exception:
        return False

    for raw in requirements:
        try:
            req = Requirement(raw)
        except Exception:
            continue
        if _normalize_package_name(req.name) != "tokenizers":
            continue
        for spec in req.specifier:
            if spec.operator in {"<", "<="} and spec.version and spec.version.startswith("0.20"):
                return True
    return False


def _should_apply_tokenizers_shim() -> Tuple[Optional[str], bool]:
    """Determine whether the tokenizers/transformers version gate needs a shim."""

    try:
        installed_version = importlib_metadata.version("tokenizers")
    except importlib_metadata.PackageNotFoundError:
        return None, False
    except Exception:
        return None, False

    if not _transformers_caps_tokenizers_below_020():
        return installed_version, False

    try:
        from packaging.version import Version
    except Exception:
        return installed_version, False

    try:
        needs_shim = Version(installed_version) >= Version("0.20")
    except Exception:
        needs_shim = False

    return installed_version, needs_shim


(
    _TOKENIZERS_INSTALLED_VERSION,
    _TOKENIZERS_NEEDS_SHIM,
) = _should_apply_tokenizers_shim()


@contextmanager
def _tokenizers_version_guard(installed_version: str):
    """Temporarily relax transformers' strict tokenizers requirement during import."""

    global TOKENIZERS_COMPAT_PATCHED_FROM

    patched_version = TOKENIZERS_REPORTED_VERSION
    original_version_func = importlib_metadata.version

    try:
        import importlib.metadata as stdlib_metadata
    except Exception:  # pragma: no cover
        stdlib_metadata = None

    stdlib_original = getattr(stdlib_metadata, "version", None) if stdlib_metadata else None

    try:
        import pkg_resources  # type: ignore[import-not-found]
    except Exception:  # pragma: no cover
        pkg_resources = None

    original_get_distribution = (
        pkg_resources.get_distribution if pkg_resources is not None else None  # type: ignore[attr-defined]
    )

    def _patched_version(package: str) -> str:
        if _normalize_package_name(package) == "tokenizers":
            return patched_version
        return original_version_func(package)

    class _DistributionProxy:
        """Distribution wrapper overriding the exposed version attribute."""

        __slots__ = ("_delegate",)

        def __init__(self, delegate: Any) -> None:
            self._delegate = delegate

        def __getattr__(self, attr: str) -> Any:
            if attr == "version":
                return patched_version
            return getattr(self._delegate, attr)

        def __dir__(self) -> List[str]:
            return list(dict.fromkeys(["version", *dir(self._delegate)]))

    def _patched_get_distribution(dist: Any):  # type: ignore[override]
        assert original_get_distribution is not None  # Narrow type for mypy
        distribution = original_get_distribution(dist)
        project_name = getattr(distribution, "project_name", None)
        key = getattr(distribution, "key", None)
        normalized = _normalize_package_name(project_name or key or "")
        if normalized == "tokenizers":
            return _DistributionProxy(distribution)
        return distribution

    try:
        importlib_metadata.version = _patched_version  # type: ignore[assignment]
        if stdlib_metadata is not None and stdlib_original is not None:
            stdlib_metadata.version = _patched_version  # type: ignore[assignment]
        if pkg_resources is not None and original_get_distribution is not None:
            pkg_resources.get_distribution = _patched_get_distribution  # type: ignore[assignment]
        TOKENIZERS_COMPAT_PATCHED_FROM = installed_version
        yield
    finally:
        importlib_metadata.version = original_version_func  # type: ignore[assignment]
        if stdlib_metadata is not None and stdlib_original is not None:
            stdlib_metadata.version = stdlib_original  # type: ignore[assignment]
        if pkg_resources is not None and original_get_distribution is not None:
            pkg_resources.get_distribution = original_get_distribution  # type: ignore[assignment]


def load_sentence_transformers() -> Tuple[Any, Any]:
    """Import sentence-transformers under a compatibility guard if required."""

    context = (
        _tokenizers_version_guard(_TOKENIZERS_INSTALLED_VERSION)
        if _TOKENIZERS_NEEDS_SHIM and _TOKENIZERS_INSTALLED_VERSION is not None
        else nullcontext()
    )

    with context:
        module = importlib.import_module("sentence_transformers")
        cross_encoder_cls = getattr(module, "CrossEncoder")
        sentence_transformer_cls = getattr(module, "SentenceTransformer")

    return cross_encoder_cls, sentence_transformer_cls


CrossEncoder, SentenceTransformer = load_sentence_transformers()

__all__ = [
    "CrossEncoder",
    "SentenceTransformer",
    "TOKENIZERS_COMPAT_PATCHED_FROM",
    "TOKENIZERS_REPORTED_VERSION",
    "load_sentence_transformers",
]
