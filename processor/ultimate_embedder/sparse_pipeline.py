"""Sparse vector utilities for the Ultimate Embedder runtime."""

from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional

import numpy as np


def _stable_term_index(term: str) -> int:
    digest = hashlib.sha1(term.encode("utf-8")).hexdigest()[:8]
    return int(digest, 16)


def build_sparse_vector_from_metadata(metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Construct a normalized sparse vector structure from chunk metadata."""

    sparse = metadata.get("sparse_features")
    if not isinstance(sparse, dict):
        return None

    term_weights = sparse.get("term_weights")
    if not isinstance(term_weights, list):
        return None

    indices: List[int] = []
    values: List[float] = []
    tokens: List[str] = []

    for entry in term_weights:
        term = entry.get("term")
        weight = entry.get("weight")
        if not isinstance(term, str):
            continue
        if not isinstance(weight, (int, float)):
            continue
        index = _stable_term_index(term)
        indices.append(index)
        values.append(float(weight))
        tokens.append(term)

    if not indices:
        return None

    vector = np.array(values, dtype=np.float32)
    norm = float(np.linalg.norm(vector))
    if norm > 0:
        normalized_values = (vector / norm).tolist()
    else:
        normalized_values = vector.tolist()

    return {
        "indices": indices,
        "values": normalized_values,
        "tokens": tokens,
        "stats": {
            "weight_norm": norm,
            "unique_terms": sparse.get("unique_terms", len(tokens)),
            "total_terms": sparse.get("total_terms", 0),
            "weighting": sparse.get("weighting", "tf-normalized"),
        },
    }


def infer_modal_hint(text: str, metadata: Dict[str, Any]) -> Optional[str]:
    """Infer the modal hint for a chunk using metadata and text heuristics."""

    hint = metadata.get("modal_hint")
    if isinstance(hint, str) and hint.strip():
        return hint.strip()

    flags = metadata.get("content_flags") or {}
    if isinstance(flags, dict):
        if flags.get("has_table"):
            return "table"
        if flags.get("has_code_block"):
            return "code"
        if flags.get("has_list"):
            return "list"
        if flags.get("has_json"):
            return "json"

    sample = text.strip().lower()[:400]
    if "```" in text or "def " in sample or "class " in sample:
        return "code"
    if "|" in text and "\n|" in text:
        return "table"
    if sample.startswith("{") or sample.startswith("["):
        return "json"
    return "prose" if text.strip() else None


__all__ = [
    "build_sparse_vector_from_metadata",
    "infer_modal_hint",
]
