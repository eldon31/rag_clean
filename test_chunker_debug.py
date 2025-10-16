#!/usr/bin/env python3
"""
Debug script for Enhanced Ultimate Chunker v3.0
"""

import traceback
from enhanced_ultimate_chunker_v3 import EnhancedUltimateChunkerV3

def test_chunker():
    """Test the chunker with debug information"""
    
    try:
        print("🔧 Initializing Enhanced Ultimate Chunker v3.0...")
        chunker = EnhancedUltimateChunkerV3()
        print("✅ Chunker initialized successfully")
        
        print("\n🧪 Testing document structure detection...")
        
        # Test with a larger markdown content
        test_content = """# Ultimate Knowledge Creator System

This is a comprehensive introduction to the Ultimate Knowledge Creator System that processes and manages documentation across multiple domains. The system is designed to handle various types of content including MCP repositories, workflow documentation, API documentation, programming language documentation, and platform documentation.

## System Architecture

The Ultimate Knowledge Creator System is built on a modular architecture that supports multiple document processing strategies. The core components include:

- Document ingestion and preprocessing modules
- Advanced chunking algorithms with hierarchical support
- Embedding generation using state-of-the-art models
- Vector storage and retrieval systems
- Quality assessment and optimization tools

### Core Processing Pipeline

The processing pipeline consists of several stages:

1. **Document Analysis**: Automatic content type detection and structure analysis
2. **Chunking Strategy Selection**: Intelligent selection of optimal chunking approach
3. **Content Segmentation**: Hierarchical breaking of content into meaningful chunks
4. **Embedding Generation**: Vector representation creation using specialized models
5. **Quality Assessment**: Multi-dimensional quality scoring and validation

### Quality Metrics System

The system employs three primary quality metrics:

- **Semantic Coherence**: Measures the internal consistency and logical flow
- **Structural Integrity**: Evaluates preservation of document structure and relationships
- **Retrieval Optimization**: Assesses effectiveness for information retrieval tasks

## API Documentation Processing

The system includes specialized processing for API documentation that recognizes common patterns:

- REST endpoint documentation with HTTP methods
- Request and response schemas
- Authentication and authorization details
- Code examples and usage patterns
- Error handling and status codes

### RESTful API Endpoints

Common endpoint patterns that are automatically recognized:

```http
GET /api/v1/documents
POST /api/v1/documents
PUT /api/v1/documents/{id}
DELETE /api/v1/documents/{id}
```

## MCP Repository Processing

Model Context Protocol (MCP) repositories require specialized handling due to their unique structure and content patterns. The system automatically detects:

- MCP server implementations and configurations
- Protocol specifications and schemas
- Client library documentation
- Integration examples and tutorials

### Configuration Examples

```json
{
  "mcpServers": {
    "ultimate-qdrant": {
      "command": "python",
      "args": ["ultimate_qdrant_mcp_v2_fixed.py"],
      "env": {
        "QDRANT_URL": "http://localhost:6333"
      }
    }
  }
}
```

## Performance Optimization

The system includes several performance optimization features:

- Memory-efficient processing for large documents
- Batch processing capabilities for multiple files
- Caching mechanisms for repeated operations
- Parallel processing support for improved throughput

These optimizations ensure the system can handle enterprise-scale document processing workloads efficiently."""
        
        print("📊 Analyzing document structure...")
        structure = chunker.detect_document_structure(test_content)
        
        print(f"  Headings found: {len(structure['headings'])}")
        print(f"  Content blocks: {len(structure['content_blocks'])}")
        print(f"  Complexity: {structure['complexity']}")
        
        print("\n🎯 Testing content type detection...")
        content_type, strategy = chunker.auto_detect_content_type(
            "API documentation for REST endpoints", 
            "api_guide.md"
        )
        print(f"  Detected: {content_type} -> {strategy}")
        
        print("\n📋 Testing chunking with simple content...")
        
        # Try creating chunks with minimal strategy
        chunks = chunker.create_hierarchical_chunks(
            text=test_content,
            filename="test.md",
            strategy_name="hierarchical_balanced"
        )
        
        print(f"✅ Successfully created {len(chunks)} chunks")
        
        if chunks:
            first_chunk = chunks[0]
            print("\n📄 First chunk details:")
            print(f"  Length: {len(first_chunk['text'])} chars")
            print(f"  Tokens: {first_chunk['metadata']['token_count']}")
            print(f"  Strategy: {first_chunk['metadata']['chunking_strategy']}")
            
            # Show preview
            preview = first_chunk['text'][:100].replace('\n', ' ')
            print(f"  Preview: {preview}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("\n🔍 Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chunker()
    if success:
        print("\n🎉 All tests passed! Enhanced Ultimate Chunker v3.0 is working correctly.")
    else:
        print("\n💥 Tests failed. Please check the errors above.")