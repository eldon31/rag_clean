# Vector Search - Quick Reference Guide

## How to Query the Docling Collection

### Method 1: Using Python (Recommended)

```python
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# 1. Connect to Qdrant
client = QdrantClient(url="http://localhost:6333")

# 2. Load embedding model (same one used for embedding)
model = SentenceTransformer("nomic-ai/CodeRankEmbed", trust_remote_code=True)

# 3. Your search query
query = "How do I convert PDF to markdown with Docling?"

# 4. Generate query embedding
query_vector = model.encode(query).tolist()

# 5. Search the collection
results = client.search(
    collection_name="docling",
    query_vector=query_vector,
    limit=5,  # Top 5 results
    with_payload=True  # Include text and metadata
)

# 6. Display results
for idx, hit in enumerate(results, 1):
    print(f"\nResult #{idx} (Score: {hit.score:.4f})")
    print(f"Source: {hit.payload['source']}")
    print(f"Text: {hit.payload['text'][:200]}...")
```

### Method 2: Using curl (HTTP API)

```bash
# First, generate embedding for your query using the model
# Then search with:

curl -X POST 'http://localhost:6333/collections/docling/points/search' \
  -H 'Content-Type: application/json' \
  -d '{
    "vector": [0.123, 0.456, ...],  # Your query embedding (3584 dims)
    "limit": 5,
    "with_payload": true
  }'
```

### Method 3: Using Qdrant Dashboard

1. Open: http://localhost:6333/dashboard#/collections/docling
2. Click "Search" tab
3. Enter vector manually or use semantic search (if enabled)

## Integration Examples

### RAG Pipeline (Retrieval-Augmented Generation)

```python
def rag_query(user_question: str, llm_client):
    # 1. Vector search
    client = QdrantClient(url="http://localhost:6333")
    model = SentenceTransformer("nomic-ai/CodeRankEmbed", trust_remote_code=True)
    
    query_vector = model.encode(user_question).tolist()
    results = client.search(
        collection_name="docling",
        query_vector=query_vector,
        limit=3
    )
    
    # 2. Build context from results
    context = "\n\n".join([hit.payload['text'] for hit in results])
    
    # 3. Query LLM with context
    prompt = f"""Based on the following documentation:

{context}

Answer this question: {user_question}
"""
    
    response = llm_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
```

### Similarity Search with Filters

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

# Search only in specific source files
results = client.search(
    collection_name="docling",
    query_vector=query_vector,
    limit=5,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="source",
                match=MatchValue(value="_docling-project_docling_1-overview.md")
            )
        ]
    )
)
```

### Batch Search (Multiple Queries)

```python
queries = [
    "How to install Docling?",
    "PDF processing features",
    "OCR capabilities"
]

# Generate embeddings for all queries
query_vectors = model.encode(queries).tolist()

# Search all at once
for query, vector in zip(queries, query_vectors):
    results = client.search(
        collection_name="docling",
        query_vector=vector,
        limit=3
    )
    print(f"\nQuery: {query}")
    for hit in results:
        print(f"  - {hit.payload['heading']}")
```

## Available Metadata Fields

Each result includes:
- `text`: The actual chunk content
- `source`: Original markdown filename
- `heading`: Section heading
- `heading_level`: H1, H2, H3, etc.
- `chunk_index`: Position in source file
- `char_count`: Character length
- `estimated_tokens`: Approximate token count
- `collection`: Always "docling"
- `indexed_at`: Timestamp of upload

## Performance Tips

1. **Cache the model**: Load `SentenceTransformer` once, reuse for multiple queries
2. **Batch queries**: Use `model.encode(list_of_queries)` for multiple searches
3. **Adjust limit**: Start with `limit=5`, increase if needed
4. **Use filters**: Narrow search with metadata filters for better results
5. **Score threshold**: Filter results with `score > 0.7` for higher quality

## Scripts in This Repo

- `scripts/search_docling.py` - Full featured search with examples
- `scripts/search_qdrant_example.py` - Generic search template
- `mcp_server/qdrant_fastmcp_server.py` - MCP server for AI assistants

## Next Steps

1. Test search: `python scripts/search_docling.py`
2. Integrate into your app
3. Build RAG pipeline with LLM
4. Deploy as API endpoint
