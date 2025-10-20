#!/usr/bin/env python3
"""
LlamaIndex NodeParser Wrappers for V5 Unified Chunker
Implements §3.3 from comprehensive_framework_analysis.md

Provides NodeParser classes that wrap:
- Docling document conversion
- Tree-sitter AST parsing
- Semchunk semantic chunking
- Hierarchical composite strategy
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from llama_index.core.node_parser import NodeParser
from llama_index.core.schema import BaseNode, Document, TextNode
from llama_index.core.utils import get_tqdm_iterable

# Import our V5 unified chunker
from processor.enhanced_ultimate_chunker_v5_unified import (
    EnhancedUltimateChunkerV5Unified,
    ChunkerConfig
)

logger = logging.getLogger(__name__)


class DoclingNodeParser(NodeParser):
    """
    LlamaIndex NodeParser wrapping Docling document conversion
    
    Features:
    - PDF/Office/HTML conversion via Docling
    - Structured metadata extraction (tables, figures, hierarchy)
    - Integration with hierarchical chunking
    
    Example:
        parser = DoclingNodeParser(
            target_model="jina-code-embeddings-1.5b",
            chunk_size=1024
        )
        
        documents = [Document(text=Path("paper.pdf"))]
        nodes = parser.get_nodes_from_documents(documents)
    """
    
    def __init__(
        self,
        target_model: str = "jina-code-embeddings-1.5b",
        chunk_size: int = 1024,
        chunk_overlap: int = 128,
        strategy_name: str = "hierarchical_balanced",
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
    ):
        """
        Initialize Docling NodeParser
        
        Args:
            target_model: Target embedding model for chunk sizing
            chunk_size: Maximum chunk size in tokens
            chunk_overlap: Overlap between chunks in tokens
            strategy_name: Chunking strategy to use
            include_metadata: Include source metadata in nodes
            include_prev_next_rel: Link consecutive nodes
        """
        super().__init__(
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel
        )
        
        # Initialize V5 unified chunker with Docling enabled
        self.chunker = EnhancedUltimateChunkerV5Unified(
            config=ChunkerConfig(
                target_model=target_model,
                chunk_size_tokens=chunk_size,
                chunk_overlap_tokens=chunk_overlap,
                use_docling=True,  # Enable Docling
                use_tree_sitter=True,
                use_semchunk=True,
            )
        )
        
        self.strategy_name = strategy_name
        
        logger.info(
            f"DoclingNodeParser initialized with {target_model}, "
            f"chunk_size={chunk_size}, strategy={strategy_name}"
        )
    
    def _parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any
    ) -> List[BaseNode]:
        """
        Parse documents into nodes using Docling pipeline
        
        Args:
            nodes: Input documents (should contain file paths or text)
            show_progress: Show progress bar
            **kwargs: Additional arguments
        
        Returns:
            List of TextNode objects with Docling metadata
        """
        all_nodes: List[BaseNode] = []
        
        nodes_with_progress = get_tqdm_iterable(
            nodes, show_progress, "Parsing documents with Docling"
        )
        
        for node in nodes_with_progress:
            # Extract file path or text from node
            if isinstance(node, Document):
                # Check if this is a file path reference
                if hasattr(node, 'metadata') and 'file_path' in node.metadata:
                    file_path = node.metadata['file_path']
                elif node.text and Path(node.text).exists():
                    file_path = node.text
                else:
                    # Plain text document - use standard processing
                    logger.warning(
                        "DoclingNodeParser expects file paths. "
                        "Falling back to standard processing."
                    )
                    file_path = None
                
                if file_path:
                    # Process via Docling pipeline
                    chunks = self.chunker.process_docling_document(
                        file_path=str(file_path),
                        output_dir=None,
                        strategy_override=self.strategy_name
                    )
                else:
                    # Fallback: process text directly
                    chunks = self.chunker.process_file_smart(
                        file_path="<text>",
                        output_dir=None,
                        auto_detect=True
                    )
                
                # Convert chunks to TextNode objects
                for chunk in chunks:
                    text_node = TextNode(
                        text=chunk["text"],
                        metadata=chunk.get("metadata", {}),
                        id_=chunk["metadata"].get("chunk_id"),
                    )
                    
                    # Add advanced scores if available
                    if "advanced_scores" in chunk:
                        text_node.metadata["advanced_scores"] = chunk["advanced_scores"]
                    
                    all_nodes.append(text_node)
        
        # Link consecutive nodes if requested
        if self.include_prev_next_rel:
            self._link_nodes(all_nodes)
        
        return all_nodes
    
    def _link_nodes(self, nodes: List[BaseNode]) -> None:
        """Link consecutive nodes with prev/next relationships"""
        for i in range(len(nodes)):
            if i > 0:
                nodes[i].relationships["previous"] = nodes[i-1].node_id
            if i < len(nodes) - 1:
                nodes[i].relationships["next"] = nodes[i+1].node_id


class TreeSitterNodeParser(NodeParser):
    """
    LlamaIndex NodeParser wrapping Tree-sitter AST parsing
    
    Features:
    - AST-based code chunking (functions, classes)
    - 8 language support (Python, JS, TS, Java, Go, Rust, C, C++)
    - Syntax-aware boundaries
    
    Example:
        parser = TreeSitterNodeParser(
            target_model="jina-code-embeddings-1.5b",
            chunk_size=2048
        )
        
        documents = [Document(text=Path("script.py").read_text())]
        nodes = parser.get_nodes_from_documents(documents)
    """
    
    def __init__(
        self,
        target_model: str = "jina-code-embeddings-1.5b",
        chunk_size: int = 2048,
        chunk_overlap: int = 200,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
    ):
        """
        Initialize Tree-sitter NodeParser
        
        Args:
            target_model: Target embedding model
            chunk_size: Maximum chunk size in tokens
            chunk_overlap: Overlap between chunks
            include_metadata: Include source metadata
            include_prev_next_rel: Link consecutive nodes
        """
        super().__init__(
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel
        )
        
        # Initialize V5 unified chunker with Tree-sitter enabled
        self.chunker = EnhancedUltimateChunkerV5Unified(
            config=ChunkerConfig(
                target_model=target_model,
                chunk_size_tokens=chunk_size,
                chunk_overlap_tokens=chunk_overlap,
                use_tree_sitter=True,  # Enable Tree-sitter
                use_semchunk=False,    # Code-only parser
            )
        )
        
        logger.info(
            f"TreeSitterNodeParser initialized with {target_model}, "
            f"chunk_size={chunk_size}"
        )
    
    def _parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any
    ) -> List[BaseNode]:
        """Parse code documents into AST-based nodes"""
        all_nodes: List[BaseNode] = []
        
        nodes_with_progress = get_tqdm_iterable(
            nodes, show_progress, "Parsing code with Tree-sitter"
        )
        
        for node in nodes_with_progress:
            if isinstance(node, Document):
                # Get file path or use temp file
                file_path = node.metadata.get('file_path', '<code>')
                
                if file_path != '<code>':
                    chunks = self.chunker.process_file_smart(
                        file_path=file_path,
                        output_dir=None,
                        auto_detect=False,
                        strategy_override="hybrid_adaptive"
                    )
                else:
                    # Process text directly
                    chunks = self.chunker.create_hierarchical_chunks(
                        text=node.text,
                        filename="<code>",
                        strategy_name="hybrid_adaptive"
                    )
                
                # Convert to TextNode
                for chunk in chunks:
                    text_node = TextNode(
                        text=chunk["text"],
                        metadata=chunk.get("metadata", {}),
                        id_=chunk["metadata"].get("chunk_id"),
                    )
                    all_nodes.append(text_node)
        
        if self.include_prev_next_rel:
            self._link_nodes(all_nodes)
        
        return all_nodes
    
    def _link_nodes(self, nodes: List[BaseNode]) -> None:
        """Link consecutive nodes"""
        for i in range(len(nodes)):
            if i > 0:
                nodes[i].relationships["previous"] = nodes[i-1].node_id
            if i < len(nodes) - 1:
                nodes[i].relationships["next"] = nodes[i+1].node_id


class SemchunkNodeParser(NodeParser):
    """
    LlamaIndex NodeParser wrapping Semchunk semantic chunking
    
    Features:
    - Semantic boundary detection
    - Token-aware chunking
    - Overlap for context preservation
    
    Example:
        parser = SemchunkNodeParser(
            target_model="jina-code-embeddings-1.5b",
            chunk_size=1024
        )
        
        documents = [Document(text="Long prose text...")]
        nodes = parser.get_nodes_from_documents(documents)
    """
    
    def __init__(
        self,
        target_model: str = "jina-code-embeddings-1.5b",
        chunk_size: int = 1024,
        chunk_overlap: int = 128,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
    ):
        """Initialize Semchunk NodeParser"""
        super().__init__(
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel
        )
        
        # Initialize V5 unified chunker with Semchunk enabled
        self.chunker = EnhancedUltimateChunkerV5Unified(
            config=ChunkerConfig(
                target_model=target_model,
                chunk_size_tokens=chunk_size,
                chunk_overlap_tokens=chunk_overlap,
                use_semchunk=True,  # Enable Semchunk
                use_tree_sitter=False,
            )
        )
        
        logger.info(
            f"SemchunkNodeParser initialized with {target_model}, "
            f"chunk_size={chunk_size}"
        )
    
    def _parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any
    ) -> List[BaseNode]:
        """Parse text documents with semantic boundaries"""
        all_nodes: List[BaseNode] = []
        
        nodes_with_progress = get_tqdm_iterable(
            nodes, show_progress, "Parsing text with Semchunk"
        )
        
        for node in nodes_with_progress:
            if isinstance(node, Document):
                chunks = self.chunker.create_hierarchical_chunks(
                    text=node.text,
                    filename=node.metadata.get('file_path', '<text>'),
                    strategy_name="hierarchical_balanced"
                )
                
                for chunk in chunks:
                    text_node = TextNode(
                        text=chunk["text"],
                        metadata=chunk.get("metadata", {}),
                        id_=chunk["metadata"].get("chunk_id"),
                    )
                    all_nodes.append(text_node)
        
        if self.include_prev_next_rel:
            self._link_nodes(all_nodes)
        
        return all_nodes
    
    def _link_nodes(self, nodes: List[BaseNode]) -> None:
        """Link consecutive nodes"""
        for i in range(len(nodes)):
            if i > 0:
                nodes[i].relationships["previous"] = nodes[i-1].node_id
            if i < len(nodes) - 1:
                nodes[i].relationships["next"] = nodes[i+1].node_id


class HierarchicalNodeParser(NodeParser):
    """
    Composite LlamaIndex NodeParser combining all strategies
    
    Implements full §3.3 architecture:
    - Docling for PDF/Office/HTML
    - Tree-sitter for code
    - Semchunk for text
    - Automatic routing based on content type
    
    Example:
        parser = HierarchicalNodeParser(
            target_model="jina-code-embeddings-1.5b",
            use_docling=True,
            use_tree_sitter=True,
            use_semchunk=True
        )
        
        documents = [
            Document(text=Path("paper.pdf")),
            Document(text=Path("script.py").read_text()),
            Document(text="Regular text...")
        ]
        
        nodes = parser.get_nodes_from_documents(documents)
    """
    
    def __init__(
        self,
        target_model: str = "jina-code-embeddings-1.5b",
        chunk_size: int = 1024,
        chunk_overlap: int = 128,
        use_docling: bool = True,
        use_tree_sitter: bool = True,
        use_semchunk: bool = True,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
    ):
        """
        Initialize Hierarchical NodeParser with all strategies
        
        Args:
            target_model: Target embedding model
            chunk_size: Maximum chunk size in tokens
            chunk_overlap: Overlap between chunks
            use_docling: Enable Docling for PDFs
            use_tree_sitter: Enable Tree-sitter for code
            use_semchunk: Enable Semchunk for text
            include_metadata: Include source metadata
            include_prev_next_rel: Link consecutive nodes
        """
        super().__init__(
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel
        )
        
        # Initialize V5 unified chunker with all strategies
        self.chunker = EnhancedUltimateChunkerV5Unified(
            config=ChunkerConfig(
                target_model=target_model,
                chunk_size_tokens=chunk_size,
                chunk_overlap_tokens=chunk_overlap,
                use_docling=use_docling,
                use_tree_sitter=use_tree_sitter,
                use_semchunk=use_semchunk,
            )
        )
        
        logger.info(
            f"HierarchicalNodeParser initialized: "
            f"docling={use_docling}, tree_sitter={use_tree_sitter}, "
            f"semchunk={use_semchunk}"
        )
    
    def _parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any
    ) -> List[BaseNode]:
        """
        Parse documents with automatic strategy routing
        
        Routes:
        - PDF/Office/HTML → Docling pipeline
        - Code files → Tree-sitter
        - Text files → Semchunk
        """
        all_nodes: List[BaseNode] = []
        
        nodes_with_progress = get_tqdm_iterable(
            nodes, show_progress, "Parsing with hierarchical strategy"
        )
        
        for node in nodes_with_progress:
            if isinstance(node, Document):
                file_path = node.metadata.get('file_path')
                
                # Route based on file type
                if file_path and Path(file_path).suffix in ['.pdf', '.docx', '.pptx', '.html']:
                    # Use Docling pipeline
                    chunks = self.chunker.process_docling_document(
                        file_path=file_path,
                        output_dir=None
                    )
                elif file_path:
                    # Use smart processing (auto-detects code vs text)
                    chunks = self.chunker.process_file_smart(
                        file_path=file_path,
                        output_dir=None,
                        auto_detect=True
                    )
                else:
                    # Process text directly
                    chunks = self.chunker.create_hierarchical_chunks(
                        text=node.text,
                        filename="<text>",
                        strategy_name="hierarchical_balanced"
                    )
                
                # Convert to TextNode
                for chunk in chunks:
                    text_node = TextNode(
                        text=chunk["text"],
                        metadata=chunk.get("metadata", {}),
                        id_=chunk["metadata"].get("chunk_id"),
                    )
                    
                    if "advanced_scores" in chunk:
                        text_node.metadata["advanced_scores"] = chunk["advanced_scores"]
                    
                    all_nodes.append(text_node)
        
        if self.include_prev_next_rel:
            self._link_nodes(all_nodes)
        
        return all_nodes
    
    def _link_nodes(self, nodes: List[BaseNode]) -> None:
        """Link consecutive nodes with prev/next relationships"""
        for i in range(len(nodes)):
            if i > 0:
                nodes[i].relationships["previous"] = nodes[i-1].node_id
            if i < len(nodes) - 1:
                nodes[i].relationships["next"] = nodes[i+1].node_id


# Usage example
if __name__ == "__main__":
    from llama_index.core import Document
    
    # Example 1: Hierarchical parser (all strategies)
    parser = HierarchicalNodeParser(
        target_model="jina-code-embeddings-1.5b",
        chunk_size=1024,
        use_docling=True,
        use_tree_sitter=True,
        use_semchunk=True
    )
    
    # Create test documents
    documents = [
        Document(
            text="# Test Document\n\nThis is a test document with multiple paragraphs...",
            metadata={"file_path": "test.md"}
        )
    ]
    
    # Parse into nodes
    nodes = parser.get_nodes_from_documents(documents)
    
    print(f"Generated {len(nodes)} nodes")
    for i, node in enumerate(nodes[:3]):
        print(f"\nNode {i}:")
        print(f"  Text: {node.text[:100]}...")
        print(f"  Metadata keys: {list(node.metadata.keys())}")