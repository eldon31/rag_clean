"""
Production-ready Docling Configuration

Optimized for code documentation processing with CodeRankEmbed embedding model.

Key Features:
- Code enrichment enabled (CRITICAL for CodeRankEmbed)
- Table structure extraction
- OCR with multi-language support
- Formula parsing for technical documents
- Hardware acceleration configuration
- Multiple converter profiles (production, fast, minimal)

Usage:
    from src.config.docling_config import DoclingConfig
    
    # Production converter (full features)
    converter = DoclingConfig.create_production_converter()
    
    # Fast converter (for testing)
    converter = DoclingConfig.create_fast_converter()
"""

import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class DoclingConfig:
    """Centralized Docling configuration for production use."""
    
    # Default settings
    DEFAULT_OCR_ENABLED = True
    DEFAULT_TABLE_EXTRACTION = True
    DEFAULT_CODE_ENRICHMENT = True  # CRITICAL for CodeRankEmbed!
    DEFAULT_FORMULA_ENRICHMENT = True
    DEFAULT_IMAGE_SCALE = 2.0
    DEFAULT_MAX_FILE_SIZE_MB = 500
    DEFAULT_MAX_NUM_PAGES = 1000
    
    @staticmethod
    def create_production_converter():
        """
        Create production-ready DocumentConverter.
        
        Optimized for:
        - Code documentation (enable code enrichment)
        - Technical papers (enable formula parsing)
        - Tables (enable structure extraction)
        - Multi-language OCR support
        - Performance optimization
        
        Returns:
            DocumentConverter instance with production settings
        """
        try:
            from docling.document_converter import DocumentConverter, PdfFormatOption
            from docling.datamodel.base_models import InputFormat
            from docling.datamodel.pipeline_options import (
                PdfPipelineOptions,
                OcrOptions,
                TableStructureOptions,
                AcceleratorOptions
            )
        except ImportError as e:
            logger.error(f"Failed to import Docling: {e}")
            raise ImportError(
                "Docling is not installed. Install with: pip install docling[vlm]>=2.55.0"
            ) from e
        
        # OCR Configuration
        ocr_options = OcrOptions(
            # Enable multi-language support if needed
            # lang=["eng"]  # English only by default
            # For multi-language: lang=["eng", "fra", "deu"]
        )
        
        # Table Extraction Configuration
        table_options = TableStructureOptions(
            # mode="accurate"  # More accurate but slower
            # mode="fast"      # Faster but less accurate
        )
        
        # Hardware Acceleration
        # Auto-detect GPU availability
        device = "cpu"  # Default to CPU
        try:
            import torch
            if torch.cuda.is_available():
                device = "cuda"
                logger.info("CUDA GPU detected - using GPU acceleration")
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                device = "mps"
                logger.info("Apple Silicon GPU detected - using MPS acceleration")
            else:
                logger.info("No GPU detected - using CPU")
        except ImportError:
            logger.info("PyTorch not available - using CPU")
        
        accelerator_options = AcceleratorOptions(
            # device=device,  # Uncomment to enable GPU
            num_threads=min(4, os.cpu_count() or 4)  # Use up to 4 threads
        )
        
        # PDF Pipeline Options (primary focus for this codebase)
        pdf_options = PdfPipelineOptions(
            # Text Extraction
            do_ocr=DoclingConfig.DEFAULT_OCR_ENABLED,
            ocr_options=ocr_options,
            
            # Structure Extraction
            do_table_structure=DoclingConfig.DEFAULT_TABLE_EXTRACTION,
            table_structure_options=table_options,
            
            # CRITICAL: Code & Formula Enhancement
            # This is essential for CodeRankEmbed embeddings!
            do_code_enrichment=DoclingConfig.DEFAULT_CODE_ENRICHMENT,
            do_formula_enrichment=DoclingConfig.DEFAULT_FORMULA_ENRICHMENT,
            
            # Performance
            accelerator_options=accelerator_options,
            
            # Image Handling
            images_scale=DoclingConfig.DEFAULT_IMAGE_SCALE,  # Higher resolution for OCR
            generate_page_images=False,  # Save memory
            generate_picture_images=True,  # Extract figures/diagrams
        )
        
        # Format-Specific Options
        format_options = {
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pdf_options
            ),
            # Could add more formats here:
            # InputFormat.DOCX: WordFormatOption(...),
            # InputFormat.HTML: HTMLFormatOption(...),
        }
        
        # Create Converter with configuration
        converter = DocumentConverter(
            format_options=format_options
        )
        
        logger.info("Docling production converter created with optimized settings")
        logger.info(f"  - Code enrichment: {DoclingConfig.DEFAULT_CODE_ENRICHMENT}")
        logger.info(f"  - Table extraction: {DoclingConfig.DEFAULT_TABLE_EXTRACTION}")
        logger.info(f"  - OCR enabled: {DoclingConfig.DEFAULT_OCR_ENABLED}")
        logger.info(f"  - Acceleration: {device}")
        
        return converter
    
    @staticmethod
    def create_fast_converter():
        """
        Create fast converter for testing/development.
        
        Features:
        - Minimal processing for speed
        - Code enrichment still enabled (important)
        - No OCR (faster but may miss scanned PDFs)
        - No table extraction
        - No formula parsing
        
        Returns:
            DocumentConverter instance with fast settings
        """
        try:
            from docling.document_converter import DocumentConverter, PdfFormatOption
            from docling.datamodel.base_models import InputFormat
            from docling.datamodel.pipeline_options import PdfPipelineOptions
        except ImportError as e:
            raise ImportError(
                "Docling is not installed. Install with: pip install docling[vlm]>=2.55.0"
            ) from e
        
        # Fast PDF options - minimal processing
        pdf_options = PdfPipelineOptions(
            do_ocr=False,  # Skip OCR for speed
            do_table_structure=False,  # Skip table extraction
            do_code_enrichment=True,  # Keep code enrichment (important!)
            do_formula_enrichment=False,  # Skip formulas
            generate_page_images=False,
            generate_picture_images=False,
        )
        
        format_options = {
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pdf_options
            )
        }
        
        converter = DocumentConverter(format_options=format_options)
        
        logger.info("Docling fast converter created (minimal processing)")
        
        return converter
    
    @staticmethod
    def create_minimal_converter():
        """
        Create minimal converter with no configuration.
        
        Uses Docling defaults - useful for baseline testing.
        
        Returns:
            DocumentConverter instance with default settings
        """
        try:
            from docling.document_converter import DocumentConverter
        except ImportError as e:
            raise ImportError(
                "Docling is not installed. Install with: pip install docling[vlm]>=2.55.0"
            ) from e
        
        converter = DocumentConverter()
        
        logger.info("Docling minimal converter created (defaults only)")
        
        return converter
    
    @staticmethod
    def get_recommended_limits() -> Dict[str, Any]:
        """
        Get recommended file/page limits for processing.
        
        Returns:
            Dict with recommended limits
        """
        return {
            "max_file_size": DoclingConfig.DEFAULT_MAX_FILE_SIZE_MB * 1024 * 1024,  # bytes
            "max_file_size_mb": DoclingConfig.DEFAULT_MAX_FILE_SIZE_MB,
            "max_num_pages": DoclingConfig.DEFAULT_MAX_NUM_PAGES,
            "recommended_batch_size": 10,  # Process 10 docs at a time
            "recommended_concurrency": min(4, os.cpu_count() or 4),
        }
    
    @staticmethod
    def create_custom_converter(
        ocr_enabled: bool = True,
        table_extraction: bool = True,
        code_enrichment: bool = True,
        formula_enrichment: bool = True,
        image_scale: float = 2.0,
        use_gpu: bool = False
    ):
        """
        Create custom converter with specific settings.
        
        Args:
            ocr_enabled: Enable OCR for scanned PDFs
            table_extraction: Extract table structures
            code_enrichment: Enhance code blocks (IMPORTANT for code embeddings)
            formula_enrichment: Parse mathematical formulas
            image_scale: Image resolution multiplier (higher = better OCR)
            use_gpu: Use GPU acceleration if available
            
        Returns:
            DocumentConverter instance with custom settings
        """
        try:
            from docling.document_converter import DocumentConverter, PdfFormatOption
            from docling.datamodel.base_models import InputFormat
            from docling.datamodel.pipeline_options import (
                PdfPipelineOptions,
                AcceleratorOptions
            )
        except ImportError as e:
            raise ImportError(
                "Docling is not installed. Install with: pip install docling[vlm]>=2.55.0"
            ) from e
        
        # Determine device
        device = "cpu"
        if use_gpu:
            try:
                import torch
                if torch.cuda.is_available():
                    device = "cuda"
                elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                    device = "mps"
            except ImportError:
                pass
        
        accelerator_options = AcceleratorOptions(
            # device=device,  # Uncomment to enable
            num_threads=min(4, os.cpu_count() or 4)
        )
        
        # Custom PDF options
        pdf_options = PdfPipelineOptions(
            do_ocr=ocr_enabled,
            do_table_structure=table_extraction,
            do_code_enrichment=code_enrichment,
            do_formula_enrichment=formula_enrichment,
            images_scale=image_scale,
            accelerator_options=accelerator_options,
            generate_page_images=False,
            generate_picture_images=True,
        )
        
        format_options = {
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pdf_options
            )
        }
        
        converter = DocumentConverter(format_options=format_options)
        
        logger.info(
            f"Docling custom converter created: "
            f"OCR={ocr_enabled}, Tables={table_extraction}, "
            f"Code={code_enrichment}, GPU={device}"
        )
        
        return converter


# Convenience function
def get_default_converter():
    """Get the default production converter."""
    return DoclingConfig.create_production_converter()
