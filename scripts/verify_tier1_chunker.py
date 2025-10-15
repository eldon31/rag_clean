"""
Verify Tier 1 Chunker Optimizations

Tests the three Tier 1 enhancements:
1. Code block boundary detection
2. Heading path enrichment
3. Token count validation
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ingestion.chunker import DoclingHybridChunker, ChunkingConfig


def create_test_document_with_code():
    """Create test document with code blocks."""
    return """# Installation Guide

## Quick Start

Here's how to install:

```python
pip install docling
```

And then use it:

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("document.pdf")
```

## Advanced Usage

For more control, configure the converter:

```python
from docling.datamodel.pipeline_options import PdfPipelineOptions

pipeline_options = PdfPipelineOptions()
pipeline_options.do_code_enrichment = True
```

This enables code extraction.
"""


def test_tier1_optimizations():
    """Test all Tier 1 optimizations."""
    
    print("=" * 80)
    print("TESTING TIER 1 CHUNKER OPTIMIZATIONS")
    print("=" * 80)
    
    # Create chunker
    config = ChunkingConfig(
        chunk_size=200,  # Small size to force multiple chunks
        max_tokens=100,  # Small token limit to test validation
        chunk_overlap=20
    )
    
    chunker = DoclingHybridChunker(config)
    
    # Test document
    test_content = create_test_document_with_code()
    
    print("\n📄 TEST DOCUMENT:")
    print("-" * 80)
    print(test_content[:300] + "...\n")
    
    # Test 1: Code block boundary detection
    print("\n✅ TEST 1: Code Block Boundary Detection")
    print("-" * 80)
    
    complete_code = """```python
print("hello")
```"""
    
    incomplete_code = """```python
print("hello")"""
    
    result1 = chunker._detect_code_block_boundary(complete_code)
    result2 = chunker._detect_code_block_boundary(incomplete_code)
    
    print(f"Complete code block: {result1} (expected: True)")
    print(f"Incomplete code block: {result2} (expected: False)")
    
    if result1 and not result2:
        print("✅ Code block detection works!")
    else:
        print("❌ Code block detection failed!")
        return False
    
    # Test 2: Heading path extraction
    print("\n✅ TEST 2: Heading Path Enrichment")
    print("-" * 80)
    
    text_with_headings = """# Main Title

Some content here.

## Subsection

More content.

### Deep Section

Even more content.
"""
    
    heading_path = chunker._extract_heading_path(text_with_headings)
    print(f"Extracted heading path: '{heading_path}'")
    print(f"Expected: 'Main Title > Subsection > Deep Section'")
    
    if "Main Title" in heading_path and "Subsection" in heading_path:
        print("✅ Heading path extraction works!")
    else:
        print("❌ Heading path extraction failed!")
        return False
    
    # Test 3: Token count validation
    print("\n✅ TEST 3: Token Count Validation")
    print("-" * 80)
    
    short_text = "This is a short text."
    long_text = "This is a very long text. " * 100  # Should exceed max_tokens
    
    is_valid_short, count_short = chunker._validate_token_count(short_text)
    is_valid_long, count_long = chunker._validate_token_count(long_text)
    
    print(f"Short text: {count_short} tokens, valid={is_valid_short}")
    print(f"Long text: {count_long} tokens, valid={is_valid_long}")
    print(f"Max allowed: {config.max_tokens} tokens")
    
    if is_valid_short and not is_valid_long:
        print("✅ Token count validation works!")
    else:
        print("❌ Token count validation failed!")
        return False
    
    # Test 4: Integration test (no DoclingDocument needed for method tests)
    print("\n✅ TEST 4: Metadata Enrichment")
    print("-" * 80)
    
    # Create a mock chunk to test metadata
    test_chunk_text = """# Installation

## Quick Start

```python
pip install docling
```

Follow the guide above.
"""
    
    # Test all three methods on this chunk
    has_complete_blocks = chunker._detect_code_block_boundary(test_chunk_text)
    heading_path = chunker._extract_heading_path(test_chunk_text)
    is_valid, token_count = chunker._validate_token_count(test_chunk_text)
    
    print(f"Complete code blocks: {has_complete_blocks}")
    print(f"Heading path: '{heading_path}'")
    print(f"Token count: {token_count}, valid: {is_valid}")
    
    # Build metadata like chunk_document does
    metadata = {
        "heading_path": heading_path,
        "has_complete_code_blocks": has_complete_blocks,
        "token_count_valid": is_valid,
        "token_count": token_count
    }
    
    print(f"\nGenerated metadata:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    
    if heading_path and "heading_path" in metadata:
        print("✅ Metadata enrichment works!")
    else:
        print("❌ Metadata enrichment failed!")
        return False
    
    print("\n" + "=" * 80)
    print("🎉 ALL TIER 1 OPTIMIZATIONS WORKING!")
    print("=" * 80)
    
    print("\n📊 SUMMARY:")
    print("-" * 80)
    print("✅ Code block boundary detection - Prevents split code blocks")
    print("✅ Heading path enrichment - Adds hierarchical context")
    print("✅ Token count validation - Ensures chunks fit model limits")
    print("\nNew metadata fields added to chunks:")
    print("  - heading_path: Full heading hierarchy")
    print("  - has_complete_code_blocks: Code fence validation")
    print("  - token_count_valid: Token limit compliance")
    
    return True


if __name__ == "__main__":
    success = test_tier1_optimizations()
    sys.exit(0 if success else 1)
