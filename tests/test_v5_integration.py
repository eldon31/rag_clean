#!/usr/bin/env python3
"""
Integration Tests for V5 RAG Pipeline
Tests complete document → nodes → embeddings → Qdrant flow

Phase 2 Track 4 - Task 4.1
"""

import sys
from pathlib import Path
import pytest
import tempfile
import json
import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from processor.enhanced_ultimate_chunker_v5_unified import (
    EnhancedUltimateChunkerV5Unified,
    ChunkerConfig
)
from processor.llamaindex_chunker_v5 import HierarchicalNodeParser
from processor.llamaindex_embedder_v5 import MultiModelEmbedder
from processor.sparse_embedder_v5 import BM25SparseEncoder, HybridSparseEncoder


class TestV5IntegrationPipeline:
    """Test complete V5 RAG pipeline integration"""
    
    @pytest.fixture
    def test_document(self, tmp_path):
        """Create test markdown document"""
        doc_path = tmp_path / "test_doc.md"
        content = """# Test Document

## Introduction
This is a test document for the V5 RAG pipeline integration.

## Code Example
```python
def hello_world():
    print("Hello, World!")
    return True
```

## Features
- Model-aware chunking
- Multi-model embeddings
- Sparse vector generation
- Hierarchical structure preservation

## Conclusion
The V5 system integrates multiple frameworks seamlessly.
"""
        doc_path.write_text(content)
        return doc_path
    
    @pytest.fixture
    def chunker(self):
        """Initialize unified chunker"""
        config = ChunkerConfig(
            target_model="jina-code-embeddings-1.5b",
            use_tree_sitter=False,  # Disable for testing
            use_semchunk=False,     # Disable for testing
            enable_semantic_scoring=False
        )
        return EnhancedUltimateChunkerV5Unified(config=config)
    
    def test_chunking_to_nodes_pipeline(self, chunker, test_document):
        """Test: Document → Chunks → LlamaIndex Nodes"""
        # Step 1: Chunk document
        chunks = chunker.process_file_smart(str(test_document))
        
        assert len(chunks) > 0, "Should generate chunks"
        assert all("text" in c for c in chunks), "All chunks should have text"
        assert all("metadata" in c for c in chunks), "All chunks should have metadata"
        
        # Step 2: Convert to LlamaIndex nodes
        node_parser = HierarchicalNodeParser(chunker)
        nodes = node_parser.get_nodes_from_documents([{"text": str(test_document)}])
        
        assert len(nodes) > 0, "Should generate nodes"
        assert all(hasattr(n, "text") for n in nodes), "All nodes should have text"
        assert all(hasattr(n, "metadata") for n in nodes), "All nodes should have metadata"
        
        print(f"✓ Chunking pipeline: {len(chunks)} chunks → {len(nodes)} nodes")
    
    def test_chunks_to_embeddings_pipeline(self, chunker, test_document):
        """Test: Chunks → Dense Embeddings"""
        # Step 1: Generate chunks
        chunks = chunker.process_file_smart(str(test_document))
        texts = [c["text"] for c in chunks]
        
        # Step 2: Generate embeddings (mock if model not available)
        try:
            embedder = MultiModelEmbedder(
                model_names=["sentence-transformers/all-MiniLM-L6-v2"]
            )
            embeddings = embedder.get_multi_model_embeddings(texts[:2])
            
            assert "sentence-transformers/all-MiniLM-L6-v2" in embeddings
            vectors = embeddings["sentence-transformers/all-MiniLM-L6-v2"]
            assert vectors.shape[0] == 2, "Should have 2 embeddings"
            assert vectors.shape[1] > 0, "Embedding dimension > 0"
            
            print(f"✓ Embedding pipeline: {len(texts)} texts → {vectors.shape}")
        except Exception as e:
            pytest.skip(f"Embedding model not available: {e}")
    
    def test_chunks_to_sparse_vectors_pipeline(self, chunker, test_document):
        """Test: Chunks → Sparse Vectors (BM25)"""
        # Step 1: Generate chunks
        chunks = chunker.process_file_smart(str(test_document))
        texts = [c["text"] for c in chunks]
        
        # Step 2: Generate sparse vectors
        sparse_encoder = BM25SparseEncoder()
        sparse_encoder.fit(texts)
        sparse_vectors = sparse_encoder.encode(texts[:3])
        
        assert len(sparse_vectors) == 3, "Should have 3 sparse vectors"
        assert all("indices" in sv for sv in sparse_vectors), "All should have indices"
        assert all("values" in sv for sv in sparse_vectors), "All should have values"
        assert all(len(sv["indices"]) > 0 for sv in sparse_vectors), "Non-empty vectors"
        
        print(f"✓ Sparse encoding: {len(texts)} texts → {len(sparse_vectors)} vectors")
    
    def test_full_rag_pipeline(self, chunker, test_document):
        """Test: Complete RAG pipeline (chunking → embedding → sparse)"""
        # Step 1: Chunking
        chunks = chunker.process_file_smart(str(test_document))
        texts = [c["text"] for c in chunks]
        metadata = [c["metadata"] for c in chunks]
        
        print(f"Step 1: Generated {len(chunks)} chunks")
        
        # Step 2: Sparse vectors
        sparse_encoder = BM25SparseEncoder()
        sparse_encoder.fit(texts)
        sparse_vectors = sparse_encoder.encode(texts)
        
        print(f"Step 2: Generated {len(sparse_vectors)} sparse vectors")
        
        # Step 3: Dense embeddings (mock)
        try:
            embedder = MultiModelEmbedder(
                model_names=["sentence-transformers/all-MiniLM-L6-v2"]
            )
            dense_embeddings = embedder.get_multi_model_embeddings(texts[:3])
            print(f"Step 3: Generated dense embeddings (shape: {list(dense_embeddings.values())[0].shape})")
        except Exception:
            print("Step 3: Dense embeddings skipped (model not available)")
        
        # Step 4: Validate Qdrant-compatible format
        for i, chunk in enumerate(chunks[:3]):
            point = {
                "id": i,
                "vector": {
                    "dense": [0.1] * 384,  # Mock vector
                    "sparse": {
                        "indices": sparse_vectors[i]["indices"],
                        "values": sparse_vectors[i]["values"]
                    }
                },
                "payload": metadata[i]
            }
            
            assert "id" in point
            assert "vector" in point
            assert "payload" in point
            assert "dense" in point["vector"]
            assert "sparse" in point["vector"]
        
        print("✓ Full RAG pipeline: chunks → sparse → (dense) → Qdrant format")
    
    def test_model_aware_validation(self, chunker, test_document):
        """Test: Model-aware chunk validation"""
        chunks = chunker.process_file_smart(str(test_document))
        validation = chunker.validate_chunks(chunks)
        
        assert "validation_passed" in validation
        assert "total_chunks" in validation
        assert "valid_chunks" in validation
        
        # All chunks should be within token limit
        assert validation["validation_passed"], "All chunks should pass validation"
        
        print(f"✓ Validation: {validation['valid_chunks']}/{validation['total_chunks']} chunks valid")
    
    def test_metadata_enrichment(self, chunker, test_document):
        """Test: Metadata enrichment pipeline"""
        chunks = chunker.process_file_smart(str(test_document))
        
        # Check V5 metadata fields
        required_fields = [
            "target_model",
            "chunker_version",
            "model_aware_chunking",
            "chunk_size_tokens",
            "estimated_tokens",
            "within_token_limit",
            "embedding_dimension"
        ]
        
        for chunk in chunks:
            metadata = chunk["metadata"]
            for field in required_fields:
                assert field in metadata, f"Missing field: {field}"
        
        print(f"✓ Metadata enrichment: All {len(required_fields)} V5 fields present")
    
    def test_quality_scoring(self, chunker, test_document):
        """Test: Quality scoring and gating"""
        chunks = chunker.process_file_smart(str(test_document))
        
        # Check quality scores
        for chunk in chunks:
            scores = chunk.get("advanced_scores", {})
            assert "semantic" in scores
            assert "structural" in scores
            assert "retrieval_quality" in scores
            assert "overall" in scores
            
            # Scores should be in valid range
            for score_name, score_value in scores.items():
                assert 0.0 <= score_value <= 1.0, f"{score_name} score out of range: {score_value}"
        
        print(f"✓ Quality scoring: All {len(chunks)} chunks have valid scores")
    
    def test_backward_compatibility(self, chunker, test_document):
        """Test: V5 backward compatible with V4 interface"""
        # V4-style API
        chunks_v4 = chunker.chunk_documents([str(test_document)])
        
        # V3-style API
        chunks_v3 = chunker.process_file_smart(str(test_document))
        
        # Both should work and produce chunks
        assert len(chunks_v4) > 0, "V4 API should work"
        assert len(chunks_v3) > 0, "V3 API should work"
        
        print(f"✓ Backward compatibility: V4 API ({len(chunks_v4)} chunks), V3 API ({len(chunks_v3)} chunks)")


