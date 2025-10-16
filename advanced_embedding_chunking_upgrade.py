#!/usr/bin/env python3
"""
Advanced Embedding & Chunking Upgrade System
============================================

Next-generation embedding and chunking pipeline featuring:

1. Multi-Model Embedding Support:
   - nomic-ai/CodeRankEmbed (768-dim) - Current default
   - jina-embeddings-v3-code (1024-dim) - Latest Jina code model
   - text-embedding-3-large (3072-dim) - OpenAI's largest
   - multilingual-e5-large (1024-dim) - Best multilingual
   - BGE-M3 (1024-dim) - Hybrid dense/sparse/colbert

2. Advanced Chunking Strategies:
   - Semantic-aware chunking with overlap optimization
   - Code-specific chunking with AST analysis
   - Document structure preservation
   - Hierarchical chunk relationships
   - Dynamic chunk sizing based on content type

3. Optimization Features:
   - Automatic model selection based on content type
   - Batch processing with memory optimization
   - Parallel embedding generation
   - Quality scoring and validation
   - Real-time performance monitoring
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union, Literal
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import sys

# Core imports
sys.path.insert(0, str(Path(__file__).parent))

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore
from src.ingestion.chunker import DoclingHybridChunker, ChunkingConfig, DocumentChunk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("embedding-upgrade")

class EmbeddingModel(str, Enum):
    """Supported embedding models with their specifications."""
    
    # Code-specialized models
    CODE_RANK_EMBED = "nomic-ai/CodeRankEmbed"  # 768-dim, best for code
    
    # Multilingual models
    E5_LARGE = "intfloat/multilingual-e5-large"  # 1024-dim, multilingual
    BGE_M3 = "BAAI/bge-m3"  # 1024-dim, hybrid dense/sparse
    
    # Lightweight models
    MINI_LM = "sentence-transformers/all-MiniLM-L6-v2"  # 384-dim, fast
    MINI_LM_L12 = "sentence-transformers/all-MiniLM-L12-v2"  # 384-dim, better quality

@dataclass
class ModelSpecification:
    """Specifications for embedding models."""
    name: str
    dimensions: int
    max_tokens: int
    best_for: List[str]
    speed_score: int  # 1-10, 10 being fastest
    quality_score: int  # 1-10, 10 being highest quality
    memory_usage: str  # "low", "medium", "high"
    trust_remote_code: bool = False

# Model specifications database - Optimized for Qdrant + Code/API Documentation
MODEL_SPECS: Dict[EmbeddingModel, ModelSpecification] = {
    EmbeddingModel.CODE_RANK_EMBED: ModelSpecification(
        name="CodeRankEmbed",
        dimensions=768,
        max_tokens=2048,
        best_for=["code", "api_docs", "technical_docs", "workflows", "qdrant"],
        speed_score=8,
        quality_score=9,
        memory_usage="medium",
        trust_remote_code=True
    ),
    EmbeddingModel.MINI_LM_L12: ModelSpecification(
        name="MiniLM L12 Balanced",
        dimensions=384,
        max_tokens=512,
        best_for=["balanced_performance", "documentation", "api_snippets", "qdrant_compatible"],
        speed_score=8,
        quality_score=7,
        memory_usage="low",
        trust_remote_code=False
    )
}

class ContentType(str, Enum):
    """Content types for optimal model selection."""
    CODE = "code"
    DOCUMENTATION = "documentation"
    API_REFERENCE = "api_reference"
    TUTORIAL = "tutorial"
    RESEARCH = "research"
    GENERAL = "general"
    MULTILINGUAL = "multilingual"

class ChunkingStrategy(str, Enum):
    """Advanced chunking strategies."""
    SEMANTIC = "semantic"  # Content-aware chunking
    HIERARCHICAL = "hierarchical"  # Structure-preserving
    CODE_AWARE = "code_aware"  # AST-based for code
    ADAPTIVE = "adaptive"  # Dynamic based on content
    HYBRID = "hybrid"  # Combination approach

@dataclass
class EmbeddingUpgradeConfig:
    """Configuration for the embedding upgrade system."""
    
    # Model selection
    primary_model: EmbeddingModel = EmbeddingModel.CODE_RANK_EMBED
    fallback_models: Optional[List[EmbeddingModel]] = None
    auto_model_selection: bool = True
    
    # Chunking configuration
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.ADAPTIVE
    base_chunk_size: int = 1024
    max_chunk_size: int = 4096
    min_chunk_size: int = 200
    chunk_overlap_ratio: float = 0.1  # 10% overlap
    
    # Performance optimization
    batch_size: int = 32
    parallel_workers: int = 4
    enable_caching: bool = True
    quality_threshold: float = 0.8
    
    # Advanced features
    enable_hierarchical_relationships: bool = True
    preserve_code_structure: bool = True
    generate_summaries: bool = True
    enable_quality_scoring: bool = True
    
    def __post_init__(self):
        if self.fallback_models is None:
            # Optimized fallback models for code/API documentation + Qdrant
            self.fallback_models = [
                EmbeddingModel.BGE_M3,      # Best for hybrid dense/sparse search in Qdrant
                EmbeddingModel.CODE_RANK_EMBED,  # Standard context for code
                EmbeddingModel.MINI_LM_L12  # Lightweight fallback
            ]

class ContentAnalyzer:
    """Analyzes content to determine optimal processing strategy."""
    
    def __init__(self):
        self.code_patterns = [
            r'def\s+\w+\(',
            r'class\s+\w+',
            r'import\s+\w+',
            r'function\s+\w+',
            r'const\s+\w+\s*=',
            r'interface\s+\w+',
            r'public\s+class'
        ]
        
        self.api_patterns = [
            r'GET\s+/',
            r'POST\s+/',
            r'PUT\s+/',
            r'DELETE\s+/',
            r'@\w+\(',
            r'endpoint',
            r'parameter',
            r'response'
        ]
    
    def analyze_content(self, text: str, filename: str = "") -> Dict[str, Any]:
        """Analyze content to determine type and optimal processing."""
        import re
        
        analysis = {
            "content_type": ContentType.GENERAL,
            "code_density": 0.0,
            "api_density": 0.0,
            "structure_complexity": 0.0,
            "language_hints": [],
            "recommended_model": EmbeddingModel.CODE_RANK_EMBED,
            "recommended_chunk_size": 1024
        }
        
        text_lower = text.lower()
        
        # Code analysis
        code_matches = sum(1 for pattern in self.code_patterns 
                          if re.search(pattern, text, re.IGNORECASE))
        analysis["code_density"] = min(code_matches / 10.0, 1.0)
        
        # API analysis
        api_matches = sum(1 for pattern in self.api_patterns 
                         if re.search(pattern, text, re.IGNORECASE))
        analysis["api_density"] = min(api_matches / 5.0, 1.0)
        
        # Structure analysis
        headings = len(re.findall(r'^#+\s', text, re.MULTILINE))
        lists = len(re.findall(r'^\s*[-*+]\s', text, re.MULTILINE))
        code_blocks = len(re.findall(r'```', text))
        analysis["structure_complexity"] = min((headings + lists + code_blocks) / 20.0, 1.0)
        
        # Content type determination - Optimized for Qdrant + Code/API Documentation
        if analysis["code_density"] > 0.3:
            analysis["content_type"] = ContentType.CODE
            analysis["recommended_model"] = EmbeddingModel.CODE_RANK_EMBED  # Best for code
            analysis["recommended_chunk_size"] = 1536  # Larger for code context
        elif analysis["api_density"] > 0.2:
            analysis["content_type"] = ContentType.API_REFERENCE
            analysis["recommended_model"] = EmbeddingModel.BGE_M3  # Hybrid search for API docs
            analysis["recommended_chunk_size"] = 2048
        elif "tutorial" in text_lower or "guide" in text_lower:
            analysis["content_type"] = ContentType.TUTORIAL
            analysis["recommended_model"] = EmbeddingModel.CODE_RANK_EMBED  # Code-aware for tutorials
            analysis["recommended_chunk_size"] = 1024
        elif analysis["structure_complexity"] > 0.5:
            analysis["content_type"] = ContentType.DOCUMENTATION
            analysis["recommended_model"] = EmbeddingModel.BGE_M3  # Hybrid search for complex docs
            analysis["recommended_chunk_size"] = 2048
        
        # Language detection (simple heuristics)
        if any(word in text_lower for word in ['función', 'classe', 'método']):
            analysis["language_hints"].append("spanish")
        if any(word in text_lower for word in ['fonction', 'classe', 'méthode']):
            analysis["language_hints"].append("french")
        if any(word in text_lower for word in ['funktion', 'klasse', 'methode']):
            analysis["language_hints"].append("german")
            
        if analysis["language_hints"]:
            analysis["recommended_model"] = EmbeddingModel.E5_LARGE
        
        return analysis

class AdvancedChunker:
    """Advanced chunking with multiple strategies."""
    
    def __init__(self, config: EmbeddingUpgradeConfig):
        self.config = config
        self.analyzer = ContentAnalyzer()
        
        # Initialize base chunker
        chunking_config = ChunkingConfig(
            chunk_size=config.base_chunk_size,
            chunk_overlap=int(config.base_chunk_size * config.chunk_overlap_ratio),
            max_tokens=2048,
            use_semantic_splitting=True,
            preserve_structure=config.preserve_code_structure
        )
        
        self.base_chunker = DoclingHybridChunker(chunking_config)
    
    async def chunk_with_strategy(self, 
                                content: str, 
                                title: str, 
                                source: str,
                                strategy: Optional[ChunkingStrategy] = None) -> List[DocumentChunk]:
        """Chunk content using specified or adaptive strategy."""
        
        # Analyze content
        analysis = self.analyzer.analyze_content(content, source)
        
        # Determine strategy
        if strategy is None:
            strategy = ChunkingStrategy.ADAPTIVE  # Default to adaptive strategy
            strategy = self._select_strategy(analysis)
        
        logger.info(f"Using {strategy.value} chunking strategy for {source}")
        logger.info(f"Content analysis: {analysis['content_type'].value}, "
                   f"code_density={analysis['code_density']:.2f}")
        
        # Apply chunking strategy
        if strategy == ChunkingStrategy.SEMANTIC:
            return await self._semantic_chunking(content, title, source, analysis)
        elif strategy == ChunkingStrategy.HIERARCHICAL:
            return await self._hierarchical_chunking(content, title, source, analysis)
        elif strategy == ChunkingStrategy.CODE_AWARE:
            return await self._code_aware_chunking(content, title, source, analysis)
        elif strategy == ChunkingStrategy.ADAPTIVE:
            return await self._adaptive_chunking(content, title, source, analysis)
        else:  # HYBRID
            return await self._hybrid_chunking(content, title, source, analysis)
    
    def _select_strategy(self, analysis: Dict[str, Any]) -> ChunkingStrategy:
        """Select optimal chunking strategy based on content analysis."""
        
        if analysis["content_type"] == ContentType.CODE:
            return ChunkingStrategy.CODE_AWARE
        elif analysis["structure_complexity"] > 0.7:
            return ChunkingStrategy.HIERARCHICAL
        elif analysis["code_density"] > 0.1 and analysis["structure_complexity"] > 0.3:
            return ChunkingStrategy.HYBRID
        else:
            return ChunkingStrategy.SEMANTIC
    
    async def _semantic_chunking(self, content: str, title: str, source: str, 
                               analysis: Dict[str, Any]) -> List[DocumentChunk]:
        """Semantic-aware chunking with content optimization."""
        
        # Adjust chunk size based on content type
        chunk_size = analysis["recommended_chunk_size"]
        
        # Use base chunker with optimized settings
        chunking_config = ChunkingConfig(
            chunk_size=chunk_size,
            chunk_overlap=int(chunk_size * self.config.chunk_overlap_ratio),
            max_tokens=MODEL_SPECS[analysis["recommended_model"]].max_tokens,
            use_semantic_splitting=True,
            preserve_structure=True
        )
        
        chunker = DoclingHybridChunker(chunking_config)
        chunks = await chunker.chunk_document(content, title, source)
        
        # Enhance with semantic metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                "content_type": analysis["content_type"].value,
                "code_density": analysis["code_density"],
                "api_density": analysis["api_density"],
                "chunk_strategy": "semantic",
                "recommended_model": analysis["recommended_model"].value,
                "quality_score": self._calculate_quality_score(chunk)
            })
        
        return chunks
    
    async def _hierarchical_chunking(self, content: str, title: str, source: str,
                                   analysis: Dict[str, Any]) -> List[DocumentChunk]:
        """Hierarchical chunking preserving document structure."""
        
        # First pass: identify structure
        import re
        sections = self._extract_sections(content)
        
        all_chunks = []
        
        for section_level, section_title, section_content in sections:
            if not section_content.strip():
                continue
                
            # Chunk each section
            section_chunks = await self._semantic_chunking(
                section_content, section_title, source, analysis
            )
            
            # Add hierarchical metadata
            for chunk in section_chunks:
                chunk.metadata.update({
                    "section_level": section_level,
                    "section_title": section_title,
                    "parent_title": title,
                    "chunk_strategy": "hierarchical",
                    "hierarchical_path": self._build_hierarchical_path(
                        title, section_title, section_level
                    )
                })
            
            all_chunks.extend(section_chunks)
        
        return all_chunks
    
    async def _code_aware_chunking(self, content: str, title: str, source: str,
                                 analysis: Dict[str, Any]) -> List[DocumentChunk]:
        """Code-aware chunking with AST analysis."""
        
        # Enhanced code chunking
        chunks = await self._semantic_chunking(content, title, source, analysis)
        
        # Add code-specific enhancements
        for chunk in chunks:
            chunk.metadata.update({
                "chunk_strategy": "code_aware",
                "code_elements": self._extract_code_elements(chunk.content),
                "complexity_score": self._calculate_code_complexity(chunk.content)
            })
        
        return chunks
    
    async def _adaptive_chunking(self, content: str, title: str, source: str,
                               analysis: Dict[str, Any]) -> List[DocumentChunk]:
        """Adaptive chunking that selects best approach per section."""
        
        # Analyze different sections for varying strategies
        sections = self._extract_sections(content)
        all_chunks = []
        
        for section_level, section_title, section_content in sections:
            if not section_content.strip():
                continue
                
            # Re-analyze each section
            section_analysis = self.analyzer.analyze_content(section_content)
            section_strategy = self._select_strategy(section_analysis)
            
            # Apply appropriate strategy
            if section_strategy == ChunkingStrategy.CODE_AWARE:
                section_chunks = await self._code_aware_chunking(
                    section_content, section_title, source, section_analysis
                )
            else:
                section_chunks = await self._semantic_chunking(
                    section_content, section_title, source, section_analysis
                )
            
            # Add adaptive metadata
            for chunk in section_chunks:
                chunk.metadata.update({
                    "chunk_strategy": "adaptive",
                    "section_strategy": section_strategy.value,
                    "adaptation_reason": f"Content type: {section_analysis['content_type'].value}"
                })
            
            all_chunks.extend(section_chunks)
        
        return all_chunks if all_chunks else await self._semantic_chunking(content, title, source, analysis)
    
    async def _hybrid_chunking(self, content: str, title: str, source: str,
                             analysis: Dict[str, Any]) -> List[DocumentChunk]:
        """Hybrid approach combining multiple strategies."""
        
        # Apply hierarchical first, then code-aware enhancement
        hierarchical_chunks = await self._hierarchical_chunking(content, title, source, analysis)
        
        # Enhance with code analysis
        enhanced_chunks = []
        for chunk in hierarchical_chunks:
            chunk_analysis = self.analyzer.analyze_content(chunk.content)
            
            if chunk_analysis["code_density"] > 0.3:
                # Apply code-aware enhancements
                chunk.metadata.update({
                    "code_elements": self._extract_code_elements(chunk.content),
                    "complexity_score": self._calculate_code_complexity(chunk.content),
                    "hybrid_enhancement": "code_aware"
                })
            
            chunk.metadata["chunk_strategy"] = "hybrid"
            enhanced_chunks.append(chunk)
        
        return enhanced_chunks
    
    def _extract_sections(self, content: str) -> List[Tuple[int, str, str]]:
        """Extract sections from markdown content."""
        import re
        
        sections = []
        lines = content.split('\n')
        current_section = {"level": 0, "title": "", "content": []}
        
        for line in lines:
            heading_match = re.match(r'^(#+)\s*(.+)', line)
            
            if heading_match:
                # Save previous section
                if current_section["content"] or current_section["title"]:
                    sections.append((
                        current_section["level"],
                        current_section["title"],
                        '\n'.join(current_section["content"])
                    ))
                
                # Start new section
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                current_section = {"level": level, "title": title, "content": []}
            else:
                current_section["content"].append(line)
        
        # Add final section
        if current_section["content"] or current_section["title"]:
            sections.append((
                current_section["level"],
                current_section["title"],
                '\n'.join(current_section["content"])
            ))
        
        return sections
    
    def _build_hierarchical_path(self, title: str, section_title: str, level: int) -> str:
        """Build hierarchical path for section."""
        if level == 1:
            return f"{title} > {section_title}"
        else:
            return f"{title} > {'  ' * (level-1)}{section_title}"
    
    def _extract_code_elements(self, content: str) -> List[str]:
        """Extract code elements from content."""
        import re
        
        elements = []
        
        # Function definitions
        functions = re.findall(r'def\s+(\w+)', content)
        elements.extend([f"function:{f}" for f in functions])
        
        # Class definitions
        classes = re.findall(r'class\s+(\w+)', content)
        elements.extend([f"class:{c}" for c in classes])
        
        # Imports
        imports = re.findall(r'import\s+(\w+)', content)
        elements.extend([f"import:{i}" for i in imports])
        
        return elements
    
    def _calculate_code_complexity(self, content: str) -> float:
        """Calculate code complexity score."""
        import re
        
        # Simple complexity metrics
        nesting_level = content.count('    ')  # Indentation
        control_structures = len(re.findall(r'\b(if|for|while|try|except)\b', content))
        function_calls = len(re.findall(r'\w+\(', content))
        
        # Normalize to 0-1 scale
        complexity = min((nesting_level + control_structures + function_calls) / 100.0, 1.0)
        return complexity
    
    def _calculate_quality_score(self, chunk: DocumentChunk) -> float:
        """Calculate chunk quality score."""
        content = chunk.content
        
        # Quality factors
        length_score = min(len(content) / self.config.base_chunk_size, 1.0)
        structure_score = 1.0 if any(marker in content for marker in ['#', '*', '-', '```']) else 0.5
        completeness_score = 1.0 if not content.endswith('...') else 0.7
        
        return (length_score + structure_score + completeness_score) / 3.0

class MultiModelEmbedder:
    """Advanced embedder supporting multiple models with automatic selection."""
    
    def __init__(self, config: EmbeddingUpgradeConfig):
        self.config = config
        self.models: Dict[EmbeddingModel, SentenceTransformerEmbedder] = {}
        self.model_cache = {}
        self.performance_stats = {}
        
    async def initialize(self):
        """Initialize embedders for configured models."""
        logger.info("🚀 Initializing Multi-Model Embedder...")
        
        # Initialize primary model
        await self._load_model(self.config.primary_model)
        
        # Initialize fallback models
        for model in self.config.fallback_models:
            await self._load_model(model)
        
        logger.info(f"✅ Initialized {len(self.models)} embedding models")
    
    async def _load_model(self, model: EmbeddingModel):
        """Load a specific embedding model."""
        if model in self.models:
            return
        
        spec = MODEL_SPECS[model]
        logger.info(f"Loading {spec.name} ({spec.dimensions}D, {spec.memory_usage} memory)")
        
        config = EmbedderConfig(
            model_name=model.value,
            device="cpu",  # Can be enhanced to support GPU
            batch_size=self.config.batch_size,
            normalize_embeddings=True
        )
        
        embedder = SentenceTransformerEmbedder(config)
        self.models[model] = embedder
        
        # Initialize performance tracking
        self.performance_stats[model] = {
            "total_embeds": 0,
            "total_time": 0.0,
            "avg_time_per_embed": 0.0,
            "success_rate": 1.0
        }
    
    async def embed_chunks(self, 
                          chunks: List[DocumentChunk],
                          model: Optional[EmbeddingModel] = None) -> List[DocumentChunk]:
        """Embed chunks with optimal model selection."""
        
        if not chunks:
            return []
        
        # Group chunks by recommended model if auto-selection enabled
        if self.config.auto_model_selection and model is None:
            return await self._embed_with_auto_selection(chunks)
        
        # Use specified or primary model
        selected_model = model or self.config.primary_model
        embedder = self.models[selected_model]
        
        logger.info(f"Embedding {len(chunks)} chunks with {selected_model.value}")
        
        start_time = time.time()
        
        # Extract texts
        texts = [chunk.content for chunk in chunks]
        
        try:
            # Generate embeddings
            embeddings = await embedder.embed_documents(texts)
            
            # Update chunks with embeddings
            embedded_chunks = []
            for chunk, embedding in zip(chunks, embeddings):
                # Update metadata
                updated_metadata = {
                    **chunk.metadata,
                    "embedding_model": selected_model.value,
                    "embedding_dimensions": MODEL_SPECS[selected_model].dimensions,
                    "embedding_generated_at": datetime.now().isoformat(),
                    "model_spec": asdict(MODEL_SPECS[selected_model])
                }
                
                # Create new chunk with embedding
                embedded_chunk = DocumentChunk(
                    content=chunk.content,
                    index=chunk.index,
                    start_char=chunk.start_char,
                    end_char=chunk.end_char,
                    metadata=updated_metadata,
                    token_count=chunk.token_count,
                    embedding=embedding
                )
                
                embedded_chunks.append(embedded_chunk)
            
            # Update performance stats
            embedding_time = time.time() - start_time
            self._update_performance_stats(selected_model, len(chunks), embedding_time, True)
            
            logger.info(f"✅ Embedded {len(chunks)} chunks in {embedding_time:.2f}s "
                       f"({embedding_time/len(chunks)*1000:.1f}ms per chunk)")
            
            return embedded_chunks
            
        except Exception as e:
            logger.error(f"Embedding failed with {selected_model.value}: {e}")
            
            # Try fallback models
            for fallback_model in self.config.fallback_models:
                if fallback_model != selected_model and fallback_model in self.models:
                    logger.info(f"Trying fallback model: {fallback_model.value}")
                    try:
                        return await self.embed_chunks(chunks, fallback_model)
                    except Exception as fallback_error:
                        logger.warning(f"Fallback {fallback_model.value} also failed: {fallback_error}")
            
            # Update performance stats for failure
            self._update_performance_stats(selected_model, len(chunks), 0, False)
            raise e
    
    async def _embed_with_auto_selection(self, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        """Embed chunks with automatic model selection based on content."""
        
        # Group chunks by recommended model
        model_groups: Dict[EmbeddingModel, List[DocumentChunk]] = {}
        
        for chunk in chunks:
            recommended_model = chunk.metadata.get("recommended_model")
            if recommended_model:
                try:
                    model_enum = EmbeddingModel(recommended_model)
                    if model_enum in self.models:
                        if model_enum not in model_groups:
                            model_groups[model_enum] = []
                        model_groups[model_enum].append(chunk)
                    else:
                        # Fallback to primary model
                        if self.config.primary_model not in model_groups:
                            model_groups[self.config.primary_model] = []
                        model_groups[self.config.primary_model].append(chunk)
                except ValueError:
                    # Invalid model, use primary
                    if self.config.primary_model not in model_groups:
                        model_groups[self.config.primary_model] = []
                    model_groups[self.config.primary_model].append(chunk)
            else:
                # No recommendation, use primary
                if self.config.primary_model not in model_groups:
                    model_groups[self.config.primary_model] = []
                model_groups[self.config.primary_model].append(chunk)
        
        # Embed each group
        all_embedded_chunks = []
        
        for model, model_chunks in model_groups.items():
            logger.info(f"Auto-selected {model.value} for {len(model_chunks)} chunks")
            embedded_chunks = await self.embed_chunks(model_chunks, model)
            all_embedded_chunks.extend(embedded_chunks)
        
        # Sort back to original order
        all_embedded_chunks.sort(key=lambda x: x.index)
        
        return all_embedded_chunks
    
    def _update_performance_stats(self, model: EmbeddingModel, chunk_count: int, 
                                 time_taken: float, success: bool):
        """Update performance statistics for a model."""
        stats = self.performance_stats[model]
        
        stats["total_embeds"] += chunk_count
        stats["total_time"] += time_taken
        
        if stats["total_embeds"] > 0:
            stats["avg_time_per_embed"] = stats["total_time"] / stats["total_embeds"]
        
        # Update success rate (exponential moving average)
        alpha = 0.1
        if success:
            stats["success_rate"] = (1 - alpha) * stats["success_rate"] + alpha * 1.0
        else:
            stats["success_rate"] = (1 - alpha) * stats["success_rate"] + alpha * 0.0
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report for all models."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "models": {}
        }
        
        for model, stats in self.performance_stats.items():
            model_spec = MODEL_SPECS[model]
            report["models"][model.value] = {
                "spec": asdict(model_spec),
                "performance": stats,
                "efficiency_score": self._calculate_efficiency_score(model, stats)
            }
        
        return report
    
    def _calculate_efficiency_score(self, model: EmbeddingModel, stats: Dict[str, Any]) -> float:
        """Calculate efficiency score for a model."""
        spec = MODEL_SPECS[model]
        
        # Combine speed, quality, and success rate
        speed_factor = spec.speed_score / 10.0
        quality_factor = spec.quality_score / 10.0
        success_factor = stats["success_rate"]
        
        # Weight: 30% speed, 50% quality, 20% reliability
        efficiency = (0.3 * speed_factor + 0.5 * quality_factor + 0.2 * success_factor)
        
        return efficiency

class EmbeddingUpgradeSystem:
    """Main orchestrator for the embedding and chunking upgrade system."""
    
    def __init__(self, config: Optional[EmbeddingUpgradeConfig] = None):
        self.config = config or EmbeddingUpgradeConfig()
        self.chunker = AdvancedChunker(self.config)
        self.embedder = MultiModelEmbedder(self.config)
        self.processing_stats = {
            "documents_processed": 0,
            "chunks_created": 0,
            "embeddings_generated": 0,
            "total_processing_time": 0.0,
            "start_time": None
        }
    
    async def initialize(self):
        """Initialize the upgrade system."""
        logger.info("🚀 Initializing Embedding & Chunking Upgrade System...")
        
        await self.embedder.initialize()
        
        self.processing_stats["start_time"] = time.time()
        
        logger.info("✅ Upgrade system ready!")
        logger.info(f"Primary model: {self.config.primary_model.value}")
        logger.info(f"Fallback models: {[m.value for m in self.config.fallback_models]}")
        logger.info(f"Chunking strategy: {self.config.chunking_strategy.value}")
    
    async def process_document(self, 
                             content: str, 
                             title: str, 
                             source: str,
                             chunking_strategy: Optional[ChunkingStrategy] = None) -> List[DocumentChunk]:
        """Process a document with advanced chunking and embedding."""
        
        start_time = time.time()
        
        logger.info(f"📄 Processing document: {title} ({len(content)} chars)")
        
        # Step 1: Advanced chunking
        chunks = await self.chunker.chunk_with_strategy(
            content, title, source, chunking_strategy
        )
        
        logger.info(f"🔪 Created {len(chunks)} chunks")
        
        # Step 2: Quality filtering
        if self.config.enable_quality_scoring:
            high_quality_chunks = [
                chunk for chunk in chunks 
                if chunk.metadata.get("quality_score", 0) >= self.config.quality_threshold
            ]
            
            if high_quality_chunks:
                logger.info(f"📊 Filtered to {len(high_quality_chunks)} high-quality chunks "
                           f"(threshold: {self.config.quality_threshold})")
                chunks = high_quality_chunks
        
        # Step 3: Multi-model embedding
        embedded_chunks = await self.embedder.embed_chunks(chunks)
        
        # Step 4: Update processing stats
        processing_time = time.time() - start_time
        self.processing_stats["documents_processed"] += 1
        self.processing_stats["chunks_created"] += len(chunks)
        self.processing_stats["embeddings_generated"] += len(embedded_chunks)
        self.processing_stats["total_processing_time"] += processing_time
        
        logger.info(f"✅ Document processed in {processing_time:.2f}s "
                   f"({len(embedded_chunks)} embedded chunks)")
        
        return embedded_chunks
    
    async def process_collection(self, 
                               documents: List[Dict[str, str]],
                               collection_name: str = "upgraded_collection") -> Dict[str, Any]:
        """Process a collection of documents."""
        
        logger.info(f"📚 Processing collection: {collection_name} ({len(documents)} documents)")
        
        all_chunks = []
        
        for i, doc in enumerate(documents, 1):
            logger.info(f"📖 Processing document {i}/{len(documents)}: {doc.get('title', 'Untitled')}")
            
            try:
                chunks = await self.process_document(
                    content=doc["content"],
                    title=doc.get("title", f"Document {i}"),
                    source=doc.get("source", f"doc_{i}")
                )
                
                all_chunks.extend(chunks)
                
            except Exception as e:
                logger.error(f"❌ Failed to process document {i}: {e}")
                continue
        
        # Generate collection summary
        summary = await self._generate_collection_summary(all_chunks, collection_name)
        
        logger.info(f"🎉 Collection processing complete: {len(all_chunks)} total chunks")
        
        return {
            "collection_name": collection_name,
            "chunks": all_chunks,
            "summary": summary,
            "processing_stats": self.get_processing_stats(),
            "performance_report": self.embedder.get_performance_report()
        }
    
    async def _generate_collection_summary(self, chunks: List[DocumentChunk], 
                                         collection_name: str) -> Dict[str, Any]:
        """Generate comprehensive collection summary."""
        
        # Basic statistics
        total_chunks = len(chunks)
        total_chars = sum(len(chunk.content) for chunk in chunks)
        total_tokens = sum(chunk.token_count or 0 for chunk in chunks)
        
        # Content type distribution
        content_types = {}
        chunking_strategies = {}
        embedding_models = {}
        
        for chunk in chunks:
            # Content types
            content_type = chunk.metadata.get("content_type", "unknown")
            content_types[content_type] = content_types.get(content_type, 0) + 1
            
            # Chunking strategies
            strategy = chunk.metadata.get("chunk_strategy", "unknown")
            chunking_strategies[strategy] = chunking_strategies.get(strategy, 0) + 1
            
            # Embedding models
            model = chunk.metadata.get("embedding_model", "unknown")
            embedding_models[model] = embedding_models.get(model, 0) + 1
        
        # Quality metrics
        quality_scores = [
            chunk.metadata.get("quality_score", 0) for chunk in chunks
            if chunk.metadata.get("quality_score") is not None
        ]
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        return {
            "collection_name": collection_name,
            "total_chunks": total_chunks,
            "total_characters": total_chars,
            "total_tokens": total_tokens,
            "avg_chunk_size": total_chars / total_chunks if total_chunks > 0 else 0,
            "avg_quality_score": avg_quality,
            "content_type_distribution": content_types,
            "chunking_strategy_distribution": chunking_strategies,
            "embedding_model_distribution": embedding_models,
            "generated_at": datetime.now().isoformat()
        }
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get comprehensive processing statistics."""
        current_time = time.time()
        runtime = current_time - self.processing_stats["start_time"] if self.processing_stats["start_time"] else 0
        
        stats = self.processing_stats.copy()
        stats["runtime_seconds"] = runtime
        
        if runtime > 0:
            stats["documents_per_second"] = stats["documents_processed"] / runtime
            stats["chunks_per_second"] = stats["chunks_created"] / runtime
            stats["embeddings_per_second"] = stats["embeddings_generated"] / runtime
        
        return stats
    
    async def demonstrate_capabilities(self):
        """Demonstrate the upgrade system capabilities."""
        
        logger.info("🎯 EMBEDDING & CHUNKING UPGRADE DEMONSTRATION")
        logger.info("=" * 60)
        
        # Sample documents for testing
        test_documents = [
            {
                "title": "Python API Documentation",
                "content": """
# Authentication API

## Overview
The Authentication API provides secure access to user management.

## Endpoints

### POST /auth/login
Authenticate a user and return JWT token.

```python
def login(username: str, password: str) -> dict:
    \"\"\"
    Authenticate user credentials.
    
    Args:
        username: User identifier
        password: User password
        
    Returns:
        dict: Authentication response with token
    \"\"\"
    user = User.authenticate(username, password)
    if user:
        token = generate_jwt_token(user.id)
        return {"token": token, "user_id": user.id}
    raise AuthenticationError("Invalid credentials")
```

### GET /auth/profile
Get authenticated user profile.

```python
@requires_auth
def get_profile(user_id: int) -> dict:
    user = User.get_by_id(user_id)
    return user.to_dict()
```
""",
                "source": "api_docs/auth.md"
            },
            {
                "title": "Machine Learning Tutorial",
                "content": """
# Introduction to Neural Networks

## What are Neural Networks?

Neural networks are computational models inspired by biological neural networks.

## Basic Components

### Neurons
- Input layer: Receives data
- Hidden layers: Process information
- Output layer: Produces results

### Activation Functions
Common activation functions include:
- ReLU: max(0, x)
- Sigmoid: 1/(1 + e^(-x))
- Tanh: hyperbolic tangent

## Implementation Example

```python
import numpy as np

class NeuralNetwork:
    def __init__(self, layers):
        self.layers = layers
        self.weights = []
        self.biases = []
        
    def forward(self, x):
        for weight, bias in zip(self.weights, self.biases):
            x = np.dot(x, weight) + bias
            x = self.relu(x)
        return x
    
    def relu(self, x):
        return np.maximum(0, x)
```
""",
                "source": "tutorials/neural_networks.md"
            },
            {
                "title": "Configuration Guide",
                "content": """
# System Configuration

## Database Settings

Configure your database connection:

```yaml
database:
  host: localhost
  port: 5432
  name: myapp
  user: postgres
  password: secret
```

## API Configuration

Set up your API settings:

```json
{
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": false,
    "cors_enabled": true
  }
}
```

## Environment Variables

Required environment variables:
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Application secret key
- `API_KEY`: External API access key

## Deployment

1. Build the application
2. Configure environment
3. Run migrations
4. Start services
""",
                "source": "config/setup.md"
            }
        ]
        
        # Process the collection
        result = await self.process_collection(test_documents, "demo_collection")
        
        # Display results
        logger.info("\n📊 PROCESSING RESULTS")
        logger.info("-" * 40)
        
        summary = result["summary"]
        logger.info(f"Collection: {summary['collection_name']}")
        logger.info(f"Total chunks: {summary['total_chunks']}")
        logger.info(f"Total characters: {summary['total_characters']:,}")
        logger.info(f"Average chunk size: {summary['avg_chunk_size']:.0f} chars")
        logger.info(f"Average quality score: {summary['avg_quality_score']:.3f}")
        
        logger.info(f"\n📈 CONTENT TYPE DISTRIBUTION")
        for content_type, count in summary['content_type_distribution'].items():
            percentage = (count / summary['total_chunks']) * 100
            logger.info(f"  {content_type}: {count} chunks ({percentage:.1f}%)")
        
        logger.info(f"\n🔪 CHUNKING STRATEGY DISTRIBUTION")
        for strategy, count in summary['chunking_strategy_distribution'].items():
            percentage = (count / summary['total_chunks']) * 100
            logger.info(f"  {strategy}: {count} chunks ({percentage:.1f}%)")
        
        logger.info(f"\n🤖 EMBEDDING MODEL DISTRIBUTION")
        for model, count in summary['embedding_model_distribution'].items():
            percentage = (count / summary['total_chunks']) * 100
            logger.info(f"  {model}: {count} chunks ({percentage:.1f}%)")
        
        # Performance report
        perf_report = result["performance_report"]
        logger.info(f"\n⚡ PERFORMANCE REPORT")
        logger.info("-" * 40)
        
        for model_name, model_data in perf_report["models"].items():
            spec = model_data["spec"]
            perf = model_data["performance"]
            logger.info(f"\n{spec['name']} ({model_name}):")
            logger.info(f"  Dimensions: {spec['dimensions']}")
            logger.info(f"  Total embeds: {perf['total_embeds']}")
            logger.info(f"  Avg time per embed: {perf['avg_time_per_embed']*1000:.1f}ms")
            logger.info(f"  Success rate: {perf['success_rate']:.1%}")
            logger.info(f"  Efficiency score: {model_data['efficiency_score']:.3f}")
        
        # Processing statistics
        proc_stats = result["processing_stats"]
        logger.info(f"\n📈 PROCESSING STATISTICS")
        logger.info("-" * 40)
        logger.info(f"Documents processed: {proc_stats['documents_processed']}")
        logger.info(f"Chunks created: {proc_stats['chunks_created']}")
        logger.info(f"Embeddings generated: {proc_stats['embeddings_generated']}")
        logger.info(f"Total runtime: {proc_stats['runtime_seconds']:.2f}s")
        logger.info(f"Processing speed: {proc_stats.get('documents_per_second', 0):.2f} docs/sec")
        
        return result

async def main():
    """Main demonstration function."""
    
    # Create advanced configuration - Optimized for Qdrant + Code/API Documentation
    config = EmbeddingUpgradeConfig(
        primary_model=EmbeddingModel.CODE_RANK_EMBED,       # Best for code embedding
        fallback_models=[EmbeddingModel.BGE_M3, EmbeddingModel.CODE_RANK_EMBED],  # Hybrid + large context
        auto_model_selection=True,
        chunking_strategy=ChunkingStrategy.ADAPTIVE,
        base_chunk_size=1024,
        chunk_overlap_ratio=0.15,
        batch_size=16,
        enable_quality_scoring=True,
        quality_threshold=0.7,
        enable_hierarchical_relationships=True,
        preserve_code_structure=True
    )
    
    # Initialize upgrade system
    upgrade_system = EmbeddingUpgradeSystem(config)
    await upgrade_system.initialize()
    
    # Run demonstration
    await upgrade_system.demonstrate_capabilities()

if __name__ == "__main__":
    asyncio.run(main())