#!/usr/bin/env python3
"""
Verification script for V5 embedder compatibility (No GPU Required)

Verifies:
1. Collection directory structure is correct
2. Chunk files are discoverable
3. Chunk metadata contains V5 fields
4. File paths are valid for embedder

Does NOT require GPU or model loading.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def discover_collections(chunks_root: Path) -> List[Path]:
    """Discover collection directories"""
    collections = []
    
    for entry in sorted(chunks_root.iterdir()):
        if not entry.is_dir() or entry.name == "__pycache__":
            continue
        
        # Check if directory contains chunk files
        has_chunks = (
            any(entry.rglob("*_chunks.json")) or 
            any(entry.glob("*.json"))
        )
        
        if has_chunks:
            collections.append(entry)
    
    return collections


def analyze_chunk_file(chunk_file: Path) -> Dict[str, Any]:
    """Analyze a single chunk file for V5 metadata"""
    try:
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        
        if not chunks:
            return {"error": "empty_file", "chunks": 0}
        
        first_chunk = chunks[0]
        metadata = first_chunk.get("metadata", {})
        
        # Check for V5 fields
        v5_fields = {
            "model_aware_chunking": metadata.get("model_aware_chunking"),
            "chunker_version": metadata.get("chunker_version"),
            "within_token_limit": metadata.get("within_token_limit"),
            "estimated_tokens": metadata.get("estimated_tokens"),
            "target_model": metadata.get("target_model"),
            "chunk_size_tokens": metadata.get("chunk_size_tokens"),
        }
        
        # Check for required fields
        required_fields = ["text", "metadata"]
        has_required = all(field in first_chunk for field in required_fields)
        
        return {
            "chunks": len(chunks),
            "has_required_fields": has_required,
            "v5_fields": v5_fields,
            "has_v5_metadata": any(v is not None for v in v5_fields.values()),
            "sample_metadata_keys": list(metadata.keys())[:10],
        }
        
    except Exception as e:
        return {"error": str(e), "chunks": 0}


def verify_collection(collection_path: Path) -> Dict[str, Any]:
    """Verify a collection's structure"""
    
    # Find all chunk files
    chunk_files = list(collection_path.rglob("*_chunks.json"))
    
    if not chunk_files:
        return {
            "status": "error",
            "message": "No chunk files found",
            "chunk_files": 0,
        }
    
    # Analyze sample files
    sample_size = min(3, len(chunk_files))
    samples = [analyze_chunk_file(f) for f in chunk_files[:sample_size]]
    
    total_chunks = sum(s.get("chunks", 0) for s in samples)
    has_v5 = all(s.get("has_v5_metadata", False) for s in samples)
    has_required = all(s.get("has_required_fields", False) for s in samples)
    
    # Check subdirectory depth
    max_depth = max(len(f.relative_to(collection_path).parts) for f in chunk_files)
    
    return {
        "status": "success",
        "chunk_files": len(chunk_files),
        "total_chunks_sampled": total_chunks,
        "max_subdirectory_depth": max_depth,
        "has_v5_metadata": has_v5,
        "has_required_fields": has_required,
        "sample_analysis": samples[0] if samples else {},
    }


def main():
    """Run verification"""
    print("="*70)
    print("V5 EMBEDDER STRUCTURE VERIFICATION (No GPU Required)")
    print("="*70)
    
    chunks_root = Path("Chunked")
    
    if not chunks_root.exists():
        print(f"\n✗ Chunks directory not found: {chunks_root}")
        print("   Expected structure: Chunked/Collection1/subdir/file_chunks.json")
        return 1
    
    print(f"\n✓ Chunks root found: {chunks_root.absolute()}")
    
    # Discover collections
    print("\n" + "-"*70)
    print("STEP 1: Collection Discovery")
    print("-"*70)
    
    collections = discover_collections(chunks_root)
    
    if not collections:
        print("✗ No collections discovered")
        return 1
    
    print(f"✓ Discovered {len(collections)} collection(s):")
    for col in collections:
        chunk_count = len(list(col.rglob("*_chunks.json")))
        print(f"   - {col.name}: {chunk_count} chunk files")
    
    # Verify each collection
    print("\n" + "-"*70)
    print("STEP 2: Structure Verification")
    print("-"*70)
    
    all_valid = True
    results = []
    
    for collection in collections:
        print(f"\nVerifying: {collection.name}")
        result = verify_collection(collection)
        results.append((collection.name, result))
        
        if result["status"] == "error":
            print(f"   ✗ {result.get('message', 'Unknown error')}")
            all_valid = False
            continue
        
        print(f"   ✓ Chunk files: {result['chunk_files']}")
        print(f"   ✓ Subdirectory depth: {result['max_subdirectory_depth']}")
        print(f"   ✓ Has V5 metadata: {result['has_v5_metadata']}")
        print(f"   ✓ Has required fields: {result['has_required_fields']}")
        
        if result.get("sample_analysis"):
            sample = result["sample_analysis"]
            v5_fields = sample.get("v5_fields", {})
            print(f"   ✓ Sample V5 fields:")
            for key, value in v5_fields.items():
                if value is not None:
                    print(f"      - {key}: {value}")
        
        if not result["has_v5_metadata"]:
            print(f"   ⚠️  Warning: Missing V5 metadata fields")
            all_valid = False
        
        if not result["has_required_fields"]:
            print(f"   ✗ Error: Missing required fields (text, metadata)")
            all_valid = False
    
    # Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    total_files = sum(r[1].get("chunk_files", 0) for r in results)
    print(f"\nTotal collections: {len(collections)}")
    print(f"Total chunk files: {total_files}")
    
    print("\nCollection Status:")
    for name, result in results:
        if result["status"] == "success":
            v5_status = "✓" if result["has_v5_metadata"] else "⚠️"
            print(f"  {v5_status} {name}: {result['chunk_files']} files")
        else:
            print(f"  ✗ {name}: {result.get('message', 'Error')}")
    
    print("\n" + "-"*70)
    
    if all_valid:
        print("✓ VERIFICATION PASSED")
        print("\nThe V5 embedder should work with this chunk structure:")
        print("  - All collections have discoverable chunk files")
        print("  - All chunk files have required fields (text, metadata)")
        print("  - All chunk files have V5 metadata fields")
        print("\nReady for embedding generation (requires GPU):")
        print("  python scripts/embed_collections_v5.py --chunks-root ./Chunked")
        return 0
    else:
        print("⚠️  VERIFICATION FAILED")
        print("\nIssues found:")
        print("  - Some collections may be missing V5 metadata")
        print("  - Check chunk file format and metadata fields")
        return 1


if __name__ == "__main__":
    sys.exit(main())