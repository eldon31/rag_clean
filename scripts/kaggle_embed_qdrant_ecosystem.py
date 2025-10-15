"""
Kaggle GPU Script: Embed qdrant_ecosystem collection

USAGE IN KAGGLE:
    1. Upload this script to Kaggle notebook
    2. Upload src/templates/embedder_template.py to Kaggle notebook  
    3. Add qdrant-ecosystem-chunked as input dataset
    4. Set accelerator to GPU T4 x2
    5. Run: !python scripts/kaggle_embed_qdrant_ecosystem.py
    6. Download output from /kaggle/working/

REQUIREMENTS:
    - GPU: Tesla T4 x2 (15.83 GB VRAM each)
    - Input dataset: qdrant_ecosystem_chunked/ (with subfolders)
    - Output: qdrant_ecosystem_embeddings_768.jsonl

EXPECTED OUTPUT:
    - ~8,108 chunks embedded with CodeRankEmbed (768-dim)
    - File size: ~60-80 MB
    - Processing time: ~10-15 minutes on dual T4

SUBFOLDERS INCLUDED:
    - qdrant_documentation/
    - qdrant_examples/
    - qdrant_fastembed/
    - qdrant_mcp-server-qdrant/
    - qdrant_qdrant/
    - qdrant_qdrant-client/
"""

import sys
from pathlib import Path

# Add templates to path - handle both direct upload and repo structure
sys.path.insert(0, '/kaggle/working')
sys.path.insert(0, '/kaggle/working/rad_clean/src/templates')
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'templates'))

# Import embedder template
from embedder_template import UniversalEmbedder, EmbedderConfig

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
