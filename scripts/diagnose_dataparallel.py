#!/usr/bin/env python3
"""
Diagnostic script to identify DataParallel and model loading issues
"""

import sys
import torch
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from processor.ultimate_embedder import UltimateKaggleEmbedderV4, KaggleGPUConfig

def diagnose():
    print("="*70)
    print("DATAPARALLEL DIAGNOSTIC SCRIPT")
    print("="*70)
    
    # Check GPU availability
    print(f"\nGPU Check:")
    print(f"  CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"  GPU count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("  Running in CPU mode")
    
    # Test model initialization
    print(f"\nInitializing embedder...")
    try:
        embedder = UltimateKaggleEmbedderV4(
            model_name="jina-code-embeddings-1.5b",
            gpu_config=KaggleGPUConfig(device_count=torch.cuda.device_count() if torch.cuda.is_available() else 1)
        )
        
        print(f"\n✓ Embedder initialized successfully")
        
        # Check primary model
        print(f"\nPrimary Model Check:")
        print(f"  Model exists: {embedder.primary_model is not None}")
        
        if embedder.primary_model:
            model = embedder.primary_model
            print(f"  Model type: {type(model).__name__}")
            print(f"  Is DataParallel: {isinstance(model, torch.nn.DataParallel)}")
            
            # Check encode method
            if hasattr(model, 'encode'):
                print(f"  ✓ Has encode() method directly")
            elif hasattr(model, 'module') and hasattr(model.module, 'encode'):
                print(f"  ✓ Has encode() method via .module (DataParallel)")
            else:
                print(f"  ✗ No encode() method found!")
            
            # Test unwrapping
            if isinstance(model, torch.nn.DataParallel):
                print(f"\n  Testing DataParallel unwrapping:")
                unwrapped = model.module
                print(f"    Unwrapped type: {type(unwrapped).__name__}")
                print(f"    Unwrapped has encode(): {hasattr(unwrapped, 'encode')}")
        
        # Check companion models
        if embedder.companion_models:
            print(f"\nCompanion Models:")
            for name, model in embedder.companion_models.items():
                is_dp = isinstance(model, torch.nn.DataParallel)
                has_encode = hasattr(model, 'encode') or (hasattr(model, 'module') and hasattr(model.module, 'encode'))
                print(f"  {name}:")
                print(f"    DataParallel: {is_dp}")
                print(f"    Has encode: {has_encode}")
        
        # Test encoding
        print(f"\nTesting encoding with sample text...")
        try:
            test_texts = ["This is a test sentence for encoding."]
            
            # Get primary model
            primary_model = embedder._get_primary_model()
            
            # Unwrap if DataParallel
            encode_model = primary_model.module if isinstance(primary_model, torch.nn.DataParallel) else primary_model
            
            # Try encoding
            embeddings = encode_model.encode(
                test_texts,
                convert_to_numpy=True,
                normalize_embeddings=True,
                device=embedder.device
            )
            
            print(f"  ✓ Encoding successful!")
            print(f"  Output shape: {embeddings.shape}")
            print(f"  Output dtype: {embeddings.dtype}")
            
        except Exception as e:
            print(f"  ✗ Encoding failed: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"\n" + "="*70)
        print(f"DIAGNOSIS COMPLETE")
        print(f"="*70)
        
    except Exception as e:
        print(f"\n✗ Initialization failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose()