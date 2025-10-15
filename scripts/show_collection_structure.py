"""
Display all Qdrant collections with actual subdirectory structures from metadata
"""
from qdrant_client import QdrantClient
from collections import defaultdict, Counter
from pathlib import Path

# Connect to local Qdrant
client = QdrantClient(url="http://localhost:6333")

print("=" * 100)
print("📚 QDRANT COLLECTIONS - COMPLETE DIRECTORY STRUCTURE")
print("=" * 100)
print()

# Get all collections
collections = client.get_collections()

total_points = 0
collection_data = []

for col in collections.collections:
    col_name = col.name
    info = client.get_collection(col_name)
    points_count = info.points_count
    vector_size = info.config.params.vectors.size
    quantization = info.config.quantization_config
    
    total_points += points_count
    
    # Sample ALL points to get complete directory structure
    all_points = []
    offset = None
    batch_size = 100
    
    while True:
        batch, next_offset = client.scroll(
            collection_name=col_name,
            limit=batch_size,
            offset=offset,
            with_payload=True,
            with_vectors=False
        )
        all_points.extend(batch)
        
        if next_offset is None or len(all_points) >= points_count:
            break
        offset = next_offset
    
    # Analyze directory structure from source paths
    dir_counts = Counter()
    file_counts = Counter()
    subdirs = set()
    
    for point in all_points:
        if point.payload and 'source' in point.payload:
            source = point.payload['source']
            # Normalize path separators
            source = source.replace('\\', '/')
            
            # Extract directory structure
            path_parts = source.split('/')
            
            # Find the collection-related directory
            for i, part in enumerate(path_parts):
                # Look for key directory markers
                if any(marker in part.lower() for marker in [
                    col_name.replace('_', ''),
                    'docs',
                    'viator',
                    'fast',
                    'pydantic',
                    'inngest'
                ]):
                    # Get subdirectory if exists
                    if i + 1 < len(path_parts) - 1:  # Has subdir before filename
                        subdir = path_parts[i + 1]
                        subdirs.add(subdir)
                        dir_counts[subdir] += 1
                    
                    # Get filename
                    if i + 1 < len(path_parts):
                        filename = path_parts[-1]
                        file_counts[filename] += 1
                    break
    
    collection_data.append({
        'name': col_name,
        'points': points_count,
        'vector_size': vector_size,
        'quantization': quantization,
        'subdirs': sorted(subdirs),
        'dir_counts': dir_counts,
        'file_counts': file_counts,
        'unique_files': len(file_counts)
    })

# Display results
for data in collection_data:
    print("=" * 100)
    print(f"📦 {data['name'].upper()}")
    print("=" * 100)
    print(f"📊 Total Chunks: {data['points']:,}")
    print(f"📏 Vector Dimension: {data['vector_size']}")
    print(f"🗜️  Quantization: {data['quantization']}")
    print(f"📄 Unique Files: {data['unique_files']}")
    print()
    
    if data['subdirs']:
        print(f"📁 SUBDIRECTORIES ({len(data['subdirs'])} total):")
        print()
        for subdir in data['subdirs']:
            count = data['dir_counts'][subdir]
            percentage = (count / data['points']) * 100
            print(f"  ├── {subdir}/")
            print(f"  │   ├─ Chunks: {count:,} ({percentage:.1f}%)")
            # Show top 3 files in this subdir
            subdir_files = [(f, c) for f, c in data['file_counts'].items() if c > 0]
            if subdir_files:
                top_files = sorted(subdir_files, key=lambda x: x[1], reverse=True)[:3]
                for fname, fcount in top_files:
                    print(f"  │   │  • {fname[:50]}: {fcount} chunks")
            print(f"  │")
        print()
    else:
        print("📁 STRUCTURE: Single directory (no subdirectories)")
        print()
        # Show top 5 files
        if data['file_counts']:
            print("  Top 5 Files:")
            top_files = sorted(data['file_counts'].items(), key=lambda x: x[1], reverse=True)[:5]
            for fname, fcount in top_files:
                percentage = (fcount / data['points']) * 100
                print(f"  ├─ {fname[:60]}: {fcount} chunks ({percentage:.1f}%)")
        print()

print("=" * 100)
print("📊 OVERALL SUMMARY")
print("=" * 100)
print(f"Total Collections: {len(collection_data)}")
print(f"Total Chunks: {total_points:,}")
print(f"Vector Dimension: 3584 (nomic-embed-code)")
print()

print("📦 Collections Overview:")
print()
for data in collection_data:
    subdirs_text = f"{len(data['subdirs'])} subdirs" if data['subdirs'] else "single dir"
    quant_text = "✓ Quantized" if data['quantization'] else "✗ Not quantized"
    print(f"  • {data['name']:25} │ {data['points']:>6,} chunks │ {data['unique_files']:>4} files │ {subdirs_text:12} │ {quant_text}")

print()
print("=" * 100)
print()

# Create detailed structure document
print("💡 TIP: For detailed subdirectory mapping, check the COLLECTION_STRUCTURE.md file")
print()
