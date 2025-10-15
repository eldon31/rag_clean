Development Environment Setup | qdrant/examples | DeepWiki

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

# Data Migration from Pinecone

Relevant source files

- [llama\_index\_recency/.gitignore](https://github.com/qdrant/examples/blob/b3c4b28f/llama_index_recency/.gitignore)
- [llama\_index\_recency/images/RankFocus.png](https://github.com/qdrant/examples/blob/b3c4b28f/llama_index_recency/images/RankFocus.png)
- [llama\_index\_recency/images/RerankFocus.png](https://github.com/qdrant/examples/blob/b3c4b28f/llama_index_recency/images/RerankFocus.png)
- [llama\_index\_recency/images/SetupFocus.png](https://github.com/qdrant/examples/blob/b3c4b28f/llama_index_recency/images/SetupFocus.png)
- [llama\_index\_recency/pyproject.toml](https://github.com/qdrant/examples/blob/b3c4b28f/llama_index_recency/pyproject.toml)

This page provides a step-by-step guide for migrating vector embeddings and associated metadata from Pinecone to Qdrant. The guide uses Vector-io, a specialized library designed to simplify data migration between vector databases using a standardized Vector Dataset Format (VDF).

Sources: [data-migration/from-pinecone-to-qdrant.ipynb8-16](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/from-pinecone-to-qdrant.ipynb#L8-L16)

## Overview of the Migration Process

Migrating from Pinecone to Qdrant involves three main steps:

1. **Export** - Using Vector-io to export data from Pinecone into the VDF format
2. **Transform** - Data is automatically standardized into the VDF format
3. **Import** - Importing the VDF-formatted data into Qdrant

This migration pathway ensures data consistency regardless of differences between the source and destination databases.

```
```

Sources: [data-migration/from-pinecone-to-qdrant.ipynb8-16](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/from-pinecone-to-qdrant.ipynb#L8-L16) [data-migration/from-pinecone-to-qdrant.ipynb278-335](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/from-pinecone-to-qdrant.ipynb#L278-L335)

## Prerequisites

Before starting the migration process, you need:

1. **API Keys and Access**:

   - Pinecone API key
   - Qdrant API key or host URL
   - OpenAI API key (if you used OpenAI embeddings)

2. **Vector-io Installation**:

   ```
   pip install vdf-io
   ```

3. **Environment Setup**: Create a `.env` file with your credentials based on the `.env-example` template:

| Environment Variable     | Description                      |
| ------------------------ | -------------------------------- |
| QDRANT\_COLLECTION\_NAME | Target collection name in Qdrant |
| QDRANT\_HOST             | Qdrant host URL                  |
| QDRANT\_API\_KEY         | Qdrant API key                   |
| OPENAI\_API\_KEY         | OpenAI API key                   |
| PINECONE\_API\_KEY       | Pinecone API key                 |
| PINECONE\_CLOUD          | Cloud provider (e.g., "aws")     |
| PINECONE\_REGION         | Region (e.g., "us-east-1")       |

Sources: [data-migration/.env-example1-11](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/.env-example#L1-L11) [data-migration/from-pinecone-to-qdrant.ipynb280-284](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/from-pinecone-to-qdrant.ipynb#L280-L284)

## The Demonstration Dataset

The example in the notebook uses a PubMed dataset from Hugging Face to illustrate the migration process. The dataset is embedded using OpenAI's text-embedding-3-small model (1536 dimensions).

### Loading and Preparing Sample Data

The notebook demonstrates:

1. Loading the PubMed dataset
2. Creating embeddings using OpenAI's embedding model
3. Storing the data in Pinecone

```
```

Sources: [data-migration/from-pinecone-to-qdrant.ipynb55-61](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/from-pinecone-to-qdrant.ipynb#L55-L61) [data-migration/from-pinecone-to-qdrant.ipynb163-270](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/from-pinecone-to-qdrant.ipynb#L163-L270)

## Step 1: Setting Up Pinecone

The notebook demonstrates creating a Pinecone index with appropriate dimensions and embedding model:

1. Initialize Pinecone client with API key
2. Create a serverless index with correct dimension (1536 for OpenAI's text-embedding-3-small model)
3. Configure the OpenAI embedding function
4. Load data and generate embeddings
5. Upsert the embedding vectors and metadata to Pinecone

The code in the notebook sets up a Pinecone index named "pubmed" with a dimension of 1536 and a cosine similarity metric.

Sources: [data-migration/from-pinecone-to-qdrant.ipynb182-270](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/from-pinecone-to-qdrant.ipynb#L182-L270)

## Step 2: Exporting Data from Pinecone

The data export step uses the Vector-io command-line interface:

```
export_vdf pinecone --serverless -c aws --region us-east-1 -i pubmed --namespace ""
```

This command:

- Specifies Pinecone as the source database
- Indicates it's a serverless instance
- Defines the cloud provider as AWS
- Sets the region to us-east-1
- Specifies the index name as "pubmed"
- Targets the default namespace

The export process:

1. Collects all points/vectors in the specified index
2. Fetches all vectors with their metadata
3. Exports them to a standardized Vector Dataset Format (VDF)
4. Stores the result in a directory with a timestamped name (e.g., `vdf_20240510_001325_88ae5/`)

The output directory contains:

- A metadata file (`VDF_META.json`) with information about the exported data
- Parquet files containing the actual vector data and metadata

Sources: [data-migration/from-pinecone-to-qdrant.ipynb290-332](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/from-pinecone-to-qdrant.ipynb#L290-L332)

## Step 3: Importing Data to Qdrant

After exporting, use the Vector-io import command to transfer the data to Qdrant:

```
import_vdf qdrant -u $QDRANT_HOST
```

When prompted, specify the directory containing the exported VDF data.

The import process:

1. Reads the VDF metadata to understand the data structure
2. Parses the vector data from the Parquet files
3. Converts metadata to the appropriate format for Qdrant
4. Creates a collection in Qdrant with matching parameters (if it doesn't exist)
5. Uploads vectors in batches to Qdrant

The import tool will report:

- Number of vectors processed
- Number of vectors successfully imported
- Time taken for the operation

Sources: [data-migration/from-pinecone-to-qdrant.ipynb342-360](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/from-pinecone-to-qdrant.ipynb#L342-L360)

## Data Flow and Transformation

During the migration process, Vector-io handles the following transformations:

```
```

The Vector Dataset Format (VDF) serves as a standardized intermediate representation, ensuring compatibility between different vector database systems. Key transformation points include:

1. **ID handling**: Ensuring consistent ID formats across systems
2. **Vector dimensionality**: Maintaining the same dimensions (1536 in this example)
3. **Metadata/payload conversion**: Converting between Pinecone's metadata and Qdrant's payload format
4. **Index configuration**: Transferring similarity metrics and other settings

Sources: [data-migration/from-pinecone-to-qdrant.ipynb8-16](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/from-pinecone-to-qdrant.ipynb#L8-L16) [data-migration/from-pinecone-to-qdrant.ipynb290-360](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/from-pinecone-to-qdrant.ipynb#L290-L360)

## Verification and Validation

After completing the migration, it's important to verify that:

1. **Vector count matches**: The number of vectors in Qdrant should match the number exported from Pinecone
2. **Metadata integrity**: Sample checks to ensure metadata was correctly transferred
3. **Search functionality**: Test similar queries in both systems to compare results

The imported collection should be visible in the Qdrant dashboard where you can verify vector counts and test search functionality.

Sources: [data-migration/from-pinecone-to-qdrant.ipynb362-366](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/from-pinecone-to-qdrant.ipynb#L362-L366)

## Best Practices and Considerations

When migrating vector data from Pinecone to Qdrant, consider the following best practices:

1. **Backup your data**: Always ensure you have a backup of your Pinecone data before migration
2. **Test with a subset**: For large collections, consider testing the migration with a small subset first
3. **Verify dimensions and metrics**: Ensure the dimension size and similarity metric match between systems
4. **Choose appropriate batch size**: For large datasets, adjust the batch size during import to optimize performance
5. **Plan for downtime**: Schedule migration during low-traffic periods
6. **Post-migration testing**: Thoroughly test your application with the new Qdrant backend

## Environment Variables

The configuration uses environment variables to manage credentials securely. The required variables include:

| Variable                 | Purpose                                        |
| ------------------------ | ---------------------------------------------- |
| QDRANT\_COLLECTION\_NAME | The name of the collection in Qdrant           |
| QDRANT\_HOST             | The URL endpoint for your Qdrant instance      |
| QDRANT\_API\_KEY         | API key for authenticating with Qdrant         |
| PINECONE\_API\_KEY       | API key for Pinecone access                    |
| PINECONE\_CLOUD          | Cloud provider for Pinecone (e.g., aws)        |
| PINECONE\_REGION         | Region for Pinecone (e.g., us-east-1)          |
| OPENAI\_API\_KEY         | API key for OpenAI (if using their embeddings) |

Sources: [data-migration/.env-example1-11](https://github.com/qdrant/examples/blob/b3c4b28f/data-migration/.env-example#L1-L11)

## Technical Details and Limitations

When migrating between Pinecone and Qdrant, be aware of these technical considerations:

1. **Similarity metrics**: Ensure you're using comparable similarity metrics (e.g., cosine, dot product, euclidean)
2. **Vector dimensions**: The vector dimensions must match between source and destination
3. **Custom metadata**: Complex metadata structures may require additional handling
4. **Scale considerations**: Very large datasets might require splitting the migration into multiple operations
5. **Network bandwidth**: For large datasets, ensure adequate network bandwidth between systems

## Conclusion

Vector-io provides a streamlined solution for migrating vector data from Pinecone to Qdrant. The standardized VDF format ensures data integrity during the migration process, making it convenient to switch between vector database providers while preserving your vector embeddings and associated metadata.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Data Migration from Pinecone](#data-migration-from-pinecone.md)
- [Overview of the Migration Process](#overview-of-the-migration-process.md)
- [Prerequisites](#prerequisites.md)
- [The Demonstration Dataset](#the-demonstration-dataset.md)
- [Loading and Preparing Sample Data](#loading-and-preparing-sample-data.md)
- [Step 1: Setting Up Pinecone](#step-1-setting-up-pinecone.md)
- [Step 2: Exporting Data from Pinecone](#step-2-exporting-data-from-pinecone.md)
- [Step 3: Importing Data to Qdrant](#step-3-importing-data-to-qdrant.md)
- [Data Flow and Transformation](#data-flow-and-transformation.md)
- [Verification and Validation](#verification-and-validation.md)
- [Best Practices and Considerations](#best-practices-and-considerations.md)
- [Environment Variables](#environment-variables.md)
- [Technical Details and Limitations](#technical-details-and-limitations.md)
- [Conclusion](#conclusion.md)
