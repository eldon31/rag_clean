"""
Migrate to CodeRankEmbed (768-dim) by uploading new embeddings.

This script:
1. Uploads 768-dim embeddings from output/embed_results/
2. Creates new collections with optimized settings
3. Validates upload success
4. Reports migration status

USAGE:
    # Upload all collections
    python scripts/migrate_to_coderank.py --all
    
    # Upload specific collection
    python scripts/migrate_to_coderank.py --collection qdrant_ecosystem
    
    # Dry run (validate files without uploading)
    python scripts/migrate_to_coderank.py --all --dry-run
    
    # Force overwrite existing collections
    python scripts/migrate_to_coderank.py --all --force
"""

import os
import json
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    OptimizersConfigDiff, HnswConfigDiff,
    QuantizationConfig, ScalarQuantization,
    ScalarType, BinaryQuantization
)
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

EMBED_RESULTS_DIR = Path("output/embed_results")

# Collection mapping: collection_name -> embedding_file
COLLECTION_MAPPING = {
    "qdrant_ecosystem": "qdrant_ecosystem_embeddings_768.jsonl",
    "docling": "docling_embeddings_768.jsonl",
    # Add more as files become available:
    # "agent_kit": "agent_kit_embeddings_768.jsonl",
    # "inngest_overall": "inngest_overall_embeddings_768.jsonl",
}

# CodeRankEmbed configuration
VECTOR_DIMENSION = 768
DISTANCE_METRIC = Distance.COSINE
BATCH_SIZE = 100


def get_collection_config(collection_name: str) -> Dict[str, Any]:
    """Get optimized collection configuration for 768-dim vectors."""
    return {
        "vectors_config": VectorParams(
            size=VECTOR_DIMENSION,
            distance=DISTANCE_METRIC,
            on_disk=False  # Keep in RAM for speed
        ),
        "optimizers_config": OptimizersConfigDiff(
            default_segment_number=2,
            indexing_threshold=10000,
            memmap_threshold=50000
        ),
        "hnsw_config": HnswConfigDiff(
            m=16,
            ef_construct=100,
            full_scan_threshold=10000
        ),
        # Quantization will be enabled after upload
    }


def enable_quantization(client: QdrantClient, collection_name: str):
    """Enable scalar + binary quantization for 768-dim vectors."""
    try:
        # Binary quantization (40x speedup for 768-dim)
        client.update_collection(
            collection_name=collection_name,
            quantization_config=BinaryQuantization(
                binary=BinaryQuantization(
                    always_ram=True
                )
            )
        )
        logger.info(f"  ✅ Binary quantization enabled for {collection_name}")
    except Exception as e:
        logger.warning(f"  ⚠️  Binary quantization failed: {e}")
        
        # Fallback to scalar quantization
        try:
            client.update_collection(
                collection_name=collection_name,
                quantization_config=ScalarQuantization(
                    scalar=ScalarQuantization(
                        type=ScalarType.INT8,
                        quantile=0.99,
                        always_ram=True
                    )
                )
            )
            logger.info(f"  ✅ Scalar quantization enabled for {collection_name}")
        except Exception as e2:
            logger.error(f"  ❌ Quantization failed: {e2}")


