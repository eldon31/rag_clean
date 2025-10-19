#!/usr/bin/env python3
"""
Auto-generated Qdrant upload script for Ultimate Kaggle Embedder V4
Updated for MCP server compatibility

Generated on: 2025-10-16T19:22:11.007381
Updated on: 2025-10-19 (MCP naming + recommendations)

USAGE:
1. Download all exported files to your local machine
2. Make sure Qdrant is running locally (docker-compose up -d)
3. Install requirements: pip install qdrant-client numpy
4. Run this script: python Sentence_Transformers_v4_upload_script.py
"""

import json
import numpy as np
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from pathlib import Path
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def upload_to_qdrant(recreate_collection: bool = False):
    """Upload embeddings to local Qdrant instance"""
    
    # Configuration with environment variable support
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
    
    # MCP-compatible collection name
    COLLECTION_NAME = "sentence_transformers"
    
    # File paths (adjust if needed)
    script_dir = Path(__file__).parent
    FILES = {
        "embeddings": str(script_dir / "Sentence_Transformers_v4_embeddings.npy"), 
        "metadata": str(script_dir / "Sentence_Transformers_v4_metadata.json"),
        "texts": str(script_dir / "Sentence_Transformers_v4_texts.json"),
        "stats": str(script_dir / "Sentence_Transformers_v4_stats.json")
    }
    
    try:
        # Connect to Qdrant
        logger.info(f"🔌 Connecting to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}...")
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        logger.info(f"✅ Connected to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
        
        # Load data
        logger.info("📂 Loading exported data...")
        
        # Validate files exist
        for file_type, file_path in FILES.items():
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Missing {file_type} file: {file_path}")
        
        embeddings = np.load(FILES["embeddings"])
        
        with open(FILES["metadata"], 'r', encoding='utf-8') as f:
            metadata_list = json.load(f)
            
        with open(FILES["texts"], 'r', encoding='utf-8') as f:
            texts_list = json.load(f)
        
        # Data validation
        assert len(embeddings) == len(metadata_list) == len(texts_list), \
            f"Data mismatch! embeddings: {len(embeddings)}, metadata: {len(metadata_list)}, texts: {len(texts_list)}"
        
        logger.info(f"📊 Loaded {len(embeddings)} embeddings ({embeddings.shape[1]}D)")
        logger.info(f"✅ Data validation passed")
        
        # Handle collection creation/recreation
        try:
            existing_collection = client.get_collection(COLLECTION_NAME)
            if recreate_collection:
                logger.info(f"🗑️  Deleting existing collection: {COLLECTION_NAME}")
                client.delete_collection(COLLECTION_NAME)
                logger.info(f"✅ Deleted old collection")
            else:
                logger.info(f"📋 Collection '{COLLECTION_NAME}' already exists (will upsert)")
        except Exception:
            logger.info(f"📋 Collection '{COLLECTION_NAME}' does not exist (will create)")
        
        # Create collection if needed
        try:
            client.get_collection(COLLECTION_NAME)
        except:
            logger.info(f"🔧 Creating collection: {COLLECTION_NAME}")
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=embeddings.shape[1],
                    distance=Distance.COSINE
                ),
                # Optimized for large collections
                hnsw_config={
                    "m": 48,
                    "ef_construct": 512,
                    "full_scan_threshold": 50000
                },
                # Enable quantization for speed
                quantization_config={
                    "scalar": {
                        "type": "int8",
                        "quantile": 0.99,
                        "always_ram": True
                    }
                }
            )
            logger.info(f"✅ Collection created")
        
        # Prepare points
        logger.info("🔄 Preparing points for upload...")
        points = []
        
        for i, (embedding, metadata, text) in enumerate(zip(embeddings, metadata_list, texts_list)):
            point = PointStruct(
                id=i,
                vector=embedding.tolist(),
                payload={
                    **metadata,
                    "text": text,  # Full text
                    "text_preview": text[:500],
                    "full_text_length": len(text),
                    "local_upload_timestamp": datetime.now().isoformat(),
                    "collection_source": "Sentence_Transformers_v4",
                    "embedding_model": "nomic-ai/CodeRankEmbed"
                }
            )
            points.append(point)
        
        logger.info(f"✅ Prepared {len(points)} points")
        
        # Batch upload
        batch_size = 1000
        total_batches = (len(points) + batch_size - 1) // batch_size
        
        logger.info(f"📤 Uploading {len(points)} points in {total_batches} batches...")
        
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=batch,
                wait=True
            )
            
            logger.info(f"✅ Uploaded batch {batch_num}/{total_batches} ({len(batch)} points)")
        
        # Verify upload
        collection_info = client.get_collection(COLLECTION_NAME)
        logger.info(f"🎯 Upload complete! Collection has {collection_info.points_count} points")
        
        # Test search
        logger.info("🔍 Testing search...")
        test_results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=embeddings[0].tolist(),
            limit=3
        )
        
        logger.info(f"✅ Search test successful! Found {len(test_results)} results")
        for idx, result in enumerate(test_results, 1):
            logger.info(f"   {idx}. Score: {result.score:.3f} - {result.payload.get('text_preview', '')[:100]}...")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🚀 SUCCESS! Your embeddings are ready!")
        logger.info(f"📋 Collection name: {COLLECTION_NAME}")
        logger.info(f"📊 Total vectors: {collection_info.points_count}")
        logger.info(f"🔗 Qdrant URL: http://{QDRANT_HOST}:{QDRANT_PORT}")
        logger.info(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Upload failed: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("SENTENCE TRANSFORMERS COLLECTION UPLOAD")
    logger.info("=" * 60)
    
    # Set recreate_collection=True to delete and recreate collection
    upload_to_qdrant(recreate_collection=False)
