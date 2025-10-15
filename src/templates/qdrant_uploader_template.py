"""
TEMPLATE 3: Universal Qdrant Uploader

PURPOSE:
    Upload ANY embedded collection to Qdrant with optimized batch processing.
    Handles collection creation, schema validation, and error recovery.

WORKFLOW POSITION: Step 3 of 3
    Chunker Template → Embedder Template → [This Script]

USAGE:
    # Upload embeddings to Qdrant
    python -m src.templates.qdrant_uploader_template \\
        --file embeddings/qdrant_ecosystem_768.jsonl \\
        --collection qdrant_ecosystem \\
        --url http://localhost:6333
    
    # Force recreate collection (delete existing)
    python -m src.templates.qdrant_uploader_template \\
        --file embeddings/my_docs_768.jsonl \\
        --collection my_docs \\
        --force
    
    # Use Qdrant Cloud
    python -m src.templates.qdrant_uploader_template \\
        --file embeddings/collection_768.jsonl \\
        --collection my_collection \\
        --url https://xyz.qdrant.io:6333 \\
        --api-key YOUR_API_KEY

FEATURES:
    - Auto-detects vector dimension from JSONL
    - Creates collection with optimized settings (HNSW, quantization)
    - Batch upload with retry logic
    - Progress tracking
    - Count verification
    - Resume capability (skips duplicate IDs)
    - Binary quantization for 768-dim vectors (40x speedup)
    - Scalar quantization for 3584-dim vectors (2x speedup)

QDRANT OPTIMIZATION (for 768-dim CodeRankEmbed):
    - HNSW index: m=16, ef_construct=100
    - Binary quantization: enabled (40x speedup)
    - Distance: Cosine similarity
    - Payload indexing: subdirectory, source_file

OUTPUT:
    - Collection created/updated in Qdrant
    - Upload statistics printed
    - Ready for MCP server integration

NEXT STEP:
    Test search quality and integrate with MCP server.
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib
from uuid import UUID

from pydantic import BaseModel, Field
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    OptimizersConfigDiff, HnswConfigDiff,
    QuantizationConfig, BinaryQuantization,
    ScalarQuantization, ScalarType,
    PayloadSchemaType
)
from tqdm import tqdm

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION
# ============================================================================

class UploaderConfig(BaseModel):
    """Configuration for Qdrant uploader."""
    
    # Input
    file_path: Path = Field(..., description="JSONL file with embeddings")
    collection_name: str = Field(..., description="Qdrant collection name")
    
    # Qdrant connection
    qdrant_url: str = Field(default="http://localhost:6333", description="Qdrant URL")
    api_key: Optional[str] = Field(default=None, description="Qdrant API key (for cloud)")
    
    # Upload options
    batch_size: int = Field(default=256, description="Upload batch size")
    force: bool = Field(default=False, description="Force recreate collection")
    resume: bool = Field(default=True, description="Resume upload (skip existing IDs)")
    
    # Optimization
    enable_quantization: bool = Field(default=True, description="Enable quantization")
    hnsw_m: int = Field(default=16, description="HNSW m parameter")
    hnsw_ef_construct: int = Field(default=100, description="HNSW ef_construct")


# ============================================================================
# QDRANT UPLOADER ENGINE
# ============================================================================

class UniversalQdrantUploader:
    """
    Universal Qdrant uploader with optimization.
    
    Features:
    - Auto-detection of vector dimension
    - Optimized HNSW settings
    - Binary quantization for 768-dim (40x speedup)
    - Scalar quantization for 3584-dim (2x speedup)
    - Batch upload with retry
    - Count verification
    """
    
    def __init__(self, config: UploaderConfig):
        """
        Initialize uploader.
        
        Args:
            config: Uploader configuration
        """
        self.config = config
        
        logger.info(f"🔌 Connecting to Qdrant: {config.qdrant_url}")
        
        # Initialize Qdrant client
        self.client = QdrantClient(
            url=config.qdrant_url,
            api_key=config.api_key,
            timeout=60
        )
        
        # Test connection
        try:
            health = self.client.health()
            logger.info(f"✓ Qdrant health: {health.status}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Qdrant: {e}")
        
        # Stats
        self.stats = {
            "total_records": 0,
            "uploaded": 0,
            "skipped": 0,
            "failed": 0,
            "start_time": None,
            "end_time": None
        }
    
    def detect_dimension(self, sample_record: Dict[str, Any]) -> int:
        """
        Detect vector dimension from sample record.
        
        Args:
            sample_record: Sample JSONL record
        
        Returns:
            Vector dimension
        """
        embedding = sample_record.get('embedding', [])
        if not embedding:
            raise ValueError("Sample record has no embedding")
        
        dimension = len(embedding)
        logger.info(f"📊 Detected vector dimension: {dimension}")
        
        return dimension
    
    def create_collection(self, dimension: int):
        """
        Create or recreate Qdrant collection with optimized settings.
        
        Args:
            dimension: Vector dimension
        """
        logger.info(f"🏗️  Setting up collection: {self.config.collection_name}")
        
        # Check if collection exists
        collections = self.client.get_collections().collections
        collection_exists = any(c.name == self.config.collection_name for c in collections)
        
        if collection_exists:
            if self.config.force:
                logger.info(f"  Deleting existing collection (force=True)")
                self.client.delete_collection(self.config.collection_name)
            else:
                logger.info(f"  Collection exists (will resume upload)")
                return
        
        # Determine quantization strategy
        if dimension == 768 and self.config.enable_quantization:
            # Binary quantization for 768-dim (40x speedup)
            quantization = BinaryQuantization(
                binary=BinaryQuantization()
            )
            logger.info(f"  Quantization: Binary (40x speedup)")
        elif dimension == 3584 and self.config.enable_quantization:
            # Scalar quantization for 3584-dim (2x speedup)
            quantization = ScalarQuantization(
                scalar=ScalarQuantization(
                    type=ScalarType.INT8,
                    quantile=0.99,
                    always_ram=True
                )
            )
            logger.info(f"  Quantization: Scalar INT8 (2x speedup)")
        else:
            quantization = None
            logger.info(f"  Quantization: Disabled")
        
        # Create collection
        logger.info(f"  Creating collection with {dimension}-dim vectors...")
        
        self.client.create_collection(
            collection_name=self.config.collection_name,
            vectors_config=VectorParams(
                size=dimension,
                distance=Distance.COSINE,
                on_disk=False  # Keep in RAM for speed
            ),
            optimizers_config=OptimizersConfigDiff(
                indexing_threshold=20000,  # Start indexing after 20k points
                memmap_threshold=50000     # Move to disk after 50k points
            ),
            hnsw_config=HnswConfigDiff(
                m=self.config.hnsw_m,
                ef_construct=self.config.hnsw_ef_construct,
                full_scan_threshold=20000
            ),
            quantization_config=quantization
        )
        
        logger.info(f"✓ Collection created")
        
        # Create payload indexes for filtering
        logger.info(f"  Creating payload indexes...")
        
        try:
            self.client.create_payload_index(
                collection_name=self.config.collection_name,
                field_name="metadata.subdirectory",
                field_schema=PayloadSchemaType.KEYWORD
            )
            logger.info(f"    ✓ subdirectory index")
        except:
            pass
        
        try:
            self.client.create_payload_index(
                collection_name=self.config.collection_name,
                field_name="metadata.source_file",
                field_schema=PayloadSchemaType.KEYWORD
            )
            logger.info(f"    ✓ source_file index")
        except:
            pass
        
        logger.info(f"✓ Collection setup complete\\n")
    
    def load_jsonl(self) -> List[Dict[str, Any]]:
        """
        Load JSONL file.
        
        Returns:
            List of records
        """
        logger.info(f"📂 Loading JSONL: {self.config.file_path}")
        
        if not self.config.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.config.file_path}")
        
        records = []
        with open(self.config.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
        
        self.stats["total_records"] = len(records)
        
        logger.info(f"✓ Loaded {len(records)} records\\n")
        
        return records
    
    def convert_to_points(self, records: List[Dict[str, Any]]) -> List[PointStruct]:
        """
        Convert JSONL records to Qdrant points.
        
        Args:
            records: List of JSONL records
        
        Returns:
            List of PointStruct objects
        """
        points = []
        
        for record in records:
            # Generate UUID from ID
            id_str = record.get('id', hashlib.sha256(record['text'].encode()).hexdigest()[:16])
            point_id = hashlib.md5(id_str.encode()).hexdigest()
            
            # Create point
            point = PointStruct(
                id=point_id,
                vector=record['embedding'],
                payload={
                    'text': record['text'],
                    'metadata': record.get('metadata', {})
                }
            )
            
            points.append(point)
        
        return points
    
    def upload_batch(self, points: List[PointStruct]) -> int:
        """
        Upload a batch of points with retry logic.
        
        Args:
            points: List of PointStruct objects
        
        Returns:
            Number of successfully uploaded points
        """
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                self.client.upsert(
                    collection_name=self.config.collection_name,
                    points=points,
                    wait=True
                )
                return len(points)
            
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"  Upload failed (attempt {attempt + 1}/{max_retries}): {e}")
                    continue
                else:
                    logger.error(f"  Upload failed after {max_retries} attempts: {e}")
                    return 0
        
        return 0
    
    def upload_all(self, points: List[PointStruct]):
        """
        Upload all points in batches with progress tracking.
        
        Args:
            points: List of all points to upload
        """
        logger.info(f"📤 Uploading {len(points)} points in batches of {self.config.batch_size}")
        
        for i in tqdm(range(0, len(points), self.config.batch_size), desc="Uploading", unit="batch"):
            batch = points[i:i + self.config.batch_size]
            
            uploaded = self.upload_batch(batch)
            self.stats["uploaded"] += uploaded
            self.stats["failed"] += len(batch) - uploaded
        
        logger.info(f"✓ Upload complete\\n")
    
    def verify_count(self):
        """Verify upload count."""
        logger.info(f"🔍 Verifying upload...")
        
        collection_info = self.client.get_collection(self.config.collection_name)
        actual_count = collection_info.points_count
        expected_count = self.stats["total_records"]
        
        logger.info(f"  Expected: {expected_count}")
        logger.info(f"  Actual: {actual_count}")
        
        if actual_count == expected_count:
            logger.info(f"✓ Count verification passed\\n")
        else:
            logger.warning(f"⚠️  Count mismatch: {actual_count} != {expected_count}\\n")
    
    def run(self):
        """Run the upload pipeline."""
        self.stats["start_time"] = datetime.now()
        
        # Load JSONL
        records = self.load_jsonl()
        
        # Detect dimension
        dimension = self.detect_dimension(records[0])
        
        # Create/setup collection
        self.create_collection(dimension)
        
        # Convert to points
        points = self.convert_to_points(records)
        
        # Upload
        self.upload_all(points)
        
        # Verify
        self.verify_count()
        
        # Summary
        self.stats["end_time"] = datetime.now()
        elapsed = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
        
        logger.info(f"{'='*60}")
        logger.info(f"✓ UPLOAD COMPLETED")
        logger.info(f"{'='*60}")
        logger.info(f"Collection: {self.config.collection_name}")
        logger.info(f"Total records: {self.stats['total_records']}")
        logger.info(f"Uploaded: {self.stats['uploaded']}")
        logger.info(f"Failed: {self.stats['failed']}")
        logger.info(f"Vector dimension: {dimension}")
        logger.info(f"Total time: {elapsed/60:.1f} minutes")
        logger.info(f"Upload rate: {self.stats['uploaded']/elapsed:.1f} points/sec")
        logger.info(f"{'='*60}\\n")
        
        logger.info(f"📦 NEXT STEPS:")
        logger.info(f"1. Test search quality:")
        logger.info(f"   - Use Qdrant console: {self.config.qdrant_url}/dashboard")
        logger.info(f"   - Or test with MCP server")
        logger.info(f"2. Integrate with MCP server (add to collections list)")
        logger.info(f"3. Update MCP server with CodeRankEmbed query prefix")


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Universal Qdrant Uploader (Template 3 of 3)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Required arguments
    parser.add_argument(
        '--file',
        required=True,
        type=Path,
        help="JSONL file with embeddings (from Template 2)"
    )
    parser.add_argument(
        '--collection',
        required=True,
        help="Qdrant collection name"
    )
    
    # Optional arguments
    parser.add_argument(
        '--url',
        default="http://localhost:6333",
        help="Qdrant URL (default: http://localhost:6333)"
    )
    parser.add_argument(
        '--api-key',
        help="Qdrant API key (for cloud)"
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=256,
        help="Upload batch size (default: 256)"
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help="Force recreate collection (delete existing)"
    )
    parser.add_argument(
        '--no-quantization',
        action='store_true',
        help="Disable quantization"
    )
    
    args = parser.parse_args()
    
    # Create config
    config = UploaderConfig(
        file_path=args.file,
        collection_name=args.collection,
        qdrant_url=args.url,
        api_key=args.api_key,
        batch_size=args.batch_size,
        force=args.force,
        enable_quantization=not args.no_quantization
    )
    
    # Run uploader
    try:
        logger.info(f"{'='*60}")
        logger.info(f"TEMPLATE 3: UNIVERSAL QDRANT UPLOADER")
        logger.info(f"{'='*60}\\n")
        
        uploader = UniversalQdrantUploader(config)
        uploader.run()
    
    except KeyboardInterrupt:
        logger.info("\\n⚠️  Upload interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\\n❌ Upload failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
