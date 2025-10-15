"""
Kaggle GPU Script: Embed docling-project_docling collection

USAGE IN KAGGLE:
    1. Upload this script to Kaggle notebook
    2. Upload src/templates/embedder_template.py to Kaggle notebook
    3. Add docling-project_docling_chunked as input dataset
    4. Set accelerator to GPU T4 x2
    5. Run: !python scripts/kaggle_embed_docling.py
    6. Download output from /kaggle/working/

REQUIREMENTS:
    - GPU: Tesla T4 x2 (15.83 GB VRAM each)
    - Input dataset: docling-project_docling_chunked/
    - Output: docling_embeddings_768.jsonl

EXPECTED OUTPUT:
    - ~1,089 chunks embedded with CodeRankEmbed (768-dim)
    - File size: ~8-12 MB
    - Processing time: ~2-5 minutes on dual T4
"""

import sys
from pathlib import Path

# Add templates to path
sys.path.insert(0, '/kaggle/working')

# Import embedder template
from embedder_template import UniversalEmbedder, EmbedderConfig

def main():
    """Embed docling-project_docling collection."""
    
    print("=" * 60)
    print("KAGGLE GPU EMBEDDING: docling-project_docling")
    print("=" * 60)
    print()
    
    # Configure paths
    config = EmbedderConfig(
        collection_name="docling-project_docling",
        input_path=Path("/kaggle/input/docling-project-docling-chunked"),
        output_path=Path("/kaggle/working/docling_embeddings_768.jsonl"),
        use_gpu=True,
        use_data_parallel=True
    )
    
    # Run embedder
    embedder = UniversalEmbedder(config)
    embedder.run()
    
    print()
    print("=" * 60)
    print("EMBEDDING COMPLETE!")
    print("=" * 60)
    print()
    print("DOWNLOAD OUTPUT:")
    print("   File: /kaggle/working/docling_embeddings_768.jsonl")
    print("   Location: Kaggle notebook -> Output tab -> Download")
    print()


if __name__ == "__main__":
    main()
