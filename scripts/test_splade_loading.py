"""Quick test to verify SPLADE model loading works correctly."""

import logging
from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

print("=" * 80)
print("Testing SPLADE Model Loading")
print("=" * 80)

# Initialize embedder with sparse enabled (default)
embedder = UltimateKaggleEmbedderV4(
    enable_sparse=True,
    sparse_models=["splade"],
    model_list=["all-MiniLM-L6-v2"],  # Small model for quick test
)

print("\n" + "=" * 80)
print("Embedder Configuration:")
print("=" * 80)
print(f"Sparse enabled: {embedder.enable_sparse}")
print(f"Sparse models loaded: {list(embedder.sparse_models.keys())}")
print(f"Sparse runtime reason: {embedder._sparse_runtime_reason}")

if embedder.sparse_models:
    print("\n✅ SUCCESS: SPLADE model loaded successfully!")
    splade_model = embedder.sparse_models.get("splade")
    if splade_model:
        print(f"   Model type: {type(splade_model).__name__}")
        print(f"   Model class: {splade_model.__class__.__module__}.{splade_model.__class__.__name__}")
        
        # Test encoding
        print("\n" + "=" * 80)
        print("Testing SPLADE Encoding:")
        print("=" * 80)
        test_text = "This is a test sentence for SPLADE encoding."
        print(f"Input: {test_text}")
        
        try:
            # SPLADE uses encode() method
            embedding = splade_model.encode(test_text)
            print(f"✅ Encoding successful!")
            print(f"   Output shape: {embedding.shape}")
            print(f"   Output dtype: {embedding.dtype}")
            
            # Check sparsity
            import numpy as np
            non_zero = np.count_nonzero(embedding)
            total = embedding.size
            sparsity = 100 * (1 - non_zero / total)
            print(f"   Non-zero elements: {non_zero:,} / {total:,}")
            print(f"   Sparsity: {sparsity:.2f}%")
        except Exception as e:
            print(f"❌ Encoding failed: {e}")
else:
    print("\n❌ FAILURE: No SPLADE models loaded")
    print(f"   Reason: {embedder._sparse_runtime_reason}")

print("\n" + "=" * 80)
