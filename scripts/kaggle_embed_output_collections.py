"""
Kaggle GPU Script: Embed all collections from the output directory.

USAGE IN KAGGLE:
    1. Upload this script to Kaggle notebook.
    2. Upload src/templates/embedder_template.py to Kaggle notebook.
    3. Add the chunked directories as input datasets (e.g., docling-project_docling_chunked).
    4. Set accelerator to GPU T4 x2.
    5. Run: !python kaggle_embed_output_collections.py
    6. Download outputs from /kaggle/working/

REQUIREMENTS:
    - GPU: Tesla T4 x2 (15.83 GB VRAM each)
    - Input datasets: Chunked directories from the 'output' folder.
    - Output: JSONL files for each embedded collection in /kaggle/working/
"""

import sys
from pathlib import Path
import os

# Add templates to path
sys.path.insert(0, '/kaggle/working')
sys.path.insert(0, '/kaggle/working/rad_clean/src/templates')
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'templates'))

# Import embedder template
from embedder_template import UniversalEmbedder, EmbedderConfig  # type: ignore

def main():
    """Embed all collections found in the /kaggle/input/ directory."""
    
    print("=" * 80)
    print("KAGGLE GPU EMBEDDING: ALL OUTPUT COLLECTIONS")
    print("=" * 80)
    print()
    
    # Dynamically find collections to process from /kaggle/input
    input_dir = Path("/kaggle/input")
    collections = []
    for item in input_dir.iterdir():
        if item.is_dir() and item.name.endswith('_chunked'):
            collection_name = item.name.replace('_chunked', '').replace('-', '_')
            collections.append({
                "name": collection_name,
                "input_dataset": item.name,
                "output_file": f"{collection_name}_embeddings_768.jsonl"
            })

    if not collections:
        print("No chunked datasets found in /kaggle/input/. Please add your chunked datasets.")
        return

    print("Found the following collections to process:")
    for collection in collections:
        print(f"  - {collection['name']}")
    print()

    # Process each collection
    for collection in collections:
        print(f"Processing collection: {collection['name']}")
        print("-" * 40)
        
        # Configure paths
        config = EmbedderConfig(
            collection_name=collection["name"],
            input_path=input_dir / collection['input_dataset'],
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
    for collection in collections:
        print(f"   - {collection['output_file']}")
    print("   Location: Kaggle notebook -> Output tab -> Download all")
    print()


if __name__ == "__main__":
    main()
