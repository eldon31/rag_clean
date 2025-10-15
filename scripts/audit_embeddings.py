"""
Post-Kaggle Verification Script
Audits embedding files after Kaggle processing

Checks:
1. Embedding file integrity
2. Vector dimensions (should be 3584)
3. No missing embeddings
4. Vector quality (no NaN, inf, all zeros)
5. Metadata consistency
6. Qdrant upload readiness
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict
from typing import List, Dict

# Paths
EMBEDDINGS_FILE = Path("output/docling/embeddings/docling_embeddings.jsonl")
# Alternative Kaggle download path
KAGGLE_EMBEDDINGS = Path("docling_embeddings.jsonl")
REPORT_FILE = Path("output/docling/post_kaggle_audit.txt")

def load_embeddings(file_path: Path) -> List[Dict]:
    """Load embeddings from JSONL file"""
    embeddings = []
    
    if not file_path.exists():
        return embeddings
    
    print(f"Loading embeddings from: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                embedding_data = json.loads(line)
                embeddings.append(embedding_data)
            except json.JSONDecodeError as e:
                print(f"  ⚠️  Line {line_num}: Invalid JSON - {e}")
    
    return embeddings

def audit_embeddings(embeddings: List[Dict]) -> Dict:
    """Comprehensive audit of embeddings"""
    
    print(f"\n{'='*70}")
    print("POST-KAGGLE AUDIT: DOCLING EMBEDDINGS")
    print(f"{'='*70}\n")
    
    audit = {
        "total_embeddings": len(embeddings),
        "missing_ids": [],
        "missing_text": [],
        "missing_embeddings": [],
        "wrong_dimensions": [],
        "nan_vectors": [],
        "inf_vectors": [],
        "zero_vectors": [],
        "vector_stats": {
            "dimensions": [],
            "norms": [],
            "min_values": [],
            "max_values": []
        },
        "metadata_fields": defaultdict(int),
        "errors": []
    }
    
    if not embeddings:
        print("❌ No embeddings loaded!")
        return audit
    
    print(f"Processing {len(embeddings)} embeddings...")
    print(f"{'─'*70}\n")
    
    for idx, emb_data in enumerate(embeddings):
        # Check required fields
        emb_id = emb_data.get("id")
        text = emb_data.get("text")
        vector = emb_data.get("embedding")
        metadata = emb_data.get("metadata", {})
        
        if not emb_id:
            audit["missing_ids"].append(idx)
        
        if not text:
            audit["missing_text"].append(emb_id or idx)
        
        if not vector:
            audit["missing_embeddings"].append(emb_id or idx)
            continue
        
        # Convert to numpy array
        try:
            vec_array = np.array(vector, dtype=np.float32)
        except Exception as e:
            audit["errors"].append(f"{emb_id}: Cannot convert to array - {e}")
            continue
        
        # Check dimensions
        dim = len(vec_array)
        audit["vector_stats"]["dimensions"].append(dim)
        
        if dim != 3584:
            audit["wrong_dimensions"].append({
                "id": emb_id or idx,
                "dimension": dim
            })
        
        # Check for NaN
        if np.isnan(vec_array).any():
            audit["nan_vectors"].append(emb_id or idx)
        
        # Check for inf
        if np.isinf(vec_array).any():
            audit["inf_vectors"].append(emb_id or idx)
        
        # Check for all zeros
        if np.allclose(vec_array, 0):
            audit["zero_vectors"].append(emb_id or idx)
        
        # Calculate statistics
        norm = np.linalg.norm(vec_array)
        audit["vector_stats"]["norms"].append(norm)
        audit["vector_stats"]["min_values"].append(float(vec_array.min()))
        audit["vector_stats"]["max_values"].append(float(vec_array.max()))
        
        # Track metadata fields
        for field in metadata.keys():
            audit["metadata_fields"][field] += 1
    
    return audit

def print_audit_report(audit: Dict):
    """Print comprehensive audit report"""
    
    print(f"\n{'='*70}")
    print("AUDIT RESULTS")
    print(f"{'='*70}\n")
    
    # Summary
    print("📊 SUMMARY")
    print(f"{'─'*70}")
    print(f"  Total embeddings:    {audit['total_embeddings']}")
    print()
    
    # Issues
    issues_found = False
    
    if audit['missing_ids']:
        issues_found = True
        print(f"❌ MISSING IDs: {len(audit['missing_ids'])} embeddings")
        print(f"   Indices: {audit['missing_ids'][:10]}")
        if len(audit['missing_ids']) > 10:
            print(f"   ... and {len(audit['missing_ids']) - 10} more")
        print()
    
    if audit['missing_text']:
        issues_found = True
        print(f"❌ MISSING TEXT: {len(audit['missing_text'])} embeddings")
        print(f"   IDs: {audit['missing_text'][:10]}")
        if len(audit['missing_text']) > 10:
            print(f"   ... and {len(audit['missing_text']) - 10} more")
        print()
    
    if audit['missing_embeddings']:
        issues_found = True
        print(f"❌ MISSING EMBEDDINGS: {len(audit['missing_embeddings'])} embeddings")
        print(f"   IDs: {audit['missing_embeddings'][:10]}")
        if len(audit['missing_embeddings']) > 10:
            print(f"   ... and {len(audit['missing_embeddings']) - 10} more")
        print()
    
    if audit['wrong_dimensions']:
        issues_found = True
        print(f"❌ WRONG DIMENSIONS: {len(audit['wrong_dimensions'])} embeddings")
        for item in audit['wrong_dimensions'][:10]:
            print(f"   - {item['id']}: {item['dimension']} (expected 3584)")
        if len(audit['wrong_dimensions']) > 10:
            print(f"   ... and {len(audit['wrong_dimensions']) - 10} more")
        print()
    
    if audit['nan_vectors']:
        issues_found = True
        print(f"❌ NaN VECTORS: {len(audit['nan_vectors'])} embeddings")
        print(f"   IDs: {audit['nan_vectors'][:10]}")
        if len(audit['nan_vectors']) > 10:
            print(f"   ... and {len(audit['nan_vectors']) - 10} more")
        print()
    
    if audit['inf_vectors']:
        issues_found = True
        print(f"❌ INF VECTORS: {len(audit['inf_vectors'])} embeddings")
        print(f"   IDs: {audit['inf_vectors'][:10]}")
        if len(audit['inf_vectors']) > 10:
            print(f"   ... and {len(audit['inf_vectors']) - 10} more")
        print()
    
    if audit['zero_vectors']:
        issues_found = True
        print(f"⚠️  ZERO VECTORS: {len(audit['zero_vectors'])} embeddings")
        print(f"   IDs: {audit['zero_vectors'][:10]}")
        if len(audit['zero_vectors']) > 10:
            print(f"   ... and {len(audit['zero_vectors']) - 10} more")
        print()
    
    if audit['errors']:
        issues_found = True
        print(f"❌ ERRORS: {len(audit['errors'])}")
        for error in audit['errors'][:10]:
            print(f"   - {error}")
        if len(audit['errors']) > 10:
            print(f"   ... and {len(audit['errors']) - 10} more")
        print()
    
    if not issues_found:
        print("✅ NO ISSUES FOUND - Embeddings are valid!")
        print()
    
    # Vector statistics
    if audit['vector_stats']['dimensions']:
        print("📊 VECTOR STATISTICS")
        print(f"{'─'*70}")
        
        dims = audit['vector_stats']['dimensions']
        norms = audit['vector_stats']['norms']
        mins = audit['vector_stats']['min_values']
        maxs = audit['vector_stats']['max_values']
        
        # Dimension consistency
        unique_dims = set(dims)
        if len(unique_dims) == 1:
            print(f"  ✅ Dimensions:       {list(unique_dims)[0]} (consistent)")
        else:
            print(f"  ❌ Dimensions:       {unique_dims} (INCONSISTENT!)")
        
        # Norm statistics
        avg_norm = np.mean(norms)
        std_norm = np.std(norms)
        min_norm = np.min(norms)
        max_norm = np.max(norms)
        
        print(f"  Vector norms:")
        print(f"    Average:           {avg_norm:.4f}")
        print(f"    Std deviation:     {std_norm:.4f}")
        print(f"    Min:               {min_norm:.4f}")
        print(f"    Max:               {max_norm:.4f}")
        print()
        
        # Value range statistics
        print(f"  Value ranges:")
        print(f"    Min value:         {np.min(mins):.6f}")
        print(f"    Max value:         {np.max(maxs):.6f}")
        print(f"    Avg min:           {np.mean(mins):.6f}")
        print(f"    Avg max:           {np.mean(maxs):.6f}")
        print()
    
    # Metadata coverage
    if audit['metadata_fields']:
        print("🏷️  METADATA COVERAGE")
        print(f"{'─'*70}")
        for field, count in sorted(audit['metadata_fields'].items()):
            coverage = (count / audit['total_embeddings'] * 100) if audit['total_embeddings'] > 0 else 0
            print(f"  {field:30} {count:5} ({coverage:5.1f}%)")
        print()
    
    # Storage estimates
    if audit['total_embeddings'] > 0:
        print("💾 STORAGE ESTIMATES")
        print(f"{'─'*70}")
        
        # Size calculations
        float32_size = audit['total_embeddings'] * 3584 * 4 / 1024 / 1024  # MB
        int8_size = audit['total_embeddings'] * 3584 / 1024 / 1024  # MB
        
        print(f"  Total vectors:       {audit['total_embeddings']:,}")
        print(f"  Vector dimension:    3584")
        print()
        print(f"  RAM (float32):       {float32_size:.2f} MB")
        print(f"  RAM (int8 quant):    {int8_size:.2f} MB (4x smaller)")
        print(f"  Disk (JSONL):        ~{float32_size * 1.2:.2f} MB (with metadata)")
        print()
    
    # Readiness check
    print(f"{'='*70}")
    print("✅ QDRANT UPLOAD READINESS")
    print(f"{'='*70}")
    
    checks = {
        "Embeddings loaded": audit['total_embeddings'] > 0,
        "All have IDs": len(audit['missing_ids']) == 0,
        "All have text": len(audit['missing_text']) == 0,
        "All have embeddings": len(audit['missing_embeddings']) == 0,
        "Correct dimensions (3584)": len(audit['wrong_dimensions']) == 0,
        "No NaN values": len(audit['nan_vectors']) == 0,
        "No inf values": len(audit['inf_vectors']) == 0,
        "Valid vectors": len(audit['zero_vectors']) < audit['total_embeddings'] * 0.01  # < 1% zeros
    }
    
    all_passed = all(checks.values())
    
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")
    
    print()
    
    if all_passed:
        print("🚀 READY FOR QDRANT UPLOAD!")
        print("\nNext steps:")
        print("1. Start Qdrant: docker-compose up -d")
        print("2. Run: python scripts/upload_to_qdrant.py")
        print("3. Verify upload with collection stats")
    else:
        print("⚠️  FIX ISSUES BEFORE UPLOADING TO QDRANT")
        print("\nRe-run kaggle_embed_docling.py to regenerate embeddings")
    
    print()

def save_report(audit: Dict, embeddings_file: Path):
    """Save audit report to file"""
    
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("POST-KAGGLE AUDIT REPORT: DOCLING EMBEDDINGS\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Source file: {embeddings_file}\n")
        f.write(f"Total embeddings: {audit['total_embeddings']}\n\n")
        
        if audit['missing_ids']:
            f.write(f"Missing IDs ({len(audit['missing_ids'])}):\n")
            for item in audit['missing_ids']:
                f.write(f"  - Index {item}\n")
            f.write("\n")
        
        if audit['wrong_dimensions']:
            f.write(f"Wrong dimensions ({len(audit['wrong_dimensions'])}):\n")
            for item in audit['wrong_dimensions']:
                f.write(f"  - {item['id']}: {item['dimension']}\n")
            f.write("\n")
        
        if audit['nan_vectors']:
            f.write(f"NaN vectors ({len(audit['nan_vectors'])}):\n")
            for item in audit['nan_vectors']:
                f.write(f"  - {item}\n")
            f.write("\n")
        
        if audit['errors']:
            f.write(f"Errors ({len(audit['errors'])}):\n")
            for error in audit['errors']:
                f.write(f"  - {error}\n")
            f.write("\n")
        
        # Statistics
        if audit['vector_stats']['norms']:
            f.write("Vector statistics:\n")
            f.write(f"  Avg norm: {np.mean(audit['vector_stats']['norms']):.4f}\n")
            f.write(f"  Std norm: {np.std(audit['vector_stats']['norms']):.4f}\n")
            f.write(f"  Min norm: {np.min(audit['vector_stats']['norms']):.4f}\n")
            f.write(f"  Max norm: {np.max(audit['vector_stats']['norms']):.4f}\n")
    
    print(f"📄 Report saved to: {REPORT_FILE}")

def main():
    """Run audit"""
    
    # Try both possible file locations
    if EMBEDDINGS_FILE.exists():
        file_path = EMBEDDINGS_FILE
    elif KAGGLE_EMBEDDINGS.exists():
        file_path = KAGGLE_EMBEDDINGS
    else:
        print(f"❌ Embeddings file not found!")
        print(f"   Looked for:")
        print(f"   - {EMBEDDINGS_FILE}")
        print(f"   - {KAGGLE_EMBEDDINGS}")
        print(f"\n   Download from Kaggle: /kaggle/working/docling_embeddings.jsonl")
        return
    
    embeddings = load_embeddings(file_path)
    audit = audit_embeddings(embeddings)
    print_audit_report(audit)
    save_report(audit, file_path)

if __name__ == "__main__":
    main()
