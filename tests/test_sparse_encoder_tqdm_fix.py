"""Test that SparseEncoder models don't receive unsupported tqdm_kwargs."""

import pytest
from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4


def test_sparse_encoder_no_tqdm_kwargs():
    """Verify SparseEncoder models don't get tqdm_kwargs that cause errors."""
    
    # Initialize embedder with SPLADE enabled
    embedder = UltimateKaggleEmbedderV4(
        model_name="all-miniLM-l6",
        enable_sparse=True,
        sparse_models=["splade"],
    )
    
    # Verify sparse model loaded
    assert "splade" in embedder.sparse_models, "SPLADE model should be loaded"
    splade_model = embedder.sparse_models["splade"]
    
    # Verify it's a SparseEncoder
    assert "SparseEncoder" in type(splade_model).__name__, "Should be SparseEncoder class"
    
    # Test that _encode_supports_kwarg returns False for SparseEncoder + tqdm_kwargs
    encode_callable = splade_model.encode
    supports_tqdm = embedder._encode_supports_kwarg(
        encode_callable, 
        "tqdm_kwargs",
        model=splade_model
    )
    
    assert not supports_tqdm, "SparseEncoder should NOT support tqdm_kwargs"
    
    # Test actual encoding works without error
    test_texts = ["This is a test sentence.", "Another test sentence."]
    
    try:
        result = embedder._call_encode(
            model=splade_model,
            texts=test_texts,
            batch_size=2,
            device="cpu",
            show_progress=False,  # Disable progress to simplify test
            progress_context=None,
            model_name="splade",
        )
        
        # Should succeed without ValueError about tqdm_kwargs
        assert result is not None
        assert result.shape[0] == 2, "Should have 2 embeddings"
        
    except ValueError as e:
        if "tqdm_kwargs" in str(e):
            pytest.fail(f"SparseEncoder should not receive tqdm_kwargs: {e}")
        raise


def test_sentence_transformer_detection():
    """Verify model type detection works correctly."""
    
    embedder = UltimateKaggleEmbedderV4(
        model_name="all-miniLM-l6",
        enable_sparse=True,
        sparse_models=["splade"],
    )
    
    # Get models
    dense_model = embedder.models.get(embedder.model_name)
    sparse_model = embedder.sparse_models.get("splade")
    
    assert dense_model is not None, "Dense model should be loaded"
    assert sparse_model is not None, "Sparse model should be loaded"
    
    # Verify type detection
    assert "SentenceTransformer" in type(dense_model).__name__, "Dense should be SentenceTransformer"
    assert "SparseEncoder" in type(sparse_model).__name__, "Sparse should be SparseEncoder"
    
    # Test _encode_supports_kwarg for both
    dense_supports = embedder._encode_supports_kwarg(
        dense_model.encode, 
        "tqdm_kwargs",
        model=dense_model
    )
    sparse_supports = embedder._encode_supports_kwarg(
        sparse_model.encode, 
        "tqdm_kwargs",
        model=sparse_model
    )
    
    # SparseEncoder should explicitly not support tqdm_kwargs
    assert not sparse_supports, "SparseEncoder must not support tqdm_kwargs"
    
    print(f"Dense model supports tqdm_kwargs: {dense_supports}")
    print(f"Sparse model supports tqdm_kwargs: {sparse_supports}")


if __name__ == "__main__":
    test_sparse_encoder_no_tqdm_kwargs()
    test_sentence_transformer_detection()
    print("✅ All tests passed!")
