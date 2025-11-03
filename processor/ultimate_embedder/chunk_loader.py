"""Chunk ingestion helpers extracted from the legacy core facade."""

from __future__ import annotations

import hashlib
import json
import logging
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

# Defensive import for psutil - optional dependency for memory monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from processor.ultimate_embedder.sparse_pipeline import (
    build_sparse_vector_from_metadata,
    infer_modal_hint,
)


@dataclass
class ChunkLoadResult:
    """Immutable snapshot of the chunk ingestion step."""

    metadata: List[Dict[str, Any]]
    processed_texts: List[str]
    raw_texts: List[str]
    sparse_vectors: List[Optional[Dict[str, Any]]]
    canonical_collection_hint: Optional[str]
    summary: Dict[str, Any]


def _build_hierarchy_path(section_path: Optional[Sequence[str]]) -> str:
    if not section_path:
        return ""
    return " > ".join(part.strip() for part in section_path if isinstance(part, str) and part.strip())


def normalize_collection_name(raw_name: str) -> str:
    if not raw_name:
        return "qdrant_ecosystem"

    normalized = raw_name.strip().lower().replace("-", "_").replace(" ", "_")

    explicit_map = {
        "qdrant_v4_outputs": "qdrant_ecosystem",
        "qdrant_ecosystem_v4_outputs": "qdrant_ecosystem",
        "qdrant_ecosystem": "qdrant_ecosystem",
        "sentence_transformers_v4_outputs": "sentence_transformers",
        "sentence_transformers": "sentence_transformers",
        "docling_v4_outputs": "docling",
        "docling": "docling",
        "fast_docs_v4_outputs": "fast_docs",
        "fast_docs": "fast_docs",
        "pydantic_pydantic_v4_outputs": "pydantic",
        "pydantic_v4_outputs": "pydantic",
        "pydantic": "pydantic",
    }

    if normalized in explicit_map:
        return explicit_map[normalized]

    keyword_map = {
        "qdrant": "qdrant_ecosystem",
        "sentence_transformer": "sentence_transformers",
        "sentence": "sentence_transformers",
        "docling": "docling",
        "fast_docs": "fast_docs",
        "pydantic": "pydantic",
    }

    for keyword, target in keyword_map.items():
        if keyword in normalized:
            return target

    return normalized


def _ensure_document_id(metadata: Dict[str, Any]) -> None:
    if metadata.get("document_id"):
        return

    source_hint = metadata.get("source_path") or metadata.get("source_file") or metadata.get("filename")
    if not source_hint:
        return

    normalized = Path(str(source_hint)).as_posix().lower()
    digest = hashlib.md5(normalized.encode("utf-8")).hexdigest()[:12]
    metadata["document_id"] = digest
    metadata.setdefault("document_name", Path(str(source_hint)).stem)


