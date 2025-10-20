#!/usr/bin/env python3
"""Final test of chunker with all dependencies"""

from processor.enhanced_ultimate_chunker_v5_unified import EnhancedUltimateChunkerV5Unified

print("="*70)
print("Enhanced Ultimate Chunker V5 - Final Verification")
print("="*70)

chunker = EnhancedUltimateChunkerV5Unified(
    target_model='jina-code-embeddings-1.5b',
    use_tree_sitter=True,
    use_semchunk=True
)

print(f"\n✓ Chunker initialized successfully!")
print(f"  Tree-sitter: {'ENABLED ✓' if chunker.config.use_tree_sitter else 'DISABLED ✗'}")
print(f"  Semchunk: {'ENABLED ✓' if chunker.config.use_semchunk else 'DISABLED ✗'}")
print(f"  Chunk size: {chunker.chunk_size_tokens:,} tokens")
print(f"  Embedding dimension: {chunker.embedding_dimension}D")
print("="*70)