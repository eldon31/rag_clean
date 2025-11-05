"""Test SPLADE encoding with rich progress bar."""

import sys
sys.path.insert(0, '.')

from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4

print("=" * 80)
print("Testing SPLADE Encoding with Rich Progress")
print("=" * 80)

# Create embedder with SPLADE
embedder = UltimateKaggleEmbedderV4(
    model_name='all-miniLM-l6',
    enable_sparse=True,
    sparse_models=['splade'],
    force_cpu=True,  # Force CPU to test the encoding
)

print(f"\n✓ Embedder initialized")
print(f"  Sparse enabled: {embedder.enable_sparse}")
print(f"  Sparse models: {list(embedder.sparse_models.keys())}")

# Test encoding some text
test_texts = [
    "This is a test sentence for SPLADE encoding.",
    "Rich progress bars are much better than tqdm.",
    "Sentence transformers 5.x+ uses SparseEncoder class.",
    "The embedding process involves dense and sparse vectors.",
    "Testing manual batching with rich progress visualization.",
]

print(f"\n{'=' * 80}")
print("Testing SPLADE Encoding")
print(f"{'=' * 80}")
print(f"Input: {len(test_texts)} texts")

try:
    # Get the SPLADE model
    splade_model = embedder.sparse_models.get('splade')
    if splade_model is None:
        print("❌ SPLADE model not loaded!")
        sys.exit(1)
    
    # Test encoding with progress
    from processor.ultimate_embedder.progress import BatchProgressContext
    
    context = BatchProgressContext(
        batch_index=0,
        total_batches=1,
        label="SPLADE",
        model_name="splade"
    )
    
    print(f"\nEncoding with rich progress...")
    embeddings = embedder._call_encode(
        model=splade_model,
        texts=test_texts,
        batch_size=2,
        device='cpu',
        show_progress=True,
        progress_context=context,
        model_name='splade'
    )
    
    print(f"\n✅ Encoding successful!")
    print(f"   Output shape: {embeddings.shape}")
    print(f"   Output dtype: {embeddings.dtype}")
    print(f"   Output layout: {embeddings.layout if hasattr(embeddings, 'layout') else 'N/A'}")
    
    # Check sparsity (SPLADE returns sparse tensors)
    import torch
    if isinstance(embeddings, torch.Tensor) and embeddings.layout == torch.sparse_csr:
        # Convert sparse tensor to check sparsity
        dense_embeddings = embeddings.to_dense()
        non_zero = torch.count_nonzero(dense_embeddings).item()
        total = dense_embeddings.numel()
        sparsity = 100 * (1 - non_zero / total)
        print(f"   Non-zero elements: {non_zero:,} / {total:,}")
        print(f"   Sparsity: {sparsity:.2f}%")
    else:
        print(f"   Not a sparse tensor (unexpected)")
    
    print(f"\n{'=' * 80}")
    print("✅ SUCCESS! SPLADE works with rich progress bars!")
    print(f"{'=' * 80}")
    
except Exception as e:
    print(f"\n❌ Encoding failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
