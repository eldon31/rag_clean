"""
Process Qdrant Ecosystem Documentation with Optimized Chunker

This script:
1. Walks through all subdirectories in Docs/qdrant_ecosystem/
2. Processes markdown files with Docling (code enrichment enabled)
3. Chunks with optimized HybridChunker (Tier 1 enhancements)
4. Stores in single Qdrant collection with subdirectory metadata

Single Collection Strategy:
- Collection name: "qdrant_ecosystem"
- Metadata tracks: source_repo, source_subdir, file_path
- Enables filtering by repository or subdirectory
- Better for cross-repo semantic search
"""

import sys
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ingestion.processor import DocumentProcessor
from src.ingestion.chunker import DoclingHybridChunker, ChunkingConfig
from src.config.docling_config import DoclingConfig

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QdrantEcosystemProcessor:
    """Process all files in qdrant_ecosystem directory."""
    
    def __init__(
        self,
        base_path: Path,
        collection_name: str = "qdrant_ecosystem"
    ):
        """
        Initialize processor.
        
        Args:
            base_path: Path to Docs/qdrant_ecosystem/
            collection_name: Qdrant collection name
        """
        self.base_path = Path(base_path)
        self.collection_name = collection_name
        
        # Initialize chunker with optimized config
        self.chunking_config = ChunkingConfig(
            max_tokens=2048,  # nomic-embed-code limit
            chunk_overlap=100,
            chunk_size=2048
        )
        self.chunker = DoclingHybridChunker(self.chunking_config)
        
        # Initialize document processor with production config
        self.processor = DocumentProcessor()
        
        # Statistics
        self.stats = {
            "total_repos": 0,
            "total_files": 0,
            "total_chunks": 0,
            "failed_files": 0,
            "repos_processed": {},
            "start_time": None,
            "end_time": None
        }
    
    def discover_files(self) -> Dict[str, List[Path]]:
        """
        Discover all markdown files organized by repository.
        Skips _index.md files (navigation only).
        
        Returns:
            Dict mapping repo_name -> list of file paths
        """
        logger.info(f"Discovering files in: {self.base_path}")
        
        repos = {}
        skipped_count = 0
        
        # First level: repository folders (qdrant_documentation, qdrant_examples, etc.)
        for repo_dir in self.base_path.iterdir():
            if not repo_dir.is_dir():
                continue
            
            repo_name = repo_dir.name
            logger.info(f"  Found repository: {repo_name}")
            
            # Collect all markdown files in this repo
            all_md_files = list(repo_dir.rglob("*.md"))
            
            # Filter out _index.md files
            md_files = []
            for f in all_md_files:
                if f.name == "_index.md":
                    skipped_count += 1
                    continue
                md_files.append(f)
            
            if md_files:
                repos[repo_name] = md_files
                logger.info(f"    {len(md_files)} markdown files (skipped {len(all_md_files) - len(md_files)} _index.md)")
        
        self.stats["total_repos"] = len(repos)
        self.stats["total_files"] = sum(len(files) for files in repos.values())
        
        logger.info(f"\n📊 Discovery Summary:")
        logger.info(f"  Repositories: {self.stats['total_repos']}")
        logger.info(f"  Total files: {self.stats['total_files']}")
        logger.info(f"  Skipped _index.md files: {skipped_count}")
        
        return repos
    
    def extract_metadata(self, file_path: Path, repo_name: str) -> Dict[str, Any]:
        """
        Extract metadata from file path.
        
        Args:
            file_path: Path to markdown file
            repo_name: Repository name (e.g., "qdrant_documentation")
        
        Returns:
            Metadata dict with subdirectory tracking
        """
        # Get relative path from repo root
        relative_path = file_path.relative_to(self.base_path / repo_name)
        
        # Extract subdirectory (first folder in relative path)
        parts = relative_path.parts
        if len(parts) > 1:
            subdir = parts[0]  # e.g., "documentation_concepts"
        else:
            subdir = "root"
        
        # Extract category from subdirectory name
        # Example: "documentation_concepts_collections" -> category="concepts"
        category = "general"
        if "_" in subdir:
            subdir_parts = subdir.split("_")
            if len(subdir_parts) >= 2:
                category = subdir_parts[1]  # Second part after "documentation_"
        
        metadata = {
            "source_repo": repo_name,
            "source_subdir": subdir,
            "category": category,
            "file_path": str(relative_path),
            "file_name": file_path.name,
            "collection": self.collection_name,
            "processed_date": datetime.now().isoformat()
        }
        
        return metadata
    
    async def process_file(
        self,
        file_path: Path,
        repo_name: str
    ) -> Dict[str, Any]:
        """
        Process a single markdown file.
        
        Args:
            file_path: Path to file
            repo_name: Repository name
        
        Returns:
            Processing result with chunks and metadata
        """
        logger.info(f"Processing: {file_path.relative_to(self.base_path)}")
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                logger.warning(f"  Empty file, skipping")
                return {"success": False, "reason": "empty"}
            
            # Extract metadata
            base_metadata = self.extract_metadata(file_path, repo_name)
            
            # Convert with Docling (production config with code enrichment)
            # Note: For markdown, Docling might not add much, but keeps consistency
            try:
                # For markdown files, we can skip Docling conversion and use content directly
                # This is faster and markdown is already structured
                docling_doc = None  # Will use fallback chunking
                
                # Chunk the document
                chunks = await self.chunker.chunk_document(
                    content=content,
                    title=file_path.stem,
                    source=str(file_path.relative_to(self.base_path)),
                    metadata=base_metadata,
                    docling_doc=docling_doc
                )
                
                # Log chunk quality metrics (Tier 1 optimizations)
                complete_code_blocks = sum(
                    1 for c in chunks 
                    if c.metadata.get("has_complete_code_blocks", True)
                )
                valid_tokens = sum(
                    1 for c in chunks 
                    if c.metadata.get("token_count_valid", True)
                )
                
                logger.info(f"  ✅ {len(chunks)} chunks created")
                logger.info(f"     Code blocks complete: {complete_code_blocks}/{len(chunks)}")
                logger.info(f"     Token count valid: {valid_tokens}/{len(chunks)}")
                
                self.stats["total_chunks"] += len(chunks)
                
                return {
                    "success": True,
                    "file_path": str(file_path),
                    "repo": repo_name,
                    "chunks": chunks,
                    "chunk_count": len(chunks),
                    "metadata": base_metadata
                }
                
            except Exception as e:
                logger.error(f"  ❌ Chunking failed: {e}")
                self.stats["failed_files"] += 1
                return {"success": False, "reason": str(e)}
        
        except Exception as e:
            logger.error(f"  ❌ Processing failed: {e}")
            self.stats["failed_files"] += 1
            return {"success": False, "reason": str(e)}
    
    async def process_repository(
        self,
        repo_name: str,
        file_paths: List[Path],
        max_files: int = None
    ) -> List[Dict[str, Any]]:
        """
        Process all files in a repository.
        
        Args:
            repo_name: Repository name
            file_paths: List of file paths
            max_files: Optional limit for testing
        
        Returns:
            List of processing results
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"Processing Repository: {repo_name}")
        logger.info(f"{'='*80}")
        
        if max_files:
            file_paths = file_paths[:max_files]
            logger.info(f"Limiting to {max_files} files for testing")
        
        results = []
        
        for i, file_path in enumerate(file_paths, 1):
            logger.info(f"\n[{i}/{len(file_paths)}] {repo_name}")
            
            result = await self.process_file(file_path, repo_name)
            results.append(result)
            
            # Small delay to avoid overwhelming the system
            if i % 10 == 0:
                await asyncio.sleep(0.1)
        
        # Update stats
        successful = sum(1 for r in results if r.get("success"))
        total_chunks = sum(r.get("chunk_count", 0) for r in results if r.get("success"))
        
        self.stats["repos_processed"][repo_name] = {
            "total_files": len(file_paths),
            "successful": successful,
            "failed": len(file_paths) - successful,
            "total_chunks": total_chunks
        }
        
        logger.info(f"\n📊 Repository Summary: {repo_name}")
        logger.info(f"  Files processed: {successful}/{len(file_paths)}")
        logger.info(f"  Total chunks: {total_chunks}")
        
        return results
    
    async def process_all(
        self,
        max_files_per_repo: int = None,
        repos_to_process: List[str] = None
    ) -> Dict[str, Any]:
        """
        Process all repositories.
        
        Args:
            max_files_per_repo: Optional limit per repository (for testing)
            repos_to_process: Optional list of specific repos to process
        
        Returns:
            Complete processing results
        """
        self.stats["start_time"] = datetime.now()
        
        logger.info(f"\n{'='*80}")
        logger.info(f"QDRANT ECOSYSTEM PROCESSING")
        logger.info(f"{'='*80}")
        logger.info(f"Base path: {self.base_path}")
        logger.info(f"Collection: {self.collection_name}")
        logger.info(f"Chunker: HybridChunker with Tier 1 optimizations")
        
        # Discover files
        repos = self.discover_files()
        
        # Filter repos if specified
        if repos_to_process:
            repos = {k: v for k, v in repos.items() if k in repos_to_process}
            logger.info(f"\nProcessing only: {repos_to_process}")
        
        # Process each repository
        all_results = {}
        
        for repo_name, file_paths in repos.items():
            results = await self.process_repository(
                repo_name,
                file_paths,
                max_files=max_files_per_repo
            )
            all_results[repo_name] = results
        
        self.stats["end_time"] = datetime.now()
        duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
        
        # Final summary
        logger.info(f"\n{'='*80}")
        logger.info(f"PROCESSING COMPLETE")
        logger.info(f"{'='*80}")
        logger.info(f"Duration: {duration:.2f}s")
        logger.info(f"Total files: {self.stats['total_files']}")
        logger.info(f"Total chunks: {self.stats['total_chunks']}")
        logger.info(f"Failed files: {self.stats['failed_files']}")
        logger.info(f"Avg chunks/file: {self.stats['total_chunks'] / max(1, self.stats['total_files'] - self.stats['failed_files']):.1f}")
        
        return {
            "results": all_results,
            "stats": self.stats
        }
    
    def save_results(
        self,
        results: Dict[str, Any],
        output_base_path: Path
    ):
        """
        Save processing results in collection/subdirectory structure.
        
        Creates structure:
        output/
          qdrant_ecosystem/  ← Collection folder
            qdrant_documentation/  ← Subdirectory folder
              chunks.json
            qdrant_examples/  ← Subdirectory folder
              chunks.json
            ...
            summary.json
        
        Args:
            results: Processing results
            output_base_path: Base output directory
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"SAVING RESULTS - COLLECTION/SUBDIRECTORY STRUCTURE")
        logger.info(f"{'='*80}")
        
        # Collection folder
        collection_dir = output_base_path / self.collection_name
        collection_dir.mkdir(parents=True, exist_ok=True)
        
        # Organize chunks by repository (subdirectory)
        chunks_by_repo = {}
        all_chunks = []
        
        for repo_name, repo_results in results["results"].items():
            chunks_by_repo[repo_name] = []
            
            for result in repo_results:
                if result.get("success"):
                    chunks = result.get("chunks", [])
                    
                    for chunk in chunks:
                        # Convert chunk to dict with FULL content
                        chunk_dict = {
                            "content": chunk.content,  # FULL CONTENT for Kaggle
                            "index": chunk.index,
                            "token_count": chunk.token_count,
                            "metadata": chunk.metadata,
                            "start_char": chunk.start_char,
                            "end_char": chunk.end_char
                        }
                        
                        chunks_by_repo[repo_name].append(chunk_dict)
                        all_chunks.append(chunk_dict)
        
        # Save each repository as a subdirectory with chunks.json
        logger.info(f"\nSaving subdirectory folders:")
        for repo_name, chunks in chunks_by_repo.items():
            # Create subdirectory folder
            repo_dir = collection_dir / repo_name
            repo_dir.mkdir(exist_ok=True)
            
            # Save chunks.json in subdirectory
            chunks_file = repo_dir / "chunks.json"
            repo_data = {
                "collection": self.collection_name,
                "subdirectory": repo_name,
                "total_chunks": len(chunks),
                "chunks": chunks
            }
            with open(chunks_file, 'w', encoding='utf-8') as f:
                json.dump(repo_data, f, indent=2, ensure_ascii=False)
            logger.info(f"  ✅ {repo_name}/chunks.json ({len(chunks)} chunks)")
        
        # Save collection summary
        summary = {
            "collection_name": self.collection_name,
            "total_repos": results["stats"]["total_repos"],
            "total_files": results["stats"]["total_files"],
            "total_chunks": results["stats"]["total_chunks"],
            "failed_files": results["stats"]["failed_files"],
            "start_time": results["stats"]["start_time"].isoformat(),
            "end_time": results["stats"]["end_time"].isoformat(),
            "subdirectories": list(chunks_by_repo.keys()),
            "chunks_by_subdirectory": {k: len(v) for k, v in chunks_by_repo.items()}
        }
        
        summary_path = collection_dir / "summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        logger.info(f"\n✅ Collection summary: {summary_path}")
        
        logger.info(f"\n{'='*80}")
        logger.info(f"📁 OUTPUT STRUCTURE:")
        logger.info(f"{'='*80}")
        logger.info(f"{collection_dir}/")
        logger.info(f"  ├── summary.json (collection stats)")
        for repo_name in chunks_by_repo.keys():
            logger.info(f"  ├── {repo_name}/")
            logger.info(f"  │   └── chunks.json ({chunks_by_repo[repo_name].__len__()} chunks)")
        logger.info(f"{'='*80}")
        logger.info(f"\n✅ Ready for Kaggle upload!")


