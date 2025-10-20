#!/usr/bin/env python3
"""
Enhanced Ultimate Chunker V5 - Unified Implementation
Model-Aware Chunking with Complete Hierarchical & Semantic Integration

UNIFIED FEATURES:
- V5: Model-aware sizing from KAGGLE_OPTIMIZED_MODELS registry
- V5: Automatic token-limit enforcement and validation
- V3: Complete hierarchical document structure analysis
- V3: Full Tree-sitter AST-based code chunking
- V3: Full Semchunk semantic boundary detection
- V3: Quality scoring and fallback promotion
- V3: Batch processing with directory automation
- Docling integration for PDF/Office/HTML (optional)
- Backward compatible with V4 interface

ARCHITECTURE ALIGNMENT:
Implements §3.1-3.3 from notes/comprehensive_framework_analysis.md:
- Docling → Hierarchical Pre-chunking → Content-Aware Refinement
- Tree-sitter (code) + Semchunk (text) + structural fallback
- Rich metadata with quality gates and sparse features
"""

from __future__ import annotations

import json
import logging
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
import hashlib

import numpy as np
import tiktoken

# Optional semantic scoring
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None
from sklearn.metrics.pairwise import cosine_similarity

# Optional frameworks
try:
    import semchunk
except ImportError:
    semchunk = None

try:
    from tree_sitter import Language, Parser
except ImportError:
    Language = None
    Parser = None

try:
    from tree_sitter_language_pack import get_language
except ImportError:
    try:
        from tree_sitter_languages import get_language
    except ImportError:
        get_language = None

# Model registry integration
try:
    from processor.kaggle_ultimate_embedder_v4 import KAGGLE_OPTIMIZED_MODELS, ModelConfig
except ImportError:
    KAGGLE_OPTIMIZED_MODELS = {}
    ModelConfig = None

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

DEFAULT_EMBEDDING_MODEL = "jina-code-embeddings-1.5b"
DEFAULT_EMBEDDING_DIMENSION = 1024  # V5: 1024D for ensemble compatibility


@dataclass
class ChunkerConfig:
    """Unified configuration combining V3 and V5 features"""
    
    # V5: Model-aware settings
    target_model: str = DEFAULT_EMBEDDING_MODEL
    chunk_size_tokens: Optional[int] = None  # Auto-calculated from model
    chunk_overlap_tokens: Optional[int] = None
    safety_margin: float = 0.8  # Use 80% of model's max_tokens
    
    # V5: Framework integration flags
    use_docling: bool = False
    use_tree_sitter: bool = True  # Enable by default if available
    use_semchunk: bool = True  # Enable by default if available
    
    # V3: Quality control
    enable_semantic_scoring: bool = False  # Requires SentenceTransformer
    quality_thresholds: Optional[Dict[str, float]] = None
    fallback_promotion_ratio: float = 0.25
    fallback_promotion_cap: int = 40
    
    # V3: Tokenizer settings
    tokenizer_name: str = "cl100k_base"
    
    # Metadata enrichment
    extract_keywords: bool = True
    generate_sparse_features: bool = True
    classify_content_type: bool = True
    
    # Backward compatibility (Task 3.5: maintains V4 chunk_documents() interface)
    backward_compatible: bool = True
    
    # Output configuration
    output_dir: str = "Chunked"
    
    # V5: Hierarchy linking control (Task 3.5: used by Phase2CEnhancer)
    preserve_hierarchy: bool = True


@dataclass
class HierarchicalMetadata:
    """Metadata container from V3 with V5 enhancements"""
    
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
    
    # V5 additions
    model_aware_chunking: bool = True
    within_token_limit: bool = True
    estimated_tokens: int = 0


