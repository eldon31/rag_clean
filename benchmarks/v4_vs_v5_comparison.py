#!/usr/bin/env python3
"""
Performance Benchmarks: V4 vs V5 Comparison
Measures chunking speed, memory usage, and quality metrics

Phase 2 Track 4 - Task 4.2
"""

import sys
from pathlib import Path
import time
import tracemalloc
from typing import Dict, Any, List
import json
from dataclasses import dataclass, as dict

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from processor.enhanced_ultimate_chunker_v5_unified import EnhancedUltimateChunkerV5Unified


@dataclass
class BenchmarkResult:
    """Benchmark result container"""
    version: str
    num_documents: int
    total_chunks: int
    processing_time_seconds: float
    memory_peak_mb: float
    chunks_per_second: float
    avg_chunk_tokens: float
    avg_quality_score: float
    features_used: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "num_documents": self.num_documents,
            "total_chunks": self.total_chunks,
            "processing_time_seconds": round(self.processing_time_seconds, 3),
            "memory_peak_mb": round(self.memory_peak_mb, 2),
            "chunks_per_second": round(self.chunks_per_second, 2),
            "avg_chunk_tokens": round(self.avg_chunk_tokens, 1),
            "avg_quality_score": round(self.avg_quality_score, 3),
            "features_used": self.features_used
        }