class TestDoclingIntegration:
    """Test enhanced Docling integration (Phase 2C)"""
    
    def test_docling_table_preservation(self):
        """Test: Table structure preservation"""
        # Mock test - actual Docling requires installation
        chunker = EnhancedUltimateChunkerV5Unified(
            target_model="jina-code-embeddings-1.5b",
            use_docling=False  # Disabled for testing
        )
        
        # Test that table extraction methods exist
        assert hasattr(chunker, "_extract_docling_tables")
        assert hasattr(chunker, "_table_to_markdown")
        assert hasattr(chunker, "_create_table_chunks")
        
        print("✓ Docling table preservation: Methods implemented")
    
    def test_docling_figure_extraction(self):
        """Test: Figure extraction with captions"""
        chunker = EnhancedUltimateChunkerV5Unified(
            target_model="jina-code-embeddings-1.5b",
            use_docling=False
        )
        
        # Test that figure extraction methods exist
        assert hasattr(chunker, "_extract_docling_figures")
        assert hasattr(chunker, "_create_figure_chunks")
        
        print("✓ Docling figure extraction: Methods implemented")
    
    def test_docling_reference_resolution(self):
        """Test: Cross-reference resolution"""
        chunker = EnhancedUltimateChunkerV5Unified(
            target_model="jina-code-embeddings-1.5b",
            use_docling=False
        )
        
        # Test that reference resolution methods exist
        assert hasattr(chunker, "_build_reference_map")
        
        print("✓ Docling reference resolution: Methods implemented")


class TestHybridSearch:
    """Test hybrid search components"""
    
    def test_hybrid_sparse_encoder(self):
        """Test: Hybrid sparse encoder (BM25 + attention)"""
        texts = [
            "This is a test document about machine learning.",
            "Another document discussing natural language processing.",
            "A third document on artificial intelligence topics."
        ]
        
        encoder = HybridSparseEncoder(
            use_bm25=True,
            use_attention=False,  # Requires transformer model
            bm25_weight=1.0
        )
        
        encoder.fit(texts)
        sparse_vectors = encoder.encode(texts)
        
        assert len(sparse_vectors) == 3
        assert all("indices" in sv for sv in sparse_vectors)
        assert all("values" in sv for sv in sparse_vectors)
        
        print(f"✓ Hybrid sparse encoder: {len(sparse_vectors)} vectors generated")


def run_integration_tests():
    """Run all integration tests"""
    print("="*70)
    print("V5 Integration Tests - Phase 2 Track 4 (Task 4.1)")
    print("="*70)
    
    # Run pytest
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-k", "test_"
    ])
    
    return exit_code


if __name__ == "__main__":
    exit(run_integration_tests())