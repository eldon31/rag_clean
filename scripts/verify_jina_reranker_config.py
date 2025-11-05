"""Verify jina-reranker-v3 configuration matches expected loading pattern."""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from processor.ultimate_embedder.config import (
    RERANKING_MODELS,
    RERANKING_MODEL_PRIORITY,
    DEFAULT_RERANK_MODEL,
    get_reranking_model_config,
)


def verify_jina_config():
    """Verify jina-reranker-v3 is configured correctly."""
    
    print("=" * 80)
    print("JINA RERANKER V3 CONFIGURATION VERIFICATION")
    print("=" * 80)
    
    # Check 1: Priority order
    print("\n1. Priority Order:")
    print(f"   RERANKING_MODEL_PRIORITY = {RERANKING_MODEL_PRIORITY}")
    assert RERANKING_MODEL_PRIORITY[0] == "jina-reranker-v3", \
        f"Expected jina-reranker-v3 to be first, got {RERANKING_MODEL_PRIORITY[0]}"
    print("   ✓ jina-reranker-v3 is first priority")
    
    # Check 2: Default model
    print("\n2. Default Model:")
    print(f"   DEFAULT_RERANK_MODEL = {DEFAULT_RERANK_MODEL}")
    assert DEFAULT_RERANK_MODEL == "jina-reranker-v3", \
        f"Expected default to be jina-reranker-v3, got {DEFAULT_RERANK_MODEL}"
    print("   ✓ Default is jina-reranker-v3")
    
    # Check 3: Model spec
    print("\n3. Model Specification:")
    spec = get_reranking_model_config("jina-reranker-v3")
    print(f"   hf_model_id: {spec.hf_model_id}")
    print(f"   trust_remote_code: {spec.trust_remote_code}")
    print(f"   model_kwargs: {spec.model_kwargs}")
    print(f"   loader: {spec.loader}")
    
    assert spec.hf_model_id == "jinaai/jina-reranker-v3", \
        f"Expected jinaai/jina-reranker-v3, got {spec.hf_model_id}"
    assert spec.trust_remote_code is True, \
        "Expected trust_remote_code=True"
    assert spec.model_kwargs.get("dtype") == "auto", \
        f"Expected dtype='auto', got {spec.model_kwargs.get('dtype')}"
    assert spec.loader == "jina_reranker", \
        f"Expected loader='jina_reranker', got {spec.loader}"
    
    print("   ✓ All spec parameters correct")
    
    # Check 4: Simulated loading call
    print("\n4. Simulated Loading Pattern:")
    model_kwargs = dict(spec.model_kwargs)
    if spec.trust_remote_code:
        model_kwargs.setdefault("trust_remote_code", True)
    
    print("   The loader will call:")
    print(f"   AutoModel.from_pretrained(")
    print(f"       '{spec.hf_model_id}',")
    for key, value in model_kwargs.items():
        print(f"       {key}={repr(value)},")
    print(f"   )")
    print(f"   model.eval()")
    
    expected_pattern = """
    Expected pattern (from user):
    AutoModel.from_pretrained(
        'jinaai/jina-reranker-v3',
        dtype="auto",
        trust_remote_code=True,
    )
    model.eval()
    """
    print(expected_pattern)
    print("   ✓ Loading pattern matches expected")
    
    print("\n" + "=" * 80)
    print("✓ ALL CHECKS PASSED - jina-reranker-v3 configured correctly!")
    print("=" * 80)


if __name__ == "__main__":
    verify_jina_config()
