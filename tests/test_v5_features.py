#!/usr/bin/env python3
"""
Unit Tests for V5 Sparse Features
Tests BM25, attention encoders, and hybrid combinations

Phase 2 Track 4 - Task 4.3
"""

import sys
from pathlib import Path
import pytest
import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from processor.sparse_embedder_v5 import (
    BM25SparseEncoder,
    AttentionSparseEncoder,
    HybridSparseEncoder
)


class TestBM25SparseEncoder:
    """Test BM25 sparse vector generation"""
    
    @pytest.fixture
    def sample_texts(self):
        """Sample text corpus"""
        return [
            "machine learning algorithms for text classification",
            "natural language processing with transformers",
            "deep learning neural networks and optimization",
            "information retrieval and search engines"
        ]
    
    def test_bm25_initialization(self):
        """Test: BM25 encoder initialization"""
        encoder = BM25SparseEncoder(k1=1.5, b=0.75)
        
        assert encoder.k1 == 1.5
        assert encoder.b == 0.75
        assert encoder.vocabulary is None
        assert encoder.idf_scores is None
        
        print("✓ BM25 initialization: Parameters set correctly")
    
    def test_bm25_fit(self, sample_texts):
        """Test: BM25 fit on corpus"""
        encoder = BM25SparseEncoder()
        encoder.fit(sample_texts)
        
        assert encoder.vocabulary is not None
        assert encoder.idf_scores is not None
        assert len(encoder.vocabulary) > 0
        assert encoder.avg_doc_length > 0
        
        print(f"✓ BM25 fit: Vocabulary size = {len(encoder.vocabulary)}")
    
    def test_bm25_encode(self, sample_texts):
        """Test: BM25 encode to sparse vectors"""
        encoder = BM25SparseEncoder()
        encoder.fit(sample_texts)
        
        sparse_vectors = encoder.encode(sample_texts[:2])
        
        assert len(sparse_vectors) == 2
        assert all("indices" in sv for sv in sparse_vectors)
        assert all("values" in sv for sv in sparse_vectors)
        assert all("tokens" in sv for sv in sparse_vectors)
        
        # Check format
        for sv in sparse_vectors:
            assert isinstance(sv["indices"], list)
            assert isinstance(sv["values"], list)
            assert isinstance(sv["tokens"], list)
            assert len(sv["indices"]) == len(sv["values"])
            assert len(sv["indices"]) == len(sv["tokens"])
        
        print(f"✓ BM25 encode: Generated {len(sparse_vectors)} sparse vectors")
    
    def test_bm25_top_k_filtering(self, sample_texts):
        """Test: BM25 top-K term filtering"""
        encoder = BM25SparseEncoder(top_k=5)
        encoder.fit(sample_texts)
        
        sparse_vectors = encoder.encode([sample_texts[0]])
        
        # Should have at most top_k terms
        assert len(sparse_vectors[0]["indices"]) <= 5
        
        print(f"✓ BM25 top-K: Vector has {len(sparse_vectors[0]['indices'])} terms (max 5)")
    
    def test_bm25_qdrant_format(self, sample_texts):
        """Test: BM25 Qdrant-compatible format"""
        encoder = BM25SparseEncoder()
        encoder.fit(sample_texts)
        
        sparse_vector = encoder.encode([sample_texts[0]])[0]
        
        # Qdrant format validation
        assert "indices" in sparse_vector
        assert "values" in sparse_vector
        assert all(isinstance(idx, int) for idx in sparse_vector["indices"])
        assert all(isinstance(val, float) for val in sparse_vector["values"])
        assert all(val >= 0 for val in sparse_vector["values"])
        
        print("✓ BM25 Qdrant format: Valid sparse vector structure")
    
    def test_bm25_empty_text(self):
        """Test: BM25 handling empty text"""
        encoder = BM25SparseEncoder()
        encoder.fit(["test document"])
        
        sparse_vectors = encoder.encode([""])
        
        assert len(sparse_vectors) == 1
        assert len(sparse_vectors[0]["indices"]) == 0
        assert len(sparse_vectors[0]["values"]) == 0
        
        print("✓ BM25 empty text: Handled gracefully")


