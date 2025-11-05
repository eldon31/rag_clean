"""Test script to verify sparse error message improvement."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from processor.ultimate_embedder.model_manager import ModelManager
from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4
from processor.ultimate_embedder.config import ModelConfig
import logging

logging.basicConfig(level=logging.INFO)

# Create a minimal embedder with sparse enabled
embedder = UltimateKaggleEmbedderV4(
    model_config=ModelConfig(
        hf_model_id="sentence-transformers/all-MiniLM-L6-v2",
        name="all-MiniLM-L6-v2",
        vector_dim=384,
        max_tokens=512,
    ),
    enable_sparse=True,
    sparse_model_names=["splade"],
    device="cpu",
)

print("\n" + "=" * 80)
print("Testing Sparse Model Error Message")
print("=" * 80)

# Try to initialize sparse models (will fail with SPLADE)
manager = ModelManager(embedder)
manager.initialize_sparse_models()

print("\n" + "=" * 80)
print("Sparse Runtime Reason:")
print(f"  {embedder._sparse_runtime_reason}")
print("=" * 80)

# Check if error message is concise
if embedder._sparse_runtime_reason:
    if len(embedder._sparse_runtime_reason) > 200:
        print("\n❌ ERROR: Message too long (>200 chars)")
    else:
        print("\n✓ SUCCESS: Message is concise")
    
    if "sparse_encoder" in embedder._sparse_runtime_reason.lower() or "incompatible" in embedder._sparse_runtime_reason.lower():
        print("✓ SUCCESS: Contains helpful error information")
    else:
        print("⚠ WARNING: May not explain the issue clearly")
else:
    print("\n✓ No error (sparse loaded successfully)")
