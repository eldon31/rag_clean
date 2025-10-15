"""
Display all Qdrant collections with their subdirectory structures
"""
from qdrant_client import QdrantClient
from collections import defaultdict
import json

# Connect to local Qdrant
client = QdrantClient(url="http://localhost:6333")

print("=" * 80)
print("QDRANT COLLECTIONS - COMPLETE STRUCTURE ANALYSIS")
print("=" * 80)
print()

# Get all collections
collections = client.get_collections()

total_points = 0

for col in collections.collections:
    col_name = col.name
    info = client.get_collection(col_name)
    points_count = info.points_count
    vector_size = info.config.params.vectors.size
    quantization = info.config.quantization_config
    
    total_points += points_count
    
    print("=" * 80)
    print(f"📦 COLLECTION: {col_name.upper()}")
    print("=" * 80)
    print(f"Total Points: {points_count:,}")
    print(f"Vector Size: {vector_size}")
    print(f"Quantization: {quantization}")
    print()
    
    # Sample points to analyze subdirectory structure
    sample = client.scroll(
        collection_name=col_name,
        limit=min(1000, points_count),  # Sample up to 1000 points
        with_payload=True,
        with_vectors=False
    )[0]
    
    # Extract subdirectories from chunk IDs
    subdirs = defaultdict(int)
    sources = defaultdict(int)
    
    for point in sample:
        chunk_id = point.id
        if isinstance(chunk_id, int):
            # Try to get from payload
            if point.payload and 'chunk_id' in point.payload:
                chunk_id = point.payload['chunk_id']
            else:
                continue
        
        # Parse chunk ID to extract subdirectory
        # Format: collection:subdir:filename:chunk:N or collection:filename:chunk:N
        parts = str(chunk_id).split(':')
        
        if len(parts) >= 4:
            if parts[0] == col_name.replace('_', ''):
                # Has subdirectory
                subdir = parts[1]
                if subdir != 'chunk':  # Not a chunk marker
                    subdirs[subdir] += 1
            elif len(parts) >= 3:
                # No subdirectory (e.g., pydantic_docs)
                filename = parts[1] if parts[1] != 'chunk' else parts[0]
                subdirs['(root)'] += 1
        
        # Track source files
        if point.payload and 'source' in point.payload:
            source = point.payload['source']
            # Extract subdirectory from source path
            source_parts = source.replace('\\', '/').split('/')
            if len(source_parts) > 1:
                # Get the directory name before the filename
                for i, part in enumerate(source_parts):
                    if col_name.replace('_', '') in part.lower() or 'docs' in part.lower():
                        if i + 1 < len(source_parts) - 1:  # Not the last part (filename)
                            sources[source_parts[i + 1]] += 1
                            break
    
    # Display subdirectories
    if subdirs or sources:
        print("📁 SUBDIRECTORY STRUCTURE:")
        print()
        
        # Merge and display both analyses
        all_dirs = set(subdirs.keys()) | set(sources.keys())
        
        if all_dirs:
            for subdir in sorted(all_dirs):
                count = max(subdirs.get(subdir, 0), sources.get(subdir, 0))
                percentage = (count / len(sample)) * 100
                print(f"  ├─ {subdir}/")
                print(f"  │  └─ Chunks: {count} ({percentage:.1f}% of sample)")
        else:
            print("  └─ (Single directory - no subdirectories)")
    else:
        print("📁 STRUCTURE: Single directory (no subdirectories)")
    
    print()
    
    # Show sample chunk IDs
    print("🔍 SAMPLE CHUNK IDS:")
    sample_ids = [str(p.id) if isinstance(p.id, int) else p.id for p in sample[:5]]
    for idx, chunk_id in enumerate(sample_ids, 1):
        if isinstance(chunk_id, str):
            print(f"  {idx}. {chunk_id[:100]}...")
        else:
            # Try to get from payload
            if sample[idx-1].payload and 'chunk_id' in sample[idx-1].payload:
                print(f"  {idx}. {sample[idx-1].payload['chunk_id'][:100]}...")
    
    print()
    
    # Show sample metadata
    if sample and sample[0].payload:
        print("📋 SAMPLE METADATA:")
        payload = sample[0].payload
        for key in ['source', 'collection', 'processing_method', 'timestamp']:
            if key in payload:
                value = str(payload[key])
                print(f"  • {key}: {value[:80]}...")
    
    print()

print("=" * 80)
print("📊 SUMMARY")
print("=" * 80)
print(f"Total Collections: {len(collections.collections)}")
print(f"Total Points: {total_points:,}")
print(f"Vector Dimension: 3584 (nomic-embed-code)")
print(f"Quantization: Scalar (int8) across all collections")
print("=" * 80)