class EnhancedUltimateChunkerV5Unified:
    """
    Unified chunker combining V3's hierarchical/semantic capabilities
    with V5's model-aware approach.
    
    KEY FEATURES:
    - Model-aware chunk sizing from embedding registry
    - Hierarchical document structure preservation
    - Tree-sitter AST-based code chunking
    - Semchunk semantic boundary detection
    - Quality scoring with fallback promotion
    - Batch processing with directory automation
    - Full backward compatibility
    
    EXAMPLE:
        chunker = EnhancedUltimateChunkerV5Unified(
            target_model="jina-code-embeddings-1.5b",
            use_tree_sitter=True,
            use_semchunk=True,
            enable_semantic_scoring=False  # Optional
        )
        
        # Single file
        chunks = chunker.process_file_smart("doc.md")
        
        # Directory batch
        summary = chunker.process_directory_smart("Docs", "Chunked")
    """
    
    def __init__(
        self,
        config: Optional[ChunkerConfig] = None,
        target_model: str = DEFAULT_EMBEDDING_MODEL,
        **kwargs
    ):
        """Initialize unified chunker with V3 + V5 capabilities"""
        
        # Initialize configuration
        if config is None:
            config = ChunkerConfig(target_model=target_model, **kwargs)
        else:
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)
        
        self.config = config
        self.target_model = config.target_model
        self.embedding_model_name = target_model
        self.project_root = Path.cwd()
        
        # V5: Model-aware configuration
        self._initialize_model_aware_settings()
        
        # V3: Tokenizer for precise token counting
        self.tokenizer = tiktoken.get_encoding(config.tokenizer_name)
        
        # V3: Content type patterns and strategies
        self._initialize_content_patterns()
        self._initialize_chunking_strategies()
        
        # V3: Quality thresholds
        self.quality_thresholds = {
            "min_semantic_score": 0.55,
            "min_structural_score": 0.60,
            "min_retrieval_quality": 0.50,
            "min_information_density": 0.35,
        }
        if config.quality_thresholds:
            self.quality_thresholds.update(config.quality_thresholds)
        
        self.fallback_promotion_ratio = max(0.05, min(config.fallback_promotion_ratio, 1.0))
        self.fallback_promotion_cap = max(5, config.fallback_promotion_cap)
        
        # V3: Collection hints
        self.default_collection_hints: Dict[str, List[str]] = {
            "mcp_repository": ["qdrant_ecosystem"],
            "workflow_documentation": ["docling"],
            "api_documentation": ["fast_docs"],
            "programming_documentation": ["sentence_transformers"],
            "platform_documentation": ["qdrant_ecosystem"],
            "hierarchical_section": ["qdrant_ecosystem"],
        }
        
        # V3: Semantic scoring (optional)
        self.embedder: Optional[Any] = None
        self.enable_semantic_scoring = False
        if config.enable_semantic_scoring and SentenceTransformer is not None:
            try:
                self.embedder = SentenceTransformer(target_model, trust_remote_code=True)
                self.enable_semantic_scoring = True
                try:
                    model_dimension = getattr(
                        self.embedder,
                        "get_sentence_embedding_dimension",
                        lambda: self.embedding_dimension,
                    )()
                    if isinstance(model_dimension, int) and model_dimension > 0:
                        self.embedding_dimension = model_dimension
                except Exception:
                    pass
            except Exception as exc:
                logger.warning(
                    "Failed to load semantic model %s (%s); semantic scoring disabled",
                    target_model,
                    exc,
                )
        
        # Initialize framework integrations
        self._initialize_frameworks()
        
        # Statistics
        self.stats = {
            "total_chunks": 0,
            "total_documents": 0,
            "oversized_chunks": 0,
            "undersized_chunks": 0,
            "quality_promoted": 0
        }
        
        # Log initialization
        self._log_initialization()
    
    def _initialize_model_aware_settings(self):
        """V5: Configure chunk sizing from model registry"""
        
        if not KAGGLE_OPTIMIZED_MODELS:
            logger.warning(
                "KAGGLE_OPTIMIZED_MODELS not available. Using default chunk sizes."
            )
            self.model_config = None
            self.chunk_size_tokens = self.config.chunk_size_tokens or 1024
            self.chunk_overlap_tokens = self.config.chunk_overlap_tokens or 128
            self.embedding_dimension = DEFAULT_EMBEDDING_DIMENSION
        else:
            if self.target_model not in KAGGLE_OPTIMIZED_MODELS:
                available = list(KAGGLE_OPTIMIZED_MODELS.keys())
                raise ValueError(
                    f"Unknown target model: {self.target_model}\n"
                    f"Available models: {available}"
                )
            
            self.model_config = KAGGLE_OPTIMIZED_MODELS[self.target_model]
            max_tokens = self.model_config.max_tokens
            
            if self.config.chunk_size_tokens is None:
                self.chunk_size_tokens = int(max_tokens * self.config.safety_margin)
            else:
                if self.config.chunk_size_tokens > max_tokens:
                    raise ValueError(
                        f"chunk_size_tokens ({self.config.chunk_size_tokens}) exceeds "
                        f"model max_tokens ({max_tokens})"
                    )
                self.chunk_size_tokens = self.config.chunk_size_tokens
            
            if self.config.chunk_overlap_tokens is None:
                self.chunk_overlap_tokens = int(self.chunk_size_tokens * 0.1)
            else:
                self.chunk_overlap_tokens = self.config.chunk_overlap_tokens
            
            self.embedding_dimension = self.model_config.vector_dim
        
        # Token-to-char estimation (Jina models: ~4 chars/token)
        self.chars_per_token = 4
        self.chunk_size_chars = self.chunk_size_tokens * self.chars_per_token
        self.chunk_overlap_chars = self.chunk_overlap_tokens * self.chars_per_token
        
        # V5: Model metadata for chunks (enhanced with registry fields)
        self.model_metadata = {
            "target_model": self.target_model,
            "chunker_version": "v5_unified",
            "model_aware_chunking": True,
            "chunk_size_tokens": self.chunk_size_tokens,
            "chunk_overlap_tokens": self.chunk_overlap_tokens,
            "chunk_size_chars": self.chunk_size_chars,
            "chunk_overlap_chars": self.chunk_overlap_chars,
            "safety_margin": self.config.safety_margin,
            "embedding_dimension": self.embedding_dimension,
        }
        
        if self.model_config:
            self.model_metadata.update({
                "model_hf_id": self.model_config.hf_model_id,
                "model_max_tokens": self.model_config.max_tokens,
                "model_vector_dim": self.model_config.vector_dim,
                # Registry fields from V5_MODEL_CONFIGURATIONS
                "recommended_batch_size": getattr(self.model_config, "recommended_batch_size", None),
                "backend": getattr(self.model_config, "backend", "pytorch"),
                "memory_efficient": getattr(self.model_config, "memory_efficient", True),
                "query_prefix": getattr(self.model_config, "query_prefix", ""),
            })
    
    def _initialize_content_patterns(self):
        """V3: Content type detection patterns"""
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
    
    def _initialize_chunking_strategies(self):
        """V3+V5: Chunking strategies with model-aware scaling"""
        # V5: Scale strategies based on model capacity
        # For large models (32K tokens), use full capacity
        # For small models (256 tokens), use conservative sizes
        
        # Calculate strategy-specific sizes relative to model capacity
        if self.chunk_size_tokens >= 8192:
            # Large context models (Jina Code 1.5B: 26,214 tokens)
            precise_tokens = min(2048, self.chunk_size_tokens // 12)
            balanced_tokens = min(4096, self.chunk_size_tokens // 6)
            context_tokens = min(8192, self.chunk_size_tokens // 3)
            adaptive_tokens = min(4096, self.chunk_size_tokens // 6)
            mcp_tokens = min(3072, self.chunk_size_tokens // 8)
        elif self.chunk_size_tokens >= 2048:
            # Medium context models (BGE-M3: ~6,554 tokens)
            precise_tokens = 512
            balanced_tokens = 1024
            context_tokens = 2048
            adaptive_tokens = 1024
            mcp_tokens = 768
        else:
            # Small context models (MiniLM: ~205 tokens)
            precise_tokens = min(128, self.chunk_size_tokens // 2)
            balanced_tokens = min(256, self.chunk_size_tokens)
            context_tokens = min(512, self.chunk_size_tokens)
            adaptive_tokens = min(256, self.chunk_size_tokens)
            mcp_tokens = min(192, self.chunk_size_tokens)
        
        self.chunking_strategies: Dict[str, Dict[str, Any]] = {
            "hierarchical_precise": {
                "max_tokens": precise_tokens,
                "overlap": int(precise_tokens * 0.15),
                "min_section_tokens": int(precise_tokens * 0.25),
                "description": "High precision with tighter chunks",
            },
            "hierarchical_balanced": {
                "max_tokens": balanced_tokens,
                "overlap": int(balanced_tokens * 0.10),
                "min_section_tokens": int(balanced_tokens * 0.18),
                "description": "Balanced chunks tuned for workflow docs",
            },
            "hierarchical_context": {
                "max_tokens": context_tokens,
                "overlap": int(context_tokens * 0.08),
                "min_section_tokens": int(context_tokens * 0.13),
                "description": "Maximum context retention",
            },
            "hybrid_adaptive": {
                "max_tokens": adaptive_tokens,
                "overlap": int(adaptive_tokens * 0.12),
                "min_section_tokens": int(adaptive_tokens * 0.16),
                "description": "Hybrid structural + semantic approach",
            },
            "mcp_optimized": {
                "max_tokens": mcp_tokens,
                "overlap": int(mcp_tokens * 0.12),
                "min_section_tokens": int(mcp_tokens * 0.18),
                "description": "Optimised for MCP repositories",
            },
            "model_aware": {
                "max_tokens": self.chunk_size_tokens,
                "overlap": self.chunk_overlap_tokens,
                "min_section_tokens": self.chunk_size_tokens // 5,
                "description": "Full model capacity (V5 model-aware)",
            },
        }
        
        # Log strategy sizing for transparency
        logger.info(f"Chunking strategies scaled for {self.chunk_size_tokens:,} token model:")
        logger.info(f"  Precise: {precise_tokens:,} | Balanced: {balanced_tokens:,} | "
                   f"Context: {context_tokens:,} | Model-aware: {self.chunk_size_tokens:,}")
    
    def _initialize_frameworks(self):
        """Initialize Tree-sitter, Semchunk, and Docling"""
        
        # Tree-sitter setup
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
        
        if not self._tree_sitter_supported and self.config.use_tree_sitter:
            logger.warning(
                "Tree-sitter not available. Install with: pip install tree-sitter tree-sitter-languages\n"
                "Falling back to structural chunking for code files."
            )
            self.config.use_tree_sitter = False
        
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
        
        # Semchunk setup
        self._semchunk_available = semchunk is not None
        self._semchunk_cache: Dict[int, Any] = {}
        
        if not self._semchunk_available and self.config.use_semchunk:
            logger.warning(
                "Semchunk not available. Install with: pip install semchunk\n"
                "Falling back to structural chunking for text files."
            )
            self.config.use_semchunk = False
        
        # Docling setup
        self.docling_converter = None
        if self.config.use_docling:
            try:
                from docling.document_converter import DocumentConverter
                self.docling_converter = DocumentConverter()
                logger.info("✓ Docling converter initialized")
            except ImportError:
                logger.warning(
                    "Docling not available. Install with: pip install docling\n"
                    "Falling back to basic text extraction for PDF/Office files."
                )
                self.config.use_docling = False
    
    def process_docling_document(
        self,
        file_path: str,
        output_dir: Optional[str] = None,
        strategy_override: Optional[str] = None,
        preserve_tables: bool = True,
        extract_figures: bool = True,
        resolve_references: bool = True,
        enable_phase2c: bool = True,
        figures_output_dir: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        V5 Phase 2C: Enhanced Docling pipeline with table preservation,
        figure extraction, and cross-reference resolution
        
        Pipeline:
        1. Docling converts PDF/Office/HTML → DoclingDocument
        2. Extract structured content (tables, figures, hierarchy)
        3. Preserve table structures as separate chunks
        4. Extract and caption figures
        5. Resolve cross-references between chunks
        6. Feed into hierarchical chunking with enriched metadata
        7. [Phase 2C] Apply advanced enhancements via Phase2CEnhancer
        
        Args:
            file_path: Path to document (PDF, DOCX, HTML, etc.)
            output_dir: Optional output directory
            strategy_override: Override auto-detected strategy
            preserve_tables: Preserve table structure (Task 3.1)
            extract_figures: Extract figures with captions (Task 3.2)
            resolve_references: Resolve cross-references (Task 3.3)
            enable_phase2c: Enable Phase 2C enhancements (hierarchy links, etc.)
            figures_output_dir: Directory to save figure images (Phase 2C)
        
        Returns:
            List of chunk dictionaries with Docling metadata
        """
        if not self.config.use_docling or self.docling_converter is None:
            logger.warning(
                "Docling not enabled. Falling back to process_file_smart(). "
                "Enable with use_docling=True"
            )
            return self.process_file_smart(file_path, output_dir, auto_detect=True)
        
        file_path_obj = Path(file_path)
        
        try:
            # Step 1: Convert document via Docling
            logger.info(f"Converting {file_path_obj.name} via Docling...")
            docling_doc = self.docling_converter.convert(str(file_path_obj))
            
            # Step 2: Extract structured content
            text = docling_doc.export_to_markdown()
            
            # Phase 2C Task 3.1: Extract table structures
            tables = []
            if preserve_tables and hasattr(docling_doc, "tables"):
                tables = self._extract_docling_tables(docling_doc)
                logger.info(f"  Extracted {len(tables)} tables")
            
            # Phase 2C Task 3.2: Extract figures with captions
            figures = []
            if extract_figures and hasattr(docling_doc, "figures"):
                figures = self._extract_docling_figures(docling_doc)
                logger.info(f"  Extracted {len(figures)} figures")
            
            # Phase 2C Task 3.3: Build cross-reference map
            reference_map = {}
            if resolve_references:
                reference_map = self._build_reference_map(docling_doc, text)
                logger.info(f"  Resolved {len(reference_map)} cross-references")
            
            # Extract Docling metadata
            docling_metadata = {
                "docling_conversion": True,
                "has_tables": len(tables) > 0,
                "has_figures": len(figures) > 0,
                "has_references": len(reference_map) > 0,
                "table_count": len(tables),
                "figure_count": len(figures),
                "reference_count": len(reference_map),
                "document_structure": getattr(docling_doc, "structure", None),
                "page_count": getattr(docling_doc, "page_count", None),
            }
            
            logger.info(
                f"  Docling extraction: {len(text)} chars, "
                f"{len(tables)} tables, {len(figures)} figures, "
                f"{len(reference_map)} refs"
            )
            
            # Step 3: Auto-detect content type and strategy
            if not text.strip():
                logger.warning(f"Empty content from Docling for {file_path}")
                return []
            
            content_type, strategy = self.auto_detect_content_type(text, file_path_obj.name)
            
            if strategy_override:
                strategy = strategy_override
            
            # Step 4: Hierarchical chunking with Docling metadata
            chunks = self.create_hierarchical_chunks(
                text=text,
                filename=str(file_path_obj),
                strategy_name=strategy,
            )
            
            # Step 5: Add table chunks (Task 3.1)
            if preserve_tables and tables:
                table_chunks = self._create_table_chunks(
                    tables,
                    str(file_path_obj),
                    len(chunks)
                )
                chunks.extend(table_chunks)
                logger.info(f"  Added {len(table_chunks)} table chunks")
            
            # Step 6: Add figure chunks (Task 3.2)
            if extract_figures and figures:
                figure_chunks = self._create_figure_chunks(
                    figures,
                    str(file_path_obj),
                    len(chunks)
                )
                chunks.extend(figure_chunks)
                logger.info(f"  Added {len(figure_chunks)} figure chunks")
            
            # Step 7: Enrich chunks with Docling metadata and basic references
            for chunk in chunks:
                chunk["metadata"].update(docling_metadata)
                chunk["metadata"]["processing_pipeline"] = "docling_enhanced"
                
                # Add basic cross-references (simplified)
                if resolve_references and reference_map:
                    chunk_id = chunk["metadata"].get("chunk_id", "")
                    chunk["metadata"]["cross_references"] = reference_map.get(chunk_id, [])
            
            if not chunks:
                logger.warning(f"No chunks generated from Docling for {file_path}")
                return []
            
            # Step 8: Apply Phase 2C enhancements (opt-in)
            if enable_phase2c:
                try:
                    from processor.phase2c_enhancements import Phase2CEnhancer
                    
                    enhancer = Phase2CEnhancer(self)
                    chunks = enhancer.enhance_chunks(
                        chunks=chunks,
                        figures=figures if extract_figures else None,
                        text=text if resolve_references else None,
                        figures_output_dir=figures_output_dir or output_dir
                    )
                    
                    # Update stats
                    self.stats.update({
                        "phase2c_cross_refs": enhancer.stats["cross_references_resolved"],
                        "phase2c_hierarchy_links": enhancer.stats["parent_child_links_created"],
                        "phase2c_figures_saved": enhancer.stats["figures_saved"],
                        "phase2c_tables_enhanced": enhancer.stats["tables_enhanced"],
                    })
                    
                    logger.info("✓ Phase 2C enhancements applied")
                except ImportError:
                    logger.warning(
                        "Phase2CEnhancer not available. Install phase2c_enhancements.py "
                        "or set enable_phase2c=False"
                    )
            
            # Step 9: Save if output directory specified
            if output_dir:
                self._save_chunks(chunks, str(file_path_obj), output_dir, content_type)
            
            logger.info(
                f"✓ Enhanced Docling processing complete: "
                f"{len(chunks)} chunks from {file_path_obj.name}"
            )
            
            return chunks
            
        except Exception as e:
            logger.error(f"Docling processing failed for {file_path}: {e}")
            logger.info("Falling back to standard text processing...")
            return self.process_file_smart(file_path, output_dir, auto_detect=True)
    
    def _extract_docling_tables(self, docling_doc: Any) -> List[Dict[str, Any]]:
        """Phase 2C Task 3.1: Extract table structures from Docling document"""
        tables = []
        
        try:
            doc_tables = getattr(docling_doc, "tables", [])
            
            for idx, table in enumerate(doc_tables):
                table_data = {
                    "table_id": f"table_{idx}",
                    "content": str(table),  # Raw table representation
                    "markdown": self._table_to_markdown(table),
                    "rows": getattr(table, "num_rows", 0),
                    "cols": getattr(table, "num_cols", 0),
                    "caption": getattr(table, "caption", ""),
                    "page": getattr(table, "page", None),
                    "bbox": getattr(table, "bbox", None),
                }
                tables.append(table_data)
        except Exception as e:
            logger.warning(f"Table extraction failed: {e}")
        
        return tables
    
    def _table_to_markdown(self, table: Any) -> str:
        """Convert Docling table to Markdown format"""
        try:
            # Try to get table data
            if hasattr(table, "to_markdown"):
                return table.to_markdown()
            elif hasattr(table, "data"):
                # Manual markdown conversion
                data = table.data
                if not data:
                    return str(table)
                
                # Header row
                header = "| " + " | ".join(str(cell) for cell in data[0]) + " |\n"
                separator = "|" + "|".join(["---"] * len(data[0])) + "|\n"
                
                # Data rows
                rows = ""
                for row in data[1:]:
                    rows += "| " + " | ".join(str(cell) for cell in row) + " |\n"
                
                return header + separator + rows
            else:
                return str(table)
        except Exception:
            return str(table)
    
    def _extract_docling_figures(self, docling_doc: Any) -> List[Dict[str, Any]]:
        """Phase 2C Task 3.2: Extract figures with captions from Docling document"""
        figures = []
        
        try:
            doc_figures = getattr(docling_doc, "figures", [])
            
            for idx, figure in enumerate(doc_figures):
                figure_data = {
                    "figure_id": f"figure_{idx}",
                    "caption": getattr(figure, "caption", ""),
                    "alt_text": getattr(figure, "alt_text", ""),
                    "path": getattr(figure, "path", None),
                    "page": getattr(figure, "page", None),
                    "bbox": getattr(figure, "bbox", None),
                    "width": getattr(figure, "width", None),
                    "height": getattr(figure, "height", None),
                }
                figures.append(figure_data)
        except Exception as e:
            logger.warning(f"Figure extraction failed: {e}")
        
        return figures
    
    def _build_reference_map(
        self,
        docling_doc: Any,
        text: str
    ) -> Dict[str, List[str]]:
        """Phase 2C Task 3.3: Build cross-reference map between chunks"""
        reference_map = {}
        
        try:
            # Extract references from Docling document
            if hasattr(docling_doc, "references"):
                doc_refs = docling_doc.references
                for ref in doc_refs:
                    source = getattr(ref, "source_id", "")
                    target = getattr(ref, "target_id", "")
                    if source and target:
                        if source not in reference_map:
                            reference_map[source] = []
                        reference_map[source].append(target)
            
            # Also detect markdown-style references
            import re
            # Pattern: [text](reference) or [reference]
            ref_pattern = r'\[([^\]]+)\]\(([^\)]+)\)|\[([^\]]+)\]'
            matches = re.findall(ref_pattern, text)
            
            for match in matches:
                ref_text = match[0] or match[2]
                ref_target = match[1] if match[1] else match[2]
                
                # Store reference relationships
                # Note: Full implementation would map these to chunk IDs
                # This is a simplified version
                if ref_text:
                    if "reference" not in reference_map:
                        reference_map["reference"] = []
                    reference_map["reference"].append(ref_target)
        
        except Exception as e:
            logger.warning(f"Reference resolution failed: {e}")
        
        return reference_map
    
    def _create_table_chunks(
        self,
        tables: List[Dict[str, Any]],
        filename: str,
        start_index: int
    ) -> List[Dict[str, Any]]:
        """Phase 2C Task 3.1: Create dedicated chunks for tables"""
        chunks = []
        document_id = self._compute_document_id(filename)
        
        for idx, table in enumerate(tables):
            chunk_index = start_index + idx
            table_text = (
                f"Table {idx + 1}: {table.get('caption', 'Untitled')}\n\n"
                f"{table['markdown']}\n\n"
                f"Dimensions: {table['rows']} rows × {table['cols']} columns"
            )
            
            metadata = self._create_chunk_metadata(
                text=table_text,
                section_path=[f"Table {idx + 1}"],
                filename=filename,
                document_id=document_id,
                chunk_index=chunk_index,
                chunking_strategy="docling_table_preservation",
                start_char=0,
                content_type="table_structure",
            )
            
            # Add table-specific metadata
            metadata_dict = asdict(metadata)
            metadata_dict.update({
                "table_id": table["table_id"],
                "table_caption": table.get("caption", ""),
                "table_rows": table["rows"],
                "table_cols": table["cols"],
                "table_page": table.get("page"),
                "is_table_chunk": True,
            })
            
            chunks.append({
                "text": table_text,
                "metadata": metadata_dict
            })
        
        return chunks
    
    def _create_figure_chunks(
        self,
        figures: List[Dict[str, Any]],
        filename: str,
        start_index: int
    ) -> List[Dict[str, Any]]:
        """Phase 2C Task 3.2: Create dedicated chunks for figures"""
        chunks = []
        document_id = self._compute_document_id(filename)
        
        for idx, figure in enumerate(figures):
            chunk_index = start_index + idx
            figure_text = (
                f"Figure {idx + 1}: {figure.get('caption', 'Untitled')}\n\n"
                f"Alt text: {figure.get('alt_text', 'No description')}\n"
            )
            
            if figure.get("path"):
                figure_text += f"Image path: {figure['path']}\n"
            
            metadata = self._create_chunk_metadata(
                text=figure_text,
                section_path=[f"Figure {idx + 1}"],
                filename=filename,
                document_id=document_id,
                chunk_index=chunk_index,
                chunking_strategy="docling_figure_extraction",
                start_char=0,
                content_type="figure_caption",
            )
            
            # Add figure-specific metadata
            metadata_dict = asdict(metadata)
            metadata_dict.update({
                "figure_id": figure["figure_id"],
                "figure_caption": figure.get("caption", ""),
                "figure_alt_text": figure.get("alt_text", ""),
                "figure_path": figure.get("path"),
                "figure_page": figure.get("page"),
                "figure_bbox": figure.get("bbox"),
                "is_figure_chunk": True,
            })
            
            chunks.append({
                "text": figure_text,
                "metadata": metadata_dict
            })
        
        return chunks
    
    def _log_initialization(self):
        """Log initialization summary"""
        logger.info("="*70)
        logger.info("Enhanced Ultimate Chunker V5 Unified - Initialized")
        logger.info("="*70)
        logger.info(f"Target model: {self.target_model}")
        if self.model_config:
            logger.info(f"  Model max tokens: {self.model_config.max_tokens:,}")
            logger.info(f"  Vector dimension: {self.model_config.vector_dim}D")
        logger.info(f"  Chunk size: {self.chunk_size_tokens:,} tokens (~{self.chunk_size_chars:,} chars)")
        logger.info(f"  Chunk overlap: {self.chunk_overlap_tokens:,} tokens (~{self.chunk_overlap_chars:,} chars)")
        logger.info(f"Framework Integration:")
        logger.info(f"  Tree-sitter: {'✓ Enabled' if self.config.use_tree_sitter else '✗ Disabled'}")
        logger.info(f"  Semchunk: {'✓ Enabled' if self.config.use_semchunk else '✗ Disabled'}")
        logger.info(f"  Docling: {'✓ Enabled' if self.config.use_docling else '✗ Disabled'}")
        logger.info(f"  Semantic scoring: {'✓ Enabled' if self.enable_semantic_scoring else '✗ Disabled'}")
        logger.info("="*70)
    
    # ========================================================================
    # V3: Helper Utilities
    # ========================================================================
    
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
    
    def _encode_tokens(self, text: str) -> List[int]:
        """V3: Encode text with robust token handling"""
        try:
            return self.tokenizer.encode(text, disallowed_special=())
        except ValueError:
            return self.tokenizer.encode(text, allowed_special="all")
    
    @staticmethod
    def _compute_chunk_hash(text: str) -> str:
        return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]
    
    @staticmethod
    def _format_section_path(section_path: List[str]) -> str:
        return " > ".join(part.strip() for part in section_path if isinstance(part, str) and part.strip())
    
    @staticmethod
    def _compute_sparse_features(text: str, top_n: int = 20) -> Dict[str, Any]:
        """V3: Generate sparse features for hybrid search"""
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
        """V3: Detect content modality (code, table, list, etc.)"""
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
    
    def _normalise_path_for_io(self, path: Path) -> str:
        """Windows long path support"""
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
    
    # ========================================================================
    # V3: Framework Integrations - Semchunk
    # ========================================================================
    
    def _get_semchunk_chunker(self, chunk_size: int):
        """V3: Get or create cached Semchunk chunker"""
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
            except Exception as exc:
                logger.warning("Semchunk initialisation failed: %s", exc)
                self._semchunk_available = False
                return None
        return self._semchunk_cache.get(chunk_size)
    
    # ========================================================================
    # V3: Framework Integrations - Tree-sitter
    # ========================================================================
    
    def _get_tree_sitter_language(self, language_name: Optional[str]):
        """V3: Get or load Tree-sitter language grammar"""
        if not language_name or not self._tree_sitter_supported:
            return None
        if language_name not in self._tree_sitter_languages:
            try:
                language_loader = get_language
                if language_loader is None:
                    raise RuntimeError("tree_sitter_languages.get_language unavailable")
                self._tree_sitter_languages[language_name] = language_loader(language_name)
            except Exception as exc:
                logger.warning("Tree-sitter language load failed for %s: %s", language_name, exc)
                self._tree_sitter_languages[language_name] = None
        return self._tree_sitter_languages.get(language_name)
    
    def _collect_tree_sitter_nodes(self, root_node: Any, language_hint: str) -> List[Any]:
        """V3: Collect function/class nodes from AST"""
        target_types = list(self._tree_sitter_node_types.get(language_hint, []))
        if not target_types:
            target_types = list(self._tree_sitter_node_types.get("python", []))
        if not target_types:
            return []
        
        nodes: List[Any] = []
        stack: List[Any] = [root_node]
        
        while stack:
            node = stack.pop()
            # is_named is a property in new tree-sitter, not a method
            is_named = getattr(node, "is_named", True)
            if not (is_named if isinstance(is_named, bool) else is_named()):
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
    
    # ========================================================================
    # V3: Content Type Detection & Backend Selection
    # ========================================================================
    
    def auto_detect_content_type(self, text: str, filename: str) -> Tuple[str, str]:
        """V3: Auto-detect content type and select strategy"""
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
    
    def _select_chunking_backend(
        self,
        section_text: str,
        filename: str,
        block_meta: Dict[str, Any],
    ) -> Tuple[str, str, Optional[str]]:
        """V3: Select appropriate chunking backend (Tree-sitter/Semchunk/structural)"""
        modal_flags = self._detect_modal_hints(section_text)
        extension = Path(filename).suffix.lower()
        language_hint = self.language_hints_by_extension.get(extension)
        
        if modal_flags["modal_hint"] == "code" or self._looks_like_code(section_text) or language_hint:
            language_hint = language_hint or "python"
            if self.config.use_tree_sitter and self._get_tree_sitter_language(language_hint):
                return "tree_sitter", "code_block", language_hint
        if modal_flags["modal_hint"] == "table":
            return "hierarchical", "table_section", None
        if modal_flags["modal_hint"] == "list":
            return "hierarchical", "list_section", None
        if self.config.use_semchunk and self._semchunk_available:
            return "semchunk", "prose_section", None
        return "hierarchical", "hierarchical_section", None
    
    # ========================================================================
    # V3: Document Structure Analysis
    # ========================================================================
    
    def detect_document_structure(self, text: str) -> Dict[str, Any]:
        """V3: Hierarchical structure detection from markdown headers"""
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
        """V3: Split text into sentences preserving code blocks"""
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
    
    # ========================================================================
    # V3: Chunking Methods - Structural
    # ========================================================================
    
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
        """V3: Structural sentence-based chunking with overlap"""
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
    
    # ========================================================================
    # V3: Chunking Methods - Semchunk
    # ========================================================================
    
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
        """V3: Semantic boundary-aware chunking via Semchunk"""
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
        except TypeError:
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
    
    # ========================================================================
    # V3: Chunking Methods - Tree-sitter
    # ========================================================================
    
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
        """V3: AST-based code chunking via Tree-sitter"""
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
        
        parser = Parser(language)
        try:
            tree = parser.parse(section_text.encode("utf-8"))
        except Exception as exc:
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
    
    # ========================================================================
    # V3: Metadata Creation
    # ========================================================================
    
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
        """V3+V5: Create metadata with both hierarchical and model-aware fields"""
        end_value = end_char if end_char is not None else start_char + len(text)
        token_count = len(self._encode_tokens(text))
        
        # V5: Check token limit compliance
        within_limit = True
        if self.model_config:
            within_limit = token_count <= self.model_config.max_tokens
            if not within_limit:
                self.stats["oversized_chunks"] += 1
        
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
            token_count=token_count,
            char_count=len(text),
            start_char=start_char,
            end_char=end_value,
            chunking_strategy=chunking_strategy,
            content_type=content_type,
            embedding_model=self.embedding_model_name,
            embedding_dimension=embedding_dimension if embedding_dimension is not None else self.embedding_dimension,
            # V5 additions
            model_aware_chunking=True,
            within_token_limit=within_limit,
            estimated_tokens=token_count,
        )
        return metadata
    
    # ========================================================================
    # V3: Quality Calculations
    # ========================================================================
    
    def calculate_semantic_coherence(self, text: str) -> float:
        """V3: Calculate semantic coherence using embeddings or heuristics"""
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
        except Exception as exc:
            logger.warning("Semantic coherence calculation failed: %s", exc)
            return self._semantic_coherence_heuristic(sentences)
    
    @staticmethod
    def _semantic_coherence_heuristic(sentences: List[str]) -> float:
        """Lightweight fallback for semantic coherence"""
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
        """V3: Calculate structural quality score"""
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
        """V3: Calculate retrieval quality score"""
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
    
    # ========================================================================
    # V3: Main Hierarchical Chunking Pipeline
    # ========================================================================
    
    def create_hierarchical_chunks(
        self,
        text: str,
        filename: str,
        strategy_name: str = "hierarchical_balanced",
    ) -> List[Dict[str, Any]]:
        """
        V3: Main hierarchical chunking method with quality gating
        
        Pipeline:
        1. Detect document structure (headings, sections)
        2. For each section, select backend (Tree-sitter/Semchunk/structural)
        3. Generate chunks with rich metadata
        4. Calculate quality scores
        5. Apply quality thresholds with fallback promotion
        """
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
        
        # V3: Quality scoring and gating
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
            
            # Convert to dict and enrich
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
            
            # V5: Model metadata integration
            metadata_dict.update(self.model_metadata)
            
            # V5: Conditional sparse features generation (Task 3.5)
            if self.config.generate_sparse_features:
                sparse_features = self._compute_sparse_features(chunk["text"])
                metadata_dict["sparse_features"] = sparse_features
            else:
                sparse_features = {"top_terms": [], "term_weights": []}
                metadata_dict["sparse_features"] = {}
            
            modal_info = self._detect_modal_hints(chunk["text"])
            metadata_dict["modal_hint"] = modal_info.pop("modal_hint")
            metadata_dict["content_flags"] = modal_info
            
            # V5: Conditional keyword extraction (Task 3.5)
            if self.config.extract_keywords:
                keywords = {kw for kw in metadata_dict.get("section_path", []) if isinstance(kw, str)}
                if metadata_dict.get("heading_text"):
                    keywords.add(metadata_dict["heading_text"])
                keywords.update(sparse_features.get("top_terms", [])[:10])
                metadata_dict["search_keywords"] = sorted(k.strip() for k in keywords if k and k.strip())
            else:
                metadata_dict["search_keywords"] = []
            
            advanced_scores = {
                "semantic": float(semantic_score),
                "structural": float(structural_score),
                "retrieval_quality": float(retrieval_quality),
                "overall": float((semantic_score + structural_score + retrieval_quality) / 3),
            }
            
            chunk["metadata"] = metadata_dict
            chunk["advanced_scores"] = advanced_scores
            
            # V3: Quality gate
            if (
                semantic_score >= self.quality_thresholds["min_semantic_score"]
                and structural_score >= self.quality_thresholds["min_structural_score"]
                and retrieval_quality >= self.quality_thresholds["min_retrieval_quality"]
            ):
                accepted.append(chunk)
            else:
                fallback.append(chunk)
        
        # V3: Fallback promotion if nothing passed
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
            self.stats["quality_promoted"] += len(promoted)
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
    
    # ========================================================================
    # V3: Public API - File Processing
    # ========================================================================
    
    def process_file_smart(
        self,
        file_path: str,
        output_dir: Optional[str] = None,
        auto_detect: bool = True,
        strategy_override: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        V3: Smart file processing with auto-detection
        
        Args:
            file_path: Path to file
            output_dir: Optional output directory
            auto_detect: Auto-detect content type and strategy
            strategy_override: Override auto-detected strategy
        
        Returns:
            List of chunk dictionaries
        """
        file_path_obj = Path(file_path)
        try:
            text = self._read_text(file_path_obj)
        except UnicodeDecodeError:
            text = self._read_text(file_path_obj, errors="ignore")
        
        if not text.strip():
            logger.warning("Skipping empty file %s", file_path)
            return []
        
        # V5: Conditional content type classification (Task 3.5)
        if auto_detect and self.config.classify_content_type:
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
        """
        V3: Batch process directory with smart detection
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            file_extensions: File extensions to process (default: common text formats)
        
        Returns:
            Summary dictionary with processing statistics
        """
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
        """Save chunks to JSON file"""
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
    
    # ========================================================================
    # V5: Public API - Backward Compatible Interface
    # ========================================================================
    
    def chunk_documents(
        self,
        file_paths: List[str],
        output_dir: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        V5: Main chunking method - chunks multiple documents
        
        Backward compatible with V5 interface.
        
        Args:
            file_paths: List of file paths to chunk
            output_dir: Output directory for chunks (optional)
            **kwargs: Additional parameters
        
        Returns:
            List of chunk dictionaries with text and metadata
        """
        output_dir = output_dir or self.config.output_dir
        all_chunks = []
        
        logger.info(f"Chunking {len(file_paths)} documents...")
        
        for file_path in file_paths:
            try:
                doc_chunks = self.chunk_single_document(file_path)
                all_chunks.extend(doc_chunks)
                self.stats["total_documents"] += 1
                
                logger.info(f"  ✓ {Path(file_path).name}: {len(doc_chunks)} chunks")
                
            except Exception as e:
                logger.error(f"  ✗ {Path(file_path).name}: {e}")
        
        self.stats["total_chunks"] = len(all_chunks)
        
        logger.info(f"Chunking complete: {self.stats['total_chunks']} total chunks")
        
        # Save chunks if output directory specified
        if output_dir:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            output_file = output_path / f"chunks_v5_unified_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_chunks, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✓ Chunks saved to {output_file}")
        
        return all_chunks
    
    def chunk_single_document(
        self,
        file_path: str
    ) -> List[Dict[str, Any]]:
        """
        V5: Chunk a single document
        
        Delegates to V3's process_file_smart for full functionality.
        
        Args:
            file_path: Path to file to chunk
        
        Returns:
            List of chunk dictionaries
        """
        return self.process_file_smart(file_path, output_dir=None, auto_detect=True)
    
    def validate_chunks(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        V5: Validate chunks for model compatibility
        
        Returns validation report with any issues found.
        """
        if not self.model_config:
            return {
                "validation_skipped": True,
                "reason": "No model config available"
            }
        
        max_tokens = self.model_config.max_tokens
        invalid_chunks = []
        
        for i, chunk in enumerate(chunks):
            metadata = chunk.get("metadata", {})
            estimated_tokens = metadata.get("estimated_tokens", 0)
            
            if estimated_tokens > max_tokens:
                invalid_chunks.append({
                    "chunk_index": i,
                    "estimated_tokens": estimated_tokens,
                    "overflow": estimated_tokens - max_tokens
                })
        
        validation = {
            "total_chunks": len(chunks),
            "valid_chunks": len(chunks) - len(invalid_chunks),
            "invalid_chunks": len(invalid_chunks),
            "validation_passed": len(invalid_chunks) == 0,
            "model_max_tokens": max_tokens,
            "oversized_chunk_details": invalid_chunks[:10]  # Show first 10
        }
        
        if not validation["validation_passed"]:
            logger.warning(
                f"⚠️  Validation failed: {len(invalid_chunks)} chunks exceed "
                f"{max_tokens} token limit"
            )
        else:
            logger.info(
                f"✓ Validation passed: All {len(chunks)} chunks within token limit"
            )
        
        return validation


def main():
    """Example usage of Enhanced Ultimate Chunker V5 Unified"""
    
    logger.info("="*70)
    logger.info("Enhanced Ultimate Chunker V5 Unified - Example Usage")
    logger.info("="*70)
    
    # Example 1: Basic usage with Jina Code 1.5B (default)
    chunker = EnhancedUltimateChunkerV5Unified(
        target_model="jina-code-embeddings-1.5b",
        use_tree_sitter=True,
        use_semchunk=True,
        enable_semantic_scoring=False,  # Optional - requires model download
        safety_margin=0.8  # Use 80% of 32,768 = 26,214 tokens
    )
    
    # Example file (create a test file if needed)
    test_file = "test_document.md"
    if not Path(test_file).exists():
        with open(test_file, 'w') as f:
            f.write("# Test Document\n\nThis is a test document for chunking.\n" * 100)
    
    # Single file processing
    logger.info("\n" + "="*70)
    logger.info("Example 1: Single File Processing (V5 API)")
    logger.info("="*70)
    chunks = chunker.chunk_single_document(test_file)
    
    # Validate chunks
    validation = chunker.validate_chunks(chunks)
    
    logger.info(f"Generated {len(chunks)} chunks")
    logger.info(f"Validation: {validation}")
    
    # Example 2: Smart file processing (V3 API)
    logger.info("\n" + "="*70)
    logger.info("Example 2: Smart File Processing (V3 API)")
    logger.info("="*70)
    chunks_v3 = chunker.process_file_smart(
        test_file,
        output_dir="Chunked",
        auto_detect=True
    )
    logger.info(f"Smart processing generated {len(chunks_v3)} chunks")
    
    # Example 3: Directory batch processing
    logger.info("\n" + "="*70)
    logger.info("Example 3: Directory Batch Processing")
    logger.info("="*70)
    
    # Create test directory
    test_dir = Path("test_docs")
    test_dir.mkdir(exist_ok=True)
    for i in range(3):
        with open(test_dir / f"doc_{i}.md", 'w') as f:
            f.write(f"# Document {i}\n\nContent for document {i}.\n" * 50)
    
    summary = chunker.process_directory_smart(
        str(test_dir),
        "Chunked",
        file_extensions=[".md", ".txt"]
    )
    
    logger.info(f"Processed {summary['processed_files']} files")
    logger.info(f"Total chunks: {summary['total_chunks']}")
    logger.info(f"Processing time: {summary['processing_time']:.2f}s")
    
    # Statistics
    logger.info("\n" + "="*70)
    logger.info("Chunker Statistics")
    logger.info("="*70)
    logger.info(f"Total documents processed: {chunker.stats['total_documents']}")
    logger.info(f"Total chunks created: {chunker.stats['total_chunks']}")
    logger.info(f"Oversized chunks: {chunker.stats['oversized_chunks']}")
    logger.info(f"Quality promoted: {chunker.stats['quality_promoted']}")
    logger.info("="*70)


if __name__ == "__main__":
    main()
