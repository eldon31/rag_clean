"""
Templates module for reusable ingestion pipelines.

This module provides unified, optimized templates for common tasks:
- Embedding & chunking (unified_pipeline.py)
- Collection processing (future)
- Data migration (future)
"""

from pathlib import Path

__all__ = ["unified_pipeline"]

# Module metadata
__version__ = "1.0.0"
__author__ = "RAG Clean Team"
__description__ = "Unified templates for document processing and embedding"
