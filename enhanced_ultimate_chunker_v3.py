#!/usr/bin/env python3
"""
🚀 ULTIMATE CHUNKER IMPROVEMENT PLAN
===================================

Based on research from our 9,654-vector knowledge base across:
- Docling: Document structure preservation and hybrid chunking
- Qdrant: Performance optimization and retrieval quality  
- SentenceTransformers: Embedding quality and optimization

KEY INSIGHTS FROM RESEARCH:
===========================

1. **HIERARCHICAL CHUNKING** (Score: 0.598 - Docling)
   - Chunks based on document structure (sections, paragraphs, tables)
   - Preserve document hierarchy for better context
   - Implementation: HierarchicalChunker with sibling element merging

2. **HYBRID CHUNKING** (Score: 0.506 - Docling)
   - Combine structural and text-based chunking approaches
   - Leverage both semantic and structural boundaries
   - Reference: examples/hybrid_chunking.ipynb

3. **OPTIMAL CHUNK SIZES** (Score: 0.549 - Docling)
   - Large chunks (1024-2048 tokens): Better context, may lose precision
   - Small overlap (50-100 tokens): Balance between speed and concept preservation
   - Risk analysis: No overlap = fast but splits concepts

4. **EMBEDDING OPTIMIZATION** (Score: 0.546 - Qdrant)
   - Focus on retrieval quality and vector search performance
   - Use consistent embedding models for indexing and search
   - Implement proper quality metrics and filtering

IMPLEMENTATION STRATEGY:
========================

Phase 1: Enhanced Hierarchical Processing
- Implement true document structure detection
- Add section-aware chunking with heading preservation
- Create parent-child chunk relationships

Phase 2: Hybrid Approach Integration
- Combine semantic boundary detection with structural analysis
- Add table and list-specific chunking strategies
- Implement content-type aware processing

Phase 3: Quality Optimization
- Advanced semantic coherence metrics
- Retrieval quality scoring
- Performance benchmarking against knowledge base

Phase 4: Production Scaling
- Batch processing optimization
- Memory management for large documents
- Parallel processing capabilities

NEXT STEPS:
===========
1. Create EnhancedUltimateChunker v3.0 with hierarchical support
2. Add hybrid chunking capabilities
3. Implement advanced quality metrics
4. Test against our 5-folder knowledge base
5. Benchmark retrieval performance

"""

import os
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import json
import tiktoken
from datetime import datetime
import re

# Advanced imports for v3.0
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class HierarchicalMetadata:
    """Enhanced metadata with hierarchical structure"""
    # Basic chunk info
    chunk_id: str
    source_file: str
    filename: str
    file_extension: str
    chunk_index: int
    
    # Hierarchical structure
    document_level: int           # 0=title, 1=section, 2=subsection, etc.
    parent_chunk_id: Optional[str]
    child_chunk_ids: List[str]
    section_path: List[str]       # ['Chapter 1', 'Section A', 'Subsection i']
    heading_text: str
    
    # Content metrics
    token_count: int
    char_count: int
    start_char: int
    end_char: int
    
    # Quality scores
    semantic_score: float
    structural_score: float       # New: How well it preserves structure
    retrieval_quality: float      # New: Predicted retrieval performance
    
    # Processing info
    chunking_strategy: str
    content_type: str
    embedding_model: str
    processing_timestamp: str

