#!/usr/bin/env python3#!/usr/bin/env python3#!/usr/bin/env python3

"""Placeholder."""

"""Research-aligned hierarchical chunker with sparse metadata enrichment.""""""

🚀 ULTIMATE CHUNKER IMPROVEMENT PLAN

from __future__ import annotations===================================



import jsonBased on research from our 9,654-vector knowledge base across:

import logging- Docling: Document structure preservation and hybrid chunking

import re- Qdrant: Performance optimization and retrieval quality  

from collections import Counter, defaultdict- SentenceTransformers: Embedding quality and optimization

from dataclasses import dataclass, asdict, field

from datetime import datetimeKEY INSIGHTS FROM RESEARCH:

from pathlib import Path===========================

from typing import Any, Dict, List, Optional, Tuple

import hashlib1. **HIERARCHICAL CHUNKING** (Score: 0.598 - Docling)

   - Chunks based on document structure (sections, paragraphs, tables)

import numpy as np   - Preserve document hierarchy for better context

import tiktoken   - Implementation: HierarchicalChunker with sibling element merging

from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity2. **HYBRID CHUNKING** (Score: 0.506 - Docling)

   - Combine structural and text-based chunking approaches

logger = logging.getLogger(__name__)   - Leverage both semantic and structural boundaries

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")   - Reference: examples/hybrid_chunking.ipynb



3. **OPTIMAL CHUNK SIZES** (Score: 0.549 - Docling)

@dataclass   - Large chunks (1024-2048 tokens): Better context, may lose precision

class HierarchicalMetadata:   - Small overlap (50-100 tokens): Balance between speed and concept preservation

    """Lightweight metadata container used during chunk construction."""   - Risk analysis: No overlap = fast but splits concepts



    chunk_id: str4. **EMBEDDING OPTIMIZATION** (Score: 0.546 - Qdrant)

    source_file: str   - Focus on retrieval quality and vector search performance

    filename: str   - Use consistent embedding models for indexing and search

    file_extension: str   - Implement proper quality metrics and filtering

    chunk_index: int

    document_level: intIMPLEMENTATION STRATEGY:

    parent_chunk_id: Optional[str]========================

    child_chunk_ids: List[str] = field(default_factory=list)

    section_path: List[str] = field(default_factory=list)Phase 1: Enhanced Hierarchical Processing

    heading_text: str = ""                "min_section_tokens": 300,

    token_count: int = 0                "description": "Maximum context with structural awareness"

    char_count: int = 0            },

    start_char: int = 0            "hybrid_adaptive": {

    end_char: int = 0                "max_tokens": 1024,

    semantic_score: float = 0.0                "overlap": 150,      # Hybrid chunking benefit

    structural_score: float = 0.0                "preserve_structure": True,

    retrieval_quality: float = 0.0                "semantic_boundaries": True,

    chunking_strategy: str = "hierarchical_balanced"                "min_section_tokens": 150,

    content_type: str = "hierarchical_section"                "description": "Hybrid structural + semantic approach (Docling research)"

    embedding_model: str = ""            },

    processing_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())            "mcp_optimized": {

                "max_tokens": 768,   # Optimized for MCP protocol docs

                """

