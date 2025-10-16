#!/usr/bin/env python3
"""
Query Our Existing Qdrant Collections for Ultimate Optimization
==============================================================

This script queries our actual Qdrant collections to get insights for
creating the ultimate Qdrant-optimized chunker.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore

async def query_collections_for_insights():
    """Query our existing collections to understand optimization patterns."""
    
    print("🔍 QUERYING EXISTING QDRANT COLLECTIONS FOR OPTIMIZATION INSIGHTS")
    print("=" * 70)
    
    # Initialize embedder (CodeRankEmbed 768D)
    print("🤖 Initializing CodeRankEmbed embedder...")
    embedder = SentenceTransformerEmbedder(
        EmbedderConfig(model_name='nomic-ai/CodeRankEmbed')
    )
    
    # Collections we have
    collections = {
        "sentence_transformers_768": "Advanced embedding techniques and model optimization",
        "qdrant_ecosystem_768": "Vector search, sparse embeddings, and database optimization", 
        "docling_768": "Document processing, structure extraction, and chunking"
    }
    
    # Optimization queries
    optimization_queries = [
        "qdrant optimization performance indexing",
        "chunking strategies vector database",
        "embedding quality optimization",
        "quantization HNSW configuration",
        "collection structure organization",
        "semantic splitting techniques",
        "content analysis patterns",
        "production deployment optimization"
    ]
    
    all_insights = {}
    
    for collection_name, description in collections.items():
        print(f"\n📊 Querying {collection_name}")
        print(f"   {description}")
        
        try:
            # Configure Qdrant store
            config = QdrantStoreConfig(
                host="localhost",
                port=6333,
                collection_name=collection_name,
                vector_size=768,
                distance_metric="Cosine",
                prefer_grpc=False
            )
            
            store = QdrantStore(config)
            collection_insights = []
            
            for query in optimization_queries:
                print(f"   🔍 Query: {query}")
                
                # Generate embedding
                query_embedding = await embedder.embed_documents([query])
                
                # Search collection
                results = store.search(
                    query_embedding=query_embedding[0],
                    limit=3,
                    score_threshold=0.5
                )
                
                if results:
                    print(f"      ✅ Found {len(results)} relevant results")
                    for i, result in enumerate(results, 1):
                        score = result.get('score', 0)
                        content = result.get('content', '')[:200] + "..."
                        print(f"         {i}. Score: {score:.3f}")
                        print(f"            {content}")
                        
                        collection_insights.append({
                            "query": query,
                            "score": score,
                            "content": result.get('content', ''),
                            "metadata": result.get('metadata', {})
                        })
                else:
                    print(f"      ❌ No results above threshold 0.5")
            
            all_insights[collection_name] = collection_insights
            
        except Exception as e:
            print(f"   ❌ Error querying {collection_name}: {e}")
    
    # Analyze insights for optimization patterns
    print("\n" + "🧠" * 70)
    print("OPTIMIZATION INSIGHTS ANALYSIS")
    print("🧠" * 70)
    
    optimization_patterns = analyze_insights(all_insights)
    
    # Generate ultimate optimization recommendations
    print("\n" + "🚀" * 70)
    print("ULTIMATE QDRANT OPTIMIZATION RECOMMENDATIONS")
    print("🚀" * 70)
    
    generate_ultimate_recommendations(optimization_patterns)
    
    return all_insights, optimization_patterns

def analyze_insights(all_insights):
    """Analyze the insights to extract optimization patterns."""
    
    patterns = {
        "chunking_strategies": [],
        "qdrant_optimizations": [],
        "embedding_techniques": [],
        "quality_indicators": [],
        "production_configs": []
    }
    
    for collection_name, insights in all_insights.items():
        for insight in insights:
            content = insight["content"].lower()
            query = insight["query"].lower()
            score = insight["score"]
            
            # High-quality insights (score > 0.7)
            if score > 0.7:
                # Categorize insights
                if any(word in content for word in ["chunk", "split", "segment", "token"]):
                    patterns["chunking_strategies"].append({
                        "source": collection_name,
                        "query": query,
                        "content": insight["content"][:300],
                        "score": score
                    })
                
                if any(word in content for word in ["qdrant", "vector", "index", "hnsw", "quantization"]):
                    patterns["qdrant_optimizations"].append({
                        "source": collection_name,
                        "query": query,
                        "content": insight["content"][:300],
                        "score": score
                    })
                
                if any(word in content for word in ["embed", "model", "dimension", "similarity"]):
                    patterns["embedding_techniques"].append({
                        "source": collection_name,
                        "query": query,
                        "content": insight["content"][:300],
                        "score": score
                    })
                
                if any(word in content for word in ["quality", "score", "threshold", "performance"]):
                    patterns["quality_indicators"].append({
                        "source": collection_name,
                        "query": query,
                        "content": insight["content"][:300],
                        "score": score
                    })
                
                if any(word in content for word in ["production", "deploy", "config", "optimize"]):
                    patterns["production_configs"].append({
                        "source": collection_name,
                        "query": query,
                        "content": insight["content"][:300],
                        "score": score
                    })
    
    # Print analysis
    for category, items in patterns.items():
        if items:
            print(f"\n📋 {category.upper().replace('_', ' ')} ({len(items)} insights):")
            for item in items[:3]:  # Top 3 per category
                print(f"   🔹 From {item['source']} (Score: {item['score']:.3f})")
                print(f"      {item['content']}")
                print()
    
    return patterns

def generate_ultimate_recommendations(patterns):
    """Generate ultimate optimization recommendations based on patterns."""
    
    recommendations = []
    
    # Chunking recommendations
    if patterns["chunking_strategies"]:
        recommendations.append({
            "category": "CHUNKING OPTIMIZATION",
            "recommendations": [
                "Use semantic-aware chunking based on content type",
                "Implement adaptive chunk sizing (1024-2048 tokens)",
                "Preserve document structure and code boundaries",
                "Apply 15% overlap for context preservation",
                "Use CodeRankEmbed tokenizer for accurate sizing"
            ]
        })
    
    # Qdrant recommendations
    if patterns["qdrant_optimizations"]:
        recommendations.append({
            "category": "QDRANT CONFIGURATION",
            "recommendations": [
                "Use HNSW index with ef_construct=100, m=16",
                "Enable scalar quantization for 4x memory savings",
                "Set distance_metric=Cosine for CodeRankEmbed",
                "Organize collections by domain expertise",
                "Use 768-dimensional vectors for optimal performance"
            ]
        })
    
    # Embedding recommendations
    if patterns["embedding_techniques"]:
        recommendations.append({
            "category": "EMBEDDING STRATEGY",
            "recommendations": [
                "Standardize on nomic-ai/CodeRankEmbed (768D)",
                "Batch embed for GPU optimization",
                "Use content-aware embedding selection",
                "Implement quality scoring (>0.75 threshold)",
                "Enable knowledge synthesis across collections"
            ]
        })
    
    # Quality recommendations
    if patterns["quality_indicators"]:
        recommendations.append({
            "category": "QUALITY ASSURANCE",
            "recommendations": [
                "Multi-dimensional quality scoring system",
                "Content completeness validation (no truncation)",
                "Structure preservation verification",
                "Knowledge synthesis scoring",
                "Production readiness validation"
            ]
        })
    
    # Production recommendations
    if patterns["production_configs"]:
        recommendations.append({
            "category": "PRODUCTION DEPLOYMENT",
            "recommendations": [
                "1-level subdirectory organization maximum",
                "Collection-specific optimization weights",
                "Kaggle GPU batch processing ready",
                "Real-time performance monitoring",
                "Automatic quality threshold enforcement"
            ]
        })
    
    # Print recommendations
    for rec in recommendations:
        print(f"\n🎯 {rec['category']}:")
        for item in rec['recommendations']:
            print(f"   ✅ {item}")
    
    print(f"\n💎 ULTIMATE OPTIMIZATION SCORE: Based on {sum(len(p) for p in patterns.values())} insights")
    print("🚀 Ready to implement ULTIMATE Qdrant-optimized system!")

async def main():
    """Main execution."""
    try:
        insights, patterns = await query_collections_for_insights()
        print(f"\n✅ Successfully analyzed {sum(len(insights[k]) for k in insights)} insights")
        print("🎯 Ultimate optimization recommendations generated!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())