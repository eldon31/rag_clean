"""
Kaggle GPU Script: Embed sentence_transformers_docs collection

USAGE IN KAGGLE:
    1. Upload this script to Kaggle notebook
    2. Upload src/templates/embedder_template.py to Kaggle notebook
    3. Add sentence-transformers-docs-chunked as input dataset
    4. Set accelerator to GPU T4 x2
    5. Run: !python scripts/kaggle_embed_sentence_transformers.py
    6. Download output from /kaggle/working/

REQUIREMENTS:
    - GPU: Tesla T4 x2 (15.83 GB VRAM each)
    - Input dataset: sentence_transformers_docs_chunked/
    - Output: sentence_transformers_embeddings_768.jsonl

EXPECTED OUTPUT:
    - ~457 chunks embedded with CodeRankEmbed (768-dim)
    - File size: ~3-5 MB
    - Processing time: ~1-3 minutes on dual T4
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
    """Embed sentence_transformers_docs collection."""
    
    print("=" * 60)
    print("KAGGLE GPU EMBEDDING: sentence_transformers_docs")
    print("=" * 60)
    print()
    
    # Configure paths
    config = EmbedderConfig(
        collection_name="sentence_transformers_docs",
        input_path=Path("/kaggle/input/sentence-transformers-docs-chunked"),
        output_path=Path("/kaggle/working/sentence_transformers_embeddings_768.jsonl"),
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
    print("   File: /kaggle/working/sentence_transformers_embeddings_768.jsonl")
    print("   Location: Kaggle notebook -> Output tab -> Download")
    print()


if __name__ == "__main__":
    main()