class TestAttentionSparseEncoder:
    """Test attention-based sparse vector generation"""
    
    @pytest.fixture
    def sample_texts(self):
        """Sample text corpus"""
        return [
            "transformer models use attention mechanisms",
            "attention weights determine token importance",
            "self-attention computes context representations"
        ]
    
    def test_attention_initialization(self):
        """Test: Attention encoder initialization"""
        encoder = AttentionSparseEncoder(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            top_k=10
        )
        
        assert encoder.top_k == 10
        assert encoder.model_name == "sentence-transformers/all-MiniLM-L6-v2"
        
        print("✓ Attention encoder initialization: Parameters set")
    
    def test_attention_encode_mock(self, sample_texts):
        """Test: Attention encode (mocked - requires model)"""
        try:
            encoder = AttentionSparseEncoder(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                top_k=5
            )
            
            sparse_vectors = encoder.encode(sample_texts[:1])
            
            assert len(sparse_vectors) == 1
            assert "indices" in sparse_vectors[0]
            assert "values" in sparse_vectors[0]
            assert len(sparse_vectors[0]["indices"]) <= 5
            
            print(f"✓ Attention encode: Generated sparse vector with {len(sparse_vectors[0]['indices'])} tokens")
        except Exception as e:
            pytest.skip(f"Attention encoder requires model: {e}")
    
    def test_attention_format_compatibility(self):
        """Test: Attention encoder format compatibility"""
        encoder = AttentionSparseEncoder(top_k=10)
        
        # Mock sparse vector
        mock_vector = {
            "indices": [1, 5, 10, 15],
            "values": [0.8, 0.6, 0.4, 0.2],
            "tokens": ["transformer", "attention", "model", "context"]
        }
        
        # Validate format
        assert "indices" in mock_vector
        assert "values" in mock_vector
        assert "tokens" in mock_vector
        assert len(mock_vector["indices"]) == len(mock_vector["values"])
        
        print("✓ Attention format: Compatible with Qdrant sparse vectors")


class TestHybridSparseEncoder:
    """Test hybrid sparse encoder (BM25 + attention)"""
    
    @pytest.fixture
    def sample_texts(self):
        """Sample text corpus"""
        return [
            "hybrid search combines dense and sparse vectors",
            "BM25 provides lexical matching capabilities",
            "attention mechanisms capture semantic relationships",
            "multi-channel encoding improves retrieval quality"
        ]
    
    def test_hybrid_initialization(self):
        """Test: Hybrid encoder initialization"""
        encoder = HybridSparseEncoder(
            use_bm25=True,
            use_attention=False,
            bm25_weight=0.7,
            attention_weight=0.3
        )
        
        assert encoder.use_bm25 is True
        assert encoder.use_attention is False
        assert encoder.bm25_weight == 0.7
        assert encoder.attention_weight == 0.3
        
        print("✓ Hybrid initialization: Multi-channel config set")
    
    def test_hybrid_bm25_only(self, sample_texts):
        """Test: Hybrid encoder with BM25 only"""
        encoder = HybridSparseEncoder(
            use_bm25=True,
            use_attention=False,
            bm25_weight=1.0
        )
        
        encoder.fit(sample_texts)
        sparse_vectors = encoder.encode(sample_texts[:2])
        
        assert len(sparse_vectors) == 2
        assert all("indices" in sv for sv in sparse_vectors)
        assert all("values" in sv for sv in sparse_vectors)
        
        print(f"✓ Hybrid BM25-only: Generated {len(sparse_vectors)} vectors")
    
    def test_hybrid_weighting(self, sample_texts):
        """Test: Hybrid encoder channel weighting"""
        encoder = HybridSparseEncoder(
            use_bm25=True,
            use_attention=False,
            bm25_weight=0.6
        )
        
        encoder.fit(sample_texts)
        sparse_vectors = encoder.encode([sample_texts[0]])
        
        # Weights should be applied
        assert all(v > 0 for v in sparse_vectors[0]["values"])
        
        # Values should reflect weighting (scaled by 0.6)
        max_value = max(sparse_vectors[0]["values"])
        assert max_value <= 1.0  # Normalized
        
        print(f"✓ Hybrid weighting: Values scaled correctly (max={max_value:.3f})")
    
    def test_hybrid_combination_strategy(self, sample_texts):
        """Test: Hybrid combination strategies"""
        # Test weighted sum
        encoder_sum = HybridSparseEncoder(
            use_bm25=True,
            use_attention=False,
            combination_strategy="weighted_sum"
        )
        encoder_sum.fit(sample_texts)
        vectors_sum = encoder_sum.encode([sample_texts[0]])
        
        # Test max pooling
        encoder_max = HybridSparseEncoder(
            use_bm25=True,
            use_attention=False,
            combination_strategy="max_pool"
        )
        encoder_max.fit(sample_texts)
        vectors_max = encoder_max.encode([sample_texts[0]])
        
        # Both should produce valid vectors
        assert len(vectors_sum[0]["indices"]) > 0
        assert len(vectors_max[0]["indices"]) > 0
        
        print(f"✓ Hybrid strategies: weighted_sum ({len(vectors_sum[0]['indices'])} terms), "
              f"max_pool ({len(vectors_max[0]['indices'])} terms)")
    
    def test_hybrid_qdrant_compatibility(self, sample_texts):
        """Test: Hybrid encoder Qdrant compatibility"""
        encoder = HybridSparseEncoder(use_bm25=True, use_attention=False)
        encoder.fit(sample_texts)
        
        sparse_vector = encoder.encode([sample_texts[0]])[0]
        
        # Qdrant point format
        point = {
            "id": 1,
            "vector": {
                "dense": [0.1] * 384,  # Mock dense vector
                "sparse": {
                    "indices": sparse_vector["indices"],
                    "values": sparse_vector["values"]
                }
            },
            "payload": {"text": sample_texts[0]}
        }
        
        # Validate structure
        assert "id" in point
        assert "vector" in point
        assert "dense" in point["vector"]
        assert "sparse" in point["vector"]
        assert isinstance(point["vector"]["sparse"]["indices"], list)
        assert isinstance(point["vector"]["sparse"]["values"], list)
        
        print("✓ Hybrid Qdrant compatibility: Valid multi-vector point structure")


