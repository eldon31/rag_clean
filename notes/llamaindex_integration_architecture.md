# LlamaIndex Integration Architecture for Ultimate Chunker & Embedder

## Executive Summary

This document outlines the integration of LlamaIndex as a unified framework for our chunking and embedding pipeline, combining the strengths of:
- **Tree-sitter**: Code-aware parsing with syntax tree analysis
- **Semchunk**: Semantic text chunking with token-aware boundaries
- **LlamaIndex**: Production-ready RAG framework with Document/Node abstraction

## Integration Goals

1. **Unified Document Model**: Use LlamaIndex's Document/Node abstraction
2. **Flexible Node Parsing**: Integrate tree-sitter and semchunk as custom NodeParsers
3. **Production RAG Pipeline**: Enable QueryEngine, Retriever, and Index functionality
4. **Backward Compatibility**: Maintain existing chunker/embedder interfaces
5. **Enhanced Metadata**: Leverage LlamaIndex's metadata propagation

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   LlamaIndex Integration Layer                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Document   │  │     Node     │  │   Metadata   │          │
│  │  Abstraction │  │  Abstraction │  │  Enrichment  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│                      Custom NodeParsers                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  TreeSitterNodeParser (Code-Aware)                  │       │
│  │  - Language detection via file extension             │       │
│  │  - AST-based chunking for functions/classes          │       │
│  │  - Preserves code structure and context              │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  SemchunkNodeParser (Semantic Text)                  │       │
│  │  - Token-aware semantic boundaries                    │       │
│  │  - Overlap support for context                        │       │
│  │  - Efficient for large documents                      │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  HierarchicalNodeParser (Structured Docs)            │       │
│  │  - Markdown/heading-based hierarchy                   │       │
│  │  - Section-aware chunking                             │       │
│  │  - Metadata from document structure                   │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│                    Embedding & Indexing                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  VectorStoreIndex                                     │       │
│  │  - Qdrant integration via QdrantVectorStore          │       │
│  │  - Multi-vector support (dense + sparse)             │       │
│  │  - Companion model embeddings                         │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  Custom Embedding Models                              │       │
│  │  - JinaAI (jina-embeddings-v4, jina-code-1.5b)      │       │
│  │  - Nomic (CodeRankEmbed)                             │       │
│  │  - BAAI (bge-m3, bge-small)                          │       │
│  │  - Ensemble support                                   │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│                   Query & Retrieval Layer                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  VectorIndexRetriever                                 │       │
│  │  - Hybrid search (dense + sparse)                     │       │
│  │  - Cross-encoder reranking                            │       │
│  │  - Modal-aware retrieval                              │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  QueryEngine                                          │       │
│  │  - Natural language queries                           │       │
│  │  - Context synthesis                                  │       │
│  │  - Response generation                                │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. LlamaIndex Document Model

```python
from llama_index.core import Document
from llama_index.core.schema import TextNode

# Convert our chunks to LlamaIndex Documents
doc = Document(
    text=chunk_text,
    metadata={
        "source_file": filename,
        "chunk_index": idx,
        "content_type": "code" | "prose" | "table",
        "hierarchy_path": "section > subsection",
        # ... existing rich metadata
    },
    excluded_llm_metadata_keys=["embedding_model"],
    excluded_embed_metadata_keys=["full_text"],
)

# Or as TextNodes for finer control
node = TextNode(
    text=chunk_text,
    metadata={...},
    relationships={
        NodeRelationship.SOURCE: parent_node_id,
        NodeRelationship.NEXT: next_node_id,
    }
)
```

### 2. Custom TreeSitterNodeParser

