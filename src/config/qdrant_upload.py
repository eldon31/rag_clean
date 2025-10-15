"""Configuration for Qdrant embedding upload process."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from qdrant_client.models import Distance


@dataclass
class QdrantUploadConfig:
    """Configuration for Qdrant embedding upload process."""
    
    # Connection settings
    url: str = "http://localhost:6333"
    api_key: Optional[str] = None
    timeout: int = 60
    
    # Collection settings
    collection_name: str = "qdrant_ecosystem"
    vector_dim: int = 3584  # Updated to match actual embeddings
    distance_metric: Distance = Distance.COSINE
    
    # Payload schema (fields to index)
    indexed_fields: list[str] = field(default_factory=lambda: [
        "subdirectory",
        "source_file",
        "source_path"
    ])
    
    # Upload settings
    embeddings_path: Path = Path("output/embed/qdrant_ecosystem_embeddings.jsonl")
    summary_path: Optional[Path] = None  # Auto-derived from embeddings_path
    batch_size: int = 256
    max_retries: int = 3
    retry_delay: float = 0.5  # Base delay in seconds
    
    # Behavior flags
    truncate_before_upload: bool = False
    force: bool = False  # Skip confirmations
    dry_run: bool = False
    verbose: bool = False
    
    def __post_init__(self):
        """Derive summary path and normalize paths."""
        # Convert string paths to Path objects
        if isinstance(self.embeddings_path, str):
            self.embeddings_path = Path(self.embeddings_path)
        
        # Auto-derive summary path if not provided
        if self.summary_path is None:
            base = self.embeddings_path.stem
            self.summary_path = self.embeddings_path.parent / f"{base}_summary.json"
        elif isinstance(self.summary_path, str):
            self.summary_path = Path(self.summary_path)
    
    @classmethod
    def from_env(cls) -> "QdrantUploadConfig":
        """Load configuration from environment variables.
        
        Supported environment variables:
        - QDRANT_URL: Qdrant server URL (default: http://localhost:6333)
        - QDRANT_API_KEY: API key for authentication (optional)
        - QDRANT_COLLECTION: Target collection name (default: qdrant_ecosystem)
        - QDRANT_TIMEOUT: Connection timeout in seconds (default: 60)
        
        Returns:
            QdrantUploadConfig with values from environment
        """
        return cls(
            url=os.getenv("QDRANT_URL", "http://localhost:6333"),
            api_key=os.getenv("QDRANT_API_KEY"),
            collection_name=os.getenv("QDRANT_COLLECTION", "qdrant_ecosystem"),
            timeout=int(os.getenv("QDRANT_TIMEOUT", "60")),
        )