class EnhancedUltimateChunkerV3:                Enhanced Ultimate Chunker roadmap derived from multi-domain research insights.

    """Hierarchical chunker used across the knowledge pipeline."""

                Key focus areas:

    def __init__(                - Hierarchical chunking that preserves document structure (Docling insights)

        self,                - Hybrid chunking that blends structural and semantic boundaries

        embedding_model: str = "nomic-ai/CodeRankEmbed",                - Tuned chunk sizes and overlaps for retrieval quality and speed

        tokenizer_name: str = "cl100k_base"                - Consistent embedding alignment with downstream Qdrant ingestion

    ) -> None:

        self.embedding_model_name = embedding_model                Implementation phases:

        self.embedder = SentenceTransformer(embedding_model, trust_remote_code=True)                - Phase 1: Enhanced hierarchical processing and metadata enrichment

        self.tokenizer = tiktoken.get_encoding(tokenizer_name)                - Phase 2: Hybrid semantic + structural chunking strategies

        self.project_root = Path.cwd()                - Phase 3: Quality-scoring and retrieval optimisation thresholds

                - Phase 4: Production scaling, batching, and memory management

        self.content_type_patterns: Dict[str, Dict[str, Any]] = {                """

            "mcp_repository": {            "has_lists": bool(re.search(r'^\s*[-*+•]\s', text, re.MULTILINE)),

                "patterns": ["mcp", "protocol", "tool", "client", "server"],            "has_tables": '|' in text and re.search(r'\|.*\|', text),

                "strategy": "hybrid_adaptive",            "line_count": text.count('\n'),

                "description": "Model Context Protocol repositories"            "avg_line_length": len(text) / max(1, text.count('\n')),

            },            "sections": len(re.findall(r'^#{1,6}\s.*$', text, re.MULTILINE)),

            "workflow_documentation": {            "paragraphs": len(re.findall(r'\n\s*\n', text)) + 1

                "patterns": ["workflow", "pipeline", "step", "process", "action"],        }

                "strategy": "hierarchical_balanced",        

                "description": "Workflow and procedural documentation"        # Detect markdown headings

            },        heading_matches = re.finditer(r'^(#{1,6})\s+(.+)$', text, re.MULTILINE)

            "api_documentation": {        for match in heading_matches:

                "patterns": ["api", "endpoint", "request", "response", "parameter"],            level = len(match.group(1))

                "strategy": "hierarchical_precise",            title = match.group(2).strip()

                "description": "Reference-style API documentation"            position = match.start()

            },            

            "programming_documentation": {            heading_info = {

                "patterns": ["python", "javascript", "typescript", "class", "function"],                "level": level,

                "strategy": "hybrid_adaptive",                "title": title,

                "description": "Language or library reference material"                "position": position,

            },                "line": text[:position].count('\n') + 1

            "platform_documentation": {            }

                "patterns": ["deployment", "kubernetes", "infrastructure", "platform"],            structure["headings"].append(heading_info)

                "strategy": "hierarchical_context",        

                "description": "Platform and infrastructure documentation"        # Build hierarchy structure

            }        for heading in structure["headings"]:

        }            level = heading["level"]

            if level not in structure["hierarchy"]:

        self.chunking_strategies: Dict[str, Dict[str, Any]] = {                structure["hierarchy"][level] = []

            "hierarchical_precise": {            

                "max_tokens": 512,            # Create section info with expected fields

                "overlap": 80,            section_info = {

                "min_section_tokens": 120,                "title": heading["title"],

                "description": "High precision with tighter chunks"                "start_line": heading["line"] - 1,  # Convert to 0-based indexing

            },                "path": f"Level{level}_{heading['title'].replace(' ', '_')}",

            "hierarchical_balanced": {                "level": level,

                "max_tokens": 1024,                "position": heading["position"]

                "overlap": 100,            }

                "min_section_tokens": 180,            structure["hierarchy"][level].append(section_info)

                "description": "Balanced chunks tuned for workflow docs"        

            },        # Split into content blocks based on headings

            "hierarchical_context": {        if structure["headings"]:

                "max_tokens": 2048,            for i, heading in enumerate(structure["headings"]):

                "overlap": 160,                start_pos = heading["position"]

                "min_section_tokens": 260,                end_pos = structure["headings"][i + 1]["position"] if i + 1 < len(structure["headings"]) else len(text)

                "description": "Maximum context retention"                

            },                content = text[start_pos:end_pos].strip()

            "hybrid_adaptive": {                if content:

                "max_tokens": 1024,                    structure["content_blocks"].append({

                "overlap": 120,                        "heading": heading,

                "min_section_tokens": 160,                        "content": content,

                "description": "Hybrid structural + semantic approach"                        "length": len(content),

            },                        "start_line": heading["line"],

            "mcp_optimized": {                        "end_line": text[:end_pos].count('\n') + 1

                "max_tokens": 768,                    })

                "overlap": 96,        else:

                "min_section_tokens": 140,            # No headings, treat as single content block

                "description": "Optimised for MCP repositories"            structure["content_blocks"].append({

            },                "heading": None,

            "performance_optimized": {                "content": text,

                "max_tokens": 1536,                "length": len(text),

                "overlap": 128,                "start_line": 1,

                "min_section_tokens": 220,                "end_line": text.count('\n') + 1

                "description": "Performance focused large chunking"            })

            }        

        }        # Determine document complexity

        complexity_score = 0

        self.quality_thresholds = {        if structure["has_headers"]: complexity_score += 2

            "min_semantic_score": 0.65,        if structure["has_code_blocks"]: complexity_score += 2

            "min_structural_score": 0.70,        if structure["has_lists"]: complexity_score += 1

            "min_retrieval_quality": 0.60,        if structure["has_tables"]: complexity_score += 1

            "min_information_density": 0.4,        if structure["sections"] > 5: complexity_score += 1

        }        

        structure["complexity"] = "high" if complexity_score > 4 else "medium" if complexity_score > 2 else "low"

        self.default_collection_hints: Dict[str, List[str]] = {        

            "mcp_repository": ["qdrant_ecosystem"],        return structure

            "workflow_documentation": ["docling"],

            "api_documentation": ["fast_docs"],    def _collection_hints(self, content_type: str) -> List[str]:

            "programming_documentation": ["sentence_transformers"],        """Return recommended Qdrant collections for a given content type."""

            "platform_documentation": ["qdrant_ecosystem"],

            "hierarchical_section": ["qdrant_ecosystem"],        return self.default_collection_hints.get(content_type, ["qdrant_ecosystem"])

        }

    def _compute_document_id(self, filename: str) -> str:

        logger.info("Enhanced Ultimate Chunker v3 initialised with %s", embedding_model)        """Stable document identifier derived from file path."""



    # ------------------------------------------------------------------        normalized = Path(filename).as_posix().lower()

    # Helper utilities        return hashlib.md5(normalized.encode("utf-8")).hexdigest()[:12]

    # ------------------------------------------------------------------

    def _collection_hints(self, content_type: str) -> List[str]:    def _make_relative_path(self, filename: str) -> str:

        return self.default_collection_hints.get(content_type, ["qdrant_ecosystem"])        """Return project-relative path when possible."""



    @staticmethod        try:

    def _compute_document_id(filename: str) -> str:            return str(Path(filename).resolve().relative_to(self.project_root))

        normalized = Path(filename).as_posix().lower()        except ValueError:

        return hashlib.md5(normalized.encode("utf-8")).hexdigest()[:12]            return str(Path(filename))



    def _make_relative_path(self, filename: str) -> str:    @staticmethod

        try:    def _compute_chunk_hash(text: str) -> str:

            return str(Path(filename).resolve().relative_to(self.project_root))        """Lightweight content hash for change detection."""

        except ValueError:

            return str(Path(filename))        return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]



    @staticmethod    @staticmethod

    def _compute_chunk_hash(text: str) -> str:    def _format_section_path(section_path: List[str]) -> str:

        return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]        """Format hierarchical section path for display."""



    @staticmethod        if not section_path:

    def _format_section_path(section_path: List[str]) -> str:            return ""

        return " > ".join(part.strip() for part in section_path if isinstance(part, str) and part.strip())        return " > ".join(part.strip() for part in section_path if isinstance(part, str) and part.strip())



    @staticmethod    @staticmethod

    def _compute_sparse_features(text: str, top_n: int = 20) -> Dict[str, Any]:    def _compute_sparse_features(text: str, top_n: int = 20) -> Dict[str, Any]:

        word_pattern = re.compile(r"[a-zA-Z0-9]{3,}")        """Compute sparse-friendly keyword statistics for downstream pipelines."""

        tokens = word_pattern.findall(text.lower())

        total_terms = len(tokens)        word_pattern = re.compile(r"[a-zA-Z0-9]{3,}")

        tokens = word_pattern.findall(text.lower())

        if total_terms == 0:        total_terms = len(tokens)

            return {

                "version": "1.0",        if total_terms == 0:

                "weighting": "tf-normalized",            return {

                "top_terms": [],                "version": "1.0",

                "term_weights": [],                "weighting": "tf-normalized",

                "unique_terms": 0,                "top_terms": [],

                "total_terms": 0,                "term_weights": [],

            }                "unique_terms": 0,

                "total_terms": 0

        frequency = Counter(tokens)            }

        most_common = frequency.most_common(top_n)

        term_weights = []        frequency = Counter(tokens)

        most_common = frequency.most_common(top_n)

        for term, count in most_common:        term_weights = []

            weight = count / total_terms

            term_weights.append({        for term, count in most_common:

                "term": term,            weight = count / total_terms

                "tf": int(count),            term_weights.append({

                "weight": float(round(weight, 6)),                "term": term,

            })                "tf": int(count),

                "weight": float(round(weight, 6))

        return {            })

            "version": "1.0",

            "weighting": "tf-normalized",        return {

            "top_terms": [term for term, _ in most_common],            "version": "1.0",

            "term_weights": term_weights,            "weighting": "tf-normalized",

            "unique_terms": len(frequency),            "top_terms": [term for term, _ in most_common],

            "total_terms": total_terms,            "term_weights": term_weights,

        }            "unique_terms": len(frequency),

            "total_terms": total_terms

    @staticmethod        }

    def _detect_modal_hints(text: str) -> Dict[str, Any]:

        has_code_block = "```" in text or bool(re.search(r"\b(def|class|function)\b", text))    @staticmethod

        has_table = bool(re.search(r"\n\|[^|]+\|", text))    def _detect_modal_hints(text: str) -> Dict[str, Any]:

        has_list = bool(re.search(r"^\s*[-*+]\s", text, re.MULTILINE))        """Detect simple modality hints (code/table/list/etc.) for downstream routing."""

        has_json = text.strip().startswith("{") or text.strip().startswith("[")

        has_formula = bool(re.search(r"\$[^$]+\$", text))        has_code_block = "```" in text or bool(re.search(r"\b(def|class|function)\b", text))

        has_table = bool(re.search(r"\n\|[^|]+\|", text))

        modal_hint = "prose"        has_list = bool(re.search(r"^\s*[-*+]\s", text, re.MULTILINE))

        if has_table:        has_json = text.strip().startswith("{") or text.strip().startswith("[")

            modal_hint = "table"        has_formula = bool(re.search(r"\$[^$]+\$", text))

        elif has_code_block:

            modal_hint = "code"        modal_hint = "prose"

        elif has_list:        if has_table:

            modal_hint = "list"            modal_hint = "table"

        elif has_json:        elif has_code_block:

            modal_hint = "json"            modal_hint = "code"

        elif has_list:

        return {            modal_hint = "list"

            "modal_hint": modal_hint,        elif has_json:

            "has_code_block": has_code_block,            modal_hint = "json"

            "has_table": has_table,

            "has_list": has_list,        return {

            "has_json": has_json,            "modal_hint": modal_hint,

            "has_formula": has_formula,            "has_code_block": has_code_block,

        }            "has_table": has_table,

            "has_list": has_list,

    # ------------------------------------------------------------------            "has_json": has_json,

    # Content type detection            "has_formula": has_formula

    # ------------------------------------------------------------------        }

    def auto_detect_content_type(self, text: str, filename: str) -> Tuple[str, str]:

        text_lower = text.lower()    def auto_detect_content_type(self, text: str, filename: str) -> Tuple[str, str]:

        filename_lower = filename.lower()        """

        Auto-detect content type based on user's specific input categories

        best_type = "workflow_documentation"        

        best_score = -1        Returns: (content_type, recommended_strategy)

        """

        for content_type, config in self.content_type_patterns.items():        

            score = 0        text_lower = text.lower()

            for pattern in config["patterns"]:        filename_lower = filename.lower()

                score += text_lower.count(pattern)        

                if pattern in filename_lower:        # Score each content type

                    score += 3        scores = {}

            if score > best_score:        for content_type, config in self.content_type_patterns.items():

                best_score = score            score = 0

                best_type = content_type            

            # Check patterns in text content

        strategy = self.content_type_patterns[best_type]["strategy"]            for pattern in config["patterns"]:

        logger.info("Auto-detected %s using %s strategy", best_type, strategy)                score += text_lower.count(pattern) * 2

        return best_type, strategy                if pattern in filename_lower:

                    score += 5  # Filename match is stronger indicator

    # ------------------------------------------------------------------            

    # Public processing APIs            scores[content_type] = score

    # ------------------------------------------------------------------        

    def process_file_smart(        # Find best match

        self,        if scores:

        file_path: str,            best_type = max(scores.items(), key=lambda x: x[1])

        output_dir: Optional[str] = None,            if best_type[1] > 3:  # Minimum threshold

        auto_detect: bool = True,                content_type = best_type[0]

        strategy_override: Optional[str] = None,                strategy = self.content_type_patterns[content_type]["strategy"]

    ) -> List[Dict[str, Any]]:                logger.info(f"🎯 Auto-detected: {content_type} -> {strategy} strategy")

        file_path_obj = Path(file_path)                return content_type, strategy

        try:        

            text = file_path_obj.read_text(encoding="utf-8")        # Default fallback

        except UnicodeDecodeError:        logger.info("📄 Using default: workflow_documentation -> hierarchical_balanced")

            text = file_path_obj.read_text(encoding="utf-8", errors="ignore")        return "workflow_documentation", "hierarchical_balanced"

    

        if not text.strip():    def process_file_smart(

            logger.warning("Skipping empty file %s", file_path)        self,

            return []        file_path: str,

        output_dir: Optional[str] = None,

        if auto_detect:        auto_detect: bool = True,

            content_type, strategy = self.auto_detect_content_type(text, file_path_obj.name)        strategy_override: Optional[str] = None

        else:    ) -> List[Dict[str, Any]]:

            content_type = "workflow_documentation"        """

            strategy = "hierarchical_balanced"        Smart file processing with auto-detection for user's input types

        

        if strategy_override:        Optimized for:

            strategy = strategy_override        - MCP Repositories

        - Workflow Documentation  

        chunks = self.create_hierarchical_chunks(        - API Documentation

            text=text,        - Programming Language Documentation

            filename=str(file_path_obj),        - Platform Documentation

            strategy_name=strategy,        """

        )        

        try:

        if not chunks:            logger.info(f"📋 Smart processing: {file_path}")

            logger.warning("No chunks generated for %s", file_path)            

            return []            # Read file content

            with open(file_path, 'r', encoding='utf-8') as f:

        if output_dir:                text = f.read()

            self._save_chunks(chunks, str(file_path_obj), output_dir, content_type)            

            if len(text.strip()) < 50:

        return chunks                logger.warning(f"⚠️ File too small: {file_path}")

                return []

    def process_directory_smart(            

        self,            # Auto-detect content type and strategy

        input_dir: str,            if auto_detect and not strategy_override:

        output_dir: str,                content_type, strategy_name = self.auto_detect_content_type(text, file_path)

        file_extensions: Optional[List[str]] = None,            else:

    ) -> Dict[str, Any]:                content_type = "general"

        extensions = file_extensions or [".md", ".txt", ".rst", ".py", ".json"]                strategy_name = strategy_override or "hierarchical_balanced"

        input_path = Path(input_dir)            

        output_path = Path(output_dir)            logger.info(f"🎯 Processing as {content_type} with {strategy_name} strategy")

        output_path.mkdir(parents=True, exist_ok=True)            

            # Create hierarchical chunks with detected strategy

        files: List[Path] = []            chunks = self.create_hierarchical_chunks(

        for ext in extensions:                text=text,

            files.extend(input_path.rglob(f"*{ext}"))                filename=file_path,

        files = sorted(files)                strategy_name=strategy_name,

                preserve_parent_context=True

        logger.info("Found %d files to process in %s", len(files), input_dir)            )

            

        summary = {            # Add content type to metadata

            "processed_files": 0,            for chunk in chunks:

            "total_chunks": 0,                collection_hints = self._collection_hints(content_type)

            "processing_time": 0.0,                chunk["metadata"]["content_type"] = content_type

            "content_types": defaultdict(int),                chunk["metadata"]["auto_detected"] = auto_detect

            "strategies_used": defaultdict(int),                chunk["metadata"]["collection_hints"] = collection_hints

            "files": [],                chunk["metadata"]["qdrant_collection_hint"] = collection_hints

        }                if not chunk["metadata"].get("hierarchy_path"):

                    chunk["metadata"]["hierarchy_path"] = self._format_section_path(chunk["metadata"].get("section_path", []))

        start_time = datetime.now()            

            # Save results if output directory specified

        for file_path in files:            if output_dir:

            chunks = self.process_file_smart(str(file_path), output_dir=str(output_path))                self._save_chunks(chunks, file_path, output_dir, content_type)

            if not chunks:            

                continue            return chunks

            

            summary["processed_files"] += 1        except Exception as e:

            summary["total_chunks"] += len(chunks)            logger.error(f"❌ Error in smart processing {file_path}: {e}")

            return []

            metadata = chunks[0]["metadata"]    

            content_type = metadata.get("content_type", "hierarchical_section")    def _save_chunks(self, chunks: List[Dict[str, Any]], file_path: str, output_dir: str, content_type: str):

            strategy = metadata.get("chunking_strategy", "hierarchical_balanced")        """Save chunks with enhanced metadata"""

        

            summary["content_types"][content_type] += 1        output_path = Path(output_dir)

            summary["strategies_used"][strategy] += 1        output_path.mkdir(exist_ok=True)

            summary["files"].append({        

                "file": str(file_path),        filename = Path(file_path).stem

                "chunks": len(chunks),        output_file = output_path / f"{filename}_{content_type}_chunks.json"

                "content_type": content_type,        

                "strategy": strategy,        # Convert any numpy types to Python types for JSON serialization

            })        for chunk in chunks:

            for key, value in chunk.get("advanced_scores", {}).items():

        summary["processing_time"] = (datetime.now() - start_time).total_seconds()                if hasattr(value, 'item'):  # numpy type

                    chunk["advanced_scores"][key] = float(value)

        summary_path = output_path / "chunk_summary.json"        

        serialisable_summary = {        with open(output_file, 'w', encoding='utf-8') as f:

            **summary,            json.dump(chunks, f, indent=2, ensure_ascii=False)

            "content_types": dict(summary["content_types"]),        

            "strategies_used": dict(summary["strategies_used"]),        logger.info(f"💾 Saved {len(chunks)} chunks to {output_file}")

        }

        summary_path.write_text(json.dumps(serialisable_summary, indent=2), encoding="utf-8")    def process_directory_smart(

        logger.info("Wrote directory summary to %s", summary_path)        self, 

        input_dir: str, 

        return serialisable_summary        output_dir: str,

        file_extensions: List[str] = ['.md', '.txt', '.rst', '.py', '.js', '.ts', '.json']

    def _save_chunks(    ) -> Dict[str, Any]:

        self,        """

        chunks: List[Dict[str, Any]],        Process entire directory with smart content detection

        file_path: str,        

        output_dir: str,        Optimized for your input types:

        content_type: str,        - MCP Repositories

    ) -> None:        - Workflow Documentation

        output_path = Path(output_dir)        - API Documentation  

        output_path.mkdir(parents=True, exist_ok=True)        - Programming Language Documentation

        - Platform Documentation

        filename = Path(file_path).stem        """

        target = output_path / f"{filename}_{content_type}_chunks.json"        

        input_path = Path(input_dir)

        def _normalise_scores(chunk: Dict[str, Any]) -> None:        results = {

            scores = chunk.get("advanced_scores", {})            "processed_files": 0,

            for key, value in list(scores.items()):            "total_chunks": 0,

                if hasattr(value, "item"):            "content_types": defaultdict(int),

                    scores[key] = float(value)            "strategies_used": defaultdict(int),

            "processing_time": 0,

        for chunk in chunks:            "files": []

            _normalise_scores(chunk)        }

        

        target.write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")        start_time = datetime.now()

        logger.info("Saved %d chunks to %s", len(chunks), target)        

        # Find all relevant files

    # ------------------------------------------------------------------        files = []

    # Structure analysis helpers        for ext in file_extensions:

    # ------------------------------------------------------------------            files.extend(input_path.rglob(f"*{ext}"))

    def detect_document_structure(self, text: str) -> Dict[str, Any]:        

        structure: Dict[str, Any] = {        logger.info(f"🔍 Found {len(files)} files to process")

            "headings": [],        

            "content_blocks": [],        for file_path in files:

            "hierarchy": defaultdict(list),            try:

            "has_headers": bool(re.search(r"^#{1,6}\s", text, re.MULTILINE)),                chunks = self.process_file_smart(

            "has_code_blocks": "```" in text,                    str(file_path),

            "has_lists": bool(re.search(r"^\s*[-*+•]\s", text, re.MULTILINE)),                    output_dir=output_dir,

            "has_tables": "|" in text and bool(re.search(r"\|.*\|", text)),                    auto_detect=True

            "line_count": text.count("\n"),                )

            "avg_line_length": len(text) / max(1, text.count("\n")),                

            "sections": len(re.findall(r"^#{1,6}\s.*$", text, re.MULTILINE)),                if chunks:

            "paragraphs": len(re.findall(r"\n\s*\n", text)) + 1,                    # Update statistics

        }                    results["processed_files"] += 1

                    results["total_chunks"] += len(chunks)

        for match in re.finditer(r"^(#{1,6})\s+(.+)$", text, re.MULTILINE):                    

            level = len(match.group(1))                    content_type = chunks[0]["metadata"]["content_type"]

            title = match.group(2).strip()                    strategy = chunks[0]["metadata"]["chunking_strategy"]

            line_number = text[: match.start()].count("\n") + 1                    

            structure["headings"].append({                    results["content_types"][content_type] += 1

                "level": level,                    results["strategies_used"][strategy] += 1

                "title": title,                    

                "start_line": line_number,                    results["files"].append({

            })                        "file": str(file_path),

            structure["hierarchy"][level].append({                        "chunks": len(chunks),

                "title": title,                        "content_type": content_type,

                "start_line": line_number - 1,                        "strategy": strategy

                "path": [title],                    })

                "level": level,                    

            })                    logger.info(f"✅ {file_path.name}: {len(chunks)} chunks ({content_type})")

                

        if not structure["headings"]:            except Exception as e:

            structure["content_blocks"].append({                logger.error(f"❌ Failed to process {file_path}: {e}")

                "heading": None,        

                "content": text,        # Calculate processing time

                "length": len(text),        results["processing_time"] = (datetime.now() - start_time).total_seconds()

                "start_line": 1,        

                "end_line": text.count("\n") + 1,        # Save summary

            })        summary_file = Path(output_dir) / "smart_processing_summary.json"

        else:        with open(summary_file, 'w', encoding='utf-8') as f:

            lines = text.split("\n")            json.dump(results, f, indent=2, ensure_ascii=False)

            for idx, heading in enumerate(structure["headings"]):        

                start = heading["start_line"] - 1        logger.info(f"🎯 Smart processing complete!")

                end = (        logger.info(f"📊 Processed {results['processed_files']} files → {results['total_chunks']} chunks")

                    structure["headings"][idx + 1]["start_line"] - 1        logger.info(f"⏱️ Time: {results['processing_time']:.2f} seconds")

                    if idx + 1 < len(structure["headings"])        logger.info(f"📋 Content types: {dict(results['content_types'])}")

                    else len(lines)        

                )        return results

                section_text = "\n".join(lines[start:end]).strip()        """

                if not section_text:        Advanced document structure detection

                    continue        

                structure["content_blocks"].append({        Based on Docling research: Hierarchical structure preservation

                    "heading": heading,        """

                    "content": section_text,        

                    "length": len(section_text),        lines = text.split('\n')

                    "start_line": start + 1,        structure = {

                    "end_line": end,            "headings": [],

                })            "sections": [],

            "hierarchy": defaultdict(list),

        return structure            "content_blocks": []

        }

    def _split_into_sentences(self, text: str) -> List[str]:        

        sentences: List[str] = []        current_section = None

        current = []        current_level = 0

        for line in text.split("\n"):        section_stack = []

            stripped = line.strip()        

            if stripped.startswith("```"):        for i, line in enumerate(lines):

                if current:            stripped = line.strip()

                    sentences.append(" ".join(current).strip())            

                    current = []            # Detect markdown headings

                sentences.append(line)            if stripped.startswith('#'):

                continue                level = len(stripped) - len(stripped.lstrip('#'))

            current.append(line)                heading_text = stripped.lstrip('#').strip()

            if stripped.endswith((".", "!", "?")):                

                sentences.append(" ".join(current).strip())                heading_info = {

                current = []                    "text": heading_text,

        if current:                    "level": level,

            sentences.append(" ".join(current).strip())                    "line_index": i,

        return [s for s in sentences if s.strip()]                    "char_position": len('\n'.join(lines[:i]))

                }

    def _chunk_section_content(                

        self,                structure["headings"].append(heading_info)

        section_text: str,                

        section_path: List[str],                # Update section stack for hierarchy

        filename: str,                while len(section_stack) >= level:

        strategy_name: str,                    section_stack.pop()

        start_chunk_index: int,                

        document_id: str,                section_stack.append(heading_text)

    ) -> List[Dict[str, Any]]:                structure["hierarchy"][level].append({

        strategy = self.chunking_strategies[strategy_name]                    "heading": heading_text,

        max_tokens = strategy["max_tokens"]                    "path": section_stack.copy(),

        overlap = strategy["overlap"]                    "start_line": i

                })

        chunks: List[Dict[str, Any]] = []                

        sentences = self._split_into_sentences(section_text)                current_level = level

        current_chunk = []                current_section = heading_text

        current_tokens = 0            

        start_char = 0            # Detect other structural elements

            elif stripped.startswith('```'):

        for sentence in sentences:                structure["content_blocks"].append({

            token_length = len(self.tokenizer.encode(sentence))                    "type": "code_block",

            if current_tokens + token_length <= max_tokens:                    "line_index": i,

                current_chunk.append(sentence)                    "section": current_section

                current_tokens += token_length                })

                continue            elif stripped.startswith('|') and '|' in stripped[1:]:

                structure["content_blocks"].append({

            if current_chunk:                    "type": "table",

                text = " ".join(current_chunk).strip()                    "line_index": i,

                metadata = HierarchicalMetadata(                    "section": current_section

                    chunk_id=f"{document_id}-{start_chunk_index + len(chunks):04d}",                })

                    source_file=filename,            elif stripped.startswith(('-', '*', '+')):

                    filename=Path(filename).name,                structure["content_blocks"].append({

                    file_extension=Path(filename).suffix,                    "type": "list_item", 

                    chunk_index=start_chunk_index + len(chunks),                    "line_index": i,

                    document_level=len(section_path),                    "section": current_section

                    parent_chunk_id=None,                })

                    section_path=section_path,        

                    heading_text=section_path[-1] if section_path else "",        return structure

                    token_count=current_tokens,    

                    char_count=len(text),    def calculate_structural_score(self, chunk_text: str, structure_info: Dict[str, Any]) -> float:

                    start_char=start_char,        """

                    end_char=start_char + len(text),        Calculate how well the chunk preserves document structure

                    chunking_strategy=strategy_name,        

                    embedding_model=self.embedding_model_name,        New metric based on Docling research insights

                )        """

                chunks.append({"text": text, "metadata": metadata})        

        score = 0.0

                overlap_tokens = self.tokenizer.decode(self.tokenizer.encode(text)[-overlap:]) if overlap else ""        

                current_chunk = [overlap_tokens] if overlap_tokens else []        # Check if chunk starts/ends at structural boundaries

                current_tokens = len(self.tokenizer.encode(overlap_tokens)) if overlap_tokens else 0        lines = chunk_text.split('\n')

                start_char += len(text)        first_line = lines[0].strip() if lines else ""

        last_line = lines[-1].strip() if lines else ""

            current_chunk.append(sentence)        

            current_tokens += token_length        # Bonus for starting with heading

        if first_line.startswith('#'):

        if current_chunk:            score += 0.3

            text = " ".join(current_chunk).strip()        

            metadata = HierarchicalMetadata(        # Bonus for complete sections

                chunk_id=f"{document_id}-{start_chunk_index + len(chunks):04d}",        heading_count = sum(1 for line in lines if line.strip().startswith('#'))

                source_file=filename,        if heading_count > 0:

                filename=Path(filename).name,            score += 0.2

                file_extension=Path(filename).suffix,        

                chunk_index=start_chunk_index + len(chunks),        # Bonus for preserving lists/tables

                document_level=len(section_path),        has_complete_list = any(line.strip().startswith(('-', '*', '+')) for line in lines)

                parent_chunk_id=None,        if has_complete_list:

                section_path=section_path,            score += 0.1

                heading_text=section_path[-1] if section_path else "",        

                token_count=len(self.tokenizer.encode(text)),        # Penalty for cutting mid-sentence (structural boundary respect)

                char_count=len(text),        if not (last_line.endswith('.') or last_line.endswith('!') or last_line.endswith('?') or last_line.startswith('#')):

                start_char=start_char,            score -= 0.2

                end_char=start_char + len(text),        

                chunking_strategy=strategy_name,        # Normalize score

                embedding_model=self.embedding_model_name,        return max(0.0, min(1.0, score + 0.4))  # Base score + bonuses

            )    

            chunks.append({"text": text, "metadata": metadata})    def calculate_retrieval_quality(self, chunk_text: str) -> float:

        """

        return chunks        Predict retrieval quality based on Qdrant research insights

        

    # ------------------------------------------------------------------        Factors: content density, semantic coherence, searchable terms

    # Quality calculations        """

    # ------------------------------------------------------------------        

    def calculate_semantic_coherence(self, text: str) -> float:        # Content richness factors

        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 10]        unique_words = len(set(chunk_text.lower().split()))

        if len(sentences) < 2:        total_words = len(chunk_text.split())

            return 0.8        word_diversity = unique_words / max(total_words, 1) if total_words > 0 else 0

        try:        

            embeddings = self.embedder.encode(sentences[:5])        # Searchable content indicators

            similarities: List[float] = []        has_technical_terms = any(term in chunk_text.lower() for term in [

            for i in range(len(embeddings)):            'algorithm', 'method', 'process', 'system', 'function', 'model', 

                for j in range(i + 1, len(embeddings)):            'implementation', 'optimization', 'performance', 'configuration'

                    sim = cosine_similarity(        ])

                        np.array([embeddings[i]]),        

                        np.array([embeddings[j]]),        # Question-answer potential

                    )[0][0]        has_actionable_content = any(indicator in chunk_text.lower() for indicator in [

                    similarities.append(sim)            'how to', 'steps', 'example', 'tutorial', 'guide', 'best practice'

            return float(np.mean(similarities)) if similarities else 0.5        ])

        except Exception as exc:  # pragma: no cover - defensive        

            logger.warning("Semantic coherence calculation failed: %s", exc)        # Length optimization (based on research: 1024-2048 tokens optimal)

            return 0.5        token_count = len(self.tokenizer.encode(chunk_text))

        length_score = 1.0 if 500 <= token_count <= 1500 else max(0.3, 1.0 - abs(token_count - 1000) / 1000)

    def calculate_structural_score(self, chunk_text: str, structure_info: Dict[str, Any]) -> float:        

        score = 0.4        # Combined retrieval quality score

        lines = chunk_text.split('\n')        quality = (

        first_line = lines[0].strip() if lines else ""            word_diversity * 0.3 +

        last_line = lines[-1].strip() if lines else ""            (0.2 if has_technical_terms else 0) +

            (0.2 if has_actionable_content else 0) +

        if first_line.startswith('#'):            length_score * 0.3

            score += 0.3        )

        heading_count = sum(1 for line in lines if line.strip().startswith('#'))        

        if heading_count > 0:        return min(1.0, quality)

            score += 0.2    

        if any(line.strip().startswith(('-', '*', '+')) for line in lines):    def create_hierarchical_chunks(

            score += 0.1        self,

        if not (        text: str,

            last_line.endswith('.')        filename: str,

            or last_line.endswith('!')        strategy_name: str = "hierarchical_balanced",

            or last_line.endswith('?')        preserve_parent_context: bool = True

            or last_line.startswith('#')    ) -> List[Dict[str, Any]]:

        ):        """

            score -= 0.2        Create hierarchical chunks with advanced structure preservation

        return max(0.0, min(1.0, score))        

        Implementation of Docling + Qdrant + SentenceTransformers research

    def calculate_retrieval_quality(self, chunk_text: str) -> float:        """

        words = chunk_text.split()        

        total_words = len(words)        strategy = self.chunking_strategies[strategy_name]

        unique_words = len(set(word.lower() for word in words))        max_tokens = strategy["max_tokens"]

        word_diversity = unique_words / max(total_words, 1)        overlap = strategy["overlap"]

        

        technical_terms = any(term in chunk_text.lower() for term in [        # Step 1: Analyze document structure

            'algorithm', 'method', 'process', 'system', 'function', 'model',        structure = self.detect_document_structure(text)

            'implementation', 'optimization', 'performance', 'configuration',        logger.info(f"📊 Detected {len(structure['headings'])} headings, {len(structure['content_blocks'])} content blocks")

        ])        

        actionable = any(trigger in chunk_text.lower() for trigger in [        document_id = self._compute_document_id(filename)

            'how to', 'steps', 'example', 'tutorial', 'guide', 'best practice',        source_path = str(Path(filename))

        ])        relative_path = self._make_relative_path(filename)

        document_name = Path(filename).stem

        token_count = len(self.tokenizer.encode(chunk_text))

        length_score = 1.0 if 500 <= token_count <= 1500 else max(        chunks = []

            0.3,        chunk_index = 0

            1.0 - abs(token_count - 1000) / 1000,        

        )        # Step 2: Process by hierarchical sections

        for level, sections in structure["hierarchy"].items():

        quality = (            for section_info in sections:

            word_diversity * 0.3                section_start = section_info["start_line"]

            + (0.2 if technical_terms else 0.0)                section_path = section_info["path"]

            + (0.2 if actionable else 0.0)                

            + length_score * 0.3                # Find section content boundaries

        )                lines = text.split('\n')

        return min(1.0, quality)                section_lines = []

                

    # ------------------------------------------------------------------                # Collect lines until next same-level heading

    # Chunk generation                for i in range(section_start, len(lines)):

    # ------------------------------------------------------------------                    line = lines[i].strip()

    def create_hierarchical_chunks(                    

        self,                    # Stop at same or higher level heading

        text: str,                    if (line.startswith('#') and 

        filename: str,                        len(line) - len(line.lstrip('#')) <= level and

        strategy_name: str = "hierarchical_balanced",                        i > section_start):

    ) -> List[Dict[str, Any]]:                        break

        structure = self.detect_document_structure(text)                    

        document_id = self._compute_document_id(filename)                    section_lines.append(lines[i])

        source_path = str(Path(filename))                

        relative_path = self._make_relative_path(filename)                section_text = '\n'.join(section_lines)

        document_name = Path(filename).stem                

                # Skip very small sections

        chunks: List[Dict[str, Any]] = []                if len(section_text.strip()) < strategy["min_section_tokens"]:

        chunk_index = 0                    continue

                

        if structure["content_blocks"]:                # Step 3: Create chunks from section

            for block in structure["content_blocks"]:                section_chunks = self._chunk_section_content(

                heading = block.get("heading")                    section_text, 

                section_path = [heading["title"]] if heading else []                    section_path,

                section_chunks = self._chunk_section_content(                    filename,

                    block["content"],                    strategy_name,

                    section_path,                    chunk_index,

                    filename,                    document_id

                    strategy_name,                )

                    chunk_index,                

                    document_id,                chunks.extend(section_chunks)

                )                chunk_index += len(section_chunks)

                chunks.extend(section_chunks)        

                chunk_index += len(section_chunks)        # Step 4: Quality filtering and enhancement

        else:        high_quality_chunks = []

            section_chunks = self._chunk_section_content(        for chunk_data in chunks:

                text,            metadata = chunk_data["metadata"]

                [],            

                filename,            # Calculate advanced quality scores

                strategy_name,            semantic_score = self.calculate_semantic_coherence(chunk_data["text"])

                chunk_index,            structural_score = self.calculate_structural_score(chunk_data["text"], structure)

                document_id,            retrieval_quality = self.calculate_retrieval_quality(chunk_data["text"])

            )            

            chunks.extend(section_chunks)            # Update metadata with new scores

            metadata.semantic_score = float(semantic_score)

        accepted: List[Dict[str, Any]] = []            metadata.structural_score = float(structural_score)

        fallback: List[Dict[str, Any]] = []            metadata.retrieval_quality = float(retrieval_quality)

            

        for chunk in chunks:            # Quality filtering based on research thresholds

            metadata: HierarchicalMetadata = chunk["metadata"]            if (semantic_score >= self.quality_thresholds["min_semantic_score"] and

            semantic_score = self.calculate_semantic_coherence(chunk["text"])                structural_score >= self.quality_thresholds["min_structural_score"] and

            structural_score = self.calculate_structural_score(chunk["text"], structure)                retrieval_quality >= self.quality_thresholds["min_retrieval_quality"]):

            retrieval_quality = self.calculate_retrieval_quality(chunk["text"])                

                metadata_dict = asdict(metadata)

            metadata.semantic_score = float(semantic_score)                metadata_dict.setdefault("content_type", "hierarchical_section")

            metadata.structural_score = float(structural_score)                metadata_dict["document_id"] = document_id

            metadata.retrieval_quality = float(retrieval_quality)                metadata_dict["document_name"] = document_name

                metadata_dict["source_path"] = source_path

            metadata_dict = asdict(metadata)                metadata_dict["source_filename"] = Path(filename).name

            metadata_dict.setdefault("content_type", "hierarchical_section")                metadata_dict["source_directory"] = str(Path(source_path).parent)

            metadata_dict["document_id"] = document_id                metadata_dict["relative_path"] = relative_path

            metadata_dict["document_name"] = document_name                metadata_dict["hierarchy_path"] = metadata_dict.get("hierarchy_path") or self._format_section_path(metadata_dict.get("section_path", []))

            metadata_dict["source_path"] = source_path                metadata_dict["chunk_hash"] = self._compute_chunk_hash(chunk_data["text"])

            metadata_dict["source_filename"] = Path(filename).name                metadata_dict["content_digest"] = metadata_dict["chunk_hash"]

            metadata_dict["source_directory"] = str(Path(source_path).parent)                metadata_dict["chunk_length"] = len(chunk_data["text"])

            metadata_dict["relative_path"] = relative_path                metadata_dict["payload_version"] = "1.2"

            metadata_dict["hierarchy_path"] = metadata_dict.get("hierarchy_path") or self._format_section_path(                metadata_dict["collection_hints"] = self._collection_hints(metadata_dict.get("content_type", ""))

                metadata_dict.get("section_path", [])                metadata_dict.setdefault("embedding_model", self.embedding_model_name)

            )

            metadata_dict["chunk_hash"] = self._compute_chunk_hash(chunk["text"])                sparse_features = self._compute_sparse_features(chunk_data["text"])

            metadata_dict["content_digest"] = metadata_dict["chunk_hash"]                metadata_dict["sparse_features"] = sparse_features

            metadata_dict["chunk_length"] = len(chunk["text"])

            metadata_dict["payload_version"] = "1.3"                modal_info = self._detect_modal_hints(chunk_data["text"])

            metadata_dict["collection_hints"] = self._collection_hints(metadata_dict.get("content_type", ""))                metadata_dict["modal_hint"] = modal_info.pop("modal_hint")

            metadata_dict.setdefault("embedding_model", self.embedding_model_name)                metadata_dict["content_flags"] = modal_info



            sparse_features = self._compute_sparse_features(chunk["text"])                keywords = {kw for kw in metadata_dict.get("section_path", []) if isinstance(kw, str)}

            metadata_dict["sparse_features"] = sparse_features                if metadata_dict.get("heading_text"):

                    keywords.add(metadata_dict["heading_text"])

            modal_info = self._detect_modal_hints(chunk["text"])                keywords.update(sparse_features.get("top_terms", [])[:10])

            metadata_dict["modal_hint"] = modal_info.pop("modal_hint")                metadata_dict["search_keywords"] = sorted(k.strip() for k in keywords if k and k.strip())

            metadata_dict["content_flags"] = modal_info

                chunk_data["metadata"] = metadata_dict

            keywords = {kw for kw in metadata_dict.get("section_path", []) if isinstance(kw, str)}                chunk_data["advanced_scores"] = {

            if metadata_dict.get("heading_text"):                    "semantic": float(semantic_score),

                keywords.add(metadata_dict["heading_text"])                    "structural": float(structural_score), 

            keywords.update(sparse_features.get("top_terms", [])[:10])                    "retrieval_quality": float(retrieval_quality),

            metadata_dict["search_keywords"] = sorted(k.strip() for k in keywords if k and k.strip())                    "overall": float((semantic_score + structural_score + retrieval_quality) / 3)

                }

            advanced_scores = {                

                "semantic": float(semantic_score),                high_quality_chunks.append(chunk_data)

                "structural": float(structural_score),        

                "retrieval_quality": float(retrieval_quality),        logger.info(f"🎯 Created {len(high_quality_chunks)} high-quality hierarchical chunks from {filename}")

                "overall": float((semantic_score + structural_score + retrieval_quality) / 3),        logger.info(f"📊 Average scores - Semantic: {np.mean([c['advanced_scores']['semantic'] for c in high_quality_chunks]):.3f}")

            }        logger.info(f"📊 Average scores - Structural: {np.mean([c['advanced_scores']['structural'] for c in high_quality_chunks]):.3f}")

        logger.info(f"📊 Average scores - Retrieval: {np.mean([c['advanced_scores']['retrieval_quality'] for c in high_quality_chunks]):.3f}")

            chunk["metadata"] = metadata_dict        

            chunk["advanced_scores"] = advanced_scores        return high_quality_chunks

    

            if (    def _chunk_section_content(

                semantic_score >= self.quality_thresholds["min_semantic_score"]        self,

                and structural_score >= self.quality_thresholds["min_structural_score"]        section_text: str,

                and retrieval_quality >= self.quality_thresholds["min_retrieval_quality"]        section_path: List[str],

            ):        filename: str,

                accepted.append(chunk)        strategy_name: str,

            else:        start_chunk_index: int,

                fallback.append(chunk)        document_id: str

    ) -> List[Dict[str, Any]]:

        if not accepted and fallback:        """Create chunks from a hierarchical section"""

            fallback.sort(key=lambda c: c["advanced_scores"]["overall"], reverse=True)        

            promoted = fallback[: max(1, min(5, len(fallback)))]        strategy = self.chunking_strategies[strategy_name]

            for chunk in promoted:        max_tokens = strategy["max_tokens"]

                chunk["metadata"]["quality_fallback"] = True        overlap = strategy["overlap"]

                chunk["metadata"]["quality_notes"] = "Promoted via relaxed thresholds"        

            accepted.extend(promoted)        chunks = []

            logger.warning(        sentences = self._split_into_sentences(section_text)

                "No chunks met all thresholds; promoted %d fallback chunks for %s",        

                len(promoted),        current_chunk = ""

                filename,        current_pos = 0

            )        

        for i, sentence in enumerate(sentences):

        if accepted:            test_chunk = current_chunk + " " + sentence if current_chunk else sentence

            semantic_avg = np.mean([c["advanced_scores"]["semantic"] for c in accepted])            

            structural_avg = np.mean([c["advanced_scores"]["structural"] for c in accepted])            if len(self.tokenizer.encode(test_chunk)) <= max_tokens:

            retrieval_avg = np.mean([c["advanced_scores"]["retrieval_quality"] for c in accepted])                current_chunk = test_chunk

            logger.info(            else:

                "Created %d chunks from %s (semantic=%.3f structural=%.3f retrieval=%.3f)",                # Create chunk with hierarchical metadata

                len(accepted),                if current_chunk.strip():

                filename,                    chunk_metadata = HierarchicalMetadata(

                semantic_avg,                        chunk_id=f"{document_id}-{start_chunk_index + len(chunks):04d}",

                structural_avg,                        source_file=filename,

                retrieval_avg,                        filename=Path(filename).name,

            )                        file_extension=Path(filename).suffix,

        else:                        chunk_index=start_chunk_index + len(chunks),

            logger.warning("No viable chunks produced for %s", filename)                        document_level=len(section_path),

                        parent_chunk_id=None,  # Will be set later if needed

        return accepted                        child_chunk_ids=[],

                        section_path=section_path,

                        heading_text=section_path[-1] if section_path else "",

if __name__ == "__main__":  # pragma: no cover - manual smoke test                        token_count=len(self.tokenizer.encode(current_chunk)),

    chunker = EnhancedUltimateChunkerV3()                        char_count=len(current_chunk),

    print("Available strategies:", list(chunker.chunking_strategies.keys()))                        start_char=current_pos,

    print("Quality thresholds:", chunker.quality_thresholds)                        end_char=current_pos + len(current_chunk),

                        semantic_score=0.0,  # Will be calculated later
                        structural_score=0.0,  # Will be calculated later
                        retrieval_quality=0.0,  # Will be calculated later
                        chunking_strategy=strategy_name,
                        content_type="hierarchical_section",
                        embedding_model=self.embedding_model_name,
                        processing_timestamp=datetime.now().isoformat()
                    )
                    
                    chunks.append({
                        "text": current_chunk,
                        "metadata": chunk_metadata
                    })
                
                # Start new chunk with overlap
                if overlap > 0 and len(chunks) > 0:
                    overlap_text = self._get_overlap_text(current_chunk, overlap)
                    current_chunk = overlap_text + " " + sentence
                else:
                    current_chunk = sentence
                
                current_pos += len(current_chunk) - len(sentence)
        
        # Handle final chunk
        if current_chunk.strip():
            chunk_metadata = HierarchicalMetadata(
                chunk_id=f"{document_id}-{start_chunk_index + len(chunks):04d}",
                source_file=filename,
                filename=Path(filename).name,
                file_extension=Path(filename).suffix,
                chunk_index=start_chunk_index + len(chunks),
                document_level=len(section_path),
                parent_chunk_id=None,
                child_chunk_ids=[],
                section_path=section_path,
                heading_text=section_path[-1] if section_path else "",
                token_count=len(self.tokenizer.encode(current_chunk)),
                char_count=len(current_chunk),
                start_char=current_pos,
                end_char=current_pos + len(current_chunk),
                semantic_score=0.0,
                structural_score=0.0,
                retrieval_quality=0.0,
                chunking_strategy=strategy_name,
                content_type="hierarchical_section",
                embedding_model=self.embedding_model_name,
                processing_timestamp=datetime.now().isoformat()
            )
            
            chunks.append({
                "text": current_chunk,
                "metadata": chunk_metadata
            })
        
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Smart sentence splitting for hierarchical processing"""
        
        # Handle code blocks and preserve them
        sentences = []
        current_sentence = ""
        
        for line in text.split('\n'):
            if line.strip().startswith('```'):
                if current_sentence:
                    sentences.append(current_sentence.strip())
                    current_sentence = ""
                sentences.append(line)
            elif line.strip().startswith('#'):
                if current_sentence:
                    sentences.append(current_sentence.strip())
                    current_sentence = ""
                sentences.append(line)
            else:
                current_sentence += line + " "
                
                # Split on sentence boundaries
                if any(line.rstrip().endswith(punct) for punct in ['.', '!', '?']):
                    sentences.append(current_sentence.strip())
                    current_sentence = ""
        
        if current_sentence.strip():
            sentences.append(current_sentence.strip())
        
        return [s for s in sentences if s.strip()]
    
    def _get_overlap_text(self, text: str, overlap_tokens: int) -> str:
        """Get overlap text for chunk continuity"""
        
        words = text.split()
        if len(words) <= overlap_tokens:
            return text
        
        overlap_words = words[-overlap_tokens:]
        return " ".join(overlap_words)
    
    def calculate_semantic_coherence(self, text: str) -> float:
        """Enhanced semantic coherence calculation"""
        
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 10]
        
        if len(sentences) < 2:
            return 0.8
        
        try:
            embeddings = self.embedder.encode(sentences[:5])
            similarities = []
            
            for i in range(len(embeddings)):
                for j in range(i + 1, len(embeddings)):
                    sim = cosine_similarity(
                        np.array([embeddings[i]]), 
                        np.array([embeddings[j]])
                    )[0][0]
                    similarities.append(sim)
            
            return float(np.mean(similarities)) if similarities else 0.5
            
        except Exception as e:
            logger.warning(f"Coherence calculation failed: {e}")
            return 0.5

def main():
    """Test the Enhanced Ultimate Chunker v3.0"""
    
    print("🚀 ULTIMATE CHUNKER V3.0 - RESEARCH-BASED IMPROVEMENTS")
    print("=" * 60)
    print("📊 Based on insights from 9,654 vectors across 3 knowledge domains")
    print("🔬 Implementing: Hierarchical + Hybrid + Quality-Optimized chunking")
    print()
    
    # Initialize the enhanced chunker
    chunker = EnhancedUltimateChunkerV3()
    
    print("✅ Enhanced Ultimate Chunker v3.0 initialized!")
    print(f"📋 Available strategies: {list(chunker.chunking_strategies.keys())}")
    print(f"🎯 Quality thresholds: {chunker.quality_thresholds}")
    print()
    print("🚀 Ready for advanced hierarchical chunking with research-based optimizations!")

if __name__ == "__main__":
    main()