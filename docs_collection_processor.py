#!/usr/bin/env python3
"""
Docs Collection Processor for Ultimate Chunker System
Processes the Docs directory with collection-based structure

Structure Logic:
- Head folder = Collection name (e.g., Docling, Qdrant, Sentence_Transformers)
- 1 level of subfolders allowed
- All files processed with collection context
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

from production_ultimate_chunker import ProductionUltimateChunker

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocsCollectionProcessor:
    """Specialized processor for Docs directory with collection-based structure"""
    
    def __init__(self):
        """Initialize the docs collection processor"""
        self.chunker = ProductionUltimateChunker()
        
        # Collection-specific strategy mappings
        self.collection_strategies = {
            "Docling": "hybrid_adaptive",  # Document processing library
            "FAST_DOCS": "api_documentation", 
            "pydantic_pydantic": "programming_language_documentation",
            "Qdrant": "platform_documentation",  # Vector database platform
            "Sentence_Transformers": "programming_language_documentation"
        }
        
        # File extensions to process
        self.supported_extensions = ['.md', '.txt', '.rst', '.py', '.js', '.ts', '.json', '.yml', '.yaml']
        
        logger.info("🗂️ Docs Collection Processor initialized")
    
    def discover_collections(self, docs_path: str) -> Dict[str, Dict[str, Any]]:
        """
        Discover all collections and their structure
        
        Returns:
            Dict mapping collection names to their structure info
        """
        
        docs_dir = Path(docs_path)
        collections = {}
        
        if not docs_dir.exists():
            logger.error(f"❌ Docs directory not found: {docs_path}")
            return collections
        
        # Scan head folders (collections)
        for collection_dir in docs_dir.iterdir():
            if collection_dir.is_dir():
                collection_name = collection_dir.name
                
                collection_info = {
                    "name": collection_name,
                    "path": str(collection_dir),
                    "strategy": self.collection_strategies.get(collection_name, "hierarchical_balanced"),
                    "subfolders": [],
                    "direct_files": [],
                    "total_files": 0
                }
                
                # Scan for subfolders and direct files
                for item in collection_dir.iterdir():
                    if item.is_dir():
                        # Subfolder
                        subfolder_files = self._count_files_in_directory(item)
                        collection_info["subfolders"].append({
                            "name": item.name,
                            "path": str(item),
                            "file_count": subfolder_files
                        })
                        collection_info["total_files"] += subfolder_files
                    elif item.is_file() and item.suffix in self.supported_extensions:
                        # Direct file
                        collection_info["direct_files"].append({
                            "name": item.name,
                            "path": str(item),
                            "size": item.stat().st_size
                        })
                        collection_info["total_files"] += 1
                
                collections[collection_name] = collection_info
                logger.info(f"📁 Collection '{collection_name}': {collection_info['total_files']} files")
        
        return collections
    
    def _count_files_in_directory(self, directory: Path) -> int:
        """Count supported files in a directory"""
        count = 0
        for file_path in directory.rglob("*"):
            if file_path.is_file() and file_path.suffix in self.supported_extensions:
                count += 1
        return count
    
    def process_collection(
        self, 
        collection_info: Dict[str, Any], 
        output_dir: str
    ) -> Dict[str, Any]:
        """
        Process a single collection (head folder)
        
        Args:
            collection_info: Collection metadata from discover_collections
            output_dir: Base output directory
            
        Returns:
            Processing results for the collection
        """
        
        collection_name = collection_info["name"]
        collection_path = Path(collection_info["path"])
        strategy = collection_info["strategy"]
        
        logger.info(f"🔄 Processing collection: {collection_name} with {strategy} strategy")
        
        # Create collection-specific output directory
        collection_output_dir = Path(output_dir) / collection_name
        collection_output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {
            "collection_name": collection_name,
            "strategy": strategy,
            "start_time": datetime.now().isoformat(),
            "files_processed": 0,
            "files_failed": 0,
            "total_chunks": 0,
            "total_tokens": 0,
            "subfolders_processed": 0,
            "direct_files_processed": 0,
            "files": []
        }
        
        # Process direct files in collection root
        for file_info in collection_info["direct_files"]:
            file_result = self._process_file_with_collection_context(
                file_info["path"],
                collection_name,
                strategy,
                str(collection_output_dir)
            )
            
            if file_result["success"]:
                results["files_processed"] += 1
                results["direct_files_processed"] += 1
                results["total_chunks"] += file_result["chunks_created"]
                results["total_tokens"] += file_result["total_tokens"]
                results["files"].append(file_result)
                logger.info(f"✅ {Path(file_info['path']).name}: {file_result['chunks_created']} chunks")
            else:
                results["files_failed"] += 1
                logger.error(f"❌ Failed: {Path(file_info['path']).name}")
        
        # Process subfolders
        for subfolder_info in collection_info["subfolders"]:
            subfolder_path = Path(subfolder_info["path"])
            subfolder_result = self._process_subfolder(
                subfolder_path,
                collection_name,
                strategy,
                str(collection_output_dir)
            )
            
            results["files_processed"] += subfolder_result["files_processed"]
            results["files_failed"] += subfolder_result["files_failed"]
            results["total_chunks"] += subfolder_result["total_chunks"]
            results["total_tokens"] += subfolder_result["total_tokens"]
            results["subfolders_processed"] += 1
            results["files"].extend(subfolder_result["files"])
            
            logger.info(f"📂 Subfolder '{subfolder_info['name']}': {subfolder_result['files_processed']} files processed")
        
        # Save collection results
        results["end_time"] = datetime.now().isoformat()
        start_time = datetime.fromisoformat(results["start_time"])
        end_time = datetime.fromisoformat(results["end_time"])
        results["processing_time_seconds"] = (end_time - start_time).total_seconds()
        
        # Save collection summary
        collection_summary_file = collection_output_dir / f"{collection_name}_processing_summary.json"
        with open(collection_summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Collection '{collection_name}' summary saved to {collection_summary_file}")
        
        return results
    
    def _process_subfolder(
        self, 
        subfolder_path: Path, 
        collection_name: str, 
        strategy: str,
        output_dir: str
    ) -> Dict[str, Any]:
        """Process all files in a subfolder"""
        
        results = {
            "subfolder_name": subfolder_path.name,
            "files_processed": 0,
            "files_failed": 0,
            "total_chunks": 0,
            "total_tokens": 0,
            "files": []
        }
        
        # Find all supported files in subfolder
        for file_path in subfolder_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in self.supported_extensions:
                file_result = self._process_file_with_collection_context(
                    str(file_path),
                    collection_name,
                    strategy,
                    output_dir,
                    subfolder_name=subfolder_path.name
                )
                
                if file_result["success"]:
                    results["files_processed"] += 1
                    results["total_chunks"] += file_result["chunks_created"]
                    results["total_tokens"] += file_result["total_tokens"]
                    results["files"].append(file_result)
                else:
                    results["files_failed"] += 1
        
        return results
    
    def _process_file_with_collection_context(
        self,
        file_path: str,
        collection_name: str,
        strategy: str,
        output_dir: str,
        subfolder_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a file with collection context and metadata
        """
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 100:
                return {"success": False, "error": "File too small"}
            
            # Create enhanced chunks with collection context
            chunks = self._create_collection_chunks(
                content, file_path, collection_name, strategy, subfolder_name
            )
            
            if not chunks:
                return {"success": False, "error": "No chunks created"}
            
            # Save chunks with collection structure
            self._save_collection_chunks(chunks, file_path, output_dir, collection_name, subfolder_name)
            
            # Calculate statistics
            total_tokens = sum(chunk['metadata']['token_count'] for chunk in chunks)
            avg_length = sum(len(chunk['text']) for chunk in chunks) / len(chunks)
            
            return {
                "success": True,
                "file_path": file_path,
                "collection_name": collection_name,
                "subfolder_name": subfolder_name,
                "strategy": strategy,
                "chunks_created": len(chunks),
                "total_tokens": total_tokens,
                "average_chunk_length": int(avg_length)
            }
            
        except Exception as e:
            logger.error(f"❌ Error processing {file_path}: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_collection_chunks(
        self,
        content: str,
        file_path: str,
        collection_name: str,
        strategy: str,
        subfolder_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Create chunks with collection-specific metadata"""
        
        # Use the production chunker's simple chunking approach
        chunks = self.chunker._create_simple_chunks(
            content, file_path, collection_name.lower(), strategy
        )
        
        # Enhance metadata with collection context
        for i, chunk in enumerate(chunks):
            chunk["metadata"].update({
                "collection_name": collection_name,
                "subfolder_name": subfolder_name,
                "collection_strategy": strategy,
                "chunk_index_in_file": i,
                "file_relative_path": str(Path(file_path).relative_to(Path(file_path).parents[2])),  # Relative to Docs
                "collection_context": f"{collection_name}/{subfolder_name}" if subfolder_name else collection_name
            })
        
        return chunks
    
    def _save_collection_chunks(
        self,
        chunks: List[Dict[str, Any]],
        file_path: str,
        output_dir: str,
        collection_name: str,
        subfolder_name: Optional[str] = None
    ):
        """Save chunks with collection-aware naming"""
        
        file_stem = Path(file_path).stem
        
        # Create hierarchical output structure
        if subfolder_name:
            chunk_output_dir = Path(output_dir) / subfolder_name
            chunk_output_dir.mkdir(exist_ok=True)
            output_file = chunk_output_dir / f"{file_stem}_chunks.json"
        else:
            output_file = Path(output_dir) / f"{file_stem}_chunks.json"
        
        # Save chunks
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
    
    def process_all_docs(
        self,
        docs_path: str = r"C:\Users\raze0\Documents\LLM_KNOWLEDGE_CREATOR\RAG\RAG_CLEAN\Docs",
        output_dir: str = r"C:\Users\raze0\Documents\LLM_KNOWLEDGE_CREATOR\RAG\RAG_CLEAN\DOCS_CHUNKS_OUTPUT"
    ) -> Dict[str, Any]:
        """
        Process all collections in the Docs directory
        
        Args:
            docs_path: Path to the Docs directory
            output_dir: Base output directory for chunks
            
        Returns:
            Complete processing results
        """
        
        logger.info(f"🚀 Starting Docs Collection Processing")
        logger.info(f"📂 Source: {docs_path}")
        logger.info(f"📁 Output: {output_dir}")
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Discover all collections
        collections = self.discover_collections(docs_path)
        
        if not collections:
            logger.error("❌ No collections found!")
            return {"success": False, "error": "No collections found"}
        
        logger.info(f"🔍 Found {len(collections)} collections: {list(collections.keys())}")
        
        # Overall results
        overall_results = {
            "start_time": datetime.now().isoformat(),
            "docs_path": docs_path,
            "output_dir": output_dir,
            "collections_discovered": len(collections),
            "collections_processed": 0,
            "collections_failed": 0,
            "total_files_processed": 0,
            "total_files_failed": 0,
            "total_chunks_created": 0,
            "total_tokens_processed": 0,
            "collection_results": {}
        }
        
        # Process each collection
        for collection_name, collection_info in collections.items():
            try:
                logger.info(f"🔄 Processing collection: {collection_name}")
                
                collection_result = self.process_collection(collection_info, output_dir)
                
                overall_results["collections_processed"] += 1
                overall_results["total_files_processed"] += collection_result["files_processed"]
                overall_results["total_files_failed"] += collection_result["files_failed"]
                overall_results["total_chunks_created"] += collection_result["total_chunks"]
                overall_results["total_tokens_processed"] += collection_result["total_tokens"]
                overall_results["collection_results"][collection_name] = collection_result
                
                logger.info(f"✅ Collection '{collection_name}': {collection_result['files_processed']} files, {collection_result['total_chunks']} chunks")
                
            except Exception as e:
                overall_results["collections_failed"] += 1
                logger.error(f"❌ Failed to process collection '{collection_name}': {e}")
        
        # Finalize results
        overall_results["end_time"] = datetime.now().isoformat()
        start_time = datetime.fromisoformat(overall_results["start_time"])
        end_time = datetime.fromisoformat(overall_results["end_time"])
        overall_results["total_processing_time_seconds"] = (end_time - start_time).total_seconds()
        
        # Save overall summary
        summary_file = Path(output_dir) / "docs_processing_complete_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(overall_results, f, indent=2, ensure_ascii=False)
        
        # Print final summary
        logger.info(f"🎯 Docs Processing Complete!")
        logger.info(f"📊 Collections processed: {overall_results['collections_processed']}/{overall_results['collections_discovered']}")
        logger.info(f"📊 Files processed: {overall_results['total_files_processed']}")
        logger.info(f"📊 Files failed: {overall_results['total_files_failed']}")
        logger.info(f"📊 Total chunks created: {overall_results['total_chunks_created']}")
        logger.info(f"📊 Total tokens processed: {overall_results['total_tokens_processed']}")
        logger.info(f"⏱️ Total processing time: {overall_results['total_processing_time_seconds']:.2f} seconds")
        logger.info(f"💾 Complete summary saved: {summary_file}")
        
        return overall_results

def main():
    """Main function to run the docs collection processing"""
    
    processor = DocsCollectionProcessor()
    
    # Process all docs with default paths
    results = processor.process_all_docs()
    
    if results.get("success", True):  # Default to True unless explicitly False
        print(f"\n🎉 Successfully processed {results['collections_processed']} collections!")
        print(f"📊 Total chunks created: {results['total_chunks_created']}")
        print(f"📊 Total tokens processed: {results['total_tokens_processed']}")
    else:
        print(f"\n❌ Processing failed: {results.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()