class ChunkLoader:
    """Load processed chunks and enrich metadata for embedding."""

    def __init__(self, *, project_root: Path, is_kaggle: bool, logger: logging.Logger) -> None:
        self.project_root = project_root
        self.is_kaggle = is_kaggle
        self.logger = logger

    def load(
        self,
        chunks_dir: str,
        *,
        preprocess_text: Callable[[str], str],
        model_name: str,
        model_vector_dim: int,
        text_cache: Any = None,
    ) -> ChunkLoadResult:
        preferred_dir = chunks_dir
        if not self.is_kaggle:
            preferred_dir = chunks_dir or str(self.project_root / "DOCS_CHUNKS_OUTPUT")

        chunks_path, attempted_paths = self._resolve_chunks_directory(preferred_dir)
        if chunks_path is None:
            self.logger.error(
                "Chunks directory not found. Tried: %s",
                ", ".join(str(path) for path in attempted_paths),
            )
            if self.is_kaggle:
                self.logger.info("On Kaggle: ensure the uploaded dataset contains a Chunked/ directory")
            return ChunkLoadResult(
                metadata=[],
                processed_texts=[],
                raw_texts=[],
                sparse_vectors=[],
                canonical_collection_hint=None,
                summary={"error": "Chunks directory not found"},
            )

        self.logger.info("Loading chunks from %s", chunks_path)

        metadata_list: List[Dict[str, Any]] = []
        processed_texts: List[str] = []
        raw_texts: List[str] = []
        sparse_vectors: List[Optional[Dict[str, Any]]] = []
        modal_hint_distribution: defaultdict[str, int] = defaultdict(int)

        results: Dict[str, Any] = {
            "collections_loaded": 0,
            "total_chunks_loaded": 0,
            "chunks_by_collection": {},
            "loading_errors": [],
            "memory_usage_mb": 0,
            "preprocessing_stats": {},
            "sparse_vectors_generated": 0,
            "modal_hint_counts": {},
        }

        canonical_hint: Optional[str] = None

        collection_priorities = {
            "qdrant_ecosystem": 1.0,
            "sentence_transformers": 0.9,
            "docling": 0.8,
            "fast_docs": 0.7,
            "pydantic": 0.6,
        }

        has_json_files = any(
            file.suffix == ".json" and not file.name.endswith("_processing_summary.json")
            for file in chunks_path.iterdir()
            if file.is_file()
        )

        if has_json_files:
            collection_name = chunks_path.name
            canonical_collection = normalize_collection_name(collection_name)
            canonical_hint = canonical_collection
            priority = collection_priorities.get(canonical_collection, 0.5)
            results["collections_loaded"] += 1

            chunk_files = self._collect_chunk_files(chunks_path)
            if not chunk_files:
                self.logger.warning("No chunk JSON files detected in %s", chunks_path)

            chunk_count = self._ingest_files(
                chunk_files,
                collection_name=collection_name,
                canonical_collection=canonical_collection,
                priority=priority,
                preprocess_text=preprocess_text,
                model_name=model_name,
                model_vector_dim=model_vector_dim,
                metadata_list=metadata_list,
                processed_texts=processed_texts,
                raw_texts=raw_texts,
                sparse_vectors=sparse_vectors,
                modal_hint_distribution=modal_hint_distribution,
                results=results,
            )
            results["chunks_by_collection"][collection_name] = chunk_count
        else:
            subdirectories = [item for item in chunks_path.iterdir() if item.is_dir() and item.name != "__pycache__"]
            for collection_dir in subdirectories:
                collection_name = collection_dir.name
                canonical_collection = normalize_collection_name(collection_name)
                priority = collection_priorities.get(canonical_collection, 0.5)
                results["collections_loaded"] += 1

                chunk_files = self._collect_chunk_files(collection_dir)
                chunk_count = self._ingest_files(
                    chunk_files,
                    collection_name=collection_name,
                    canonical_collection=canonical_collection,
                    priority=priority,
                    preprocess_text=preprocess_text,
                    model_name=model_name,
                    model_vector_dim=model_vector_dim,
                    metadata_list=metadata_list,
                    processed_texts=processed_texts,
                    raw_texts=raw_texts,
                    sparse_vectors=sparse_vectors,
                    modal_hint_distribution=modal_hint_distribution,
                    results=results,
                )
                results["chunks_by_collection"][collection_name] = chunk_count

        results["total_chunks_loaded"] = len(metadata_list)
        
        # Memory monitoring (optional if psutil available)
        if PSUTIL_AVAILABLE:
            try:
                results["memory_usage_mb"] = psutil.Process().memory_info().rss / 1024 / 1024
            except Exception:  # pragma: no cover - defensive
                results["memory_usage_mb"] = 0.0
        else:
            results["memory_usage_mb"] = 0.0
            
        if text_cache:
            try:
                results["preprocessing_stats"] = text_cache.get_stats()
            except Exception:  # pragma: no cover - defensive
                pass
        results["modal_hint_counts"] = dict(sorted(modal_hint_distribution.items()))

        return ChunkLoadResult(
            metadata=metadata_list,
            processed_texts=processed_texts,
            raw_texts=raw_texts,
            sparse_vectors=sparse_vectors,
            canonical_collection_hint=canonical_hint,
            summary=results,
        )

    def _resolve_chunks_directory(self, preferred_dir: str) -> Tuple[Optional[Path], List[Path]]:
        attempted: List[Path] = []
        candidates: List[Path] = []

        preferred_path = Path(preferred_dir)
        candidates.extend([preferred_path, preferred_path / "Chunked", preferred_path / "chunked"])

        if self.is_kaggle:
            candidates.extend([
                Path("/kaggle/working/rag_clean/Chunked"),
                Path("/kaggle/working/Chunked"),
            ])
            kaggle_root = Path("/kaggle/input")
            if kaggle_root.exists():
                for dataset_dir in sorted(kaggle_root.iterdir()):
                    if dataset_dir.is_dir():
                        candidates.extend([
                            dataset_dir / "Chunked",
                            dataset_dir / "chunked",
                            dataset_dir,
                        ])
            candidates.extend([
                Path("/kaggle/input/docs-chunks-output"),
                Path("/kaggle/input/docs-chunks-output/Chunked"),
            ])
        else:
            local_root = self.project_root / "DOCS_CHUNKS_OUTPUT"
            candidates.extend([
                self.project_root / "Chunked",
                self.project_root / "chunked",
                self.project_root / "output" / "Chunked",
                local_root,
                local_root / "Chunked",
                local_root / "chunked",
                Path(r"C:\Users\raze0\Documents\LLM_KNOWLEDGE_CREATOR\RAG\RAG_CLEAN\DOCS_CHUNKS_OUTPUT"),
            ])

        seen: set[Path] = set()

        for candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)
            attempted.append(candidate)
            if self._looks_like_chunk_dir(candidate):
                self.logger.info("Resolved chunks directory to %s", candidate)
                return candidate, attempted

        return None, attempted

    def _looks_like_chunk_dir(self, path: Path) -> bool:
        if not path.exists() or path.is_file():
            return False
        try:
            for entry in path.iterdir():
                if entry.is_dir():
                    return True
                if entry.suffix.lower() == ".json":
                    return True
        except Exception:
            return False
        return False

    def _collect_chunk_files(self, directory: Path) -> List[Path]:
        patterns = ["*_chunks.json", "*chunks.json", "*.json"]
        discovered: Dict[Path, None] = {}
        for pattern in patterns:
            for path in directory.glob(pattern):
                if path.is_file():
                    discovered.setdefault(path, None)
        return sorted(discovered.keys())

    def _ingest_files(
        self,
        files: List[Path],
        *,
        collection_name: str,
        canonical_collection: str,
        priority: float,
        preprocess_text: Callable[[str], str],
        model_name: str,
        model_vector_dim: int,
        metadata_list: List[Dict[str, Any]],
        processed_texts: List[str],
        raw_texts: List[str],
        sparse_vectors: List[Optional[Dict[str, Any]]],
        modal_hint_distribution: defaultdict[str, int],
        results: Dict[str, Any],
    ) -> int:
        chunk_count = 0
        for chunk_file in files:
            # Per-file throughput logging START
            file_name = chunk_file.name
            start_time = time.time()
            start_timestamp = datetime.now().isoformat()
            file_chunk_count = 0
            
            self.logger.info(
                f"[FILE_START] Loading: {file_name} | Start: {start_timestamp}"
            )
            
            try:
                with open(chunk_file, "r", encoding="utf-8") as handle:
                    raw_chunks = json.load(handle)
            except Exception as exc:
                message = f"Error loading {chunk_file}: {exc}"
                self.logger.error(message)
                results["loading_errors"].append(message)
                continue

            file_chunks = self._coerce_file_chunks(raw_chunks, chunk_file)
            if not file_chunks:
                message = f"No usable chunks extracted from {chunk_file}"
                self.logger.warning(message)
                results["loading_errors"].append(message)
                continue

            for chunk in file_chunks:
                metadata = chunk.get("metadata", {}) or {}
                token_count = metadata.get("token_count", 0)
                if isinstance(token_count, (int, float)) and token_count < 50:
                    continue

                original_text = chunk.get("text", "")
                processed_text = preprocess_text(original_text)
                chunk_id = len(metadata_list)
                hierarchy_path = metadata.get("hierarchy_path") or _build_hierarchy_path(metadata.get("section_path"))

                collection_hints_raw = metadata.get("collection_hints") or metadata.get("qdrant_collection_hint")
                if isinstance(collection_hints_raw, str):
                    collection_hints = [collection_hints_raw]
                elif isinstance(collection_hints_raw, list):
                    seen_hints: set[str] = set()
                    collection_hints = [
                        hint for hint in collection_hints_raw if isinstance(hint, str) and not (hint in seen_hints or seen_hints.add(hint))
                    ]
                else:
                    collection_hints = [canonical_collection]

                metadata_updates = {
                    "global_chunk_id": chunk_id,
                    "collection_priority": priority,
                    "quality_score": min(1.0, float(token_count) / 1000.0) if token_count else 0.0,
                    "text_preprocessing_applied": True,
                    "original_length": len(original_text),
                    "processed_length": len(processed_text),
                    "full_text_length": len(original_text),
                    "kaggle_processing_timestamp": datetime.now().isoformat(),
                    "model_target": model_name,
                    "embedding_dimension": model_vector_dim,
                    "qdrant_collection": canonical_collection,
                    "collection_alias": collection_name,
                    "collection_hints": collection_hints,
                    "hierarchy_path": hierarchy_path,
                }

                metadata.update(metadata_updates)
                metadata["qdrant_collection_hint"] = metadata["collection_hints"]
                metadata.setdefault("payload_version", "1.2")
                source_path = metadata.get("source_path") or metadata.get("source_file") or metadata.get("filename") or str(chunk_file)
                metadata.setdefault("source_path", source_path)
                metadata.setdefault("source_file", metadata["source_path"])
                metadata.setdefault("source_filename", Path(str(metadata["source_file"])).name)
                metadata["chunk_file_name"] = file_name  # Track the chunk JSON filename for progress display
                metadata.setdefault("document_name", Path(str(metadata["source_file"])).stem)
                if not metadata.get("chunk_hash"):
                    digest = hashlib.sha1(original_text.encode("utf-8")).hexdigest()[:16]
                    metadata["chunk_hash"] = digest
                metadata.setdefault("content_digest", metadata["chunk_hash"])
                metadata.setdefault("content_type", metadata.get("content_type", "hierarchical_section"))

                keywords = set(k for k in metadata.get("search_keywords", []) if isinstance(k, str))
                if hierarchy_path:
                    keywords.update(part.strip() for part in hierarchy_path.split(" > ") if part.strip())
                heading = metadata.get("heading_text")
                if isinstance(heading, str) and heading.strip():
                    keywords.add(heading)
                metadata["search_keywords"] = sorted(k for k in keywords if k)

                sparse_vector = build_sparse_vector_from_metadata(metadata)
                sparse_vectors.append(sparse_vector)
                if sparse_vector:
                    results["sparse_vectors_generated"] += 1
                    metadata["sparse_vector"] = sparse_vector
                else:
                    metadata.pop("sparse_vector", None)

                metadata["sparse_vector_tokens"] = sparse_vector.get("tokens") if sparse_vector else []
                metadata["sparse_vector_weight_norm"] = sparse_vector.get("stats", {}).get("weight_norm") if sparse_vector else 0.0

                modal_hint = infer_modal_hint(original_text, metadata)
                if modal_hint:
                    metadata["modal_hint"] = modal_hint
                    metadata.setdefault("embedding_modal_hint", modal_hint)
                    modal_hint_distribution[modal_hint] += 1

                _ensure_document_id(metadata)

                chunk["metadata"] = metadata
                metadata_list.append(metadata)
                processed_texts.append(processed_text)
                raw_texts.append(original_text)
                chunk_count += 1
                file_chunk_count += 1
            
            # Per-file throughput logging END
            end_time = time.time()
            duration = end_time - start_time
            end_timestamp = datetime.now().isoformat()
            processing_rate = file_chunk_count / duration if duration > 0 else 0.0
            
            self.logger.info(
                f"[FILE_END] Loaded: {file_name} | "
                f"Chunks: {file_chunk_count} | "
                f"Duration: {duration:.2f}s | "
                f"Rate: {processing_rate:.1f} chunks/sec | "
                f"End: {end_timestamp}"
            )

        return chunk_count

    def _coerce_file_chunks(self, payload: Any, chunk_file: Path) -> List[Dict[str, Any]]:
        """Normalize arbitrary JSON payloads into chunk dictionaries."""

        # Handle wrapper dicts that store chunks under a known key.
        if isinstance(payload, dict):
            for key in ("chunks", "data", "records", "items"):
                value = payload.get(key)
                if isinstance(value, list):
                    return self._coerce_file_chunks(value, chunk_file)
            return [payload]

        if isinstance(payload, list):
            normalized: List[Dict[str, Any]] = []
            malformed_entries = 0
            for entry in payload:
                if isinstance(entry, dict):
                    normalized.append(entry)
                    continue
                if isinstance(entry, str):
                    normalized.append({"text": entry, "metadata": {}})
                    malformed_entries += 1
                    continue
                malformed_entries += 1

            if malformed_entries:
                self.logger.warning(
                    "Coerced %s malformed entries to chunk records in %s",
                    malformed_entries,
                    chunk_file,
                )
            return normalized

        if isinstance(payload, str):
            self.logger.warning("Wrapping string payload as chunk in %s", chunk_file)
            return [{"text": payload, "metadata": {}}]

        self.logger.error(
            "Unsupported chunk payload type %s in %s", type(payload).__name__, chunk_file
        )
        return []


__all__ = ["ChunkLoader", "ChunkLoadResult", "normalize_collection_name"]
