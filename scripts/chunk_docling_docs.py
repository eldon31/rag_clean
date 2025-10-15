"""
Chunk Docling Documentation using HybridChunker
Pure chunking pipeline without embedding generation

Uses src/ingestion/chunker.py with Docling's HybridChunker for intelligent document splitting
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import directly from modules to avoid embedder initialization
from src.ingestion.chunker import DoclingHybridChunker, ChunkingConfig
from src.ingestion.processor import DocumentProcessor

# Configuration
COLLECTION_NAME = "docling"
INPUT_DIR = Path("Docs/docling-project_docling")
OUTPUT_CHUNKED_DIR = Path("output/docling/chunked")

def setup_directories():
    """Create output directories"""
    OUTPUT_CHUNKED_DIR.mkdir(parents=True, exist_ok=True)
    print("✓ Output directories ready")

def chunk_documents_with_hybrid() -> List[Dict]:
    """Chunk documents using HybridChunker"""
    print(f"\n{'='*60}")
    print("CHUNKING DOCUMENTS WITH HYBRIDCHUNKER")
    print(f"{'='*60}")

    if not INPUT_DIR.exists():
        print(f"❌ Error: {INPUT_DIR} not found!")
        return []

    # Initialize chunker with config
    chunking_config = ChunkingConfig(
        chunk_size=2048,        # Target characters per chunk (optimized for code)
        chunk_overlap=100,      # Character overlap between chunks
        max_chunk_size=4096,    # Maximum chunk size
        min_chunk_size=100,     # Minimum chunk size
        use_semantic_splitting=True,  # Use HybridChunker
        preserve_structure=True,      # Preserve document structure
        max_tokens=2048         # Maximum tokens for nomic-embed-code model
    )
    
    chunker = DoclingHybridChunker(chunking_config)
    print(f"✓ Initialized HybridChunker (max_tokens={chunking_config.max_tokens})")

    # Initialize processor for markdown processing
    processor = DocumentProcessor()
    print("✓ Initialized DocumentProcessor")

    all_chunks_data = []
    unique_ids = set()

    md_files = sorted(INPUT_DIR.glob("*.md"))
    print(f"\nFound {len(md_files)} markdown files\n")

    for md_file in md_files:
        try:
            print(f"Processing {md_file.name}...")
            
            # Read markdown content
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                print(f"  ⊘ Empty file, skipping")
                continue

            # Process markdown file to get DoclingDocument
            processed_doc = processor.process_file(str(md_file))
            docling_doc = processed_doc.docling_document
            
            # Chunk using HybridChunker (async method, run synchronously)
            import asyncio
            chunks = asyncio.run(chunker.chunk_document(
                content=content,
                title=md_file.stem,
                source=md_file.name,
                metadata={
                    "collection": COLLECTION_NAME,
                    "file_path": str(md_file)
                },
                docling_doc=docling_doc
            ))

            if chunks:
                # Convert DocumentChunk objects to dict format
                chunks_data = []
                for chunk in chunks:
                    chunk_id = f"{COLLECTION_NAME}:{md_file.name}:chunk:{chunk.index}"
                    
                    if chunk_id in unique_ids:
                        print(f"  ⚠️ Duplicate ID: {chunk_id}")
                    unique_ids.add(chunk_id)
                    
                    chunk_dict = {
                        "chunk_id": chunk_id,
                        "content": chunk.content,
                        "metadata": {
                            **chunk.metadata,
                            "chunk_index": chunk.index,
                            "token_count": chunk.token_count,
                            "char_start": chunk.start_char,
                            "char_end": chunk.end_char
                        }
                    }
                    chunks_data.append(chunk_dict)

                # Save chunks to JSON
                output_file = OUTPUT_CHUNKED_DIR / f"{md_file.stem}_chunks.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(chunks_data, f, ensure_ascii=False, indent=2)

                all_chunks_data.extend(chunks_data)
                
                # Calculate average tokens (handling None values)
                total_tokens = sum(c.token_count for c in chunks if c.token_count is not None)
                avg_tokens = total_tokens // len(chunks) if chunks else 0
                print(f"  ✓ {md_file.name}: {len(chunks)} chunks (avg {avg_tokens} tokens/chunk)")

        except Exception as e:
            print(f"  ✗ Error processing {md_file.name}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*60}")
    print(f"✓ Total chunks: {len(all_chunks_data)}")
    print(f"✓ Unique IDs: {len(unique_ids)}")
    print(f"✓ Output directory: {OUTPUT_CHUNKED_DIR}")
    print(f"{'='*60}\n")

    return all_chunks_data

def save_summary(chunks: List[Dict]):
    """Save chunking summary"""
    summary_file = OUTPUT_CHUNKED_DIR / "chunking_summary.json"
    
    summary = {
        "collection": COLLECTION_NAME,
        "timestamp": datetime.now().isoformat(),
        "total_chunks": len(chunks),
        "chunking_method": "HybridChunker (Docling)",
        "files_processed": len(set(c["metadata"]["source"] for c in chunks)),
        "chunks_by_file": {}
    }
    
    # Group by file
    for chunk in chunks:
        source = chunk["metadata"]["source"]
        if source not in summary["chunks_by_file"]:
            summary["chunks_by_file"][source] = 0
        summary["chunks_by_file"][source] += 1
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Saved summary to {summary_file}")

def main():
    """Main execution"""
    pipeline_start = datetime.now()

    print(f"\n{'='*60}")
    print("DOCLING DOCS CHUNKING PIPELINE")
    print(f"{'='*60}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Input: {INPUT_DIR}")
    print(f"Method: HybridChunker (Docling)")
    print(f"{'='*60}\n")

    setup_directories()
    chunks = chunk_documents_with_hybrid()

    if not chunks:
        print("❌ No chunks generated!")
        return

    save_summary(chunks)

    total_time = (datetime.now() - pipeline_start).total_seconds()

    print(f"\n{'='*60}")
    print("✓ CHUNKING COMPLETED")
    print(f"{'='*60}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Time: {total_time:.2f} seconds")
    print(f"Output: {OUTPUT_CHUNKED_DIR}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
