#!/usr/bin/env python3
"""Research-aligned hierarchical chunker with sparse metadata enrichment."""

from __future__ import annotations

import json
import logging
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
import hashlib

import numpy as np
import tiktoken

try:
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover - optional dependency
    SentenceTransformer = None  # type: ignore[assignment]
from sklearn.metrics.pairwise import cosine_similarity

try:
    import semchunk  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    semchunk = None  # type: ignore

try:
    from tree_sitter import Language, Parser  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    Language = None  # type: ignore
    Parser = None  # type: ignore

try:
    from tree_sitter_languages import get_language  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    get_language = None  # type: ignore

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DEFAULT_EMBEDDING_MODEL = "jina-code-embeddings-1.5b"
DEFAULT_EMBEDDING_DIMENSION = 1536


@dataclass
class HierarchicalMetadata:
    """Lightweight metadata container used during chunk construction."""

    chunk_id: str
    source_file: str
    filename: str
    file_extension: str
    chunk_index: int
    document_level: int
    parent_chunk_id: Optional[str]
    child_chunk_ids: List[str] = field(default_factory=list)
    section_path: List[str] = field(default_factory=list)
    heading_text: str = ""
    token_count: int = 0
    char_count: int = 0
    start_char: int = 0
    end_char: int = 0
    semantic_score: float = 0.0
    structural_score: float = 0.0
    retrieval_quality: float = 0.0
    chunking_strategy: str = "hierarchical_balanced"
    content_type: str = "hierarchical_section"
    embedding_model: str = ""
    embedding_dimension: int = DEFAULT_EMBEDDING_DIMENSION
    processing_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class EnhancedUltimateChunkerV3:
    """Hierarchical chunker feeding the downstream embedding/ingestion pipeline."""

    def __init__(
        self,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
        embedding_dimension: int = DEFAULT_EMBEDDING_DIMENSION,
        tokenizer_name: str = "cl100k_base",
        quality_thresholds: Optional[Dict[str, float]] = None,
        fallback_promotion_ratio: float = 0.25,
        fallback_promotion_cap: int = 40,
    ) -> None:
        self.embedding_model_name = embedding_model or "semantic_scoring_disabled"
        self.embedding_dimension = max(1, int(embedding_dimension))
        self.embedder: Optional[Any] = None
        self.enable_semantic_scoring = False

        if embedding_model and SentenceTransformer is not None:
            try:
                self.embedder = SentenceTransformer(embedding_model, trust_remote_code=True)
                self.enable_semantic_scoring = True
                try:
                    model_dimension = getattr(
                        self.embedder,
                        "get_sentence_embedding_dimension",
                        lambda: self.embedding_dimension,
                    )()
                    if isinstance(model_dimension, int) and model_dimension > 0:
                        self.embedding_dimension = model_dimension
                except Exception:  # pragma: no cover - defensive
                    logger.debug("Unable to determine embedding dimension from model %s", embedding_model)
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning(
                    "Failed to load semantic model %s (%s); semantic scoring disabled",
                    embedding_model,
                    exc,
                )
        elif embedding_model and SentenceTransformer is None:
            logger.warning(
                "SentenceTransformer package not available; semantic scoring disabled"
            )

        self.tokenizer = tiktoken.get_encoding(tokenizer_name)
        self.project_root = Path.cwd()

        self.content_type_patterns: Dict[str, Dict[str, Any]] = {
            "mcp_repository": {
                "patterns": ["mcp", "protocol", "tool", "client", "server"],
                "strategy": "hybrid_adaptive",
                "description": "Model Context Protocol repositories",
            },
            "workflow_documentation": {
                "patterns": ["workflow", "pipeline", "step", "process", "action"],
                "strategy": "hierarchical_balanced",
                "description": "Workflow and procedural documentation",
            },
            "api_documentation": {
                "patterns": ["api", "endpoint", "request", "response", "parameter"],
                "strategy": "hierarchical_precise",
                "description": "Reference-style API documentation",
            },
            "programming_documentation": {
                "patterns": ["python", "javascript", "typescript", "class", "function"],
                "strategy": "hybrid_adaptive",
                "description": "Language or library reference material",
            },
            "platform_documentation": {
                "patterns": ["deployment", "kubernetes", "infrastructure", "platform"],
                "strategy": "hierarchical_context",
                "description": "Platform and infrastructure documentation",
            },
        }

        self.chunking_strategies: Dict[str, Dict[str, Any]] = {
            "hierarchical_precise": {
                "max_tokens": 512,
                "overlap": 80,
                "min_section_tokens": 120,
                "description": "High precision with tighter chunks",
            },
            "hierarchical_balanced": {
                "max_tokens": 1024,
                "overlap": 100,
                "min_section_tokens": 180,
                "description": "Balanced chunks tuned for workflow docs",
            },
            "hierarchical_context": {
                "max_tokens": 2048,
                "overlap": 160,
                "min_section_tokens": 260,
                "description": "Maximum context retention",
            },
            "hybrid_adaptive": {
                "max_tokens": 1024,
                "overlap": 120,
                "min_section_tokens": 160,
                "description": "Hybrid structural + semantic approach",
            },
            "mcp_optimized": {
                "max_tokens": 768,
                "overlap": 96,
                "min_section_tokens": 140,
                "description": "Optimised for MCP repositories",
            },
            "performance_optimized": {
                "max_tokens": 1536,
                "overlap": 128,
                "min_section_tokens": 220,
                "description": "Performance focused large chunking",
            },
        }

        self._semchunk_available = semchunk is not None
        self._semchunk_cache: Dict[int, Any] = {}
        self._tree_sitter_languages: Dict[str, Any] = {}
        self._tree_sitter_node_types: Dict[str, Sequence[str]] = {
            "python": ["function_definition", "class_definition"],
            "javascript": ["function_declaration", "method_definition", "class_declaration"],
            "typescript": ["function_declaration", "method_definition", "class_declaration"],
            "java": ["class_declaration", "method_declaration"],
            "go": ["function_declaration", "method_declaration"],
            "rust": ["function_item", "impl_item", "struct_item"],
            "c": ["function_definition"],
            "cpp": ["function_definition", "class_specifier"],
        }
        self._tree_sitter_supported = Parser is not None and get_language is not None

        self.language_hints_by_extension: Dict[str, str] = {
            ".py": "python",
            ".ipynb": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".jsx": "javascript",
            ".java": "java",
            ".go": "go",
            ".rs": "rust",
            ".c": "c",
            ".h": "c",
            ".cpp": "cpp",
            ".hpp": "cpp",
        }

        self.quality_thresholds = {
            "min_semantic_score": 0.55,
            "min_structural_score": 0.60,
            "min_retrieval_quality": 0.50,
            "min_information_density": 0.35,
        }

        if quality_thresholds:
            self.quality_thresholds.update(quality_thresholds)

        self.fallback_promotion_ratio = max(0.05, min(fallback_promotion_ratio, 1.0))
        self.fallback_promotion_cap = max(5, fallback_promotion_cap)

        self.default_collection_hints: Dict[str, List[str]] = {
            "mcp_repository": ["qdrant_ecosystem"],
            "workflow_documentation": ["docling"],
            "api_documentation": ["fast_docs"],
            "programming_documentation": ["sentence_transformers"],
            "platform_documentation": ["qdrant_ecosystem"],
            "hierarchical_section": ["qdrant_ecosystem"],
        }

        logger.info("Enhanced Ultimate Chunker v3 initialised with %s", embedding_model)

    # ------------------------------------------------------------------
    # Helper utilities
    # ------------------------------------------------------------------
    def _collection_hints(self, content_type: str) -> List[str]:
        return self.default_collection_hints.get(content_type, ["qdrant_ecosystem"])

    @staticmethod
    def _compute_document_id(filename: str) -> str:
        normalised = Path(filename).as_posix().lower()
        return hashlib.md5(normalised.encode("utf-8")).hexdigest()[:12]

    def _make_relative_path(self, filename: str) -> str:
        try:
            return str(Path(filename).resolve().relative_to(self.project_root))
        except ValueError:
            return str(Path(filename))

    @staticmethod
    def _build_byte_to_char_lookup(text: str) -> List[int]:
        lookup: List[int] = [0]
        for index, character in enumerate(text):
            lookup.extend([index + 1] * len(character.encode("utf-8")))
        return lookup

    def _looks_like_code(self, text: str) -> bool:
        if "```" in text:
            return True
        code_keywords = ["def ", "class ", "function ", "#include", "import ", "public ", "void "]
        keyword_hits = sum(1 for keyword in code_keywords if keyword in text)
        punctuation_density = sum(text.count(sym) for sym in "{}();:=") / max(len(text), 1)
        return keyword_hits >= 2 or punctuation_density > 0.025

    def _get_semchunk_chunker(self, chunk_size: int):
        if not self._semchunk_available:
            return None
        chunk_size = max(32, int(chunk_size))
        if chunk_size not in self._semchunk_cache:
            def token_counter(value: str) -> int:
                return len(self._encode_tokens(value))

            try:
                chunker_factory = getattr(semchunk, "chunkerify", None) if semchunk else None
                if chunker_factory is None:
                    raise AttributeError("semchunk.chunkerify not available")
                self._semchunk_cache[chunk_size] = chunker_factory(token_counter, chunk_size)
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning("Semchunk initialisation failed: %s", exc)
                self._semchunk_available = False
                return None
        return self._semchunk_cache.get(chunk_size)

    def _get_tree_sitter_language(self, language_name: Optional[str]):
        if not language_name or not self._tree_sitter_supported:
            return None
        if language_name not in self._tree_sitter_languages:
            try:
                language_loader = get_language
                if language_loader is None:
                    raise RuntimeError("tree_sitter_languages.get_language unavailable")
                self._tree_sitter_languages[language_name] = language_loader(language_name)
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning("Tree-sitter language load failed for %s: %s", language_name, exc)
                self._tree_sitter_languages[language_name] = None
        return self._tree_sitter_languages.get(language_name)

    def _select_chunking_backend(
        self,
        section_text: str,
        filename: str,
        block_meta: Dict[str, Any],
    ) -> Tuple[str, str, Optional[str]]:
        modal_flags = self._detect_modal_hints(section_text)
        extension = Path(filename).suffix.lower()
        language_hint = self.language_hints_by_extension.get(extension)

        if modal_flags["modal_hint"] == "code" or self._looks_like_code(section_text) or language_hint:
            language_hint = language_hint or "python"
            if self._get_tree_sitter_language(language_hint):
                return "tree_sitter", "code_block", language_hint
        if modal_flags["modal_hint"] == "table":
            return "hierarchical", "table_section", None
        if modal_flags["modal_hint"] == "list":
            return "hierarchical", "list_section", None
        if self._semchunk_available:
            return "semchunk", "prose_section", None
        return "hierarchical", "hierarchical_section", None

    def _create_chunk_metadata(
        self,
        text: str,
        section_path: Sequence[str],
        filename: str,
        document_id: str,
        chunk_index: int,
        chunking_strategy: str,
        start_char: int,
        content_type: str,
        end_char: Optional[int] = None,
        embedding_dimension: Optional[int] = None,
    ) -> HierarchicalMetadata:
        end_value = end_char if end_char is not None else start_char + len(text)
        metadata = HierarchicalMetadata(
            chunk_id=f"{document_id}-{chunk_index:04d}",
            source_file=filename,
            filename=Path(filename).name,
            file_extension=Path(filename).suffix,
            chunk_index=chunk_index,
            document_level=len(section_path),
            parent_chunk_id=None,
            section_path=list(section_path),
            heading_text=section_path[-1] if section_path else "",
            token_count=len(self._encode_tokens(text)),
            char_count=len(text),
            start_char=start_char,
            end_char=end_value,
            chunking_strategy=chunking_strategy,
            content_type=content_type,
            embedding_model=self.embedding_model_name,
            embedding_dimension=embedding_dimension if embedding_dimension is not None else self.embedding_dimension,
        )
        return metadata

    @staticmethod
    def _compute_chunk_hash(text: str) -> str:
        return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]

    def _encode_tokens(self, text: str) -> List[int]:
        """Encode text with special-token tolerance for robustness."""
        try:
            return self.tokenizer.encode(text, disallowed_special=())
        except ValueError as exc:  # pragma: no cover - defensive fallback
            logger.debug("Token encoding fallback for %s: %s", text[:40], exc)
            return self.tokenizer.encode(text, allowed_special="all")

    def _normalise_path_for_io(self, path: Path) -> str:
        path_str = str(path)
        if os.name != "nt":
            return path_str

        normalised = os.path.normpath(path_str)
        if normalised.startswith("\\\\?\\"):
            return normalised

        if len(normalised) < 248:
            return normalised

        if normalised.startswith("\\\\"):
            return f"\\\\?\\UNC{normalised[1:]}"

        return f"\\\\?\\{normalised}"

    def _read_text(self, path: Path, *, errors: Optional[str] = None) -> str:
        parameters: Dict[str, Any] = {"encoding": "utf-8"}
        if errors is not None:
            parameters["errors"] = errors

        with open(self._normalise_path_for_io(path), "r", **parameters) as handle:
            return handle.read()

    def _write_text(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._normalise_path_for_io(path), "w", encoding="utf-8") as handle:
            handle.write(content)

    @staticmethod
    def _format_section_path(section_path: List[str]) -> str:
        return " > ".join(part.strip() for part in section_path if isinstance(part, str) and part.strip())

    @staticmethod
    def _compute_sparse_features(text: str, top_n: int = 20) -> Dict[str, Any]:
        word_pattern = re.compile(r"[a-zA-Z0-9]{3,}")
        tokens = word_pattern.findall(text.lower())
        total_terms = len(tokens)

        if total_terms == 0:
            return {
                "version": "1.0",
                "weighting": "tf-normalized",
                "top_terms": [],
                "term_weights": [],
                "unique_terms": 0,
                "total_terms": 0,
            }

        frequency = Counter(tokens)
        most_common = frequency.most_common(top_n)
        term_weights = []
        for term, count in most_common:
            weight = count / total_terms
            term_weights.append({
                "term": term,
                "tf": int(count),
                "weight": float(round(weight, 6)),
            })

        return {
            "version": "1.0",
            "weighting": "tf-normalized",
            "top_terms": [term for term, _ in most_common],
            "term_weights": term_weights,
            "unique_terms": len(frequency),
            "total_terms": total_terms,
        }

    @staticmethod
    def _detect_modal_hints(text: str) -> Dict[str, Any]:
        has_code_block = "```" in text or bool(re.search(r"\b(def|class|function)\b", text))
        has_table = bool(re.search(r"\n\|[^|]+\|", text))
        has_list = bool(re.search(r"^\s*[-*+]\s", text, re.MULTILINE))
        has_json = text.strip().startswith("{") or text.strip().startswith("[")
        has_formula = bool(re.search(r"\$[^$]+\$", text))

        modal_hint = "prose"
        if has_table:
            modal_hint = "table"
        elif has_code_block:
            modal_hint = "code"
        elif has_list:
            modal_hint = "list"
        elif has_json:
            modal_hint = "json"

        return {
            "modal_hint": modal_hint,
            "has_code_block": has_code_block,
            "has_table": has_table,
            "has_list": has_list,
            "has_json": has_json,
            "has_formula": has_formula,
        }

    # ------------------------------------------------------------------
    # Content type detection
    # ------------------------------------------------------------------
    def auto_detect_content_type(self, text: str, filename: str) -> Tuple[str, str]:
        text_lower = text.lower()
        filename_lower = filename.lower()

        best_type = "workflow_documentation"
        best_score = -1

        for content_type, config in self.content_type_patterns.items():
            score = 0
            for pattern in config["patterns"]:
                score += text_lower.count(pattern)
                if pattern in filename_lower:
                    score += 3
            if score > best_score:
                best_score = score
                best_type = content_type

        strategy = self.content_type_patterns[best_type]["strategy"]
        logger.info("Auto-detected %s → %s", best_type, strategy)
        return best_type, strategy

    # ------------------------------------------------------------------
    # Public processing APIs
    # ------------------------------------------------------------------
    def process_file_smart(
        self,
        file_path: str,
        output_dir: Optional[str] = None,
        auto_detect: bool = True,
        strategy_override: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        file_path_obj = Path(file_path)
        try:
            text = self._read_text(file_path_obj)
        except UnicodeDecodeError:
            text = self._read_text(file_path_obj, errors="ignore")

        if not text.strip():
            logger.warning("Skipping empty file %s", file_path)
            return []

        if auto_detect:
            content_type, strategy = self.auto_detect_content_type(text, file_path_obj.name)
        else:
            content_type, strategy = "workflow_documentation", "hierarchical_balanced"

        if strategy_override:
            strategy = strategy_override

        chunks = self.create_hierarchical_chunks(
            text=text,
            filename=str(file_path_obj),
            strategy_name=strategy,
        )

        if not chunks:
            logger.warning("No chunks generated for %s", file_path)
            return []

        if output_dir:
            self._save_chunks(chunks, str(file_path_obj), output_dir, content_type)

        return chunks

    def process_directory_smart(
        self,
        input_dir: str,
        output_dir: str,
        file_extensions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        extensions = file_extensions or [".md", ".txt", ".rst", ".py", ".json"]
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        files: List[Path] = []
        for ext in extensions:
            files.extend(input_path.rglob(f"*{ext}"))
        files = sorted(files)

        logger.info("Found %d files to process in %s", len(files), input_dir)

        summary = {
            "processed_files": 0,
            "total_chunks": 0,
            "processing_time": 0.0,
            "content_types": defaultdict(int),
            "strategies_used": defaultdict(int),
            "files": [],
        }

        start_time = datetime.now()

        for file_path in files:
            chunks = self.process_file_smart(str(file_path), output_dir=str(output_path))
            if not chunks:
                continue

            summary["processed_files"] += 1
            summary["total_chunks"] += len(chunks)

            metadata = chunks[0]["metadata"]
            content_type = metadata.get("content_type", "hierarchical_section")
            strategy = metadata.get("chunking_strategy", "hierarchical_balanced")

            summary["content_types"][content_type] += 1
            summary["strategies_used"][strategy] += 1
            summary["files"].append({
                "file": str(file_path),
                "chunks": len(chunks),
                "content_type": content_type,
                "strategy": strategy,
            })

        summary["processing_time"] = (datetime.now() - start_time).total_seconds()

        summary_path = output_path / "chunk_summary.json"
        serialisable_summary = {
            **summary,
            "content_types": dict(summary["content_types"]),
            "strategies_used": dict(summary["strategies_used"]),
        }
        self._write_text(summary_path, json.dumps(serialisable_summary, indent=2))
        logger.info("Wrote directory summary to %s", summary_path)

        return serialisable_summary

    def _save_chunks(
        self,
        chunks: List[Dict[str, Any]],
        file_path: str,
        output_dir: str,
        content_type: str,
    ) -> None:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        filename = Path(file_path).stem
        target = output_path / f"{filename}_{content_type}_chunks.json"

        for chunk in chunks:
            scores = chunk.get("advanced_scores", {})
            for key, value in list(scores.items()):
                if hasattr(value, "item"):
                    scores[key] = float(value)

        self._write_text(target, json.dumps(chunks, indent=2, ensure_ascii=False))
        logger.info("Saved %d chunks to %s", len(chunks), target)

    # ------------------------------------------------------------------
    # Structure analysis helpers
    # ------------------------------------------------------------------
    def detect_document_structure(self, text: str) -> Dict[str, Any]:
        structure: Dict[str, Any] = {
            "headings": [],
            "content_blocks": [],
            "hierarchy": defaultdict(list),
            "has_headers": bool(re.search(r"^#{1,6}\s", text, re.MULTILINE)),
            "has_code_blocks": "```" in text,
            "has_lists": bool(re.search(r"^\s*[-*+]\s", text, re.MULTILINE)),
            "has_tables": "|" in text and bool(re.search(r"\|.*\|", text)),
            "line_count": text.count("\n"),
            "avg_line_length": len(text) / max(1, text.count("\n")),
            "sections": len(re.findall(r"^#{1,6}\s.*$", text, re.MULTILINE)),
            "paragraphs": len(re.findall(r"\n\s*\n", text)) + 1,
        }

        for match in re.finditer(r"^(#{1,6})\s+(.+)$", text, re.MULTILINE):
            level = len(match.group(1))
            title = match.group(2).strip()
            line_number = text[: match.start()].count("\n") + 1
            structure["headings"].append({
                "level": level,
                "title": title,
                "start_line": line_number,
            })
            structure["hierarchy"][level].append({
                "title": title,
                "start_line": line_number - 1,
                "path": [title],
                "level": level,
            })

        lines = text.split("\n")
        line_offsets: List[int] = []
        running_offset = 0
        for line in lines:
            line_offsets.append(running_offset)
            running_offset += len(line) + 1
        total_length = len(text)

        if not structure["headings"]:
            stripped = text.strip()
            if stripped:
                leading_trim = len(text) - len(text.lstrip())
                start_char = leading_trim
                end_char = start_char + len(stripped)
                structure["content_blocks"].append({
                    "heading": None,
                    "content": stripped,
                    "length": len(stripped),
                    "start_line": 1,
                    "end_line": len(lines),
                    "start_char": start_char,
                    "end_char": end_char,
                })
        else:
            for idx, heading in enumerate(structure["headings"]):
                start = heading["start_line"] - 1
                end = (
                    structure["headings"][idx + 1]["start_line"] - 1
                    if idx + 1 < len(structure["headings"])
                    else len(lines)
                )
                block_start_char = line_offsets[start] if start < len(line_offsets) else total_length
                block_end_char = line_offsets[end] if end < len(line_offsets) else total_length
                raw_section = text[block_start_char:block_end_char]
                section_text = raw_section.strip()
                if not section_text:
                    continue
                leading_trim = len(raw_section) - len(raw_section.lstrip())
                start_char = block_start_char + leading_trim
                end_char = start_char + len(section_text)
                structure["content_blocks"].append({
                    "heading": heading,
                    "content": section_text,
                    "length": len(section_text),
                    "start_line": start + 1,
                    "end_line": end,
                    "start_char": start_char,
                    "end_char": end_char,
                })

        return structure

    def _split_into_sentences(self, text: str) -> List[str]:
        sentences: List[str] = []
        current: List[str] = []
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("```"):
                if current:
                    sentences.append(" ".join(current).strip())
                    current = []
                sentences.append(line)
                continue
            current.append(line)
            if stripped.endswith((".", "!", "?")):
                sentences.append(" ".join(current).strip())
                current = []
        if current:
            sentences.append(" ".join(current).strip())
        return [s for s in sentences if s.strip()]

    def _chunk_section_structural(
        self,
        section_text: str,
        section_path: List[str],
        filename: str,
        strategy_name: str,
        start_chunk_index: int,
        document_id: str,
        block_start_char: int,
        content_type: str,
    ) -> List[Dict[str, Any]]:
        strategy = self.chunking_strategies.get(
            strategy_name,
            self.chunking_strategies["hierarchical_balanced"],
        )
        max_tokens = strategy["max_tokens"]
        overlap = strategy["overlap"]

        chunks: List[Dict[str, Any]] = []
        sentences = self._split_into_sentences(section_text)
        buffer: List[str] = []
        start_char = 0

        def flush_buffer() -> None:
            nonlocal buffer, start_char, current_tokens
            if not buffer:
                return
            text = " ".join(buffer).strip()
            if not text:
                buffer = []
                return
            chunk_index = start_chunk_index + len(chunks)
            metadata = self._create_chunk_metadata(
                text=text,
                section_path=section_path,
                filename=filename,
                document_id=document_id,
                chunk_index=chunk_index,
                chunking_strategy=f"{strategy_name}_structural",
                start_char=block_start_char + start_char,
                content_type=content_type,
                end_char=block_start_char + start_char + len(text),
            )
            chunks.append({"text": text, "metadata": metadata})

            if overlap and text:
                tokens = self._encode_tokens(text)
                overlap_tokens = tokens[-min(len(tokens), overlap):]
                overlap_text = self.tokenizer.decode(overlap_tokens)
                buffer = [overlap_text] if overlap_text else []
                current_tokens = len(overlap_tokens) if overlap_text else 0
                start_char += len(text)
            else:
                buffer = []
                current_tokens = 0
                start_char += len(text)

        current_tokens = 0
        for sentence in sentences:
            sentence_tokens = len(self._encode_tokens(sentence))
            tentative = current_tokens + sentence_tokens
            if tentative <= max_tokens:
                buffer.append(sentence)
                current_tokens = tentative
                continue
            flush_buffer()
            buffer.append(sentence)
            current_tokens = len(self._encode_tokens(" ".join(buffer)))

        flush_buffer()
        return chunks

    def _chunk_section_semchunk(
        self,
        section_text: str,
        section_path: List[str],
        filename: str,
        strategy_label: str,
        start_chunk_index: int,
        document_id: str,
        block_start_char: int,
        content_type: str,
        max_tokens: int,
        overlap: int,
    ) -> List[Dict[str, Any]]:
        chunker = self._get_semchunk_chunker(max_tokens)
        if chunker is None:
            return self._chunk_section_structural(
                section_text,
                section_path,
                filename,
                strategy_label.rsplit("_", 1)[0] if "_" in strategy_label else strategy_label,
                start_chunk_index,
                document_id,
                block_start_char,
                content_type,
            )

        kwargs: Dict[str, Any] = {"offsets": True}
        if overlap:
            kwargs["overlap"] = min(overlap, max_tokens - 1)

        try:
            chunk_texts, offsets = chunker(section_text, **kwargs)
        except TypeError:  # pragma: no cover - compatibility
            chunk_texts = chunker(section_text)
            offsets = None

        if isinstance(chunk_texts, list) and chunk_texts and isinstance(chunk_texts[0], list):
            chunk_texts = chunk_texts[0]
            offsets = offsets[0] if offsets else None

        results: List[Dict[str, Any]] = []
        running_offset = 0

        for idx, chunk_text in enumerate(chunk_texts):
            text = chunk_text.strip()
            if not text:
                continue
            if offsets and idx < len(offsets):
                start_offset, end_offset = offsets[idx]
            else:
                start_offset = running_offset
                end_offset = start_offset + len(text)
            chunk_index = start_chunk_index + len(results)
            metadata = self._create_chunk_metadata(
                text=text,
                section_path=section_path,
                filename=filename,
                document_id=document_id,
                chunk_index=chunk_index,
                chunking_strategy=strategy_label,
                start_char=block_start_char + start_offset,
                content_type=content_type,
                end_char=block_start_char + end_offset,
                embedding_dimension=self.embedding_dimension,
            )
            results.append({"text": text, "metadata": metadata})
            running_offset = end_offset

        return results

    def _collect_tree_sitter_nodes(self, root_node: Any, language_hint: str) -> List[Any]:
        target_types = list(self._tree_sitter_node_types.get(language_hint, []))
        if not target_types:
            target_types = list(self._tree_sitter_node_types.get("python", []))
        if not target_types:
            return []

        nodes: List[Any] = []
        stack: List[Any] = [root_node]

        while stack:
            node = stack.pop()
            if not getattr(node, "is_named", lambda: True)():
                continue
            if node.type in target_types:
                parent = getattr(node, "parent", None)
                parent_type = parent.type if parent else None
                if parent_type not in target_types:
                    nodes.append(node)
                continue
            children = getattr(node, "children", [])
            stack.extend(reversed(children))

        nodes.sort(key=lambda n: n.start_byte)
        return nodes

    def _chunk_section_tree_sitter(
        self,
        section_text: str,
        section_path: List[str],
        filename: str,
        strategy_name: str,
        start_chunk_index: int,
        document_id: str,
        block_start_char: int,
        content_type: str,
        language_hint: str,
    ) -> List[Dict[str, Any]]:
        language = self._get_tree_sitter_language(language_hint)
        if language is None or Parser is None:
            return self._chunk_section_structural(
                section_text,
                section_path,
                filename,
                strategy_name,
                start_chunk_index,
                document_id,
                block_start_char,
                content_type,
            )

        parser = Parser()  # type: ignore[call-arg]
        parser.set_language(language)  # type: ignore[attr-defined]
        try:
            tree = parser.parse(section_text.encode("utf-8"))
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Tree-sitter parse failed (%s); falling back", exc)
            return self._chunk_section_structural(
                section_text,
                section_path,
                filename,
                strategy_name,
                start_chunk_index,
                document_id,
                block_start_char,
                content_type,
            )

        nodes = self._collect_tree_sitter_nodes(tree.root_node, language_hint)
        if not nodes:
            return self._chunk_section_structural(
                section_text,
                section_path,
                filename,
                strategy_name,
                start_chunk_index,
                document_id,
                block_start_char,
                content_type,
            )

        lookup = self._build_byte_to_char_lookup(section_text)
        strategy = self.chunking_strategies.get(
            strategy_name,
            self.chunking_strategies["hierarchical_balanced"],
        )
        max_tokens = strategy["max_tokens"]
        overlap = strategy["overlap"]

        chunks: List[Dict[str, Any]] = []

        for node in nodes:
            start_byte = min(node.start_byte, len(lookup) - 1)
            end_byte = min(node.end_byte, len(lookup) - 1)
            char_start = lookup[start_byte]
            char_end = lookup[end_byte]
            slice_text = section_text[char_start:char_end]
            stripped = slice_text.strip()
            if not stripped:
                continue
            leading_trim = len(slice_text) - len(slice_text.lstrip())
            adjusted_start = char_start + leading_trim
            adjusted_end = adjusted_start + len(stripped)
            token_count = len(self._encode_tokens(stripped))

            if token_count > max_tokens and self._semchunk_available:
                sub_chunks = self._chunk_section_semchunk(
                    stripped,
                    section_path,
                    filename,
                    f"{strategy_name}_tree_sitter_semchunk",
                    start_chunk_index + len(chunks),
                    document_id,
                    block_start_char + adjusted_start,
                    content_type,
                    max_tokens,
                    overlap,
                )
                chunks.extend(sub_chunks)
                continue

            chunk_index = start_chunk_index + len(chunks)
            metadata = self._create_chunk_metadata(
                text=stripped,
                section_path=section_path,
                filename=filename,
                document_id=document_id,
                chunk_index=chunk_index,
                chunking_strategy=f"{strategy_name}_tree_sitter",
                start_char=block_start_char + adjusted_start,
                content_type=content_type,
                end_char=block_start_char + adjusted_end,
                embedding_dimension=self.embedding_dimension,
            )
            metadata.section_path.append(f"{language_hint}:{node.type}")
            chunks.append({"text": stripped, "metadata": metadata})

        return chunks

    # ------------------------------------------------------------------
    # Quality calculations
    # ------------------------------------------------------------------
    def calculate_semantic_coherence(self, text: str) -> float:
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 10]
        if len(sentences) < 2:
            return 0.8
        if not self.enable_semantic_scoring or self.embedder is None:
            return self._semantic_coherence_heuristic(sentences)
        try:
            embeddings = self.embedder.encode(sentences[:5])
            similarities: List[float] = []
            for i in range(len(embeddings)):
                for j in range(i + 1, len(embeddings)):
                    sim = cosine_similarity(
                        np.array([embeddings[i]]),
                        np.array([embeddings[j]]),
                    )[0][0]
                    similarities.append(sim)
            return float(np.mean(similarities)) if similarities else 0.5
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Semantic coherence calculation failed: %s", exc)
            return self._semantic_coherence_heuristic(sentences)

    @staticmethod
    def _semantic_coherence_heuristic(sentences: List[str]) -> float:
        """Lightweight fallback for semantic coherence when no encoder is available."""

        total_length = sum(len(sentence) for sentence in sentences)
        avg_length = total_length / max(len(sentences), 1)
        diversity = len({sentence[:40] for sentence in sentences}) / max(len(sentences), 1)

        score = 0.6
        if avg_length > 120:
            score += 0.1
        if diversity > 0.7:
            score += 0.1
        if avg_length < 60:
            score -= 0.1

        return max(0.4, min(0.9, score))

    def calculate_structural_score(self, chunk_text: str, structure_info: Dict[str, Any]) -> float:
        score = 0.4
        lines = chunk_text.split('\n')
        first_line = lines[0].strip() if lines else ""
        last_line = lines[-1].strip() if lines else ""

        if first_line.startswith('#'):
            score += 0.3
        heading_count = sum(1 for line in lines if line.strip().startswith('#'))
        if heading_count > 0:
            score += 0.2
        if any(line.strip().startswith(('-', '*', '+')) for line in lines):
            score += 0.1
        if not (
            last_line.endswith('.')
            or last_line.endswith('!')
            or last_line.endswith('?')
            or last_line.startswith('#')
        ):
            score -= 0.2
        return max(0.0, min(1.0, score))

    def calculate_retrieval_quality(self, chunk_text: str) -> float:
        words = chunk_text.split()
        total_words = len(words)
        unique_words = len({word.lower() for word in words})
        word_diversity = unique_words / max(total_words, 1)

        technical_terms = any(term in chunk_text.lower() for term in [
            'algorithm', 'method', 'process', 'system', 'function', 'model',
            'implementation', 'optimization', 'performance', 'configuration',
        ])
        actionable = any(trigger in chunk_text.lower() for trigger in [
            'how to', 'steps', 'example', 'tutorial', 'guide', 'best practice',
        ])

        token_count = len(self._encode_tokens(chunk_text))
        length_score = 1.0 if 500 <= token_count <= 1500 else max(
            0.3,
            1.0 - abs(token_count - 1000) / 1000,
        )

        quality = (
            word_diversity * 0.3
            + (0.2 if technical_terms else 0.0)
            + (0.2 if actionable else 0.0)
            + length_score * 0.3
        )
        return min(1.0, quality)

    # ------------------------------------------------------------------
    # Chunk generation
    # ------------------------------------------------------------------
    def create_hierarchical_chunks(
        self,
        text: str,
        filename: str,
        strategy_name: str = "hierarchical_balanced",
    ) -> List[Dict[str, Any]]:
        structure = self.detect_document_structure(text)
        document_id = self._compute_document_id(filename)
        source_path = str(Path(filename))
        relative_path = self._make_relative_path(filename)
        document_name = Path(filename).stem

        chunks: List[Dict[str, Any]] = []
        chunk_index = 0
        strategy = self.chunking_strategies.get(strategy_name, self.chunking_strategies["hierarchical_balanced"])

        content_blocks = structure["content_blocks"]
        if not content_blocks and text.strip():
            stripped = text.strip()
            leading_trim = len(text) - len(text.lstrip())
            content_blocks = [{
                "heading": None,
                "content": stripped,
                "start_char": leading_trim,
                "end_char": leading_trim + len(stripped),
            }]

        for block in content_blocks:
            section_text = block.get("content", "")
            if not section_text:
                continue
            heading = block.get("heading")
            section_path = [heading["title"]] if heading else []
            block_start_char = block.get("start_char", 0)
            backend, content_type_hint, language_hint = self._select_chunking_backend(
                section_text,
                filename,
                block,
            )
            content_type = content_type_hint or "hierarchical_section"

            if backend == "semchunk":
                section_chunks = self._chunk_section_semchunk(
                    section_text,
                    section_path,
                    filename,
                    f"{strategy_name}_semchunk",
                    chunk_index,
                    document_id,
                    block_start_char,
                    content_type,
                    strategy["max_tokens"],
                    strategy["overlap"],
                )
            elif backend == "tree_sitter":
                section_chunks = self._chunk_section_tree_sitter(
                    section_text,
                    section_path,
                    filename,
                    strategy_name,
                    chunk_index,
                    document_id,
                    block_start_char,
                    content_type,
                    language_hint or "python",
                )
            else:
                section_chunks = self._chunk_section_structural(
                    section_text,
                    section_path,
                    filename,
                    strategy_name,
                    chunk_index,
                    document_id,
                    block_start_char,
                    content_type,
                )

            if not section_chunks:
                continue
            chunks.extend(section_chunks)
            chunk_index += len(section_chunks)

        accepted: List[Dict[str, Any]] = []
        fallback: List[Dict[str, Any]] = []

        for chunk in chunks:
            metadata: HierarchicalMetadata = chunk["metadata"]
            semantic_score = self.calculate_semantic_coherence(chunk["text"])
            structural_score = self.calculate_structural_score(chunk["text"], structure)
            retrieval_quality = self.calculate_retrieval_quality(chunk["text"])

            metadata.semantic_score = float(semantic_score)
            metadata.structural_score = float(structural_score)
            metadata.retrieval_quality = float(retrieval_quality)

            metadata_dict = asdict(metadata)
            metadata_dict.setdefault("content_type", "hierarchical_section")
            metadata_dict["document_id"] = document_id
            metadata_dict["document_name"] = document_name
            metadata_dict["source_path"] = source_path
            metadata_dict["source_filename"] = Path(filename).name
            metadata_dict["source_directory"] = str(Path(source_path).parent)
            metadata_dict["relative_path"] = relative_path
            metadata_dict["hierarchy_path"] = metadata_dict.get("hierarchy_path") or self._format_section_path(
                metadata_dict.get("section_path", [])
            )
            metadata_dict["chunk_hash"] = self._compute_chunk_hash(chunk["text"])
            metadata_dict["content_digest"] = metadata_dict["chunk_hash"]
            metadata_dict["chunk_length"] = len(chunk["text"])
            metadata_dict["payload_version"] = "1.3"
            metadata_dict["collection_hints"] = self._collection_hints(metadata_dict.get("content_type", ""))
            metadata_dict.setdefault("embedding_model", self.embedding_model_name)
            metadata_dict.setdefault("embedding_dimension", self.embedding_dimension)

            sparse_features = self._compute_sparse_features(chunk["text"])
            metadata_dict["sparse_features"] = sparse_features

            modal_info = self._detect_modal_hints(chunk["text"])
            metadata_dict["modal_hint"] = modal_info.pop("modal_hint")
            metadata_dict["content_flags"] = modal_info

            keywords = {kw for kw in metadata_dict.get("section_path", []) if isinstance(kw, str)}
            if metadata_dict.get("heading_text"):
                keywords.add(metadata_dict["heading_text"])
            keywords.update(sparse_features.get("top_terms", [])[:10])
            metadata_dict["search_keywords"] = sorted(k.strip() for k in keywords if k and k.strip())

            advanced_scores = {
                "semantic": float(semantic_score),
                "structural": float(structural_score),
                "retrieval_quality": float(retrieval_quality),
                "overall": float((semantic_score + structural_score + retrieval_quality) / 3),
            }

            chunk["metadata"] = metadata_dict
            chunk["advanced_scores"] = advanced_scores

            if (
                semantic_score >= self.quality_thresholds["min_semantic_score"]
                and structural_score >= self.quality_thresholds["min_structural_score"]
                and retrieval_quality >= self.quality_thresholds["min_retrieval_quality"]
            ):
                accepted.append(chunk)
            else:
                fallback.append(chunk)

        if not accepted and fallback:
            fallback.sort(key=lambda c: c["advanced_scores"]["overall"], reverse=True)
            limit = max(
                1,
                min(
                    self.fallback_promotion_cap,
                    int(len(fallback) * self.fallback_promotion_ratio),
                ),
            )
            promoted = fallback[:limit]
            for chunk in promoted:
                chunk["metadata"]["quality_fallback"] = True
                chunk["metadata"]["quality_notes"] = "Promoted via relaxed thresholds"
            accepted.extend(promoted)
            logger.warning(
                "No chunks met all thresholds; promoted %d fallback chunks for %s",
                len(promoted),
                filename,
            )

        if accepted:
            semantic_avg = np.mean([c["advanced_scores"]["semantic"] for c in accepted])
            structural_avg = np.mean([c["advanced_scores"]["structural"] for c in accepted])
            retrieval_avg = np.mean([c["advanced_scores"]["retrieval_quality"] for c in accepted])
            logger.info(
                "Created %d chunks from %s (semantic=%.3f structural=%.3f retrieval=%.3f)",
                len(accepted),
                filename,
                semantic_avg,
                structural_avg,
                retrieval_avg,
            )
        else:
            logger.warning("No viable chunks produced for %s", filename)

        return accepted


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    chunker = EnhancedUltimateChunkerV3()
    print("Available strategies:", list(chunker.chunking_strategies.keys()))
    print("Quality thresholds:", chunker.quality_thresholds)