class V5Benchmark:
    """V5 performance benchmarking"""
    
    def __init__(self, test_data_dir: str = "test_data"):
        self.test_data_dir = Path(test_data_dir)
        self.results: List[BenchmarkResult] = []
    
    def create_test_documents(self, num_docs: int = 10):
        """Create test documents for benchmarking"""
        self.test_data_dir.mkdir(exist_ok=True)
        
        template = """# Document {idx}

## Introduction
This is test document number {idx} for benchmarking the V5 RAG pipeline.
It contains multiple sections to test hierarchical chunking.

## Technical Content
Machine learning and natural language processing are fundamental to modern AI systems.
Transformers have revolutionized the field with attention mechanisms.
BERT, GPT, and other models demonstrate impressive capabilities.

## Code Example
```python
def process_data(input_file: str) -> Dict[str, Any]:
    \"\"\"Process input data and return results.\"\"\"
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    results = {{
        'processed': True,
        'count': len(data),
        'timestamp': datetime.now().isoformat()
    }}
    return results
```

## Features List
- Model-aware chunking with token limits
- Hierarchical document structure preservation
- Tree-sitter AST parsing for code
- Semchunk semantic boundary detection
- Quality scoring and fallback promotion

## Mathematical Concepts
The attention mechanism can be expressed as:

Attention(Q, K, V) = softmax(QK^T / √d_k)V

Where Q, K, V are query, key, and value matrices.

## Conclusion
This document demonstrates various content types for comprehensive testing.
The V5 system should handle all sections appropriately with optimal chunking.
"""
        
        for i in range(num_docs):
            doc_path = self.test_data_dir / f"test_doc_{i:03d}.md"
            content = template.format(idx=i)
            doc_path.write_text(content)
        
        print(f"✓ Created {num_docs} test documents in {self.test_data_dir}")
        return list(self.test_data_dir.glob("test_doc_*.md"))
    
    def benchmark_v5_basic(self, test_files: List[Path]) -> BenchmarkResult:
        """Benchmark V5 with basic settings (no frameworks)"""
        print("\n" + "="*70)
        print("Benchmarking V5 (Basic Mode)")
        print("="*70)
        
        chunker = EnhancedUltimateChunkerV5Unified(
            target_model="jina-code-embeddings-1.5b",
            use_tree_sitter=False,
            use_semchunk=False,
            enable_semantic_scoring=False
        )
        
        # Start benchmarking
        tracemalloc.start()
        start_time = time.time()
        
        all_chunks = []
        for file_path in test_files:
            chunks = chunker.process_file_smart(str(file_path))
            all_chunks.extend(chunks)
        
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Calculate metrics
        processing_time = end_time - start_time
        memory_peak_mb = peak / 1024 / 1024
        chunks_per_second = len(all_chunks) / processing_time if processing_time > 0 else 0
        
        avg_tokens = sum(c["metadata"]["token_count"] for c in all_chunks) / len(all_chunks)
        avg_quality = sum(c["advanced_scores"]["overall"] for c in all_chunks) / len(all_chunks)
        
        result = BenchmarkResult(
            version="V5 (Basic)",
            num_documents=len(test_files),
            total_chunks=len(all_chunks),
            processing_time_seconds=processing_time,
            memory_peak_mb=memory_peak_mb,
            chunks_per_second=chunks_per_second,
            avg_chunk_tokens=avg_tokens,
            avg_quality_score=avg_quality,
            features_used=["model_aware", "hierarchical", "quality_gating"]
        )
        
        self.results.append(result)
        self._print_result(result)
        return result
    
    def benchmark_v5_full(self, test_files: List[Path]) -> BenchmarkResult:
        """Benchmark V5 with all features enabled"""
        print("\n" + "="*70)
        print("Benchmarking V5 (Full Features)")
        print("="*70)
        
        chunker = EnhancedUltimateChunkerV5Unified(
            target_model="jina-code-embeddings-1.5b",
            use_tree_sitter=True,
            use_semchunk=True,
            enable_semantic_scoring=False  # Disable to avoid model download
        )
        
        # Start benchmarking
        tracemalloc.start()
        start_time = time.time()
        
        all_chunks = []
        for file_path in test_files:
            chunks = chunker.process_file_smart(str(file_path))
            all_chunks.extend(chunks)
        
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Calculate metrics
        processing_time = end_time - start_time
        memory_peak_mb = peak / 1024 / 1024
        chunks_per_second = len(all_chunks) / processing_time if processing_time > 0 else 0
        
        avg_tokens = sum(c["metadata"]["token_count"] for c in all_chunks) / len(all_chunks)
        avg_quality = sum(c["advanced_scores"]["overall"] for c in all_chunks) / len(all_chunks)
        
        result = BenchmarkResult(
            version="V5 (Full)",
            num_documents=len(test_files),
            total_chunks=len(all_chunks),
            processing_time_seconds=processing_time,
            memory_peak_mb=memory_peak_mb,
            chunks_per_second=chunks_per_second,
            avg_chunk_tokens=avg_tokens,
            avg_quality_score=avg_quality,
            features_used=["model_aware", "hierarchical", "tree_sitter", "semchunk", "quality_gating"]
        )
        
        self.results.append(result)
        self._print_result(result)
        return result
    
    def benchmark_model_comparison(self, test_files: List[Path]) -> List[BenchmarkResult]:
        """Benchmark different target models"""
        print("\n" + "="*70)
        print("Benchmarking Different Target Models")
        print("="*70)
        
        models = [
            "jina-code-embeddings-1.5b",    # 32,768 tokens
            "bge-m3",                        # 8,192 tokens
            "all-miniLM-l6"                  # 256 tokens
        ]
        
        model_results = []
        
        for model in models:
            print(f"\nTesting model: {model}")
            
            try:
                chunker = EnhancedUltimateChunkerV5Unified(
                    target_model=model,
                    use_tree_sitter=False,
                    use_semchunk=False,
                    enable_semantic_scoring=False
                )
                
                start_time = time.time()
                
                all_chunks = []
                for file_path in test_files[:3]:  # Test with 3 files
                    chunks = chunker.process_file_smart(str(file_path))
                    all_chunks.extend(chunks)
                
                processing_time = time.time() - start_time
                
                avg_tokens = sum(c["metadata"]["token_count"] for c in all_chunks) / len(all_chunks)
                avg_quality = sum(c["advanced_scores"]["overall"] for c in all_chunks) / len(all_chunks)
                
                result = BenchmarkResult(
                    version=f"V5 ({model})",
                    num_documents=3,
                    total_chunks=len(all_chunks),
                    processing_time_seconds=processing_time,
                    memory_peak_mb=0.0,  # Not measured for this test
                    chunks_per_second=len(all_chunks) / processing_time,
                    avg_chunk_tokens=avg_tokens,
                    avg_quality_score=avg_quality,
                    features_used=["model_aware", "hierarchical"]
                )
                
                model_results.append(result)
                self._print_result(result)
            
            except Exception as e:
                print(f"  ⚠️  Skipping {model}: {e}")
        
        self.results.extend(model_results)
        return model_results
    
    def _print_result(self, result: BenchmarkResult):
        """Print benchmark result"""
        print(f"\n{result.version} Results:")
        print(f"  Documents: {result.num_documents}")
        print(f"  Total chunks: {result.total_chunks}")
        print(f"  Processing time: {result.processing_time_seconds:.3f}s")
        print(f"  Throughput: {result.chunks_per_second:.2f} chunks/sec")
        print(f"  Memory peak: {result.memory_peak_mb:.2f} MB")
        print(f"  Avg chunk tokens: {result.avg_chunk_tokens:.1f}")
        print(f"  Avg quality score: {result.avg_quality_score:.3f}")
        print(f"  Features: {', '.join(result.features_used)}")
    
    def generate_comparison_report(self, output_file: str = "benchmark_report.json"):
        """Generate comparison report"""
        report = {
            "benchmark_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "system_info": {
                "python_version": sys.version,
                "platform": sys.platform
            },
            "results": [r.to_dict() for r in self.results],
            "summary": self._generate_summary()
        }
        
        output_path = Path(output_file)
        output_path.write_text(json.dumps(report, indent=2))
        
        print(f"\n✓ Benchmark report saved to {output_path}")
        return report
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate benchmark summary"""
        if not self.results:
            return {}
        
        return {
            "total_benchmarks": len(self.results),
            "fastest_version": min(self.results, key=lambda r: r.processing_time_seconds).version,
            "most_memory_efficient": min(
                [r for r in self.results if r.memory_peak_mb > 0],
                key=lambda r: r.memory_peak_mb,
                default=self.results[0]
            ).version if any(r.memory_peak_mb > 0 for r in self.results) else "N/A",
            "highest_quality": max(self.results, key=lambda r: r.avg_quality_score).version,
            "highest_throughput": max(self.results, key=lambda r: r.chunks_per_second).version
        }
    
    def print_comparison_table(self):
        """Print comparison table"""
        print("\n" + "="*70)
        print("Performance Comparison Table")
        print("="*70)
        
        print(f"\n{'Version':<25} {'Time(s)':<10} {'Chunks/s':<12} {'Memory(MB)':<12} {'Quality':<10}")
        print("-" * 70)
        
        for result in self.results:
            print(f"{result.version:<25} "
                  f"{result.processing_time_seconds:<10.3f} "
                  f"{result.chunks_per_second:<12.2f} "
                  f"{result.memory_peak_mb:<12.2f} "
                  f"{result.avg_quality_score:<10.3f}")
        
        print("="*70)


def main():
    """Run all benchmarks"""
    print("="*70)
    print("V5 Performance Benchmarks - Phase 2 Track 4 (Task 4.2)")
    print("="*70)
    
    benchmark = V5Benchmark()
    
    # Create test data
    test_files = benchmark.create_test_documents(num_docs=10)
    
    # Run benchmarks
    benchmark.benchmark_v5_basic(test_files)
    benchmark.benchmark_v5_full(test_files)
    benchmark.benchmark_model_comparison(test_files)
    
    # Generate report
    benchmark.print_comparison_table()
    report = benchmark.generate_comparison_report("benchmarks/benchmark_report.json")
    
    # Print summary
    print("\n" + "="*70)
    print("Benchmark Summary")
    print("="*70)
    summary = report["summary"]
    print(f"Total benchmarks: {summary['total_benchmarks']}")
    print(f"Fastest version: {summary['fastest_version']}")
    print(f"Most memory efficient: {summary['most_memory_efficient']}")
    print(f"Highest quality: {summary['highest_quality']}")
    print(f"Highest throughput: {summary['highest_throughput']}")
    print("="*70)


if __name__ == "__main__":
    main()