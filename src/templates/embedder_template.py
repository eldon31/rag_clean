"""
TEMPLATE 2: CodeRankEmbed Embedder (Kaggle Tesla T4 x2)

PURPOSE:
    Embed ANY collection of pre-chunked documents using CodeRankEmbed (768-dim).
    Designed for Kaggle GPU Tesla T4 x2 (15.83 GB VRAM each).

WORKFLOW POSITION: Step 2 of 3
    Chunker Template → [This Script] → Qdrant Uploader

USAGE (on Kaggle):
    # Upload chunked JSON from Template 1 as Kaggle dataset
    # Then run this script on Kaggle with GPU T4 x2
    
    python embedder_template.py \
        --collection qdrant_ecosystem \
        --input /kaggle/input/qdrant_ecosystem_chunked/ \
        --output /kaggle/working/qdrant_ecosystem_768.jsonl

MODEL:
    - CodeRankEmbed: 768-dim, 137M params, 75x faster queries
    - Model ID: nomic-ai/CodeRankEmbed
    - Optimized for Tesla T4 x2 (15.83 GB VRAM each)

GPU OPTIMIZATION:
    - Data parallelism across 2x Tesla T4 GPUs
    - Batch size: 32 per GPU (64 total)
    - Memory-efficient processing
    - Progress tracking
    - Automatic CUDA cache clearing every 5 batches

OUTPUT FORMAT:
    JSONL file with Qdrant-ready format:
    {
        "id": "unique_hash",
        "text": "chunk content...",
        "embedding": [0.123, -0.456, ...],  # 768-dim
        "metadata": {
            "embedding_model": "CodeRankEmbed-768",
            "embedding_model_version": "nomic-ai/CodeRankEmbed",
            "vector_dimension": 768,
            "source_file": "path/to/file.md",
            ...
        }
    }

NEXT STEP:
    Download output JSONL from Kaggle /working/ directory.
    Upload to Qdrant using Template 3 (qdrant_uploader_template.py).

KAGGLE SETUP:
    1. Create new Kaggle notebook
    2. Upload this script
    3. Add chunked data as dataset
    4. Set accelerator to GPU T4 x2
    5. Run script
    6. Download embeddings from /kaggle/working/
"""

import os

# Prevent transformers from loading TensorFlow
os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import json
import logging
import argparse
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Literal
from datetime import datetime

import numpy as np
import torch
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Check NumPy version (Kaggle issue)
if tuple(map(int, np.__version__.split(".")[:2])) >= (2, 0):
    logger.warning(
        "⚠️  NumPy 2.x detected. If you encounter errors, run: "
        "pip install -q --force-reinstall 'numpy==1.26.4' 'scikit-learn==1.4.2' "
        "and restart runtime."
    )


# ============================================================================
# CONFIGURATION
# ============================================================================

class ModelConfig(BaseModel):
    """CodeRankEmbed configuration for Tesla T4 x2."""
    
    name: str = "CodeRankEmbed"
    hf_model_id: str = "nomic-ai/CodeRankEmbed"
    vector_dim: int = 768
    max_tokens: int = 2048
    query_prefix: str = "Represent this query for searching relevant code: "
    trust_remote_code: bool = True
    batch_size_per_gpu: int = 32  # Safe for 15.83 GB VRAM
    batch_size_cpu: int = 8


# Single model configuration - CodeRankEmbed only
MODEL_CONFIG = ModelConfig()


class EmbedderConfig(BaseModel):
    """Embedder configuration."""
    
    collection_name: str
    input_path: Path
    output_path: Path
    use_gpu: bool = True
    use_data_parallel: bool = True  # Use 2 Tesla T4 GPUs


# ============================================================================
# UNIVERSAL EMBEDDER ENGINE
# ============================================================================

