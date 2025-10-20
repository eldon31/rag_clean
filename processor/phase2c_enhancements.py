#!/usr/bin/env python3
"""
Phase 2C Enhancements for Enhanced Ultimate Chunker V5

Implements advanced Docling features:
- Cross-reference resolution with chunk ID mapping
- Parent-child hierarchy linking
- Figure image saving to disk
- Cell-level table indexing

These enhancements are separate from the main chunker to:
1. Maintain stability of core chunking
2. Allow opt-in usage
3. Enable independent testing
4. Provide clear separation of concerns

Usage:
    from processor.phase2c_enhancements import Phase2CEnhancer
    
    enhancer = Phase2CEnhancer(chunker)
    enhanced_chunks = enhancer.enhance_chunks(
        chunks=chunks,
        figures=figures,
        text=original_text,
        figures_output_dir="figures"
    )
"""

from __future__ import annotations

import logging
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class Phase2CEnhancer:
    """
    Phase 2C enhancement module for Enhanced Ultimate Chunker V5.
    
    Provides:
    - Cross-reference resolution (maps references to chunk IDs)
    - Parent-child hierarchy linking
    - Figure image saving
    - Cell-level table indexing
    
    Example:
        enhancer = Phase2CEnhancer(chunker)
        
        # Apply all enhancements
        enhanced_chunks = enhancer.enhance_chunks(
            chunks=chunks,
            figures=figures,
            text=original_text,
            figures_output_dir="figures"
        )
        
        # Or apply individually
        enhancer.resolve_cross_references(chunks, original_text)
        enhancer.build_hierarchy_links(chunks)
        enhancer.save_figure_images(chunks, figures, "figures")
        enhancer.enhance_table_indexing(chunks)
    """
    
    def __init__(self, chunker: Any):
        """
        Initialize Phase 2C enhancer.
        
        Args:
            chunker: EnhancedUltimateChunkerV5Unified instance
        """
        self.chunker = chunker
        self.stats = {
            "cross_references_resolved": 0,
            "parent_child_links_created": 0,
            "figures_saved": 0,
            "tables_enhanced": 0,
        }
    
    def enhance_chunks(
        self,
        chunks: List[Dict[str, Any]],
        figures: Optional[List[Dict[str, Any]]] = None,
        text: Optional[str] = None,
        figures_output_dir: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Apply all Phase 2C enhancements to chunks.
        
        Args:
            chunks: List of chunk dictionaries
            figures: List of figure metadata (for figure saving)
            text: Original document text (for cross-reference resolution)
            figures_output_dir: Directory to save figures
        
        Returns:
            Enhanced chunks with all Phase 2C features
        """
        logger.info("Applying Phase 2C enhancements...")
        
        # Enhancement 1: Resolve cross-references
        if text:
            self.resolve_cross_references(chunks, text)
            logger.info(f"  ✓ Cross-references: {self.stats['cross_references_resolved']} resolved")
        
        # Enhancement 2: Build hierarchy links (Task 3.5: honor preserve_hierarchy flag)
        if self.chunker.config.preserve_hierarchy:
            self.build_hierarchy_links(chunks)
            logger.info(f"  ✓ Hierarchy links: {self.stats['parent_child_links_created']} created")
        else:
            logger.info(f"  ⊘ Hierarchy links skipped (preserve_hierarchy=False)")
        
        # Enhancement 3: Save figure images
        if figures and figures_output_dir:
            self.save_figure_images(chunks, figures, figures_output_dir)
            logger.info(f"  ✓ Figures saved: {self.stats['figures_saved']} images")
        
        # Enhancement 4: Enhance table indexing
        self.enhance_table_indexing(chunks)
        logger.info(f"  ✓ Tables enhanced: {self.stats['tables_enhanced']} tables")
        
        logger.info("✓ Phase 2C enhancements complete")
        return chunks
    
    def resolve_cross_references(
        self,
        chunks: List[Dict[str, Any]],
        text: str
    ) -> List[Dict[str, Any]]:
        """
        Resolve cross-references to chunk IDs (NOT simplified placeholders).
        
        Detects references like:
        - "See Section 3.2"
        - "[Chapter 5](#chapter-5)"
        - "Table 2 shows..."
        - "As discussed in Introduction..."
        
        Maps reference text → chunk IDs containing that content.
        
        Args:
            chunks: List of chunk dictionaries
            text: Original document text
        
        Returns:
            Chunks with cross_references field populated
        """
        # Build chunk index: heading/section → chunk_id
        chunk_index: Dict[str, str] = {}
        
        for chunk in chunks:
            metadata = chunk.get("metadata", {})
            chunk_id = metadata.get("chunk_id", "")
            
            # Index by section path elements
            section_path = metadata.get("section_path", [])
            for section in section_path:
                if section:
                    chunk_index[section.lower()] = chunk_id
            
            # Index by heading text
            heading = metadata.get("heading_text", "")
            if heading:
                chunk_index[heading.lower()] = chunk_id
            
            # Index by table/figure IDs
            if metadata.get("is_table_chunk"):
                table_id = metadata.get("table_id", "")
                if table_id:
                    chunk_index[table_id.lower()] = chunk_id
            
            if metadata.get("is_figure_chunk"):
                figure_id = metadata.get("figure_id", "")
                if figure_id:
                    chunk_index[figure_id.lower()] = chunk_id
        
        # Detect references in text
        reference_patterns = [
            r"[Ss]ee [Ss]ection ([\d\.]+)",
            r"[Ss]ee [Cc]hapter (\d+)",
            r"\[([^\]]+)\]\(#([^\)]+)\)",  # Markdown links
            r"[Tt]able (\d+)",
            r"[Ff]igure (\d+)",
            r"[Aa]s (?:discussed|mentioned|shown) in ([^,.;]+)",
        ]
        
        references_found: Dict[str, List[str]] = {}
        reverse_references: Dict[str, List[str]] = {}  # target → sources
        
        for chunk in chunks:
            chunk_id = chunk["metadata"].get("chunk_id", "")
            chunk_text = chunk.get("text", "")
            chunk_refs: List[str] = []
            
            # Search for references in chunk text
            for pattern in reference_patterns:
                matches = re.findall(pattern, chunk_text, re.IGNORECASE)
                
                for match in matches:
                    # Handle different match types
                    if isinstance(match, tuple):
                        ref_text = match[0] if match[0] else match[1]
                    else:
                        ref_text = match
                    
                    # Try to resolve reference to chunk ID
                    target_chunk_id = self._resolve_reference_to_chunk(
                        ref_text, chunk_index
                    )
                    
                    if target_chunk_id and target_chunk_id != chunk_id:
                        if target_chunk_id not in chunk_refs:
                            chunk_refs.append(target_chunk_id)
                        
                        # Build reverse index
                        if target_chunk_id not in reverse_references:
                            reverse_references[target_chunk_id] = []
                        if chunk_id not in reverse_references[target_chunk_id]:
                            reverse_references[target_chunk_id].append(chunk_id)
            
            if chunk_refs:
                references_found[chunk_id] = chunk_refs
                self.stats["cross_references_resolved"] += len(chunk_refs)
        
        # Add references and reverse references to metadata
        for chunk in chunks:
            metadata = chunk["metadata"]
            chunk_id = metadata.get("chunk_id", "")
            
            # Forward references (this chunk references others)
            metadata["cross_references"] = references_found.get(chunk_id, [])
            
            # Reverse references (other chunks reference this one)
            metadata["referenced_by"] = reverse_references.get(chunk_id, [])
        
        return chunks
    
    def _resolve_reference_to_chunk(
        self,
        ref_text: str,
        chunk_index: Dict[str, str]
    ) -> Optional[str]:
        """
        Resolve reference text to chunk ID using fuzzy matching.
        
        Args:
            ref_text: Reference text (e.g., "Section 3.2", "Introduction")
            chunk_index: Map of section/heading → chunk_id
        
        Returns:
            Chunk ID if found, None otherwise
        """
        ref_lower = ref_text.lower().strip()
        
        # Exact match
        if ref_lower in chunk_index:
            return chunk_index[ref_lower]
        
        # Try fuzzy matching
        best_match = None
        best_score = 0.0
        
        for key, chunk_id in chunk_index.items():
            score = SequenceMatcher(None, ref_lower, key).ratio()
            if score > best_score and score >= 0.7:  # 70% similarity threshold
                best_score = score
                best_match = chunk_id
        
        return best_match
    
    def build_hierarchy_links(
        self,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Build parent-child hierarchy links between chunks.
        
        Populates:
        - parent_chunk_id: ID of parent chunk (higher level)
        - child_chunk_ids: List of child chunk IDs (lower levels)
        
        Logic:
        - Chunks with lower document_level are parents
        - Chunks with higher document_level are children
        - Links are based on section hierarchy
        
        Args:
            chunks: List of chunk dictionaries
        
        Returns:
            Chunks with hierarchy links populated
        """
        # Sort chunks by document order (chunk_index)
        sorted_chunks = sorted(
            chunks,
            key=lambda c: c["metadata"].get("chunk_index", 0)
        )
        
        # Build parent-child relationships
        for i, chunk in enumerate(sorted_chunks):
            metadata = chunk["metadata"]
            level = metadata.get("document_level", 0)
            
            # Skip if level 0 (top-level, no parent)
            if level == 0:
                continue
            
            # Find parent (previous chunk with lower level)
            parent_id = None
            for j in range(i - 1, -1, -1):
                prev_chunk = sorted_chunks[j]
                prev_level = prev_chunk["metadata"].get("document_level", 0)
                
                if prev_level < level:
                    parent_id = prev_chunk["metadata"].get("chunk_id")
                    break
            
            if parent_id:
                metadata["parent_chunk_id"] = parent_id
                self.stats["parent_child_links_created"] += 1
        
        # Build child lists (reverse mapping)
        child_map: Dict[str, List[str]] = {}
        
        for chunk in chunks:
            metadata = chunk["metadata"]
            parent_id = metadata.get("parent_chunk_id")
            chunk_id = metadata.get("chunk_id")
            
            if parent_id:
                if parent_id not in child_map:
                    child_map[parent_id] = []
                child_map[parent_id].append(chunk_id)
        
        # Add child lists to parent chunks
        for chunk in chunks:
            metadata = chunk["metadata"]
            chunk_id = metadata.get("chunk_id")
            metadata["child_chunk_ids"] = child_map.get(chunk_id, [])
        
        return chunks
    
    def save_figure_images(
        self,
        chunks: List[Dict[str, Any]],
        figures: List[Dict[str, Any]],
        output_dir: str
    ) -> List[Dict[str, Any]]:
        """
        Save figure images to disk and update chunk metadata with saved paths.
        
        Args:
            chunks: List of chunk dictionaries
            figures: List of figure metadata from Docling
            output_dir: Directory to save figures
        
        Returns:
            Chunks with figure_saved_path field populated
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Map figure IDs to figure data
        figure_map = {
            fig.get("figure_id"): fig for fig in figures
        }
        
        for chunk in chunks:
            metadata = chunk["metadata"]
            
            # Only process figure chunks
            if not metadata.get("is_figure_chunk"):
                continue
            
            figure_id = metadata.get("figure_id")
            if not figure_id or figure_id not in figure_map:
                continue
            
            figure = figure_map[figure_id]
            source_path = figure.get("path")
            
            if not source_path or not Path(source_path).exists():
                logger.warning(f"Figure source not found: {source_path}")
                continue
            
            try:
                # Copy figure to output directory
                source_file = Path(source_path)
                dest_file = output_path / f"{figure_id}{source_file.suffix}"
                
                shutil.copy2(source_file, dest_file)
                
                # Update metadata with saved path
                metadata["figure_saved_path"] = str(dest_file)
                self.stats["figures_saved"] += 1
                
                logger.debug(f"Saved figure: {dest_file}")
            
            except Exception as e:
                logger.error(f"Failed to save figure {figure_id}: {e}")
        
        return chunks
    
    def enhance_table_indexing(
        self,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Enhance table chunks with cell-level indexing.
        
        Adds:
        - table_headers: List of column headers
        - table_cells: Dict mapping (row, col) → cell content
        - table_cell_index: Flat list of all cell contents for search
        
        Args:
            chunks: List of chunk dictionaries
        
        Returns:
            Chunks with enhanced table metadata
        """
        for chunk in chunks:
            metadata = chunk["metadata"]
            
            # Only process table chunks
            if not metadata.get("is_table_chunk"):
                continue
            
            # Parse markdown table from chunk text
            text = chunk.get("text", "")
            table_data = self._parse_markdown_table(text)
            
            if not table_data:
                continue
            
            headers, rows = table_data
            
            # Add table headers
            metadata["table_headers"] = headers
            
            # Create cell-level index
            cells: Dict[str, str] = {}
            cell_index: List[str] = []
            
            for row_idx, row in enumerate(rows):
                for col_idx, cell in enumerate(row):
                    cell_key = f"r{row_idx}c{col_idx}"
                    cells[cell_key] = cell
                    cell_index.append(cell)
            
            metadata["table_cells"] = cells
            metadata["table_cell_index"] = cell_index
            self.stats["tables_enhanced"] += 1
        
        return chunks
    
    def _parse_markdown_table(
        self,
        text: str
    ) -> Optional[Tuple[List[str], List[List[str]]]]:
        """
        Parse markdown table into headers and rows.
        
        Args:
            text: Chunk text containing markdown table
        
        Returns:
            Tuple of (headers, rows) or None if no table found
        """
        lines = text.split("\n")
        
        # Find table lines (start with |)
        table_lines = [line for line in lines if line.strip().startswith("|")]
        
        if len(table_lines) < 2:  # Need at least header + separator
            return None
        
        # Parse header row
        header_line = table_lines[0]
        headers = [
            cell.strip()
            for cell in header_line.split("|")
            if cell.strip()
        ]
        
        # Parse data rows (skip separator row)
        rows: List[List[str]] = []
        for line in table_lines[2:]:  # Skip header and separator
            cells = [
                cell.strip()
                for cell in line.split("|")
                if cell.strip()
            ]
            if cells:
                rows.append(cells)
        
        return (headers, rows)


def integrate_phase2c_enhancements(
    chunks: List[Dict[str, Any]],
    chunker: Any,
    figures: Optional[List[Dict[str, Any]]] = None,
    text: Optional[str] = None,
    figures_output_dir: str = "figures"
) -> List[Dict[str, Any]]:
    """
    Convenience function to apply all Phase 2C enhancements.
    
    Args:
        chunks: List of chunk dictionaries from chunker
        chunker: EnhancedUltimateChunkerV5Unified instance
        figures: List of figure metadata from Docling
        text: Original document text
        figures_output_dir: Directory to save figures
    
    Returns:
        Enhanced chunks with all Phase 2C features
    
    Example:
        chunks = chunker.process_docling_document("paper.pdf")
        enhanced = integrate_phase2c_enhancements(
            chunks=chunks,
            chunker=chunker,
            figures=docling_figures,
            text=original_text
        )
    """
    enhancer = Phase2CEnhancer(chunker)
    return enhancer.enhance_chunks(
        chunks=chunks,
        figures=figures,
        text=text,
        figures_output_dir=figures_output_dir
    )