```python
from llama_index.core.node_parser import NodeParser
from tree_sitter import Parser, Language

class TreeSitterNodeParser(NodeParser):
    """LlamaIndex NodeParser using tree-sitter for code chunking"""
    
    def __init__(
        self,
        language: str = "python",
        chunk_size: int = 1024,
        chunk_overlap: int = 100,
    ):
        self.language = language
        self.parser = Parser()
        self.parser.set_language(get_language(language))
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def _parse_nodes(
        self,
        documents: List[Document],
        show_progress: bool = False,
    ) -> List[TextNode]:
        """Parse documents into nodes using tree-sitter AST"""
        nodes = []
        for doc in documents:
            tree = self.parser.parse(doc.text.encode('utf-8'))
            # Extract function/class definitions as nodes
            for node in self._collect_code_blocks(tree.root_node):
                text_node = TextNode(
                    text=node.text,
                    metadata={
                        **doc.metadata,
                        "node_type": node.type,
                        "language": self.language,
                    },
                )
                nodes.append(text_node)
        return nodes
```

### 3. Custom SemchunkNodeParser

```python
import semchunk

class SemchunkNodeParser(NodeParser):
    """LlamaIndex NodeParser using semchunk for semantic chunking"""
    
    def __init__(
        self,
        chunk_size: int = 512,
        overlap_ratio: float = 0.1,
        tokenizer: str = "cl100k_base",
    ):
        import tiktoken
        self.tokenizer = tiktoken.get_encoding(tokenizer)
        self.chunk_size = chunk_size
        self.chunker = semchunk.chunkerify(
            lambda text: len(self.tokenizer.encode(text)),
            chunk_size
        )
    
    def _parse_nodes(
        self,
        documents: List[Document],
        show_progress: bool = False,
    ) -> List[TextNode]:
        """Parse documents using semantic chunking"""
        nodes = []
        for doc in documents:
            chunks, offsets = self.chunker(
                doc.text,
                offsets=True,
                overlap=self.overlap_ratio
            )
            for i, (chunk, (start, end)) in enumerate(zip(chunks, offsets)):
                node = TextNode(
                    text=chunk,
                    metadata={
                        **doc.metadata,
                        "chunk_index": i,
                        "start_char": start,
                        "end_char": end,
                    },
                )
                nodes.append(node)
        return nodes
```

### 4. Qdrant Vector Store Integration

```python
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from qdrant_client import QdrantClient

# Initialize Qdrant client
client = QdrantClient(host="localhost", port=6333)

# Create vector store with multi-vector support
vector_store = QdrantVectorStore(
    client=client,
    collection_name="qdrant_ecosystem_v5",
    enable_hybrid=True,  # Dense + sparse vectors
)

# Create storage context
storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

# Build index from nodes
index = VectorStoreIndex(
    nodes=parsed_nodes,
    storage_context=storage_context,
    embed_model=custom_embed_model,
)
```

### 5. Query Engine with Reranking

```python
from llama_index.core.postprocessor import SentenceTransformerRerank

# Create query engine with reranking
query_engine = index.as_query_engine(
    similarity_top_k=100,  # Initial retrieval
    node_postprocessors=[
        SentenceTransformerRerank(
            model="cross-encoder/ms-marco-MiniLM-L-6-v2",
            top_n=20,  # Final reranked results
        )
    ],
    response_mode="tree_summarize",
)

# Query with natural language
response = query_engine.query(
    "How do I optimize vector search in Qdrant?"
)
```

## Implementation Strategy

### Phase 1: Core Integration (Week 1)

1. **Create LlamaIndex-compatible wrappers**
   - `LlamaIndexChunkerV5`: Wraps existing chunker, outputs Documents/Nodes
   - `LlamaIndexEmbedderV5`: Integrates with VectorStoreIndex
   - Maintain backward compatibility with V3/V4 interfaces

2. **Implement Custom NodeParsers**
   - `TreeSitterNodeParser`: Code-aware chunking
   - `SemchunkNodeParser`: Semantic text chunking
   - `HierarchicalNodeParser`: Structured document chunking

3. **Test with existing pipeline**
   - Process sample documents through new parsers
   - Validate output format compatibility
   - Benchmark performance vs V3/V4

