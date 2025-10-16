"""
KAGGLE NOTEBOOK: Batch Embed All Collections with CodeRankEmbed

This notebook runs all three embedding scripts in sequence.
Upload this entire file to Kaggle and run it.

SETUP:
1. Create new Kaggle Notebook
2. Add these INPUT datasets:
   - qdrant-ecosystem-chunked
   - docling-project-docling-chunked
   - sentence-transformers-docs-chunked
3. Set accelerator: GPU T4 x2
4. Upload this file + embedder_template.py
5. Run all cells

OUTPUTS (Download from /kaggle/working/):
   - qdrant_ecosystem_embeddings_768.jsonl (~60-80 MB)
   - docling_embeddings_768.jsonl (~8-12 MB)
   - sentence_transformers_embeddings_768.jsonl (~3-5 MB)

TOTAL TIME: ~15-20 minutes on GPU T4 x2
"""

# ============================================================================
# CELL 1: Setup and Imports
# ============================================================================

import sys
from pathlib import Path
import json

print("=" * 70)
print("KAGGLE BATCH EMBEDDING: CodeRankEmbed (768-dim)")
print("=" * 70)
print()
print("Collections to embed:")
print("  1. qdrant_ecosystem (~8,108 chunks)")
print("  2. docling-project_docling (~1,089 chunks)")
print("  3. sentence_transformers_docs (~457 chunks)")
print()
print("Model: nomic-ai/CodeRankEmbed (768-dim)")
print("GPU: Tesla T4 x2")
print("=" * 70)
print()

# Add templates to path
sys.path.insert(0, '/kaggle/working')
sys.path.insert(0, '/kaggle/working/rad_clean/src/templates')

# Import embedder template
try:
    from embedder_template import UniversalEmbedder, EmbedderConfig
    print("✅ Successfully imported embedder_template")
except ImportError as e:
    print(f"❌ Failed to import embedder_template: {e}")
    print("⚠️  Make sure embedder_template.py is uploaded to Kaggle!")
    sys.exit(1)

print()


# ============================================================================
# CELL 2: Verify Input Datasets
# ============================================================================

print("=" * 70)
print("CHECKING INPUT DATASETS")
print("=" * 70)
print()

datasets = {
    "qdrant_ecosystem": Path("/kaggle/input/qdrant-ecosystem-chunked"),
    "docling": Path("/kaggle/input/docling-project-docling-chunked"),
    "sentence_transformers": Path("/kaggle/input/sentence-transformers-docs-chunked")
}

all_found = True
for name, path in datasets.items():
    if path.exists():
        chunk_files = list(path.glob("**/*_chunks.json"))
        print(f"✅ {name}: {len(chunk_files)} chunk files found")
    else:
        print(f"❌ {name}: NOT FOUND at {path}")
        all_found = False

if not all_found:
    print()
    print("⚠️  Missing datasets! Add them as Kaggle inputs before running.")
    sys.exit(1)

print()
print("✅ All datasets found!")
print()


# ============================================================================
# CELL 3: Embed qdrant_ecosystem (Largest, ~10-15 min)
# ============================================================================

print("=" * 70)
print("EMBEDDING 1/3: qdrant_ecosystem")
print("=" * 70)
print()

config_qdrant = EmbedderConfig(
    collection_name="qdrant_ecosystem",
    input_path=Path("/kaggle/input/qdrant-ecosystem-chunked"),
    output_path=Path("/kaggle/working/qdrant_ecosystem_embeddings_768.jsonl"),
    use_gpu=True,
    use_data_parallel=True
)

embedder_qdrant = UniversalEmbedder(config_qdrant)
embedder_qdrant.run()

print()
print("✅ qdrant_ecosystem complete!")
print()


# ============================================================================
# CELL 4: Embed docling (Medium, ~2-5 min)
# ============================================================================

print("=" * 70)
print("EMBEDDING 2/3: docling-project_docling")
print("=" * 70)
print()

config_docling = EmbedderConfig(
    collection_name="docling-project_docling",
    input_path=Path("/kaggle/input/docling-project-docling-chunked"),
    output_path=Path("/kaggle/working/docling_embeddings_768.jsonl"),
    use_gpu=True,
    use_data_parallel=True
)

embedder_docling = UniversalEmbedder(config_docling)
embedder_docling.run()

print()
print("✅ docling complete!")
print()


# ============================================================================
# CELL 5: Embed sentence_transformers (Small, ~1-3 min)
# ============================================================================

print("=" * 70)
print("EMBEDDING 3/3: sentence_transformers_docs")
print("=" * 70)
print()

config_st = EmbedderConfig(
    collection_name="sentence_transformers_docs",
    input_path=Path("/kaggle/input/sentence-transformers-docs-chunked"),
    output_path=Path("/kaggle/working/sentence_transformers_embeddings_768.jsonl"),
    use_gpu=True,
    use_data_parallel=True
)

embedder_st = UniversalEmbedder(config_st)
embedder_st.run()

print()
print("✅ sentence_transformers complete!")
print()


# ============================================================================
# CELL 6: Verify All Outputs
# ============================================================================

print("=" * 70)
print("VERIFICATION: All Embeddings")
print("=" * 70)
print()

output_files = [
    Path("/kaggle/working/qdrant_ecosystem_embeddings_768.jsonl"),
    Path("/kaggle/working/docling_embeddings_768.jsonl"),
    Path("/kaggle/working/sentence_transformers_embeddings_768.jsonl")
]

total_size = 0
total_embeddings = 0

for output_file in output_files:
    if not output_file.exists():
        print(f"❌ {output_file.name}: NOT FOUND")
        continue
    
    # Count lines (embeddings)
    with open(output_file, 'r') as f:
        num_lines = sum(1 for _ in f)
    
    # Check file size
    size_mb = output_file.stat().st_size / 1e6
    total_size += size_mb
    total_embeddings += num_lines
    
    # Verify first line is valid JSON with 768-dim embedding
    with open(output_file, 'r') as f:
        first_line = f.readline().strip()
        try:
            record = json.loads(first_line)
            embedding_dim = len(record.get('embedding', []))
            
            if embedding_dim == 768:
                print(f"✅ {output_file.name}")
                print(f"   Embeddings: {num_lines:,}")
                print(f"   Size: {size_mb:.2f} MB")
                print(f"   Dimension: {embedding_dim} ✓")
            else:
                print(f"⚠️  {output_file.name}")
                print(f"   Embeddings: {num_lines:,}")
                print(f"   Dimension: {embedding_dim} (expected 768)")
        except json.JSONDecodeError:
            print(f"❌ {output_file.name}: Invalid JSON format")
    
    print()

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Total embeddings: {total_embeddings:,}")
print(f"Total file size: {total_size:.2f} MB")
print(f"Vector dimension: 768 (CodeRankEmbed)")
print()
print("DOWNLOAD FILES:")
print("1. Go to Kaggle notebook -> Output tab")
print("2. Download all .jsonl files")
print("3. Upload to your local machine for Qdrant ingestion")
print()
print("=" * 70)
print("🎉 ALL EMBEDDINGS COMPLETE!")
print("=" * 70)
