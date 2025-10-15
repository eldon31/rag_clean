"""
Pre-Kaggle Verification Script
Audits chunked data before uploading to Kaggle

Checks:
1. All chunk files are valid JSON
2. Chunk IDs are unique
3. Content is not empty
4. Metadata is complete
5. File structure is correct
6. Estimates embedding requirements
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set

# Paths
CHUNKED_DIR = Path("output/docling/chunked")
REPORT_FILE = Path("output/docling/pre_kaggle_audit.txt")

def audit_chunks() -> Dict:
    """Comprehensive audit of chunked data"""
    
    print(f"\n{'='*70}")
    print("PRE-KAGGLE AUDIT: DOCLING CHUNKS")
    print(f"{'='*70}\n")
    
    # Initialize audit results
    audit = {
        "total_files": 0,
        "total_chunks": 0,
        "unique_ids": set(),
        "duplicate_ids": [],
        "empty_content": [],
        "missing_metadata": [],
        "invalid_json": [],
        "chunk_sizes": [],
        "metadata_fields": defaultdict(int),
        "errors": []
    }
    
    if not CHUNKED_DIR.exists():
        print(f"❌ ERROR: {CHUNKED_DIR} does not exist!")
        print("Run chunk_docling_simple.py first to generate chunks")
        return audit
    
    chunk_files = sorted(CHUNKED_DIR.glob("*_chunks.json"))
    
    if not chunk_files:
        print(f"❌ ERROR: No chunk files found in {CHUNKED_DIR}")
        return audit
    
    print(f"Found {len(chunk_files)} chunk files")
    print(f"{'─'*70}\n")
    
    # Process each file
    for chunk_file in chunk_files:
        audit["total_files"] += 1
        
        try:
            # 1. Validate JSON
            with open(chunk_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            if not isinstance(chunks, list):
                audit["errors"].append(f"{chunk_file.name}: Not a list")
                continue
            
            # 2. Process each chunk
            for idx, chunk in enumerate(chunks):
                audit["total_chunks"] += 1
                
                # Check structure
                if not isinstance(chunk, dict):
                    audit["errors"].append(f"{chunk_file.name}[{idx}]: Not a dict")
                    continue
                
                # 3. Check chunk_id
                chunk_id = chunk.get("chunk_id")
                if not chunk_id:
                    audit["errors"].append(f"{chunk_file.name}[{idx}]: Missing chunk_id")
                    continue
                
                # Check for duplicate IDs
                if chunk_id in audit["unique_ids"]:
                    audit["duplicate_ids"].append(chunk_id)
                else:
                    audit["unique_ids"].add(chunk_id)
                
                # 4. Check content
                content = chunk.get("content", "")
                if not content or not content.strip():
                    audit["empty_content"].append(chunk_id)
                else:
                    audit["chunk_sizes"].append(len(content))
                
                # 5. Check metadata
                metadata = chunk.get("metadata", {})
                if not metadata:
                    audit["missing_metadata"].append(chunk_id)
                else:
                    # Track metadata fields
                    for field in metadata.keys():
                        audit["metadata_fields"][field] += 1
        
        except json.JSONDecodeError as e:
            audit["invalid_json"].append(f"{chunk_file.name}: {str(e)}")
        except Exception as e:
            audit["errors"].append(f"{chunk_file.name}: {str(e)}")
    
    return audit

def print_audit_report(audit: Dict):
    """Print comprehensive audit report"""
    
    print(f"\n{'='*70}")
    print("AUDIT RESULTS")
    print(f"{'='*70}\n")
    
    # Summary
    print("📊 SUMMARY")
    print(f"{'─'*70}")
    print(f"  Files processed:     {audit['total_files']}")
    print(f"  Total chunks:        {audit['total_chunks']}")
    print(f"  Unique chunk IDs:    {len(audit['unique_ids'])}")
    print()
    
    # Issues
    issues_found = False
    
    if audit['duplicate_ids']:
        issues_found = True
        print(f"❌ DUPLICATE IDs: {len(audit['duplicate_ids'])}")
        for dup_id in audit['duplicate_ids'][:10]:
            print(f"   - {dup_id}")
        if len(audit['duplicate_ids']) > 10:
            print(f"   ... and {len(audit['duplicate_ids']) - 10} more")
        print()
    
    if audit['empty_content']:
        issues_found = True
        print(f"❌ EMPTY CONTENT: {len(audit['empty_content'])} chunks")
        for chunk_id in audit['empty_content'][:10]:
            print(f"   - {chunk_id}")
        if len(audit['empty_content']) > 10:
            print(f"   ... and {len(audit['empty_content']) - 10} more")
        print()
    
    if audit['missing_metadata']:
        issues_found = True
        print(f"⚠️  MISSING METADATA: {len(audit['missing_metadata'])} chunks")
        for chunk_id in audit['missing_metadata'][:10]:
            print(f"   - {chunk_id}")
        if len(audit['missing_metadata']) > 10:
            print(f"   ... and {len(audit['missing_metadata']) - 10} more")
        print()
    
    if audit['invalid_json']:
        issues_found = True
        print(f"❌ INVALID JSON: {len(audit['invalid_json'])} files")
        for error in audit['invalid_json']:
            print(f"   - {error}")
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
        print("✅ NO ISSUES FOUND - Data is clean!")
        print()
    
    # Content statistics
    if audit['chunk_sizes']:
        print("📏 CONTENT STATISTICS")
        print(f"{'─'*70}")
        avg_size = sum(audit['chunk_sizes']) / len(audit['chunk_sizes'])
        min_size = min(audit['chunk_sizes'])
        max_size = max(audit['chunk_sizes'])
        total_chars = sum(audit['chunk_sizes'])
        est_tokens = total_chars // 4  # Rough estimate
        
        print(f"  Average chunk size:  {avg_size:.0f} characters (~{avg_size//4:.0f} tokens)")
        print(f"  Min chunk size:      {min_size} characters")
        print(f"  Max chunk size:      {max_size} characters")
        print(f"  Total characters:    {total_chars:,}")
        print(f"  Estimated tokens:    {est_tokens:,}")
        print()
    
    # Metadata statistics
    if audit['metadata_fields']:
        print("🏷️  METADATA FIELDS")
        print(f"{'─'*70}")
        for field, count in sorted(audit['metadata_fields'].items()):
            coverage = (count / audit['total_chunks'] * 100) if audit['total_chunks'] > 0 else 0
            print(f"  {field:30} {count:5} chunks ({coverage:5.1f}%)")
        print()
    
    # Embedding estimates
    if audit['chunk_sizes']:
        print("🔮 EMBEDDING ESTIMATES (nomic-embed-code)")
        print(f"{'─'*70}")
        est_tokens = sum(audit['chunk_sizes']) // 4
        
        # GPU T4 x2 estimates
        chunks_per_sec_dual_gpu = 8  # Conservative estimate
        chunks_per_sec_single_gpu = 4
        
        time_dual_gpu = audit['total_chunks'] / chunks_per_sec_dual_gpu / 60
        time_single_gpu = audit['total_chunks'] / chunks_per_sec_single_gpu / 60
        
        print(f"  Total chunks:        {audit['total_chunks']:,}")
        print(f"  Estimated tokens:    {est_tokens:,}")
        print(f"  Vector dimension:    3584 (nomic-embed-code)")
        print()
        print(f"  Time (GPU T4 x2):    ~{time_dual_gpu:.1f} minutes")
        print(f"  Time (GPU T4 x1):    ~{time_single_gpu:.1f} minutes")
        print()
        print(f"  Memory per vector:   ~14.3 KB (float32)")
        print(f"  Total memory (RAM):  ~{audit['total_chunks'] * 14.3 / 1024:.1f} MB")
        print(f"  With int8 quant:     ~{audit['total_chunks'] * 3.6 / 1024:.1f} MB (4x smaller)")
        print()
    
    # Readiness check
    print(f"{'='*70}")
    print("✅ KAGGLE READINESS CHECK")
    print(f"{'='*70}")
    
    checks = {
        "Chunk files exist": audit['total_files'] > 0,
        "Chunks loaded": audit['total_chunks'] > 0,
        "No duplicate IDs": len(audit['duplicate_ids']) == 0,
        "No empty content": len(audit['empty_content']) == 0,
        "No invalid JSON": len(audit['invalid_json']) == 0,
        "Metadata present": audit['total_chunks'] - len(audit['missing_metadata']) > 0
    }
    
    all_passed = all(checks.values())
    
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")
    
    print()
    
    if all_passed:
        print("🚀 READY FOR KAGGLE!")
        print("\nNext steps:")
        print("1. Zip the output/docling/chunked/ folder")
        print("2. Upload to Kaggle as a dataset")
        print("3. Run kaggle_embed_docling.py with GPU T4 x2")
    else:
        print("⚠️  FIX ISSUES BEFORE UPLOADING TO KAGGLE")
        print("\nRun chunk_docling_simple.py again to regenerate chunks")
    
    print()

def save_report(audit: Dict):
    """Save audit report to file"""
    
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("PRE-KAGGLE AUDIT REPORT: DOCLING CHUNKS\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Total files: {audit['total_files']}\n")
        f.write(f"Total chunks: {audit['total_chunks']}\n")
        f.write(f"Unique IDs: {len(audit['unique_ids'])}\n\n")
        
        if audit['duplicate_ids']:
            f.write(f"Duplicate IDs ({len(audit['duplicate_ids'])}):\n")
            for dup_id in audit['duplicate_ids']:
                f.write(f"  - {dup_id}\n")
            f.write("\n")
        
        if audit['empty_content']:
            f.write(f"Empty content ({len(audit['empty_content'])}):\n")
            for chunk_id in audit['empty_content']:
                f.write(f"  - {chunk_id}\n")
            f.write("\n")
        
        if audit['errors']:
            f.write(f"Errors ({len(audit['errors'])}):\n")
            for error in audit['errors']:
                f.write(f"  - {error}\n")
            f.write("\n")
        
        f.write("Metadata fields:\n")
        for field, count in sorted(audit['metadata_fields'].items()):
            f.write(f"  {field}: {count}\n")
    
    print(f"📄 Report saved to: {REPORT_FILE}")

def main():
    """Run audit"""
    audit = audit_chunks()
    print_audit_report(audit)
    save_report(audit)

if __name__ == "__main__":
    main()