### Phase 2: Advanced Features (Week 2)

4. **Qdrant Vector Store Integration**
   - Custom `QdrantVectorStore` with multi-vector support
   - Sparse vector sidecar handling
   - Companion model embeddings

5. **Query Engine Enhancement**
   - Hybrid search (dense + sparse)
   - Cross-encoder reranking
   - Modal-aware retrieval (code vs prose)

6. **Agentic Workflow Support**
   - Tools for document processing
   - Memory integration
   - Workflow orchestration

### Phase 3: Production Deployment (Week 3)

7. **Kaggle Optimization**
   - T4 x2 GPU batch processing
   - Memory-efficient indexing
   - Checkpoint/resume support

8. **Local Qdrant Upload**
   - Export in LlamaIndex-compatible format
   - Bulk upload scripts
   - Collection management

9. **Documentation & Examples**
   - Migration guide from V3/V4
   - Usage examples
   - Performance benchmarks

## Benefits of LlamaIndex Integration

### 1. **Production-Ready RAG Pipeline**
- Complete query engine out of the box
- Response synthesis and generation
- Built-in context management

### 2. **Framework Ecosystem**
- 160+ data connectors (LlamaHub)
- Multiple LLM providers
- Observability and debugging tools

### 3. **Flexible Architecture**
- Mix and match NodeParsers
- Custom embedding models
- Plugin system for extensions

### 4. **Advanced Features**
- Agentic workflows and tools
- Memory and conversation history
- Multi-modal support (text, images, audio)

### 5. **Community & Support**
- Active development (2000+ contributors)
- Extensive documentation
- Production deployments at scale

## Backward Compatibility

### V3/V4 Interface Preservation

```python
# Old interface (V3/V4) still works
chunker = EnhancedUltimateChunkerV3(
    embedding_model="jinaai/jina-code-embeddings-1.5b"
)
chunks = chunker.process_file_smart("file.py")

# New interface (V5) with LlamaIndex
from processor.llamaindex_chunker_v5 import LlamaIndexChunkerV5

chunker = LlamaIndexChunkerV5(
    node_parser="tree-sitter",  # or "semchunk", "hierarchical"
    embedding_model="jinaai/jina-code-embeddings-1.5b"
)
documents = chunker.process_file_to_documents("file.py")
nodes = chunker.process_file_to_nodes("file.py")

# Or use directly with LlamaIndex
from llama_index.core import VectorStoreIndex
index = VectorStoreIndex.from_documents(documents)
```

## File Structure

```
processor/
├── enhanced_ultimate_chunker_v3.py       # Existing chunker
├── kaggle_ultimate_embedder_v4.py        # Existing embedder
├── llamaindex_chunker_v5.py              # NEW: LlamaIndex integration
├── llamaindex_embedder_v5.py             # NEW: LlamaIndex indexing
└── llamaindex_parsers/                   # NEW: Custom parsers
    ├── __init__.py
    ├── tree_sitter_parser.py
    ├── semchunk_parser.py
    └── hierarchical_parser.py

scripts/
├── chunk_docs.py                         # Existing script
├── embed_collections_v4.py               # Existing script
└── llamaindex_pipeline_v5.py             # NEW: Full pipeline

examples/
└── llamaindex_usage.py                   # NEW: Usage examples
```

## Next Steps

1. ✅ Complete architecture design
2. 🔄 Implement `LlamaIndexChunkerV5` with custom NodeParsers
3. ⏳ Implement `LlamaIndexEmbedderV5` with VectorStoreIndex
4. ⏳ Create integration examples
5. ⏳ Performance benchmarking
6. ⏳ Documentation and migration guide

## Conclusion

This integration combines the best of all three frameworks:
- **Tree-sitter**: Code-aware parsing
- **Semchunk**: Semantic chunking
- **LlamaIndex**: Production RAG framework

The result is a powerful, flexible system that maintains backward compatibility while enabling advanced RAG capabilities for production deployment.