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


def _sanitize_collection_dir(name: str) -> str:
    if not name:
        return "collection"

    sanitized = "".join(
        character if character.isalnum() or character in {"-", "_"} else "_"
        for character in name
    ).strip("_")

    return sanitized or "collection"


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

    def _evaluate_chunk_viability(self, token_count: int, original_text: str) -> tuple[bool, Optional[str]]:
        """Return whether the chunk should be processed along with an optional skip reason."""

        text = original_text if isinstance(original_text, str) else str(original_text)
        if not text.strip():
            return False, "empty_text"

        if token_count <= 0:
            return False, "missing_tokens"

        return True, None

    def _log_chunk_skip(
        self,
        *,
        file_name: str,
        chunk_idx: int,
        token_count: int,
        reason: Optional[str],
        results: Dict[str, Any],
    ) -> None:
        """Emit structured logging when a chunk is skipped."""

        reason_label = reason or "unspecified"
        message = (
            "[CHUNK_SKIP] File: %s | chunk_idx: %d | tokens: %d | reason: %s"
            % (file_name, chunk_idx, token_count, reason_label)
        )
        self.logger.info(message)
        print(
            "[chunk_loader] SKIP %s | chunk_idx=%d | tokens=%d | reason=%s"
            % (file_name, chunk_idx, token_count, reason_label),
            flush=True,
        )
        results.setdefault("skipped_chunks", []).append(
            {
                "file": file_name,
                "chunk_idx": chunk_idx,
                "token_count": token_count,
                "reason": reason_label,
            }
        )

    def load(
        self,
        chunks_dir: str,
        *,
        preprocess_text: Callable[[str], str],
        model_name: str,
        model_vector_dim: int,
        text_cache: Any = None,
        device: str = "unknown",
        collection_name_hint: Optional[str] = None,
        single_collection_mode: Optional[bool] = None,
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
            "collection_summaries": {},
            "collection_roots": {},
            "skipped_chunks": [],
        }

        canonical_hint: Optional[str] = None
        active_collection_alias: Optional[str] = None
        active_collection_safe_dir: Optional[str] = None

        collection_priorities = {
            "qdrant_ecosystem": 1.0,
            "sentence_transformers": 0.9,
            "docling": 0.8,
            "fast_docs": 0.7,
            "pydantic": 0.6,
        }

        normalized_dir_name = chunks_path.name.lower()
        resolved_single_mode = single_collection_mode
        if resolved_single_mode is None:
            if collection_name_hint:
                resolved_single_mode = True
            else:
                resolved_single_mode = normalized_dir_name not in {"chunked", "chunked_output", "docs_chunks_output"}

        def process_collection(collection_name: str, collection_path: Path) -> Tuple[int, bool, str]:
            nonlocal canonical_hint

            canonical_collection = normalize_collection_name(collection_name)
            priority = collection_priorities.get(canonical_collection, 0.5)
            chunk_files = self._collect_chunk_files(collection_path)
            if not chunk_files:
                self.logger.warning("No chunk JSON files detected in %s", collection_path)

            results["collection_roots"][collection_name] = str(collection_path)

            chunk_count = self._ingest_files(
                chunk_files,
                collection_name=collection_name,
                canonical_collection=canonical_collection,
                priority=priority,
                preprocess_text=preprocess_text,
                model_name=model_name,
                model_vector_dim=model_vector_dim,
                device=device,
                metadata_list=metadata_list,
                processed_texts=processed_texts,
                raw_texts=raw_texts,
                sparse_vectors=sparse_vectors,
                modal_hint_distribution=modal_hint_distribution,
                results=results,
                collection_path=collection_path,
            )

            results["chunks_by_collection"][collection_name] = chunk_count
            had_files = bool(chunk_files)
            if had_files:
                results["collections_loaded"] += 1
                if canonical_hint is None:
                    canonical_hint = canonical_collection
            elif canonical_hint is None and chunk_count:
                canonical_hint = canonical_collection

            return chunk_count, had_files, canonical_collection

        if resolved_single_mode:
            collection_name = collection_name_hint or chunks_path.name
            chunk_count, had_files, _ = process_collection(collection_name, chunks_path)
            if had_files:
                active_collection_alias = collection_name
                active_collection_safe_dir = _sanitize_collection_dir(collection_name)
            else:
                results["collections_loaded"] = 0
        else:
            collected_any = False
            subdirectories = [
                item for item in chunks_path.iterdir() if item.is_dir() and item.name != "__pycache__"
            ]

            for collection_dir in subdirectories:
                chunk_count, had_files, _ = process_collection(collection_dir.name, collection_dir)
                if had_files:
                    collected_any = True

            if not collected_any:
                collection_name = collection_name_hint or chunks_path.name
                chunk_count, had_files, _ = process_collection(collection_name, chunks_path)
                if had_files:
                    active_collection_alias = collection_name
                    active_collection_safe_dir = _sanitize_collection_dir(collection_name)
                    resolved_single_mode = True
                else:
                    results["collections_loaded"] = 0

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

        if active_collection_alias:
            results["active_collection"] = active_collection_alias
            if active_collection_safe_dir:
                results["active_collection_safe_dir"] = active_collection_safe_dir

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
        candidates.extend([
            preferred_path / "Chunked",
            preferred_path / "chunked",
            preferred_path,
        ])

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
            for path in directory.rglob(pattern):
                if path.is_file() and not self._is_summary_file(path):
                    discovered.setdefault(path, None)
        return sorted(discovered.keys())

    @staticmethod
    def _is_summary_file(path: Path) -> bool:
        if not path.name.lower().endswith(".json"):
            return False
        name = path.name.lower()
        if name == "processing_summary.json":
            return True
        if name.endswith("_processing_summary.json"):
            return True
        return False

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
        collection_path: Path,
        metadata_list: List[Dict[str, Any]],
        processed_texts: List[str],
        raw_texts: List[str],
        sparse_vectors: List[Optional[Dict[str, Any]]],
        modal_hint_distribution: defaultdict[str, int],
        results: Dict[str, Any],
        device: str,
    ) -> int:
        chunk_count = 0
        processed_files = 0
        collection_start = time.time()
        collection_start_ts = datetime.now().isoformat()
        total_files = len(files)

        self.logger.info(
            (
                "[COLLECTION_START] Name: %s | Canonical: %s | Files: %d | Priority: %.2f | "
                "Model: %s | Device: %s | Start: %s"
            ),
            collection_name,
            canonical_collection,
            total_files,
            priority,
            model_name,
            device,
            collection_start_ts,
        )
        print(
            "[throughput] collection_start | collection=%s | canonical=%s | files=%d | model=%s | device=%s | start=%s"
            % (
                collection_name,
                canonical_collection,
                total_files,
                model_name,
                device,
                collection_start_ts,
            ),
            flush=True,
        )

        for chunk_file in files:
            # Per-file throughput logging START
            file_name = chunk_file.name
            start_time = time.time()
            start_timestamp = datetime.now().isoformat()
            file_chunk_count = 0
            processed_files += 1
            
            self.logger.info(
                f"[FILE_START] Loading: {file_name} | Start: {start_timestamp}"
            )
            print(
                "[chunk_loader] Loading %s | model=%s | device=%s"
                % (file_name, model_name, device),
                flush=True,
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

            for chunk_idx, chunk in enumerate(file_chunks, start=1):
                metadata = chunk.get("metadata", {}) or {}
                original_text = chunk.get("text", "")
                if not isinstance(original_text, str):
                    original_text = str(original_text)

                token_count_value = metadata.get("token_count")
                if isinstance(token_count_value, (int, float)):
                    token_count = int(token_count_value)
                else:
                    token_count = len(original_text.split())
                    if token_count:
                        metadata.setdefault("token_count", token_count)

                viable, skip_reason = self._evaluate_chunk_viability(token_count, original_text)
                if not viable:
                    self._log_chunk_skip(
                        file_name=file_name,
                        chunk_idx=chunk_idx,
                        token_count=token_count,
                        reason=skip_reason,
                        results=results,
                    )
                    continue

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

                self.logger.info(
                    "[CHUNK_PROCESS] File: %s | chunk_idx: %d | global_id: %d | tokens: %d | processed_length: %d",
                    file_name,
                    chunk_idx,
                    chunk_id,
                    token_count,
                    len(processed_text),
                )
                print(
                    "[chunk_loader] PROCESS %s | chunk_idx=%d | global_id=%d | tokens=%d"
                    % (file_name, chunk_idx, chunk_id, token_count),
                    flush=True,
                )
            
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
                f"Model: {model_name} | "
                f"Device: {device} | "
                f"End: {end_timestamp}"
            )
            print(
                "[chunk_loader] File=%s | chunks=%d | duration=%.2fs | rate=%.2f chunk/s | model=%s | device=%s"
                % (
                    file_name,
                    file_chunk_count,
                    duration,
                    processing_rate,
                    model_name,
                    device,
                ),
                flush=True,
            )

        collection_end_ts = datetime.now().isoformat()
        collection_duration = time.time() - collection_start
        collection_rate = chunk_count / collection_duration if collection_duration > 0 else 0.0

        self.logger.info(
            (
                "[COLLECTION_END] Name: %s | Canonical: %s | Files: %d | Chunks: %d | "
                "Duration: %.2fs | Rate: %.2f chunks/sec | End: %s"
            ),
            collection_name,
            canonical_collection,
            processed_files,
            chunk_count,
            collection_duration,
            collection_rate,
            collection_end_ts,
        )
        print(
            "[throughput] collection_end | collection=%s | canonical=%s | files=%d | chunks=%d | duration=%.2fs | rate=%.2f chunk/s | end=%s"
            % (
                collection_name,
                canonical_collection,
                processed_files,
                chunk_count,
                collection_duration,
                collection_rate,
                collection_end_ts,
            ),
            flush=True,
        )

        try:
            summaries = results.setdefault("collection_summaries", {})
            summaries[collection_name] = {
                "collection": collection_name,
                "canonical_collection": canonical_collection,
                "files_enumerated": total_files,
                "files_processed": processed_files,
                "chunks_processed": chunk_count,
                "duration_seconds": collection_duration,
                "chunks_per_second": collection_rate,
                "start_timestamp": collection_start_ts,
                "end_timestamp": collection_end_ts,
                "model": model_name,
                "device": device,
                "collection_path": str(collection_path),
                "output_subdir": _sanitize_collection_dir(collection_name),
            }
        except Exception:  # pragma: no cover - defensive write guard
            pass

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
