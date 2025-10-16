"""
Kaggle GPU Script: Embed qdrant_ecosystem collection

USAGE IN KAGGLE:
    1. Upload this script to Kaggle notebook
    2. Upload src/templates/embedder_template.py to Kaggle notebook  
    3. Add qdrant-ecosystem-chunked as input dataset
    4. Set accelerator to GPU T4 x2
    5. Run: !python embed_qdrant_ecosystem_collection.py
    6. Download output from /kaggle/working/

REQUIREMENTS:
    - GPU: Tesla T4 x2 (15.83 GB VRAM each)
    - Input dataset: qdrant_ecosystem_chunked/ (with subfolders)
    - Output: qdrant_ecosystem_embeddings_768.jsonl
"""

import sys
from pathlib import Path

# Add templates to path
sys.path.insert(0, '/kaggle/working')
sys.path.insert(0, '/kaggle/working/rad_clean/src/templates')
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'templates'))

# Import embedder template
from embedder_template import UniversalEmbedder, EmbedderConfig  # type: ignore

def main():
    """Embed qdrant_ecosystem collection."""
    
    print("=" * 60)
    print("KAGGLE GPU EMBEDDING: qdrant_ecosystem")
    print("=" * 60)
    print()
    
    # Configure paths
    config = EmbedderConfig(
        collection_name="qdrant_ecosystem",
        input_path=Path("/kaggle/input/qdrant-ecosystem-chunked"),
        output_path=Path("/kaggle/working/qdrant_ecosystem_embeddings_768.jsonl"),
        use_gpu=True,
        use_data_parallel=True
    )
    
    # Run embedder
    embedder = UniversalEmbedder(config)
    embedder.run()

    if config.output_path.exists():
        with open(config.output_path, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f if _.strip())
        print(f"JSONL VALIDATION: {line_count:,} records written to {config.output_path.name}")
        if line_count <= 1:
            print("WARNING: Expected multiple JSONL records. Inspect the output file before uploading.")
    
    print()
    print("=" * 60)
    print("EMBEDDING COMPLETE!")
    print("=" * 60)
    print()
    print("DOWNLOAD OUTPUT:")
    print("   File: /kaggle/working/qdrant_ecosystem_embeddings_768.jsonl")
    print("   Location: Kaggle notebook -> Output tab -> Download")
    print()


if __name__ == "__main__":
    main()