class UniversalEmbedder:
    """
    CodeRankEmbed embedder optimized for Kaggle Tesla T4 x2.
    
    Features:
    - Dual Tesla T4 GPU support (15.83 GB VRAM each)
    - Data parallelism across 2 GPUs
    - Batch size: 32 per GPU (64 total)
    - Memory-efficient processing with CUDA cache clearing
    - 768-dimensional embeddings
    """
    
    def __init__(self, config: EmbedderConfig):
        """
        Initialize CodeRankEmbed embedder.
        
        Args:
            config: Embedder configuration
        """
        self.config = config
        self.model_config = MODEL_CONFIG
        
        # Device detection
        self.has_cuda = torch.cuda.is_available()
        self.num_gpus = torch.cuda.device_count() if self.has_cuda else 0
        self.use_gpu = config.use_gpu and self.has_cuda
        self.use_data_parallel = config.use_data_parallel and self.num_gpus >= 2
        
        logger.info(f"{'='*60}")
        logger.info(f"GPU SETUP")
        logger.info(f"{'='*60}")
        logger.info(f"CUDA available: {self.has_cuda}")
        logger.info(f"GPU count: {self.num_gpus}")
        if self.has_cuda:
            for i in range(self.num_gpus):
                logger.info(f"GPU {i}: {torch.cuda.get_device_name(i)}")
                props = torch.cuda.get_device_properties(i)
                logger.info(f"  Memory: {props.total_memory / 1e9:.2f} GB")
        logger.info(f"{'='*60}\\n")
        
        # Batch size selection
        if self.use_gpu:
            self.batch_size = self.model_config.batch_size_per_gpu
        else:
            self.batch_size = self.model_config.batch_size_cpu
        
        logger.info(f"🚀 Initializing CodeRankEmbed Embedder")
        logger.info(f"  Model: {self.model_config.hf_model_id}")
        logger.info(f"  Dimension: {self.model_config.vector_dim}")
        logger.info(f"  Device: {'GPU' if self.use_gpu else 'CPU'}")
        logger.info(f"  Batch size per GPU: {self.batch_size}")
        logger.info(f"  Data parallel: {self.use_data_parallel}")
        if self.use_data_parallel:
            logger.info(f"  Total batch size: {self.batch_size * 2}")
        
        # Load model(s)
        if self.use_data_parallel:
            logger.info(f"\\n🚀 Loading models with DATA PARALLELISM (2 GPUs)")
            logger.info(f"   GPU 0: Process even batches")
            logger.info(f"   GPU 1: Process odd batches")
            
            self.model_gpu0 = SentenceTransformer(
                self.model_config.hf_model_id,
                trust_remote_code=self.model_config.trust_remote_code,
                device='cuda:0'
            )
            self.model_gpu0.eval()
            
            self.model_gpu1 = SentenceTransformer(
                self.model_config.hf_model_id,
                trust_remote_code=self.model_config.trust_remote_code,
                device='cuda:1'
            )
            self.model_gpu1.eval()
            
            logger.info(f"✓ Models loaded on 2 GPUs")
        else:
            logger.info(f"\\n🚀 Loading single model")
            
            self.model = SentenceTransformer(
                self.model_config.hf_model_id,
                trust_remote_code=self.model_config.trust_remote_code
            )
            
            if self.use_gpu:
                self.model = self.model.to('cuda')
                logger.info(f"✓ Model loaded on GPU")
            else:
                logger.info(f"✓ Model loaded on CPU (slow)")
        
        # Verify dimension
        if self.use_data_parallel:
            actual_dim = self.model_gpu0.get_sentence_embedding_dimension()
        else:
            actual_dim = self.model.get_sentence_embedding_dimension()
        
        assert actual_dim == self.model_config.vector_dim, (
            f"Dimension mismatch: expected {self.model_config.vector_dim}, got {actual_dim}"
        )
        
        logger.info(f"✓ Verified dimension: {actual_dim}\\n")
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """
        Embed a batch of texts.
        
        Args:
            texts: List of texts to embed (documents, not queries)
        
        Returns:
            Numpy array of embeddings
        """
        if self.use_data_parallel:
            # Split batch across 2 GPUs
            mid = len(texts) // 2
            texts_gpu0 = texts[:mid]
            texts_gpu1 = texts[mid:]
            
            # TRUE PARALLELISM: Run both GPUs simultaneously using threads
            def encode_gpu0():
                with torch.no_grad():
                    return self.model_gpu0.encode(
                        texts_gpu0,
                        batch_size=len(texts_gpu0),
                        show_progress_bar=False,
                        convert_to_numpy=True,
                        normalize_embeddings=True
                    )
            
            def encode_gpu1():
                with torch.no_grad():
                    return self.model_gpu1.encode(
                        texts_gpu1,
                        batch_size=len(texts_gpu1),
                        show_progress_bar=False,
                        convert_to_numpy=True,
                        normalize_embeddings=True
                    )
            
            # Execute both GPUs in parallel
            with ThreadPoolExecutor(max_workers=2) as executor:
                future0 = executor.submit(encode_gpu0)
                future1 = executor.submit(encode_gpu1)
                emb0 = future0.result()
                emb1 = future1.result()
            
            return np.vstack([emb0, emb1])
        else:
            with torch.no_grad():
                embeddings = self.model.encode(
                    texts,
                    batch_size=self.batch_size,
                    show_progress_bar=False,
                    convert_to_numpy=True,
                    normalize_embeddings=True
                )
            
            return embeddings
    
    def load_chunks(self) -> List[Dict[str, Any]]:
        """
        Load pre-chunked JSON files.
        
        Returns:
            List of chunk dictionaries
        """
        logger.info(f"📂 Loading pre-chunked JSON from: {self.config.input_path}")
        
        all_chunks: List[Dict[str, Any]] = []
        search_roots: List[Path] = [self.config.input_path]

        # Allow automatic fallback to additional Kaggle runtime locations so
        # Template 2 remains standalone regardless of where the chunk artifacts
        # were produced (dataset, /kaggle/output, or repo workspace).
        input_str = str(self.config.input_path)
        if input_str.startswith("/kaggle/input/"):
            suffix = input_str[len("/kaggle/input/"):]
            output_candidate = Path("/kaggle/output") / suffix
            working_candidate = Path("/kaggle/working") / suffix
            # Avoid duplicates if the candidates already exist in search_roots
            for candidate in (output_candidate, working_candidate):
                if candidate not in search_roots:
                    search_roots.append(candidate)

        # When running in a Kaggle notebook that cloned the repository, the
        # chunk outputs often reside under /kaggle/working/rad_clean/output/*.
        repo_root = Path(__file__).resolve().parents[2]
        repo_output_root = repo_root / "output"
        if repo_output_root not in search_roots:
            search_roots.append(repo_output_root)

        # Add collection-specific folder heuristics (hyphen vs underscore)
        collection_slug_variants = {
            self.config.collection_name,
            self.config.collection_name.replace('-', '_'),
            self.config.collection_name.replace('_', '-'),
        }
        for variant in collection_slug_variants:
            for suffix in ("", "_chunked"):
                candidate = repo_output_root / f"{variant}{suffix}"
                if candidate not in search_roots:
                    search_roots.append(candidate)

        chunk_files: List[Path] = []
        search_patterns = [
            "**/*_chunks.json",
            "**/*_chunks.jsonl",
            "**/*chunks.json",
            "**/*chunks.jsonl",
            "**/*chunked.json",
            "**/*chunked.jsonl",
        ]

        for root in search_roots:
            if not root.exists():
                continue

            for pattern in search_patterns:
                matches = sorted(p for p in root.glob(pattern) if p.is_file())
                if matches:
                    logger.info(
                        "  ✓ Found %s chunk file(s) under %s using pattern '%s'",
                        len(matches),
                        root,
                        pattern,
                    )
                    chunk_files = matches
                    break

            if chunk_files:
                break

        if not chunk_files:
            searched_locations = " | ".join(str(path) for path in search_roots)
            raise FileNotFoundError(
                "No *_chunks.json files found.\n"
                f"Searched locations: {searched_locations}\n"
                "Ensure Template 1 output is available (upload dataset or copy files)."
            )
        logger.info(f"  Found {len(chunk_files)} chunk files")
        
        for chunk_file in chunk_files:
            try:
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                
                if chunks:
                    all_chunks.extend(chunks)
                    logger.info(f"  ✓ {chunk_file.name}: {len(chunks)} chunks")
            
            except Exception as e:
                logger.error(f"  ✗ Error loading {chunk_file.name}: {e}")
        
        logger.info(f"✓ Loaded {len(all_chunks)} chunks total\\n")
        
        return all_chunks
    
    def embed_all(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Embed all chunks with progress tracking.
        
        Args:
            chunks: List of chunk dictionaries
        
        Returns:
            List of chunk dictionaries with embeddings
        """
        logger.info(f"🔄 Embedding {len(chunks)} chunks in batches of {self.batch_size}")
        
        embeddings_data = []
        start_time = datetime.now()
        
        for i in tqdm(range(0, len(chunks), self.batch_size), desc="Embedding", unit="batch"):
            batch = chunks[i:i + self.batch_size]
            texts = [chunk.get('content', '') for chunk in batch]
            
            # Generate embeddings
            embeddings = self.embed_batch(texts)
            
            # Attach embeddings
            for chunk, embedding in zip(batch, embeddings):
                # Generate unique ID
                chunk_id = chunk.get('chunk_id', f"chunk_{i}")
                unique_id = hashlib.sha256(chunk_id.encode()).hexdigest()[:16]
                
                # Enrich metadata
                metadata = chunk.get('metadata', {})
                metadata.update({
                    'embedding_model': f"{self.model_config.name}-{self.model_config.vector_dim}",
                    'embedding_model_version': self.model_config.hf_model_id,
                    'vector_dimension': self.model_config.vector_dim,
                    'collection': self.config.collection_name
                })
                
                # Create embedding record
                record = {
                    'id': unique_id,
                    'text': chunk.get('content', ''),
                    'embedding': embedding.tolist(),
                    'metadata': metadata
                }
                
                embeddings_data.append(record)
            
            # Memory cleanup every 5 batches
            if self.use_gpu and i % (self.batch_size * 5) == 0:
                torch.cuda.empty_cache()
            
            # Progress reporting
            if (i // self.batch_size) % 10 == 0:
                elapsed = (datetime.now() - start_time).total_seconds()
                processed = min(i + self.batch_size, len(chunks))
                rate = processed / elapsed if elapsed > 0 else 0
                eta = (len(chunks) - processed) / rate if rate > 0 else 0
                logger.info(
                    f"  Progress: {processed}/{len(chunks)} "
                    f"({processed/len(chunks)*100:.1f}%) - "
                    f"{rate:.1f} chunks/sec - ETA: {eta/60:.1f} min"
                )
        
        logger.info(f"✓ Embedded {len(embeddings_data)} chunks\\n")
        
        return embeddings_data
    
    def save_jsonl(self, embeddings: List[Dict[str, Any]]):
        """
        Save embeddings to a newline-delimited JSON file (JSONL).
        
        Args:
            embeddings: List of embedding records
        """
        logger.info(f"💾 Saving embeddings to: {self.config.output_path}")

        self.config.output_path.parent.mkdir(parents=True, exist_ok=True)

        lines_written = 0
        with open(self.config.output_path, 'w', encoding='utf-8') as f:
            for record in embeddings:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
                lines_written += 1

        # Validate that the file is newline-delimited JSON for Kaggle downloads
        if lines_written:
            self._validate_jsonl_file(lines_written)

        logger.info(f"✓ Saved {lines_written} embeddings\\n")

    def _validate_jsonl_file(self, expected_lines: int):
        """Ensure the persisted file is valid JSONL (one JSON object per line)."""
        actual_lines = 0
        try:
            with open(self.config.output_path, 'r', encoding='utf-8') as f:
                for actual_lines, line in enumerate(f, start=1):
                    if not line.strip():
                        continue
                    json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Output file is not valid JSONL; failed to parse line as JSON."
            ) from exc

        if expected_lines != actual_lines:
            logger.warning(
                "⚠️  JSONL validation mismatch: expected %s lines, found %s.",
                expected_lines,
                actual_lines
            )
    
    def run(self):
        """Run the embedding pipeline."""
        start_time = datetime.now()
        
        # Load chunks
        chunks = self.load_chunks()
        
        # Embed chunks
        embeddings = self.embed_all(chunks)
        
        # Save to JSONL
        self.save_jsonl(embeddings)
        
        # Summary
        end_time = datetime.now()
        elapsed = (end_time - start_time).total_seconds()
        
        logger.info(f"{'='*60}")
        logger.info(f"✓ EMBEDDING COMPLETED")
        logger.info(f"{'='*60}")
        logger.info(f"Collection: {self.config.collection_name}")
        logger.info(f"Model: {self.model_config.hf_model_id}")
        logger.info(f"Total chunks: {len(embeddings)}")
        logger.info(f"Vector dimension: {self.model_config.vector_dim}")
        logger.info(f"Total time: {elapsed/60:.1f} minutes")
        logger.info(f"Average speed: {len(embeddings)/elapsed:.1f} chunks/sec")
        logger.info(f"Output file: {self.config.output_path}")
        logger.info(f"File size: {self.config.output_path.stat().st_size / 1e6:.1f} MB")
        logger.info(f"{'='*60}\\n")
        
        logger.info(f"📦 NEXT STEPS:")
        logger.info(f"1. Download {self.config.output_path.name} from Kaggle /working/")
        logger.info(f"2. Run Template 3 (qdrant_uploader_template.py) locally:")
        logger.info(f"   python -m src.templates.qdrant_uploader_template \\\\")
        logger.info(f"       --file {self.config.output_path.name} \\\\")
        logger.info(f"       --collection {self.config.collection_name}")


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Universal Embedder (Template 2 of 3 - Kaggle GPU)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Required arguments
    parser.add_argument(
        '--collection',
        required=True,
        help="Collection name (must match Template 1)"
    )
    parser.add_argument(
        '--input',
        required=True,
        type=Path,
        help="Input directory with *_chunks.json files (from Template 1)"
    )
    parser.add_argument(
        '--output',
        required=True,
        type=Path,
        help="Output JSONL file path"
    )
    
    # Optional arguments
    parser.add_argument(
        '--no-gpu',
        action='store_true',
        help="Force CPU mode (not recommended, CodeRankEmbed needs GPU)"
    )
    parser.add_argument(
        '--no-data-parallel',
        action='store_true',
        help="Disable data parallelism (use single Tesla T4 instead of both)"
    )
    
    args = parser.parse_args()
    
    # Create config
    config = EmbedderConfig(
        collection_name=args.collection,
        input_path=args.input,
        output_path=args.output,
        use_gpu=not args.no_gpu,
        use_data_parallel=not args.no_data_parallel
    )
    
    # Run embedder
    try:
        logger.info(f"{'='*60}")
        logger.info(f"TEMPLATE 2: CodeRankEmbed Embedder (Tesla T4 x2)")
        logger.info(f"{'='*60}\n")
        
        embedder = UniversalEmbedder(config)
        embedder.run()
    
    except KeyboardInterrupt:
        logger.info("\\n⚠️  Embedding interrupted by user")
        exit(1)
    except Exception as e:
        logger.error(f"\\n❌ Embedding failed: {e}", exc_info=True)
        exit(1)


if __name__ == "__main__":
    main()