class EnhancedUltimateChunkerV3:
    """
    🏆 ULTIMATE CHUNKER V3.0 - Research-Based Implementation
    
    Implements findings from our 9,654-vector knowledge base:
    - Hierarchical structure preservation (Docling insights)
    - Hybrid chunking approach (structural + semantic)
    - Retrieval quality optimization (Qdrant insights)
    - Advanced embedding techniques (SentenceTransformers)
    """
    
    def __init__(
        self,
        embedding_model: str = "nomic-ai/CodeRankEmbed",
        tokenizer_name: str = "cl100k_base"
    ):
        """Initialize the research-enhanced chunker"""
        
        self.embedding_model_name = embedding_model
        self.embedder = SentenceTransformer(embedding_model, trust_remote_code=True)
        self.tokenizer = tiktoken.get_encoding(tokenizer_name)
        
        # Content type detection for user's specific inputs
        self.content_type_patterns = {
            "mcp_repository": {
                "patterns": ["mcp", "server", "protocol", "tool", "function", "client"],
                "strategy": "hybrid_adaptive",
                "description": "MCP Repositories - Protocol and tool documentation"
            },
            "workflow_documentation": {
                "patterns": ["workflow", "pipeline", "step", "process", "task", "action"],
                "strategy": "hierarchical_balanced", 
                "description": "Workflow Documentation - Process and procedure guides"
            },
            "api_documentation": {
                "patterns": ["api", "endpoint", "request", "response", "parameter", "method"],
                "strategy": "hierarchical_precise",
                "description": "API Documentation - Technical reference materials"
            },
            "programming_language": {
                "patterns": ["function", "class", "variable", "syntax", "import", "def"],
                "strategy": "hybrid_adaptive",
                "description": "Programming Language Documentation - Code and syntax guides"
            },
            "platform_documentation": {
                "patterns": ["platform", "service", "configuration", "setup", "installation"],
                "strategy": "hierarchical_context",
                "description": "Platform Documentation - Setup and configuration guides"
            }
        }
        # Hierarchical chunking strategies (based on research)
        self.chunking_strategies = {
            "hierarchical_precise": {
                "max_tokens": 512,
                "overlap": 50,  # Small overlap as per Docling research
                "preserve_structure": True,
                "min_section_tokens": 100,
                "description": "High precision with structure preservation"
            },
            "hierarchical_balanced": {
                "max_tokens": 1024,  # Optimal range from Docling research
                "overlap": 100,      # Balance between speed and concept preservation
                "preserve_structure": True,
                "min_section_tokens": 200,
                "description": "Balanced context with hierarchy (recommended)"
            },
            "hierarchical_context": {
                "max_tokens": 2048,  # Large chunks for better context (Docling)
                "overlap": 200,
                "preserve_structure": True,
                "min_section_tokens": 300,
                "description": "Maximum context with structural awareness"
            },
            "hybrid_adaptive": {
                "max_tokens": 1024,
                "overlap": 150,      # Hybrid chunking benefit
                "preserve_structure": True,
                "semantic_boundaries": True,
                "min_section_tokens": 150,
                "description": "Hybrid structural + semantic approach (Docling research)"
            },
            "mcp_optimized": {
                "max_tokens": 768,   # Optimized for MCP protocol docs
                "overlap": 75,
                "preserve_structure": True,
                "semantic_boundaries": True,
                "min_section_tokens": 100,
                "description": "Optimized for MCP repositories and protocol documentation"
            },
            "performance_optimized": {
                "max_tokens": 1536,  # Based on SentenceTransformers research
                "overlap": 128,      # Memory optimization
                "preserve_structure": True,
                "semantic_boundaries": True,
                "min_section_tokens": 200,
                "batch_processing": True,
                "description": "Performance optimized with memory management"
            }
        }
        
        # Quality thresholds (research-optimized)
        self.quality_thresholds = {
            "min_semantic_score": 0.65,      # Increased based on Qdrant research
            "min_structural_score": 0.70,    # New metric for structure preservation
            "min_retrieval_quality": 0.60,   # New metric for retrieval performance
            "min_information_density": 0.4
        }
        
        logger.info(f"🏆 Enhanced Ultimate Chunker v3.0 initialized with {embedding_model}")
        logger.info(f"📊 Research-based strategies: {len(self.chunking_strategies)} available")
    
    def detect_document_structure(self, text: str) -> Dict[str, Any]:
        """Detect document structure for optimal chunking"""
        
        structure = {
            "headings": [],
            "content_blocks": [],
            "hierarchy": {},
            "has_headers": bool(re.search(r'^#{1,6}\s', text, re.MULTILINE)),
            "has_code_blocks": '```' in text,
            "has_lists": bool(re.search(r'^\s*[-*+•]\s', text, re.MULTILINE)),
            "has_tables": '|' in text and re.search(r'\|.*\|', text),
            "line_count": text.count('\n'),
            "avg_line_length": len(text) / max(1, text.count('\n')),
            "sections": len(re.findall(r'^#{1,6}\s.*$', text, re.MULTILINE)),
            "paragraphs": len(re.findall(r'\n\s*\n', text)) + 1
        }
        
        # Detect markdown headings
        heading_matches = re.finditer(r'^(#{1,6})\s+(.+)$', text, re.MULTILINE)
        for match in heading_matches:
            level = len(match.group(1))
            title = match.group(2).strip()
            position = match.start()
            
            heading_info = {
                "level": level,
                "title": title,
                "position": position,
                "line": text[:position].count('\n') + 1
            }
            structure["headings"].append(heading_info)
        
        # Build hierarchy structure
        for heading in structure["headings"]:
            level = heading["level"]
            if level not in structure["hierarchy"]:
                structure["hierarchy"][level] = []
            
            # Create section info with expected fields
            section_info = {
                "title": heading["title"],
                "start_line": heading["line"] - 1,  # Convert to 0-based indexing
                "path": f"Level{level}_{heading['title'].replace(' ', '_')}",
                "level": level,
                "position": heading["position"]
            }
            structure["hierarchy"][level].append(section_info)
        
        # Split into content blocks based on headings
        if structure["headings"]:
            for i, heading in enumerate(structure["headings"]):
                start_pos = heading["position"]
                end_pos = structure["headings"][i + 1]["position"] if i + 1 < len(structure["headings"]) else len(text)
                
                content = text[start_pos:end_pos].strip()
                if content:
                    structure["content_blocks"].append({
                        "heading": heading,
                        "content": content,
                        "length": len(content),
                        "start_line": heading["line"],
                        "end_line": text[:end_pos].count('\n') + 1
                    })
        else:
            # No headings, treat as single content block
            structure["content_blocks"].append({
                "heading": None,
                "content": text,
                "length": len(text),
                "start_line": 1,
                "end_line": text.count('\n') + 1
            })
        
        # Determine document complexity
        complexity_score = 0
        if structure["has_headers"]: complexity_score += 2
        if structure["has_code_blocks"]: complexity_score += 2
        if structure["has_lists"]: complexity_score += 1
        if structure["has_tables"]: complexity_score += 1
        if structure["sections"] > 5: complexity_score += 1
        
        structure["complexity"] = "high" if complexity_score > 4 else "medium" if complexity_score > 2 else "low"
        
        return structure

    def auto_detect_content_type(self, text: str, filename: str) -> Tuple[str, str]:
        """
        Auto-detect content type based on user's specific input categories
        
        Returns: (content_type, recommended_strategy)
        """
        
        text_lower = text.lower()
        filename_lower = filename.lower()
        
        # Score each content type
        scores = {}
        for content_type, config in self.content_type_patterns.items():
            score = 0
            
            # Check patterns in text content
            for pattern in config["patterns"]:
                score += text_lower.count(pattern) * 2
                if pattern in filename_lower:
                    score += 5  # Filename match is stronger indicator
            
            scores[content_type] = score
        
        # Find best match
        if scores:
            best_type = max(scores.items(), key=lambda x: x[1])
            if best_type[1] > 3:  # Minimum threshold
                content_type = best_type[0]
                strategy = self.content_type_patterns[content_type]["strategy"]
                logger.info(f"🎯 Auto-detected: {content_type} -> {strategy} strategy")
                return content_type, strategy
        
        # Default fallback
        logger.info("📄 Using default: workflow_documentation -> hierarchical_balanced")
        return "workflow_documentation", "hierarchical_balanced"
    
    def process_file_smart(
        self,
        file_path: str,
        output_dir: Optional[str] = None,
        auto_detect: bool = True,
        strategy_override: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Smart file processing with auto-detection for user's input types
        
        Optimized for:
        - MCP Repositories
        - Workflow Documentation  
        - API Documentation
        - Programming Language Documentation
        - Platform Documentation
        """
        
        try:
            logger.info(f"📋 Smart processing: {file_path}")
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if len(text.strip()) < 50:
                logger.warning(f"⚠️ File too small: {file_path}")
                return []
            
            # Auto-detect content type and strategy
            if auto_detect and not strategy_override:
                content_type, strategy_name = self.auto_detect_content_type(text, file_path)
            else:
                content_type = "general"
                strategy_name = strategy_override or "hierarchical_balanced"
            
            logger.info(f"🎯 Processing as {content_type} with {strategy_name} strategy")
            
            # Create hierarchical chunks with detected strategy
            chunks = self.create_hierarchical_chunks(
                text=text,
                filename=file_path,
                strategy_name=strategy_name,
                preserve_parent_context=True
            )
            
            # Add content type to metadata
            for chunk in chunks:
                chunk["metadata"]["content_type"] = content_type
                chunk["metadata"]["auto_detected"] = auto_detect
            
            # Save results if output directory specified
            if output_dir:
                self._save_chunks(chunks, file_path, output_dir, content_type)
            
            return chunks
            
        except Exception as e:
            logger.error(f"❌ Error in smart processing {file_path}: {e}")
            return []
    
    def _save_chunks(self, chunks: List[Dict[str, Any]], file_path: str, output_dir: str, content_type: str):
        """Save chunks with enhanced metadata"""
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        filename = Path(file_path).stem
        output_file = output_path / f"{filename}_{content_type}_chunks.json"
        
        # Convert any numpy types to Python types for JSON serialization
        for chunk in chunks:
            for key, value in chunk.get("advanced_scores", {}).items():
                if hasattr(value, 'item'):  # numpy type
                    chunk["advanced_scores"][key] = float(value)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Saved {len(chunks)} chunks to {output_file}")

    def process_directory_smart(
        self, 
        input_dir: str, 
        output_dir: str,
        file_extensions: List[str] = ['.md', '.txt', '.rst', '.py', '.js', '.ts', '.json']
    ) -> Dict[str, Any]:
        """
        Process entire directory with smart content detection
        
        Optimized for your input types:
        - MCP Repositories
        - Workflow Documentation
        - API Documentation  
        - Programming Language Documentation
        - Platform Documentation
        """
        
        input_path = Path(input_dir)
        results = {
            "processed_files": 0,
            "total_chunks": 0,
            "content_types": defaultdict(int),
            "strategies_used": defaultdict(int),
            "processing_time": 0,
            "files": []
        }
        
        start_time = datetime.now()
        
        # Find all relevant files
        files = []
        for ext in file_extensions:
            files.extend(input_path.rglob(f"*{ext}"))
        
        logger.info(f"🔍 Found {len(files)} files to process")
        
        for file_path in files:
            try:
                chunks = self.process_file_smart(
                    str(file_path),
                    output_dir=output_dir,
                    auto_detect=True
                )
                
                if chunks:
                    # Update statistics
                    results["processed_files"] += 1
                    results["total_chunks"] += len(chunks)
                    
                    content_type = chunks[0]["metadata"]["content_type"]
                    strategy = chunks[0]["metadata"]["chunking_strategy"]
                    
                    results["content_types"][content_type] += 1
                    results["strategies_used"][strategy] += 1
                    
                    results["files"].append({
                        "file": str(file_path),
                        "chunks": len(chunks),
                        "content_type": content_type,
                        "strategy": strategy
                    })
                    
                    logger.info(f"✅ {file_path.name}: {len(chunks)} chunks ({content_type})")
                
            except Exception as e:
                logger.error(f"❌ Failed to process {file_path}: {e}")
        
        # Calculate processing time
        results["processing_time"] = (datetime.now() - start_time).total_seconds()
        
        # Save summary
        summary_file = Path(output_dir) / "smart_processing_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"🎯 Smart processing complete!")
        logger.info(f"📊 Processed {results['processed_files']} files → {results['total_chunks']} chunks")
        logger.info(f"⏱️ Time: {results['processing_time']:.2f} seconds")
        logger.info(f"📋 Content types: {dict(results['content_types'])}")
        
        return results
        """
        Advanced document structure detection
        
        Based on Docling research: Hierarchical structure preservation
        """
        
        lines = text.split('\n')
        structure = {
            "headings": [],
            "sections": [],
            "hierarchy": defaultdict(list),
            "content_blocks": []
        }
        
        current_section = None
        current_level = 0
        section_stack = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Detect markdown headings
            if stripped.startswith('#'):
                level = len(stripped) - len(stripped.lstrip('#'))
                heading_text = stripped.lstrip('#').strip()
                
                heading_info = {
                    "text": heading_text,
                    "level": level,
                    "line_index": i,
                    "char_position": len('\n'.join(lines[:i]))
                }
                
                structure["headings"].append(heading_info)
                
                # Update section stack for hierarchy
                while len(section_stack) >= level:
                    section_stack.pop()
                
                section_stack.append(heading_text)
                structure["hierarchy"][level].append({
                    "heading": heading_text,
                    "path": section_stack.copy(),
                    "start_line": i
                })
                
                current_level = level
                current_section = heading_text
            
            # Detect other structural elements
            elif stripped.startswith('```'):
                structure["content_blocks"].append({
                    "type": "code_block",
                    "line_index": i,
                    "section": current_section
                })
            elif stripped.startswith('|') and '|' in stripped[1:]:
                structure["content_blocks"].append({
                    "type": "table",
                    "line_index": i,
                    "section": current_section
                })
            elif stripped.startswith(('-', '*', '+')):
                structure["content_blocks"].append({
                    "type": "list_item", 
                    "line_index": i,
                    "section": current_section
                })
        
        return structure
    
    def calculate_structural_score(self, chunk_text: str, structure_info: Dict[str, Any]) -> float:
        """
        Calculate how well the chunk preserves document structure
        
        New metric based on Docling research insights
        """
        
        score = 0.0
        
        # Check if chunk starts/ends at structural boundaries
        lines = chunk_text.split('\n')
        first_line = lines[0].strip() if lines else ""
        last_line = lines[-1].strip() if lines else ""
        
        # Bonus for starting with heading
        if first_line.startswith('#'):
            score += 0.3
        
        # Bonus for complete sections
        heading_count = sum(1 for line in lines if line.strip().startswith('#'))
        if heading_count > 0:
            score += 0.2
        
        # Bonus for preserving lists/tables
        has_complete_list = any(line.strip().startswith(('-', '*', '+')) for line in lines)
        if has_complete_list:
            score += 0.1
        
        # Penalty for cutting mid-sentence (structural boundary respect)
        if not (last_line.endswith('.') or last_line.endswith('!') or last_line.endswith('?') or last_line.startswith('#')):
            score -= 0.2
        
        # Normalize score
        return max(0.0, min(1.0, score + 0.4))  # Base score + bonuses
    
    def calculate_retrieval_quality(self, chunk_text: str) -> float:
        """
        Predict retrieval quality based on Qdrant research insights
        
        Factors: content density, semantic coherence, searchable terms
        """
        
        # Content richness factors
        unique_words = len(set(chunk_text.lower().split()))
        total_words = len(chunk_text.split())
        word_diversity = unique_words / max(total_words, 1) if total_words > 0 else 0
        
        # Searchable content indicators
        has_technical_terms = any(term in chunk_text.lower() for term in [
            'algorithm', 'method', 'process', 'system', 'function', 'model', 
            'implementation', 'optimization', 'performance', 'configuration'
        ])
        
        # Question-answer potential
        has_actionable_content = any(indicator in chunk_text.lower() for indicator in [
            'how to', 'steps', 'example', 'tutorial', 'guide', 'best practice'
        ])
        
        # Length optimization (based on research: 1024-2048 tokens optimal)
        token_count = len(self.tokenizer.encode(chunk_text))
        length_score = 1.0 if 500 <= token_count <= 1500 else max(0.3, 1.0 - abs(token_count - 1000) / 1000)
        
        # Combined retrieval quality score
        quality = (
            word_diversity * 0.3 +
            (0.2 if has_technical_terms else 0) +
            (0.2 if has_actionable_content else 0) +
            length_score * 0.3
        )
        
        return min(1.0, quality)
    
    def create_hierarchical_chunks(
        self,
        text: str,
        filename: str,
        strategy_name: str = "hierarchical_balanced",
        preserve_parent_context: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Create hierarchical chunks with advanced structure preservation
        
        Implementation of Docling + Qdrant + SentenceTransformers research
        """
        
        strategy = self.chunking_strategies[strategy_name]
        max_tokens = strategy["max_tokens"]
        overlap = strategy["overlap"]
        
        # Step 1: Analyze document structure
        structure = self.detect_document_structure(text)
        logger.info(f"📊 Detected {len(structure['headings'])} headings, {len(structure['content_blocks'])} content blocks")
        
        chunks = []
        chunk_index = 0
        
        # Step 2: Process by hierarchical sections
        for level, sections in structure["hierarchy"].items():
            for section_info in sections:
                section_start = section_info["start_line"]
                section_path = section_info["path"]
                
                # Find section content boundaries
                lines = text.split('\n')
                section_lines = []
                
                # Collect lines until next same-level heading
                for i in range(section_start, len(lines)):
                    line = lines[i].strip()
                    
                    # Stop at same or higher level heading
                    if (line.startswith('#') and 
                        len(line) - len(line.lstrip('#')) <= level and
                        i > section_start):
                        break
                    
                    section_lines.append(lines[i])
                
                section_text = '\n'.join(section_lines)
                
                # Skip very small sections
                if len(section_text.strip()) < strategy["min_section_tokens"]:
                    continue
                
                # Step 3: Create chunks from section
                section_chunks = self._chunk_section_content(
                    section_text, 
                    section_path,
                    filename,
                    strategy_name,
                    chunk_index
                )
                
                chunks.extend(section_chunks)
                chunk_index += len(section_chunks)
        
        # Step 4: Quality filtering and enhancement
        high_quality_chunks = []
        for chunk_data in chunks:
            metadata = chunk_data["metadata"]
            
            # Calculate advanced quality scores
            semantic_score = self.calculate_semantic_coherence(chunk_data["text"])
            structural_score = self.calculate_structural_score(chunk_data["text"], structure)
            retrieval_quality = self.calculate_retrieval_quality(chunk_data["text"])
            
            # Update metadata with new scores
            metadata.semantic_score = float(semantic_score)
            metadata.structural_score = float(structural_score)
            metadata.retrieval_quality = float(retrieval_quality)
            
            # Quality filtering based on research thresholds
            if (semantic_score >= self.quality_thresholds["min_semantic_score"] and
                structural_score >= self.quality_thresholds["min_structural_score"] and
                retrieval_quality >= self.quality_thresholds["min_retrieval_quality"]):
                
                chunk_data["metadata"] = asdict(metadata)
                chunk_data["advanced_scores"] = {
                    "semantic": float(semantic_score),
                    "structural": float(structural_score), 
                    "retrieval_quality": float(retrieval_quality),
                    "overall": float((semantic_score + structural_score + retrieval_quality) / 3)
                }
                
                high_quality_chunks.append(chunk_data)
        
        logger.info(f"🎯 Created {len(high_quality_chunks)} high-quality hierarchical chunks from {filename}")
        logger.info(f"📊 Average scores - Semantic: {np.mean([c['advanced_scores']['semantic'] for c in high_quality_chunks]):.3f}")
        logger.info(f"📊 Average scores - Structural: {np.mean([c['advanced_scores']['structural'] for c in high_quality_chunks]):.3f}")
        logger.info(f"📊 Average scores - Retrieval: {np.mean([c['advanced_scores']['retrieval_quality'] for c in high_quality_chunks]):.3f}")
        
        return high_quality_chunks
    
    def _chunk_section_content(
        self,
        section_text: str,
        section_path: List[str],
        filename: str,
        strategy_name: str,
        start_chunk_index: int
    ) -> List[Dict[str, Any]]:
        """Create chunks from a hierarchical section"""
        
        strategy = self.chunking_strategies[strategy_name]
        max_tokens = strategy["max_tokens"]
        overlap = strategy["overlap"]
        
        chunks = []
        sentences = self._split_into_sentences(section_text)
        
        current_chunk = ""
        current_pos = 0
        
        for i, sentence in enumerate(sentences):
            test_chunk = current_chunk + " " + sentence if current_chunk else sentence
            
            if len(self.tokenizer.encode(test_chunk)) <= max_tokens:
                current_chunk = test_chunk
            else:
                # Create chunk with hierarchical metadata
                if current_chunk.strip():
                    chunk_metadata = HierarchicalMetadata(
                        chunk_id=f"{Path(filename).stem}_{start_chunk_index + len(chunks):04d}",
                        source_file=filename,
                        filename=Path(filename).name,
                        file_extension=Path(filename).suffix,
                        chunk_index=start_chunk_index + len(chunks),
                        document_level=len(section_path),
                        parent_chunk_id=None,  # Will be set later if needed
                        child_chunk_ids=[],
                        section_path=section_path,
                        heading_text=section_path[-1] if section_path else "",
                        token_count=len(self.tokenizer.encode(current_chunk)),
                        char_count=len(current_chunk),
                        start_char=current_pos,
                        end_char=current_pos + len(current_chunk),
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
                chunk_id=f"{Path(filename).stem}_{start_chunk_index + len(chunks):04d}",
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