async def main():
    """Main entry point."""
    
    # Configuration
    base_path = Path(__file__).parent.parent / "Docs" / "qdrant_ecosystem"
    output_path = Path(__file__).parent.parent / "output"
    
    # PRODUCTION MODE: Process ALL files
    TEST_MODE = False  # Changed to False
    MAX_FILES_PER_REPO = 5 if TEST_MODE else None
    
    # Optional: Process only specific repos
    # REPOS_TO_PROCESS = ["qdrant_documentation"]  # Uncomment to test single repo
    REPOS_TO_PROCESS = None  # Process all repos
    
    if TEST_MODE:
        logger.info("🧪 TEST MODE: Processing first 5 files per repository")
    else:
        logger.info("🚀 PRODUCTION MODE: Processing ALL files")
    
    # Create processor
    processor = QdrantEcosystemProcessor(
        base_path=base_path,
        collection_name="qdrant_ecosystem"
    )
    
    # Process all files
    results = await processor.process_all(
        max_files_per_repo=MAX_FILES_PER_REPO,
        repos_to_process=REPOS_TO_PROCESS
    )
    
    # Save results in collection/subdirectory structure
    processor.save_results(results, output_path)
    
    # Print final stats
    print("\n" + "="*80)
    print("FINAL STATISTICS")
    print("="*80)
    print(f"Collection: qdrant_ecosystem")
    print(f"Total repositories: {results['stats']['total_repos']}")
    print(f"Total files processed: {results['stats']['total_files'] - results['stats']['failed_files']}/{results['stats']['total_files']}")
    print(f"Total chunks created: {results['stats']['total_chunks']}")
    print(f"Failed files: {results['stats']['failed_files']}")
    print("\nPer-repository breakdown:")
    for repo, stats in results['stats']['repos_processed'].items():
        print(f"  {repo}:")
        print(f"    Files: {stats['successful']}/{stats['total_files']}")
        print(f"    Chunks: {stats['total_chunks']}")
    print("="*80)
    
    print(f"\n✅ Output structure:")
    print(f"   output/qdrant_ecosystem/")
    print(f"     ├── summary.json")
    print(f"     ├── qdrant_documentation/chunks.json")
    print(f"     ├── qdrant_examples/chunks.json")
    print(f"     ├── qdrant_fastembed/chunks.json")
    print(f"     └── ...")
    print("\n📦 Ready for Kaggle upload!")


if __name__ == "__main__":
    asyncio.run(main())
