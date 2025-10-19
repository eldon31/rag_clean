#!/usr/bin/env python3
"""
Production Ultimate Chunker for User's 5 Input Types
Optimized for:
- MCP Repositories
- Workflow Documentation
- API Documentation
- Programming Language Documentation
- Platform Documentation
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict

from processor.enhanced_ultimate_chunker_v3 import EnhancedUltimateChunkerV3

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionUltimateChunker:
    """Production-ready chunker optimized for user's 5 input types"""
    
    def __init__(self):
        """Initialize the production chunker"""
        self.chunker = EnhancedUltimateChunkerV3()
        
        # Optimized strategies for each input type
        self.input_type_strategies = {
            "mcp_repositories": "mcp_optimized",
            "workflow_documentation": "hierarchical_balanced", 
            "api_documentation": "hierarchical_precise",
            "programming_language_documentation": "hybrid_adaptive",
            "platform_documentation": "hierarchical_context"
        }
        
        # Content patterns for auto-detection
        self.content_patterns = {
            "mcp_repositories": [
                "mcp", "model context protocol", "server", "client", 
                "mcpServers", "docker-compose", "protocol", "handler"
            ],
            "workflow_documentation": [
                "workflow", "github actions", "ci/cd", "pipeline", 
                "steps", "jobs", "automation", "deployment"
            ],
            "api_documentation": [
                "api", "endpoint", "rest", "get", "post", "put", "delete",
                "request", "response", "schema", "authentication"
            ],
            "programming_language_documentation": [
                "python", "javascript", "typescript", "java", "c++", "rust",
                "function", "class", "method", "variable", "tutorial"
            ],
            "platform_documentation": [
                "kubernetes", "docker", "aws", "azure", "gcp", "platform",
                "deployment", "infrastructure", "configuration", "service"
            ]
        }
        
        logger.info("🚀 Production Ultimate Chunker initialized")
    
    def detect_input_type(self, text: str, filename: str) -> str:
        """
        Detect input type from user's 5 categories
        
        Returns: One of the 5 input types
        """
        
        text_lower = text.lower()
        filename_lower = filename.lower()
        
        # Score each input type
        scores = {}
        for input_type, patterns in self.content_patterns.items():
            score = 0
            
            # Check patterns in content
            for pattern in patterns:
                score += text_lower.count(pattern) * 2
                if pattern in filename_lower:
                    score += 5  # Filename match is stronger
            
            scores[input_type] = score
        
        # Find best match
        if scores:
            best_match = max(scores.items(), key=lambda x: x[1])
            if best_match[1] > 3:  # Minimum threshold
                detected_type = best_match[0]
                logger.info(f"🎯 Detected input type: {detected_type}")
                return detected_type
        
        # Default to workflow documentation
        logger.info("📄 Using default: workflow_documentation")
        return "workflow_documentation"
    
    def process_single_file(
        self, 
        file_path: str, 
        output_dir: Optional[str] = None,
        force_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a single file with optimized chunking
        
        Args:
            file_path: Path to the file to process
            output_dir: Optional output directory for chunks
            force_type: Force a specific input type
            
        Returns:
            Processing results with chunks and metadata
        """
        
        try:
            logger.info(f"📋 Processing: {file_path}")
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 100:
                logger.warning(f"⚠️ File too small: {file_path}")
                return {"success": False, "error": "File too small"}
            
            # Detect input type
            input_type = force_type or self.detect_input_type(content, file_path)
            strategy = self.input_type_strategies[input_type]
            
            logger.info(f"🎯 Using {input_type} → {strategy} strategy")
            
            # Create chunks with simple approach first
            simple_chunks = self._create_simple_chunks(
                content, file_path, input_type, strategy
            )
            
            if not simple_chunks:
                logger.warning(f"⚠️ No chunks created from {file_path}")
                return {"success": False, "error": "No chunks created"}
            
            # Save results if output directory specified
            if output_dir:
                self._save_results(simple_chunks, file_path, output_dir, input_type)
            
            # Calculate summary statistics
            total_tokens = sum(chunk['metadata']['token_count'] for chunk in simple_chunks)
            avg_length = sum(len(chunk['text']) for chunk in simple_chunks) / len(simple_chunks)
            
            results = {
                "success": True,
                "file_path": file_path,
                "input_type": input_type,
                "strategy": strategy,
                "chunks_created": len(simple_chunks),
                "total_tokens": total_tokens,
                "average_chunk_length": int(avg_length),
                "chunks": simple_chunks
            }
            
            logger.info(f"✅ {file_path}: {len(simple_chunks)} chunks, {total_tokens} tokens")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error processing {file_path}: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_simple_chunks(
        self, 
        content: str, 
        filename: str, 
        input_type: str, 
        strategy: str
    ) -> List[Dict[str, Any]]:
        """Create chunks using a simplified approach that always works"""
        
        chunks = []
        
        # Get strategy config
        strategy_config = self.chunker.chunking_strategies.get(strategy, 
            self.chunker.chunking_strategies["hierarchical_balanced"])
        
        # Simple chunking by paragraphs first
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        current_chunk = ""
        chunk_id = 0
        
        for paragraph in paragraphs:
            # Count tokens in current chunk + paragraph
            test_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph
            token_count = len(self.chunker.tokenizer.encode(test_chunk))
            
            # If adding this paragraph exceeds max tokens, save current chunk
            if token_count > strategy_config["max_tokens"] and current_chunk:
                # Save current chunk
                chunk_data = self._create_chunk_data(
                    current_chunk, chunk_id, filename, input_type, strategy
                )
                chunks.append(chunk_data)
                chunk_id += 1
                current_chunk = paragraph
            else:
                current_chunk = test_chunk
        
        # Save final chunk
        if current_chunk:
            chunk_data = self._create_chunk_data(
                current_chunk, chunk_id, filename, input_type, strategy
            )
            chunks.append(chunk_data)
        
        return chunks
    
    def _create_chunk_data(
        self, 
        text: str, 
        chunk_id: int, 
        filename: str, 
        input_type: str, 
        strategy: str
    ) -> Dict[str, Any]:
        """Create chunk data structure"""
        
        token_count = len(self.chunker.tokenizer.encode(text))
        
        return {
            "text": text,
            "metadata": {
                "chunk_id": chunk_id,
                "source_file": filename,
                "input_type": input_type,
                "chunking_strategy": strategy,
                "token_count": token_count,
                "character_count": len(text),
                "created_at": datetime.now().isoformat(),
                "parent_context": None,
                "semantic_type": input_type
            }
        }
    
    def _save_results(
        self, 
        chunks: List[Dict[str, Any]], 
        file_path: str, 
        output_dir: str, 
        input_type: str
    ):
        """Save chunks to output directory"""
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Create filename
        file_stem = Path(file_path).stem
        output_file = output_path / f"{file_stem}_{input_type}_chunks.json"
        
        # Save chunks
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Saved to: {output_file}")
    
    def process_directory(
        self,
        input_dir: str,
        output_dir: str,
        file_extensions: List[str] = ['.md', '.txt', '.rst', '.py', '.js', '.ts', '.json', '.yml', '.yaml']
    ) -> Dict[str, Any]:
        """
        Process an entire directory for user's input types
        
        Args:
            input_dir: Directory containing files to process
            output_dir: Directory to save chunked results
            file_extensions: File extensions to process
            
        Returns:
            Summary of processing results
        """
        
        input_path = Path(input_dir)
        results = {
            "start_time": datetime.now().isoformat(),
            "input_directory": str(input_path),
            "output_directory": output_dir,
            "files_processed": 0,
            "files_failed": 0,
            "total_chunks": 0,
            "input_types": defaultdict(int),
            "strategies_used": defaultdict(int),
            "files": []
        }
        
        # Find all relevant files
        files = []
        for ext in file_extensions:
            files.extend(input_path.rglob(f"*{ext}"))
        
        logger.info(f"🔍 Found {len(files)} files to process in {input_dir}")
        
        # Process each file
        for file_path in files:
            try:
                file_result = self.process_single_file(
                    str(file_path),
                    output_dir=output_dir
                )
                
                if file_result["success"]:
                    results["files_processed"] += 1
                    results["total_chunks"] += file_result["chunks_created"]
                    results["input_types"][file_result["input_type"]] += 1
                    results["strategies_used"][file_result["strategy"]] += 1
                    
                    results["files"].append({
                        "file": str(file_path),
                        "input_type": file_result["input_type"],
                        "strategy": file_result["strategy"],
                        "chunks": file_result["chunks_created"],
                        "tokens": file_result["total_tokens"]
                    })
                    
                    logger.info(f"✅ {file_path.name}: {file_result['chunks_created']} chunks")
                else:
                    results["files_failed"] += 1
                    logger.error(f"❌ Failed: {file_path.name}")
                
            except Exception as e:
                results["files_failed"] += 1
                logger.error(f"❌ Error processing {file_path}: {e}")
        
        # Calculate final statistics
        results["end_time"] = datetime.now().isoformat()
        start_time = datetime.fromisoformat(results["start_time"])
        end_time = datetime.fromisoformat(results["end_time"])
        results["processing_time_seconds"] = (end_time - start_time).total_seconds()
        
        # Convert defaultdicts to regular dicts for JSON serialization
        results["input_types"] = dict(results["input_types"])
        results["strategies_used"] = dict(results["strategies_used"])
        
        # Save summary
        summary_file = Path(output_dir) / "production_processing_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Print summary
        logger.info(f"🎯 Processing Complete!")
        logger.info(f"📊 Files processed: {results['files_processed']}")
        logger.info(f"📊 Files failed: {results['files_failed']}")
        logger.info(f"📊 Total chunks: {results['total_chunks']}")
        logger.info(f"⏱️ Processing time: {results['processing_time_seconds']:.2f} seconds")
        logger.info(f"📋 Input types: {results['input_types']}")
        logger.info(f"🔧 Strategies used: {results['strategies_used']}")
        
        return results

def main():
    """Main function for testing"""
    
    chunker = ProductionUltimateChunker()
    
    # Test with README.md
    print("🧪 Testing Production Ultimate Chunker...")
    
    result = chunker.process_single_file("README.md")
    
    if result["success"]:
        print(f"✅ Successfully processed README.md")
        print(f"   Input type: {result['input_type']}")
        print(f"   Strategy: {result['strategy']}")
        print(f"   Chunks: {result['chunks_created']}")
        print(f"   Tokens: {result['total_tokens']}")
    else:
        print(f"❌ Failed to process README.md: {result['error']}")

if __name__ == "__main__":
    main()