def load_embeddings(file_path: Path) -> List[Dict[str, Any]]:
    """Load embeddings from JSONL file."""
    embeddings = []
    
    logger.info(f"📂 Loading embeddings from: {file_path.name}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                record = json.loads(line.strip())
                
                # Validate required fields
                if 'id' not in record:
                    logger.warning(f"  Line {line_num}: Missing 'id' field, skipping")
                    continue
                
                if 'embedding' not in record:
                    logger.warning(f"  Line {line_num}: Missing 'embedding' field, skipping")
                    continue
                
                # Validate dimension
                embedding = record['embedding']
                if len(embedding) != VECTOR_DIMENSION:
                    logger.error(
                        f"  Line {line_num}: Wrong dimension {len(embedding)}, "
                        f"expected {VECTOR_DIMENSION}, skipping"
                    )
                    continue
                
                embeddings.append(record)
                
            except json.JSONDecodeError as e:
                logger.warning(f"  Line {line_num}: Invalid JSON, skipping: {e}")
                continue
    
    logger.info(f"  ✅ Loaded {len(embeddings)} valid embeddings")
    return embeddings


def upload_embeddings(
    client: QdrantClient,
    collection_name: str,
    embeddings: List[Dict[str, Any]],
    batch_size: int = BATCH_SIZE,
    dry_run: bool = False
) -> int:
    """Upload embeddings to Qdrant collection."""
    if dry_run:
        logger.info(f"🔍 [DRY RUN] Would upload {len(embeddings)} points to {collection_name}")
        return len(embeddings)
    
    uploaded = 0
    failed = 0
    
    logger.info(f"⬆️  Uploading {len(embeddings)} points to {collection_name}...")
    
    for i in tqdm(range(0, len(embeddings), batch_size), desc="Uploading", unit="batch"):
        batch = embeddings[i:i + batch_size]
        
        points = []
        for record in batch:
            try:
                point = PointStruct(
                    id=record['id'],
                    vector=record['embedding'],
                    payload={
                        'text': record.get('text', ''),
                        **record.get('metadata', {})
                    }
                )
                points.append(point)
            except Exception as e:
                logger.warning(f"  Failed to create point {record.get('id')}: {e}")
                failed += 1
                continue
        
        if not points:
            continue
        
        try:
            client.upsert(
                collection_name=collection_name,
                points=points,
                wait=True
            )
            uploaded += len(points)
        except Exception as e:
            logger.error(f"  ❌ Batch upload failed: {e}")
            failed += len(points)
    
    logger.info(f"  ✅ Uploaded: {uploaded} points")
    if failed > 0:
        logger.warning(f"  ⚠️  Failed: {failed} points")
    
    return uploaded


def migrate_collection(
    client: QdrantClient,
    collection_name: str,
    embedding_file: Path,
    force: bool = False,
    dry_run: bool = False
) -> bool:
    """Migrate a single collection to CodeRankEmbed."""
    logger.info(f"\n{'='*60}")
    logger.info(f"MIGRATING: {collection_name}")
    logger.info(f"{'='*60}")
    
    # Check if collection exists
    try:
        existing = client.get_collection(collection_name)
        if not force and not dry_run:
            logger.error(
                f"❌ Collection {collection_name} already exists with "
                f"{existing.points_count} points. Use --force to overwrite."
            )
            return False
        
        if force and not dry_run:
            logger.warning(f"⚠️  Deleting existing collection {collection_name}...")
            client.delete_collection(collection_name)
    except:
        pass  # Collection doesn't exist, which is fine
    
    # Load embeddings
    if not embedding_file.exists():
        logger.error(f"❌ Embedding file not found: {embedding_file}")
        return False
    
    embeddings = load_embeddings(embedding_file)
    
    if not embeddings:
        logger.error(f"❌ No valid embeddings found in {embedding_file}")
        return False
    
    # Create collection
    if not dry_run:
        logger.info(f"📦 Creating collection {collection_name}...")
        config = get_collection_config(collection_name)
        
        client.create_collection(
            collection_name=collection_name,
            **config
        )
        logger.info(f"  ✅ Collection created with 768-dim vectors")
    
    # Upload embeddings
    uploaded = upload_embeddings(
        client,
        collection_name,
        embeddings,
        batch_size=BATCH_SIZE,
        dry_run=dry_run
    )
    
    # Enable quantization
    if not dry_run and uploaded > 0:
        logger.info("⚙️  Enabling quantization...")
        enable_quantization(client, collection_name)
    
    # Verify upload
    if not dry_run:
        info = client.get_collection(collection_name)
        logger.info(f"\n✅ MIGRATION COMPLETE: {collection_name}")
        logger.info(f"  Points: {info.points_count}")
        logger.info(f"  Dimension: {info.config.params.vectors.size}")
        logger.info(f"  Indexed: {info.indexed_vectors_count}")
        
        if info.points_count != len(embeddings):
            logger.warning(
                f"⚠️  Point count mismatch: uploaded {len(embeddings)}, "
                f"stored {info.points_count}"
            )
            return False
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Migrate collections to CodeRankEmbed (768-dim)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help="Migrate all available collections"
    )
    parser.add_argument(
        '--collection',
        type=str,
        help="Migrate specific collection (e.g., qdrant_ecosystem)"
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help="Overwrite existing collections"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Validate files without uploading"
    )
    parser.add_argument(
        '--embed-dir',
        type=Path,
        default=EMBED_RESULTS_DIR,
        help=f"Directory with embedding files (default: {EMBED_RESULTS_DIR})"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.all and not args.collection:
        parser.error("Must specify --all or --collection")
    
    if args.collection and args.collection not in COLLECTION_MAPPING:
        parser.error(
            f"Unknown collection: {args.collection}. "
            f"Available: {', '.join(COLLECTION_MAPPING.keys())}"
        )
    
    logger.info("=" * 60)
    logger.info("CODERANK MIGRATION - Upload 768-dim Embeddings")
    logger.info("=" * 60)
    logger.info(f"Qdrant URL: {QDRANT_URL}")
    logger.info(f"Embedding directory: {args.embed_dir}")
    logger.info(f"Vector dimension: {VECTOR_DIMENSION}")
    logger.info(f"Batch size: {BATCH_SIZE}")
    
    if args.dry_run:
        logger.info("Mode: DRY RUN (no changes will be made)")
    elif args.force:
        logger.info("Mode: FORCE OVERWRITE ⚠️")
    else:
        logger.info("Mode: CREATE NEW COLLECTIONS")
    
    logger.info("=" * 60)
    
    # Connect to Qdrant
    try:
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            timeout=60
        )
        
        collections = client.get_collections()
        logger.info(f"✅ Connected to Qdrant ({len(collections.collections)} existing collections)")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Qdrant: {e}")
        return 1
    
    # Determine which collections to migrate
    if args.all:
        collections_to_migrate = list(COLLECTION_MAPPING.keys())
    else:
        collections_to_migrate = [args.collection]
    
    # Migrate collections
    results = {}
    for collection_name in collections_to_migrate:
        embedding_file = args.embed_dir / COLLECTION_MAPPING[collection_name]
        
        success = migrate_collection(
            client,
            collection_name,
            embedding_file,
            force=args.force,
            dry_run=args.dry_run
        )
        
        results[collection_name] = success
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("MIGRATION SUMMARY")
    logger.info("=" * 60)
    
    successful = [name for name, success in results.items() if success]
    failed = [name for name, success in results.items() if not success]
    
    logger.info(f"✅ Successful: {len(successful)}/{len(results)}")
    for name in successful:
        logger.info(f"  ✅ {name}")
    
    if failed:
        logger.info(f"\n❌ Failed: {len(failed)}/{len(results)}")
        for name in failed:
            logger.info(f"  ❌ {name}")
    
    logger.info("=" * 60)
    
    if args.dry_run:
        logger.info("\n💡 This was a dry run. Remove --dry-run to actually upload.")
    elif len(successful) > 0:
        logger.info("\n🎉 Migration complete! Collections ready for CodeRank queries.")
        logger.info("   Next step: Update MCP server to use CodeRankEmbed for queries")
    
    return 0 if len(failed) == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
