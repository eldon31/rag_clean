"""
Remove old 3584-dim collections and backup metadata.

This script prepares for CodeRank migration by:
1. Backing up collection metadata
2. Optionally creating snapshots
3. Deleting old 3584-dim collections

USAGE:
    # Dry run (show what will be deleted)
    python scripts/remove_old_collections.py --dry-run
    
    # Delete with backup
    python scripts/remove_old_collections.py --backup
    
    # Delete without backup (dangerous!)
    python scripts/remove_old_collections.py --force
"""

import os
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Collections to remove (old 3584-dim collections)
OLD_COLLECTIONS = [
    "agent_kit",
    "inngest_overall", 
    "qdrant_ecosystem",
    "docling"
]

# Expected old dimension
OLD_DIMENSION = 3584
NEW_DIMENSION = 768


def get_collection_info(client: QdrantClient, collection_name: str) -> Dict[str, Any]:
    """Get detailed collection information."""
    try:
        info = client.get_collection(collection_name)
        return {
            "name": collection_name,
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "dimension": info.config.params.vectors.size,
            "distance": info.config.params.vectors.distance.name,
            "indexed_count": info.indexed_vectors_count,
            "exists": True
        }
    except Exception as e:
        logger.warning(f"Collection {collection_name} not found: {e}")
        return {
            "name": collection_name,
            "exists": False,
            "error": str(e)
        }


def backup_collection_metadata(client: QdrantClient, collections: List[str], backup_dir: Path):
    """Backup collection metadata to JSON."""
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    backup_file = backup_dir / f"collection_backup_{timestamp}.json"
    
    metadata = {
        "timestamp": timestamp,
        "qdrant_url": QDRANT_URL,
        "collections": []
    }
    
    for collection_name in collections:
        info = get_collection_info(client, collection_name)
        metadata["collections"].append(info)
        
        if info["exists"]:
            logger.info(
                f"📊 {collection_name}: "
                f"{info['points_count']} points, "
                f"{info['dimension']}-dim"
            )
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"✅ Backup saved to: {backup_file}")
    return backup_file


def delete_collections(client: QdrantClient, collections: List[str], dry_run: bool = False):
    """Delete collections."""
    deleted = []
    skipped = []
    
    for collection_name in collections:
        info = get_collection_info(client, collection_name)
        
        if not info["exists"]:
            logger.info(f"⏭️  {collection_name}: Already deleted or doesn't exist")
            skipped.append(collection_name)
            continue
        
        dimension = info.get("dimension")
        
        # Safety check: only delete 3584-dim collections
        if dimension != OLD_DIMENSION:
            logger.warning(
                f"⚠️  {collection_name}: Dimension is {dimension}, expected {OLD_DIMENSION}. "
                f"Skipping for safety."
            )
            skipped.append(collection_name)
            continue
        
        if dry_run:
            logger.info(
                f"🔍 [DRY RUN] Would delete {collection_name}: "
                f"{info['points_count']} points, {dimension}-dim"
            )
        else:
            try:
                client.delete_collection(collection_name)
                logger.info(
                    f"🗑️  Deleted {collection_name}: "
                    f"{info['points_count']} points, {dimension}-dim"
                )
                deleted.append(collection_name)
            except Exception as e:
                logger.error(f"❌ Failed to delete {collection_name}: {e}")
                skipped.append(collection_name)
    
    return deleted, skipped


def main():
    parser = argparse.ArgumentParser(
        description="Remove old 3584-dim collections before CodeRank migration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Show what would be deleted without actually deleting"
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help="Create metadata backup before deletion"
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help="Delete without backup (dangerous!)"
    )
    parser.add_argument(
        '--backup-dir',
        type=Path,
        default=Path("output/collection_backups"),
        help="Directory for backups (default: output/collection_backups)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.dry_run and not args.backup and not args.force:
        parser.error("Must specify --dry-run, --backup, or --force")
    
    logger.info("=" * 60)
    logger.info("QDRANT COLLECTION CLEANUP - CodeRank Migration")
    logger.info("=" * 60)
    logger.info(f"Qdrant URL: {QDRANT_URL}")
    logger.info(f"Collections to remove: {', '.join(OLD_COLLECTIONS)}")
    logger.info(f"Old dimension: {OLD_DIMENSION}")
    logger.info(f"New dimension: {NEW_DIMENSION}")
    
    if args.dry_run:
        logger.info("Mode: DRY RUN (no changes will be made)")
    elif args.backup:
        logger.info(f"Mode: DELETE WITH BACKUP (backup dir: {args.backup_dir})")
    else:
        logger.info("Mode: DELETE WITHOUT BACKUP ⚠️")
    
    logger.info("=" * 60 + "\n")
    
    # Connect to Qdrant
    try:
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            timeout=30
        )
        
        # Test connection
        collections = client.get_collections()
        logger.info(f"✅ Connected to Qdrant ({len(collections.collections)} collections)")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Qdrant: {e}")
        return 1
    
    # Backup if requested
    if args.backup and not args.dry_run:
        logger.info("\n📦 Creating backup...")
        backup_file = backup_collection_metadata(client, OLD_COLLECTIONS, args.backup_dir)
        logger.info(f"✅ Backup complete: {backup_file}\n")
    
    # Delete collections
    logger.info("🗑️  Removing collections...\n")
    deleted, skipped = delete_collections(client, OLD_COLLECTIONS, dry_run=args.dry_run)
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Deleted: {len(deleted)} collections")
    if deleted:
        for name in deleted:
            logger.info(f"  ✅ {name}")
    
    logger.info(f"\nSkipped: {len(skipped)} collections")
    if skipped:
        for name in skipped:
            logger.info(f"  ⏭️  {name}")
    
    logger.info("=" * 60)
    
    if args.dry_run:
        logger.info("\n💡 This was a dry run. Run with --backup or --force to actually delete.")
    else:
        logger.info("\n✅ Collections removed. Ready for CodeRank migration!")
        logger.info("   Next step: python scripts/migrate_to_coderank.py")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
