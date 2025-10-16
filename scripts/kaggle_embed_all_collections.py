"""
Kaggle GPU Script: Embed all collections (docling, qdrant_ecosystem, sentence_transformers)

USAGE IN KAGGLE:
    1. Upload this script to Kaggle notebook
    2. Upload src/templates/embedder_template.py to Kaggle notebook
    3. Add the following as input datasets:
       - docling-project_docling_chunked
       - qdrant-ecosystem-chunked
       - sentence-transformers-docs-chunked
    4. Set accelerator to GPU T4 x2
    5. Run: !python kaggle_embed_all_collections.py
    6. Download outputs from /kaggle/working/

REQUIREMENTS:
    - GPU: Tesla T4 x2 (15.83 GB VRAM each)
    - Input datasets: The three chunked directories
    - Output: Three JSONL files in /kaggle/working/

EXPECTED OUTPUT:
    - docling_embeddings_768.jsonl
    - qdrant_ecosystem_embeddings_768.jsonl
    - sentence_transformers_embeddings_768.jsonl
    - Processing time: ~30-60 minutes total on dual T4

COLLECTIONS PROCESSED:
    - docling: Docling project documentation
    - qdrant_ecosystem: Qdrant ecosystem docs
    - sentence_transformers: Sentence Transformers docs
"""

import sys
from pathlib import Path

# Add templates to path - handle both direct upload and repo structure
sys.path.insert(0, '/kaggle/working')
sys.path.insert(0, '/kaggle/working/rad_clean/src/templates')
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'templates'))

# Import embedder template
from embedder_template import UniversalEmbedder, EmbedderConfig  # type: ignore

def main():
    """Embed all collections."""
    
    print("=" * 80)
    print("KAGGLE GPU EMBEDDING: ALL COLLECTIONS")
    print("=" * 80)
    print()
    
    # Define collections to process
    collections = [
        {
            "name": "docling",
            "input_dataset": "docling-project_docling_chunked",
            "output_file": "docling_embeddings_768.jsonl"
        },
        {
            "name": "qdrant_ecosystem", 
            "input_dataset": "qdrant-ecosystem-chunked",
            "output_file": "qdrant_ecosystem_embeddings_768.jsonl"
        },
        {
            "name": "sentence_transformers",
            "input_dataset": "sentence-transformers-docs-chunked", 
            "output_file": "sentence_transformers_embeddings_768.jsonl"
        }
    ]
    
    # Process each collection
    for collection in collections:
        print(f"Processing collection: {collection['name']}")
        print("-" * 40)
        
        # Configure paths
        config = EmbedderConfig(
            collection_name=collection["name"],
            input_path=Path(f"/kaggle/input/{collection['input_dataset']}"),
            output_path=Path(f"/kaggle/working/{collection['output_file']}"),
            use_gpu=True,
            use_data_parallel=True
        )
        
        # Check if input exists
        if not config.input_path.exists():
            print(f"WARNING: Input path {config.input_path} does not exist. Skipping {collection['name']}.")
            print()
            continue
        
        # Run embedder
        embedder = UniversalEmbedder(config)
        embedder.run()
        
        # Validate output
        if config.output_path.exists():
            with open(config.output_path, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f if _.strip())
            print(f"✓ {collection['name']}: {line_count:,} records written to {config.output_path.name}")
        else:
            print(f"✗ {collection['name']}: No output file created")
        
        print()
    
    print("=" * 80)
    print("ALL EMBEDDINGS COMPLETE!")
    print("=" * 80)
    print()
    print("DOWNLOAD OUTPUTS:")
    print("   Files in /kaggle/working/:")
    print("   - docling_embeddings_768.jsonl")
    print("   - qdrant_ecosystem_embeddings_768.jsonl") 
    print("   - sentence_transformers_embeddings_768.jsonl")
    print("   Location: Kaggle notebook -> Output tab -> Download all")
    print()


if __name__ == "__main__":
    main()