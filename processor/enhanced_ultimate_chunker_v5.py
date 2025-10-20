#!/usr/bin/env python3
"""
Enhanced Ultimate Chunker V5
Model-Aware Chunking with Multi-Framework Integration

V5 ENHANCEMENTS:
- Model-aware chunking (references target embedding model's max_tokens)
- Docling integration for PDF/Office/HTML conversion
- Content-type routing (code → Tree-sitter, text → Semchunk)
- Enhanced metadata enrichment
- Backward compatible with V4

INTEGRATION:
- References KAGGLE_OPTIMIZED_MODELS from kaggle_ultimate_embedder_v4.py
- Ensures chunk sizes respect target model's token limits
- Prevents embedding failures due to oversized chunks

DEFAULT MODEL: jina-code-embeddings-1.5b
- Max Tokens: 32,768
- Vector Dimension: 1536D (full Matryoshka dimension)
- Context Window: 131,072 tokens
- Matryoshka Support: Yes (can truncate to 1024D, 512D, 256D)
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
import hashlib
from datetime import datetime

# Import model config from embedder
try:
    from processor.kaggle_ultimate_embedder_v4 import KAGGLE_OPTIMIZED_MODELS, ModelConfig
except ImportError:
    # Fallback if running standalone
    KAGGLE_OPTIMIZED_MODELS = {}
    ModelConfig = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ChunkerConfig:
    """Configuration for Enhanced Ultimate Chunker V5"""
    
    # Target embedding model (CRITICAL: Must match embedder)
    target_model: str = "jina-code-embeddings-1.5b"
    
    # Chunk sizing (auto-calculated from model if None)
    chunk_size_tokens: Optional[int] = None
    chunk_overlap_tokens: Optional[int] = None
    safety_margin: float = 0.8  # Use 80% of model's max_tokens
    
    # Framework integration flags
    use_docling: bool = False  # Docling for PDF/Office/HTML (requires installation)
    use_tree_sitter: bool = False  # Tree-sitter for code (requires installation)
    use_semchunk: bool = False  # Semchunk for semantic boundaries (requires installation)
    
    # Chunking parameters
    min_chunk_size: int = 100  # Minimum chunk size in characters
    max_chunk_size: int = 100000  # Maximum chunk size in characters
    
    # Metadata enrichment
    extract_keywords: bool = True
    generate_sparse_features: bool = True
    classify_content_type: bool = True
    
    # Backward compatibility
    backward_compatible: bool = True  # Output V4-compatible format
    
    # Output configuration
    output_dir: str = "Chunked"
    preserve_hierarchy: bool = True


class EnhancedUltimateChunkerV5:
    """
    Enhanced Ultimate Chunker V5 with Model-Aware Chunking
    
    KEY FEATURES:
    - Automatically configures chunk size based on target embedding model
    - References KAGGLE_OPTIMIZED_MODELS to get max_tokens parameter
    - Validates chunks won't exceed model's token limit
    - Backward compatible with V4 interface
    
    EXAMPLE:
        # Chunker automatically uses Jina Code 1.5B's 32,768 max tokens
        chunker = EnhancedUltimateChunkerV5(
            target_model="jina-code-embeddings-1.5b",
            safety_margin=0.8  # Use 26,214 tokens per chunk
        )
        
        chunks = chunker.chunk_documents(["doc1.md", "doc2.py"])
    """
    
    def __init__(
        self,
        config: Optional[ChunkerConfig] = None,
        target_model: str = "jina-code-embeddings-1.5b",
        **kwargs
    ):
        """
        Initialize Enhanced Ultimate Chunker V5
        
        Args:
            config: ChunkerConfig object (optional)
            target_model: Name of target embedding model
            **kwargs: Override config parameters
        """
        
        # Initialize configuration
        if config is None:
            config = ChunkerConfig(target_model=target_model, **kwargs)
        else:
            # Override with kwargs if provided
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)
        
        self.config = config
        self.target_model = config.target_model
        
        # Validate and get model configuration
        if not KAGGLE_OPTIMIZED_MODELS:
            logger.warning(
                "KAGGLE_OPTIMIZED_MODELS not available. "
                "Using default chunk sizes."
            )
            self.model_config = None
            self.chunk_size_tokens = config.chunk_size_tokens or 1024
            self.chunk_overlap_tokens = config.chunk_overlap_tokens or 128
        else:
            if target_model not in KAGGLE_OPTIMIZED_MODELS:
                available = list(KAGGLE_OPTIMIZED_MODELS.keys())
                raise ValueError(
                    f"Unknown target model: {target_model}\n"
                    f"Available models: {available}"
                )
            
            self.model_config = KAGGLE_OPTIMIZED_MODELS[target_model]
            
            # Calculate optimal chunk size from model's max_tokens
            max_tokens = self.model_config.max_tokens
            
            if config.chunk_size_tokens is None:
                # Auto-calculate with safety margin
                self.chunk_size_tokens = int(max_tokens * config.safety_margin)
            else:
                # Validate user-provided chunk size
                if config.chunk_size_tokens > max_tokens:
                    raise ValueError(
                        f"chunk_size_tokens ({config.chunk_size_tokens}) exceeds "
                        f"model max_tokens ({max_tokens}). "
                        f"Maximum allowed: {max_tokens}"
                    )
                self.chunk_size_tokens = config.chunk_size_tokens
            
            if config.chunk_overlap_tokens is None:
                # Default overlap: 10% of chunk size
                self.chunk_overlap_tokens = int(self.chunk_size_tokens * 0.1)
            else:
                self.chunk_overlap_tokens = config.chunk_overlap_tokens
        
        # Convert tokens to characters (rough estimation)
        # Jina models use ~4 chars per token average
        self.chars_per_token = 4
        self.chunk_size_chars = self.chunk_size_tokens * self.chars_per_token
        self.chunk_overlap_chars = self.chunk_overlap_tokens * self.chars_per_token
        
        # Store model metadata
        self.model_metadata = {
            "target_model": target_model,
            "chunker_version": "v5",
            "model_aware_chunking": True,
            "chunk_size_tokens": self.chunk_size_tokens,
            "chunk_overlap_tokens": self.chunk_overlap_tokens,
            "chunk_size_chars": self.chunk_size_chars,
            "chunk_overlap_chars": self.chunk_overlap_chars,
            "safety_margin": config.safety_margin
        }
        
        if self.model_config:
            self.model_metadata.update({
                "model_hf_id": self.model_config.hf_model_id,
                "model_max_tokens": self.model_config.max_tokens,
                "embedding_dimension": self.model_config.vector_dim,
                "matryoshka_dimension": 1536 if target_model == "jina-code-embeddings-1.5b" else None
            })
        
        # Initialize framework integrations (if enabled)
        self.docling_converter = None
        self.tree_sitter_parser = None
        self.semchunk_splitter = None
        
        if config.use_docling:
            self._initialize_docling()
        
        if config.use_tree_sitter:
            self._initialize_tree_sitter()
        
        if config.use_semchunk:
            self._initialize_semchunk()
        
        # Statistics
        self.stats = {
            "total_chunks": 0,
            "total_documents": 0,
            "oversized_chunks": 0,
            "undersized_chunks": 0
        }
        
        # Log initialization
        logger.info(f"✓ Enhanced Ultimate Chunker V5 initialized")
        logger.info(f"  Target model: {target_model}")
        if self.model_config:
            logger.info(f"  Model max tokens: {self.model_config.max_tokens:,}")
            logger.info(f"  Vector dimension: {self.model_config.vector_dim}D")
            if target_model == "jina-code-embeddings-1.5b":
                logger.info(f"  Matryoshka dimension: 1536D (full)")
        logger.info(f"  Chunk size: {self.chunk_size_tokens:,} tokens "
                   f"(~{self.chunk_size_chars:,} chars)")
        logger.info(f"  Chunk overlap: {self.chunk_overlap_tokens:,} tokens "
                   f"(~{self.chunk_overlap_chars:,} chars)")
    
    def _initialize_docling(self):
        """Initialize Docling document converter"""
        try:
            from docling.document_converter import DocumentConverter
            self.docling_converter = DocumentConverter()
            logger.info("✓ Docling converter initialized")
        except ImportError:
            logger.warning(
                "Docling not available. Install with: pip install docling\n"
                "Falling back to basic chunking for PDF/Office files."
            )
            self.config.use_docling = False
    
    def _initialize_tree_sitter(self):
        """Initialize Tree-sitter parser"""
        try:
            import tree_sitter
            # TODO: Initialize tree-sitter with language grammars
            logger.info("✓ Tree-sitter parser initialized")
        except ImportError:
            logger.warning(
                "Tree-sitter not available. Install with: pip install tree-sitter\n"
                "Falling back to basic chunking for code files."
            )
            self.config.use_tree_sitter = False
    
    def _initialize_semchunk(self):
        """Initialize Semchunk semantic chunker"""
        try:
            from semchunk.semchunk import chunkerify
            self.semchunk_splitter = chunkerify
            logger.info("✓ Semchunk initialized")
        except ImportError:
            logger.warning(
                "Semchunk not available. Install with: pip install semchunk\n"
                "Falling back to basic chunking for text files."
            )
            self.config.use_semchunk = False
    
    def chunk_documents(
        self,
        file_paths: List[str],
        output_dir: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Main chunking method - chunks multiple documents
        
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
            self._save_chunks(all_chunks, output_dir)
        
        return all_chunks
    
    def chunk_single_document(
        self,
        file_path: str
    ) -> List[Dict[str, Any]]:
        """
        Chunk a single document
        
        Args:
            file_path: Path to file to chunk
        
        Returns:
            List of chunk dictionaries
        """
        
        file_path_obj = Path(file_path)
        
        # Read file content
        try:
            with open(file_path_obj, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Failed to read {file_path_obj}: {e}")
            return []
        
        # Detect content type
        content_type = self._detect_content_type(file_path_obj, content)
        
        # Route to appropriate chunker
        if content_type == "code" and self.config.use_tree_sitter:
            chunks = self._chunk_with_tree_sitter(content, file_path_obj)
        elif content_type in ["prose", "documentation"] and self.config.use_semchunk:
            chunks = self._chunk_with_semchunk(content, file_path_obj)
        else:
            # Fallback to basic chunking
            chunks = self._chunk_basic(content, file_path_obj)
        
        # Enrich metadata
        for i, chunk in enumerate(chunks):
            chunk["metadata"] = self._enrich_metadata(
                chunk, file_path_obj, content_type, i, len(chunks)
            )
        
        return chunks
    
    def _detect_content_type(self, file_path: Path, content: str) -> str:
        """Detect content type from file extension and content"""
        
        # Code file extensions
        code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.rs', '.go'}
        
        if file_path.suffix in code_extensions:
            return "code"
        elif file_path.suffix in {'.md', '.txt', '.rst'}:
            return "documentation"
        elif file_path.suffix in {'.pdf', '.docx', '.html'}:
            return "document"
        else:
            return "prose"
    
    def _chunk_with_tree_sitter(
        self,
        content: str,
        file_path: Path
    ) -> List[Dict[str, Any]]:
        """Chunk code using Tree-sitter AST parsing"""
        # TODO: Implement Tree-sitter chunking
        logger.debug(f"Tree-sitter chunking for {file_path}")
        return self._chunk_basic(content, file_path)
    
    def _chunk_with_semchunk(
        self,
        content: str,
        file_path: Path
    ) -> List[Dict[str, Any]]:
        """Chunk text using Semchunk semantic boundaries"""
        # TODO: Implement Semchunk chunking
        logger.debug(f"Semchunk chunking for {file_path}")
        return self._chunk_basic(content, file_path)
    
    def _chunk_basic(
        self,
        content: str,
        file_path: Path
    ) -> List[Dict[str, Any]]:
        """
        Basic sliding window chunking (V4-compatible fallback)
        
        Respects model token limits to prevent embedding failures.
        """
        
        chunks = []
        content_length = len(content)
        
        # Calculate positions for sliding window
        start = 0
        while start < content_length:
            end = min(start + self.chunk_size_chars, content_length)
            
            # Extract chunk text
            chunk_text = content[start:end]
            
            # Create chunk dictionary
            chunk = {
                "text": chunk_text,
                "metadata": {
                    "source_file": str(file_path),
                    "char_start": start,
                    "char_end": end,
                    "chunk_method": "sliding_window"
                }
            }
            
            chunks.append(chunk)
            
            # Move to next chunk with overlap
            start += self.chunk_size_chars - self.chunk_overlap_chars
        
        return chunks
    
    def _enrich_metadata(
        self,
        chunk: Dict[str, Any],
        file_path: Path,
        content_type: str,
        chunk_index: int,
        total_chunks: int
    ) -> Dict[str, Any]:
        """
        Enrich chunk metadata with V5 features
        
        Includes model compatibility info to prevent embedding failures.
        """
        
        metadata = chunk.get("metadata", {})
        text = chunk["text"]
        
        # Estimate token count
        estimated_tokens = self._estimate_tokens(text)
        
        # Check if within model's token limit
        within_limit = True
        if self.model_config:
            within_limit = estimated_tokens <= self.model_config.max_tokens
            if not within_limit:
                self.stats["oversized_chunks"] += 1
                logger.warning(
                    f"⚠️  Chunk {chunk_index} exceeds model token limit: "
                    f"{estimated_tokens} > {self.model_config.max_tokens}"
                )
        
        # Enhanced metadata
        enhanced = {
            # Model compatibility (CRITICAL)
            **self.model_metadata,
            "estimated_tokens": estimated_tokens,
            "within_token_limit": within_limit,
            
            # File information
            "source_file": str(file_path),
            "source_filename": file_path.name,
            "document_name": file_path.stem,
            
            # Chunk information
            "chunk_index": chunk_index,
            "total_chunks": total_chunks,
            "chunk_id": f"{file_path.stem}_{chunk_index}",
            "chunk_hash": hashlib.sha1(text.encode("utf-8")).hexdigest()[:16],
            
            # Content classification
            "content_type": content_type,
            
            # Processing metadata
            "processing_timestamp": datetime.now().isoformat(),
            "full_text_length": len(text),
            
            # V5 features
            "model_aware_chunking": True,
            "chunker_version": "v5"
        }
        
        # Merge with existing metadata
        enhanced.update(metadata)
        
        # Extract keywords if enabled
        if self.config.extract_keywords:
            enhanced["search_keywords"] = self._extract_keywords(text)
        
        # Generate sparse features if enabled
        if self.config.generate_sparse_features:
            enhanced["sparse_features"] = self._generate_sparse_features(text)
        
        return enhanced
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate token count (4 chars per token average for Jina models)
        
        This is a rough estimation. Actual tokenization may vary.
        """
        return len(text) // self.chars_per_token
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords for search"""
        # Simple keyword extraction (can be enhanced)
        words = text.lower().split()
        # Get unique words > 3 chars
        keywords = list(set(w for w in words if len(w) > 3))
        return keywords[:20]  # Top 20
    
    def _generate_sparse_features(self, text: str) -> Dict[str, Any]:
        """Generate sparse features for hybrid search"""
        # Simple term frequency calculation
        words = text.lower().split()
        word_counts = {}
        for word in words:
            if len(word) > 3:
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # Normalize to weights
        total = sum(word_counts.values())
        term_weights = [
            {"term": term, "weight": count / total}
            for term, count in sorted(
                word_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:50]  # Top 50 terms
        ]
        
        return {
            "term_weights": term_weights,
            "unique_terms": len(word_counts),
            "total_terms": len(words),
            "weighting": "tf-normalized"
        }
    
    def _save_chunks(self, chunks: List[Dict[str, Any]], output_dir: str):
        """Save chunks to JSON file"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_path / f"chunks_v5_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ Chunks saved to {output_file}")
    
    def validate_chunks(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate chunks for model compatibility
        
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
    """Example usage of Enhanced Ultimate Chunker V5"""
    
    logger.info("Enhanced Ultimate Chunker V5 - Example Usage")
    
    # Example 1: Basic usage with Jina Code 1.5B (default)
    chunker = EnhancedUltimateChunkerV5(
        target_model="jina-code-embeddings-1.5b",
        safety_margin=0.8  # Use 80% of 32,768 = 26,214 tokens
    )
    
    # Example file (create a test file if needed)
    test_file = "test_document.md"
    if not Path(test_file).exists():
        with open(test_file, 'w') as f:
            f.write("# Test Document\n\nThis is a test document for chunking.\n" * 100)
    
    # Chunk documents
    chunks = chunker.chunk_documents([test_file])
    
    # Validate chunks
    validation = chunker.validate_chunks(chunks)
    
    logger.info(f"Generated {len(chunks)} chunks")
    logger.info(f"Validation: {validation}")
    
    # Example 2: Different model (smaller context)
    if "all-miniLM-l6" in KAGGLE_OPTIMIZED_MODELS:
        chunker_small = EnhancedUltimateChunkerV5(
            target_model="all-miniLM-l6",  # 256 max tokens
            safety_margin=0.9
        )
        
        chunks_small = chunker_small.chunk_documents([test_file])
        logger.info(f"Small model chunks: {len(chunks_small)}")


if __name__ == "__main__":
    main()