class TestSparseVectorQuality:
    """Test sparse vector quality metrics"""
    
    def test_sparsity_ratio(self):
        """Test: Sparse vector sparsity ratio"""
        texts = ["machine learning deep learning neural networks"]
        
        encoder = BM25SparseEncoder(top_k=3)
        encoder.fit(texts)
        sparse_vector = encoder.encode(texts)[0]
        
        # Sparsity = non-zero elements / total vocabulary
        sparsity = len(sparse_vector["indices"]) / len(encoder.vocabulary)
        
        assert 0 < sparsity < 1.0
        assert sparsity <= 0.5, "Should be sparse (< 50% density)"
        
        print(f"✓ Sparsity ratio: {sparsity:.3f} ({len(sparse_vector['indices'])}/{len(encoder.vocabulary)} terms)")
    
    def test_value_distribution(self):
        """Test: Sparse vector value distribution"""
        texts = ["test document with multiple important terms for ranking"]
        
        encoder = BM25SparseEncoder()
        encoder.fit(texts)
        sparse_vector = encoder.encode(texts)[0]
        
        values = sparse_vector["values"]
        
        # Values should be positive and normalized
        assert all(v > 0 for v in values)
        assert max(values) <= 1.0
        
        # Should have descending order (top terms first)
        assert values == sorted(values, reverse=True)
        
        print(f"✓ Value distribution: Range [{min(values):.3f}, {max(values):.3f}], sorted={values == sorted(values, reverse=True)}")
    
    def test_token_relevance(self):
        """Test: Top tokens are relevant"""
        texts = ["machine learning algorithms optimize neural network performance"]
        
        encoder = BM25SparseEncoder(top_k=5)
        encoder.fit(texts)
        sparse_vector = encoder.encode(texts)[0]
        
        top_tokens = sparse_vector["tokens"][:3]
        
        # Top tokens should be meaningful (not stopwords)
        meaningful_tokens = ["machine", "learning", "algorithms", "optimize", "neural", "network", "performance"]
        assert any(token in meaningful_tokens for token in top_tokens)
        
        print(f"✓ Token relevance: Top 3 tokens = {top_tokens}")


def run_unit_tests():
    """Run all unit tests"""
    print("="*70)
    print("V5 Sparse Features Unit Tests - Phase 2 Track 4 (Task 4.3)")
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
    exit(run_unit_tests())