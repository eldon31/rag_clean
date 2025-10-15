"""
Simple Chunking Script for Docling Documentation
No API keys required - pure chunking without embeddings

Uses simple regex-based chunking for markdown files
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Configuration
COLLECTION_NAME = "docling"
INPUT_DIR = Path("Docs/docling-project_docling")
OUTPUT_CHUNKED_DIR = Path("output/docling/chunked")
MAX_CHUNK_SIZE = 2048  # Characters per chunk (roughly 512 tokens)
MIN_CHUNK_SIZE = 100   # Minimum chunk size
CHUNK_OVERLAP = 200    # Overlap between chunks

def setup_directories():
    """Create output directories"""
    OUTPUT_CHUNKED_DIR.mkdir(parents=True, exist_ok=True)
    print("✓ Output directories ready")

def chunk_markdown_file(content: str, source_file: str) -> List[Dict]:
    """
    Chunk markdown content by headings and size
    
    Strategy:
    1. Split by markdown headings (# ## ### etc)
    2. Keep chunks under MAX_CHUNK_SIZE
    3. Add overlap for context
    4. Preserve heading hierarchy
    """
    chunks = []
    
    # Find all headings with regex
    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    sections = []
    current_section = {"heading": "", "level": 0, "content": ""}
    last_pos = 0
    
    for match in heading_pattern.finditer(content):
        # Save previous section
        if current_section["content"].strip():
            sections.append(current_section.copy())
        
        level = len(match.group(1))
        heading = match.group(2).strip()
        start_pos = match.start()
        
        # Add content before this heading to previous section
        if last_pos < start_pos:
            if sections:
                sections[-1]["content"] += content[last_pos:start_pos]
            else:
                current_section["content"] = content[last_pos:start_pos]
        
        # Start new section
        current_section = {
            "heading": heading,
            "level": level,
            "content": match.group(0) + "\n"
        }
        last_pos = match.end()
    
    # Add remaining content
    if last_pos < len(content):
        current_section["content"] += content[last_pos:]
    if current_section["content"].strip():
        sections.append(current_section)
    
    # If no headings found, treat entire file as one section
    if not sections:
        sections = [{
            "heading": source_file.replace('.md', ''),
            "level": 1,
            "content": content
        }]
    
    # Now chunk each section
    chunk_index = 0
    for section in sections:
        section_content = section["content"].strip()
        
        if not section_content or len(section_content) < MIN_CHUNK_SIZE:
            continue
        
        if len(section_content) > MAX_CHUNK_SIZE:
            # Split large sections into smaller chunks
            paragraphs = section_content.split('\n\n')
            current_chunk = ""
            
            for para in paragraphs:
                # If adding this paragraph exceeds max size, save current chunk
                if len(current_chunk) + len(para) > MAX_CHUNK_SIZE and current_chunk:
                    chunks.append({
                        "chunk_id": f"{COLLECTION_NAME}:{source_file}:chunk:{chunk_index}",
                        "content": current_chunk.strip(),
                        "metadata": {
                            "source": source_file,
                            "heading": section["heading"],
                            "heading_level": section["level"],
                            "chunk_index": chunk_index,
                            "collection": COLLECTION_NAME,
                            "char_count": len(current_chunk.strip()),
                            "estimated_tokens": len(current_chunk.strip()) // 4
                        }
                    })
                    chunk_index += 1
                    # Start new chunk with overlap
                    overlap_text = current_chunk[-CHUNK_OVERLAP:] if len(current_chunk) > CHUNK_OVERLAP else ""
                    current_chunk = overlap_text + para + "\n\n"
                else:
                    current_chunk += para + "\n\n"
            
            # Save remaining chunk
            if current_chunk.strip():
                chunks.append({
                    "chunk_id": f"{COLLECTION_NAME}:{source_file}:chunk:{chunk_index}",
                    "content": current_chunk.strip(),
                    "metadata": {
                        "source": source_file,
                        "heading": section["heading"],
                        "heading_level": section["level"],
                        "chunk_index": chunk_index,
                        "collection": COLLECTION_NAME,
                        "char_count": len(current_chunk.strip()),
                        "estimated_tokens": len(current_chunk.strip()) // 4
                    }
                })
                chunk_index += 1
        else:
            # Section is small enough, use as-is
            chunks.append({
                "chunk_id": f"{COLLECTION_NAME}:{source_file}:chunk:{chunk_index}",
                "content": section_content,
                "metadata": {
                    "source": source_file,
                    "heading": section["heading"],
                    "heading_level": section["level"],
                    "chunk_index": chunk_index,
                    "collection": COLLECTION_NAME,
                    "char_count": len(section_content),
                    "estimated_tokens": len(section_content) // 4
                }
            })
            chunk_index += 1
    
    # Update total chunks in metadata
    for chunk in chunks:
        chunk["metadata"]["total_chunks"] = len(chunks)
    
    return chunks

def chunk_all_documents() -> List[Dict]:
    """Process all markdown files in the input directory"""
    print(f"\n{'='*60}")
    print("CHUNKING DOCLING DOCUMENTATION")
    print(f"{'='*60}")
    print(f"Input: {INPUT_DIR}")
    print(f"Max chunk size: {MAX_CHUNK_SIZE} characters (~{MAX_CHUNK_SIZE//4} tokens)")
    print(f"Overlap: {CHUNK_OVERLAP} characters")
    print(f"{'='*60}\n")
    
    if not INPUT_DIR.exists():
        print(f"❌ Error: {INPUT_DIR} not found!")
        return []
    
    all_chunks = []
    unique_ids = set()
    
    md_files = sorted(INPUT_DIR.glob("*.md"))
    print(f"Found {len(md_files)} markdown files\n")
    
    for md_file in md_files:
        try:
            # Read markdown content
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                print(f"  ⊘ {md_file.name}: Empty file, skipping")
                continue
            
            # Chunk the file
            chunks = chunk_markdown_file(content, md_file.name)
            
            if chunks:
                # Check for duplicate IDs
                for chunk in chunks:
                    chunk_id = chunk["chunk_id"]
                    if chunk_id in unique_ids:
                        print(f"  ⚠️ Duplicate ID: {chunk_id}")
                    unique_ids.add(chunk_id)
                
                # Save chunks to individual file
                output_file = OUTPUT_CHUNKED_DIR / f"{md_file.stem}_chunks.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(chunks, f, ensure_ascii=False, indent=2)
                
                all_chunks.extend(chunks)
                avg_tokens = sum(c["metadata"]["estimated_tokens"] for c in chunks) // len(chunks)
                print(f"  ✓ {md_file.name}: {len(chunks)} chunks (avg ~{avg_tokens} tokens/chunk)")
        
        except Exception as e:
            print(f"  ✗ Error processing {md_file.name}: {e}")
    
    return all_chunks

def save_summary(chunks: List[Dict]):
    """Save chunking summary"""
    summary_file = OUTPUT_CHUNKED_DIR / "chunking_summary.json"
    
    # Calculate statistics
    total_chars = sum(c["metadata"]["char_count"] for c in chunks)
    total_tokens = sum(c["metadata"]["estimated_tokens"] for c in chunks)
    
    summary = {
        "collection": COLLECTION_NAME,
        "timestamp": datetime.now().isoformat(),
        "total_chunks": len(chunks),
        "chunking_method": "Regex-based (heading-aware)",
        "total_characters": total_chars,
        "estimated_total_tokens": total_tokens,
        "avg_chars_per_chunk": total_chars // len(chunks) if chunks else 0,
        "avg_tokens_per_chunk": total_tokens // len(chunks) if chunks else 0,
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
    
    print(f"\n✓ Saved summary to {summary_file}")
    return summary

def main():
    """Main execution"""
    pipeline_start = datetime.now()
    
    print(f"\n{'='*60}")
    print("DOCLING DOCS CHUNKING PIPELINE")
    print(f"{'='*60}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Method: Regex-based (no API required)")
    print(f"{'='*60}\n")
    
    setup_directories()
    chunks = chunk_all_documents()
    
    if not chunks:
        print("\n❌ No chunks generated!")
        return
    
    summary = save_summary(chunks)
    
    total_time = (datetime.now() - pipeline_start).total_seconds()
    
    print(f"\n{'='*60}")
    print("✓ CHUNKING COMPLETED")
    print(f"{'='*60}")
    print(f"Total chunks: {summary['total_chunks']}")
    print(f"Files processed: {summary['files_processed']}")
    print(f"Average chunk size: ~{summary['avg_tokens_per_chunk']} tokens")
    print(f"Total estimated tokens: ~{summary['estimated_total_tokens']:,}")
    print(f"Time: {total_time:.2f} seconds")
    print(f"Output: {OUTPUT_CHUNKED_DIR}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
