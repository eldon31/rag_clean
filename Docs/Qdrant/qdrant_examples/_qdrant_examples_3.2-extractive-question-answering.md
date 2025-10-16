Extractive Question Answering | qdrant/examples | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/examples](https://github.com/qdrant/examples "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 26 June 2025 ([b3c4b2](https://github.com/qdrant/examples/commits/b3c4b28f))

- [Overview](qdrant/examples/1-overview.md)
- [Getting Started with Qdrant](qdrant/examples/2-getting-started-with-qdrant.md)
- [Text Data Applications](qdrant/examples/3-text-data-applications.md)
- [Code Search with Dual Embeddings](qdrant/examples/3.1-code-search-with-dual-embeddings.md)
- [Extractive Question Answering](qdrant/examples/3.2-extractive-question-answering.md)
- [Movie Recommendations with Sparse Vectors](qdrant/examples/3.3-movie-recommendations-with-sparse-vectors.md)
- [Image Data Applications](qdrant/examples/4-image-data-applications.md)
- [E-commerce Reverse Image Search](qdrant/examples/4.1-e-commerce-reverse-image-search.md)
- [Medical Image Search with Vision Transformers](qdrant/examples/4.2-medical-image-search-with-vision-transformers.md)
- [Audio Data Applications](qdrant/examples/5-audio-data-applications.md)
- [Music Recommendation Engine](qdrant/examples/5.1-music-recommendation-engine.md)
- [Advanced RAG Systems](qdrant/examples/6-advanced-rag-systems.md)
- [Multivector RAG with DSPy](qdrant/examples/6.1-multivector-rag-with-dspy.md)
- [Graph-Enhanced RAG with Neo4j](qdrant/examples/6.2-graph-enhanced-rag-with-neo4j.md)
- [PDF Retrieval at Scale](qdrant/examples/6.3-pdf-retrieval-at-scale.md)
- [Agentic Systems with CrewAI](qdrant/examples/7-agentic-systems-with-crewai.md)
- [Meeting Analysis with Agentic RAG](qdrant/examples/7.1-meeting-analysis-with-agentic-rag.md)
- [Additional Use Cases](qdrant/examples/8-additional-use-cases.md)
- [Self-Query Systems with LangChain](qdrant/examples/8.1-self-query-systems-with-langchain.md)
- [Development Environment Setup](qdrant/examples/8.2-development-environment-setup.md)

Menu

# Extractive Question Answering

Relevant source files

- [extractive\_qa/extractive-question-answering.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb)
- [qdrant\_101\_text\_data/qdrant\_and\_text\_data.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/qdrant_and_text_data.ipynb)

## Overview

The Extractive Question Answering system implements a retriever-reader architecture that extracts precise answers from movie plot data. The system uses the DuoRC dataset containing movie plots from Wikipedia and IMDb to demonstrate semantic search and answer extraction capabilities.

**Key Components:**

- **Retriever**: `TextEmbedding` model (`BAAI/bge-small-en-v1.5`) for semantic search
- **Vector Database**: Qdrant collection named `extractive-question-answering`
- **Reader**: `bert-large-uncased-whole-word-masking-finetuned-squad` for answer extraction

The system extracts answers directly from source text rather than generating new content, ensuring factual accuracy and traceability.

Sources: [extractive\_qa/extractive-question-answering.ipynb17-27](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L17-L27) [extractive\_qa/extractive-question-answering.ipynb622-623](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L622-L623) [extractive\_qa/extractive-question-answering.ipynb733-737](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L733-L737)

## Architecture

**System Architecture with Code Entities**

```
```

**Component Mapping:**

| Component       | Code Entity                                                                                     | Purpose                                  |
| --------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------- |
| Retriever       | `TextEmbedding("BAAI/bge-small-en-v1.5")`                                                       | Converts text to 384-dimensional vectors |
| Vector Database | `QdrantClient(":memory:")`                                                                      | Stores and searches embeddings           |
| Collection      | `"extractive-question-answering"`                                                               | Named collection with cosine distance    |
| Reader          | `pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")` | Extracts answer spans                    |

Sources: [extractive\_qa/extractive-question-answering.ipynb91-96](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L91-L96) [extractive\_qa/extractive-question-answering.ipynb473](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L473-L473) [extractive\_qa/extractive-question-answering.ipynb522](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L522-L522) [extractive\_qa/extractive-question-answering.ipynb735-737](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L735-L737)

## Implementation Details

### Data Preparation

**Dataset Processing Pipeline**

```
```

The implementation processes 9,919 unique movie plots from the DuoRC dataset:

- Dataset loading: `load_dataset("duorc", "ParaphraseRC", split="train")`
- Deduplication: `df.drop_duplicates(subset="plot")`
- Batch processing: 64 documents per batch for efficient embedding generation
- Storage format: `models.Batch(ids=ids, vectors=emb, payloads=meta)`

Sources: [extractive\_qa/extractive-question-answering.ipynb442-449](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L442-L449) [extractive\_qa/extractive-question-answering.ipynb688-702](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L688-L702)

### Retriever Component

**TextEmbedding Configuration**

| Parameter  | Value                      | Purpose                       |
| ---------- | -------------------------- | ----------------------------- |
| Model      | `"BAAI/bge-small-en-v1.5"` | Optimized for semantic search |
| Dimensions | 384                        | Vector size for embeddings    |
| Library    | `fastembed.TextEmbedding`  | Fast embedding generation     |

**Core Functions:**

- **Indexing**: `retriever.embed(batch["plot"].tolist())` - converts plot text to vectors
- **Querying**: `retriever.query_embed(question)` - converts questions to search vectors

The retriever ensures semantic similarity between questions and relevant contexts by mapping both to the same 384-dimensional vector space.

Sources: [extractive\_qa/extractive-question-answering.ipynb622-623](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L622-L623) [extractive\_qa/extractive-question-answering.ipynb693](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L693-L693) [extractive\_qa/extractive-question-answering.ipynb786](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L786-L786)

### Qdrant Vector Database

**Collection Configuration**

```
```

**Key Implementation Details:**

- Client: `QdrantClient(":memory:")` for demonstration
- Collection: `"extractive-question-answering"`
- Vector configuration: `models.VectorParams(size=384, distance=models.Distance.COSINE)`
- Search method: `client.query_points(collection_name, query, limit)`

Sources: [extractive\_qa/extractive-question-answering.ipynb473](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L473-L473) [extractive\_qa/extractive-question-answering.ipynb529-535](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L529-L535) [extractive\_qa/extractive-question-answering.ipynb788-792](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L788-L792)

### Reader Model

The reader model extracts the precise answer from the retrieved context passages:

- Model: `bert-large-uncased-whole-word-masking-finetuned-squad`
- Type: Transformer-based question answering model
- Training: Fine-tuned on the SQuAD dataset

The reader processes each retrieved context separately and returns:

- The extracted answer text
- A confidence score
- The title of the source document

Sources: [extractive\_qa/extractive-question-answering.ipynb718-721](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L718-L721) [extractive\_qa/extractive-question-answering.ipynb735-737](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L735-L737)

## Workflow

**Function Call Sequence**

```
```

**Core Function Implementations:**

| Function              | Input                               | Output                     | Line Reference                                                                                                                                                            |
| --------------------- | ----------------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get_relevant_plot()` | `question: str, top_k: int`         | `List[str]` context pairs  | [extractive\_qa/extractive-question-answering.ipynb774-800](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L774-L800) |
| `extract_answer()`    | `question: str, context: List[str]` | Ranked answers with scores | [extractive\_qa/extractive-question-answering.ipynb835-863](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L835-L863) |

Sources: [extractive\_qa/extractive-question-answering.ipynb774-800](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L774-L800) [extractive\_qa/extractive-question-answering.ipynb835-863](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L835-L863) [extractive\_qa/extractive-question-answering.ipynb786](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L786-L786) [extractive\_qa/extractive-question-answering.ipynb846](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L846-L846)

## Data Flow Details

**Code Entity Data Transformation**

```
```

**Variable Flow:**

- Input: `question: str`, `top_k: int`
- Embedding: `encoded_query = next(retriever.query_embed(question)).tolist()`
- Search: `result = client.query_points(...).points`
- Context: `context = [[x.payload["title"], x.payload["plot"]] for x in result]`
- Answers: `answer = reader(question=question, context=c[1])`

Sources: [extractive\_qa/extractive-question-answering.ipynb786](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L786-L786) [extractive\_qa/extractive-question-answering.ipynb788-796](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L788-L796) [extractive\_qa/extractive-question-answering.ipynb844-853](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L844-L853)

## Implementation Code Structure

**Function Signatures and Dependencies**

| Function              | Signature                                  | Dependencies          | Purpose                                   |
| --------------------- | ------------------------------------------ | --------------------- | ----------------------------------------- |
| `get_relevant_plot()` | `(question: str, top_k: int) -> List[str]` | `retriever`, `client` | Vector search for relevant contexts       |
| `extract_answer()`    | `(question: str, context: List[str])`      | `reader` pipeline     | Answer extraction with confidence scoring |

**Batch Processing Implementation**

```
```

**Key Variables:**

- `batch_size = 64` for memory-efficient processing
- `collection_name = "extractive-question-answering"`
- `retriever = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")`
- `reader = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")`

Sources: [extractive\_qa/extractive-question-answering.ipynb688-702](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L688-L702) [extractive\_qa/extractive-question-answering.ipynb774-800](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L774-L800) [extractive\_qa/extractive-question-answering.ipynb835-863](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L835-L863)

## Example Usage

The system can answer various types of questions about movie plots. Here are some examples from the implementation:

### Example 1: College Name in "3 Idiots"

```
Question: "In the movie 3 Idiots, what is the name of the college where the main characters Rancho, Farhan, and Raju study"
Answer: "Imperial College of Engineering" (Score: 0.90)
Title: "Three Idiots"
```

### Example 2: Escape Tool in "The Shawshank Redemption"

```
Question: "In the movie The Shawshank Redemption, what was the item that Andy Dufresne used to escape from Shawshank State Penitentiary?"
Answer: "rock hammer" (Score: 0.87)
Title: "The Shawshank Redemption"
```

### Example 3: Multiple Sources

```
Question: "who killed the spy"
Answers: 
1. "Soviet agents" (Score: 0.79)
   Title: "Tinker, Tailor, Soldier, Spy"
2. "Gila" (Score: 0.12)
   Title: "Our Man Flint"
3. "Gabriel's assassins" (Score: 0.06)
   Title: "Live Free or Die Hard"
```

Sources: [extractive\_qa/extractive-question-answering.ipynb905-906](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L905-L906) [extractive\_qa/extractive-question-answering.ipynb1006-1008](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L1006-L1008) [extractive\_qa/extractive-question-answering.ipynb1048-1050](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L1048-L1050)

## Limitations and Considerations

1. **Answer Confidence**: The system might return low-confidence answers when the question is difficult or the answer isn't clearly stated in the context
2. **Context Relevance**: The quality of answers depends on retrieving relevant contexts
3. **Exact Answer Extraction**: The system is designed to extract spans of text, not generate new content

For implementing a more advanced question answering system that can generate responses, consider exploring the RAG systems documented in [Advanced RAG Systems](qdrant/examples/6-advanced-rag-systems.md).

Sources: [extractive\_qa/extractive-question-answering.ipynb915-916](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L915-L916) [extractive\_qa/extractive-question-answering.ipynb949-954](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L949-L954)

## Technical Requirements

The implementation requires the following libraries:

- datasets (2.12.0)
- qdrant-client (1.10.1)
- fastembed (0.3.3)
- sentence-transformers (2.2.2)
- torch (2.0.1)
- transformers (for the reader model)

Sources: [extractive\_qa/extractive-question-answering.ipynb67](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L67-L67) [extractive\_qa/extractive-question-answering.ipynb90-96](https://github.com/qdrant/examples/blob/b3c4b28f/extractive_qa/extractive-question-answering.ipynb#L90-L96)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Extractive Question Answering](#extractive-question-answering.md)
- [Overview](#overview.md)
- [Architecture](#architecture.md)
- [Implementation Details](#implementation-details.md)
- [Data Preparation](#data-preparation.md)
- [Retriever Component](#retriever-component.md)
- [Qdrant Vector Database](#qdrant-vector-database.md)
- [Reader Model](#reader-model.md)
- [Workflow](#workflow.md)
- [Data Flow Details](#data-flow-details.md)
- [Implementation Code Structure](#implementation-code-structure.md)
- [Example Usage](#example-usage.md)
- [Example 1: College Name in "3 Idiots"](#example-1-college-name-in-3-idiots.md)
- [Example 2: Escape Tool in "The Shawshank Redemption"](#example-2-escape-tool-in-the-shawshank-redemption.md)
- [Example 3: Multiple Sources](#example-3-multiple-sources.md)
- [Limitations and Considerations](#limitations-and-considerations.md)
- [Technical Requirements](#technical-requirements.md)
