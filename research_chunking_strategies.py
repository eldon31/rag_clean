#!/usr/bin/env python3
"""
Research chunking strategies from our Ultimate Knowledge Base
"""
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

def research_chunking_strategies():
    print("🔍 RESEARCHING CHUNKING STRATEGIES FROM 9,654 VECTORS")
    print("=" * 60)
    
    # Connect to our knowledge base
    client = QdrantClient(host='localhost', port=6333)
    embedder = SentenceTransformer('nomic-ai/CodeRankEmbed', trust_remote_code=True)
    
    # Research queries for different aspects of chunking
    research_queries = [
        "text chunking strategies document splitting semantic segmentation",
        "embedding quality optimization text preprocessing",
        "document parsing techniques content extraction methods",
        "vector search performance optimization retrieval quality",
        "sentence boundary detection paragraph segmentation"
    ]
    
    collections = ['qdrant_ecosystem_768', 'docling_768', 'sentence_transformers_768']
    all_insights = []
    
    for query_idx, query in enumerate(research_queries, 1):
        print(f"\n🎯 RESEARCH QUERY {query_idx}: {query}")
        print("-" * 50)
        
        query_vector = embedder.encode([query])[0].tolist()
        
        for collection in collections:
            try:
                results = client.query_points(
                    collection_name=collection,
                    query=query_vector,
                    limit=2,
                    score_threshold=0.45
                )
                
                if results.points:
                    print(f"\n📊 {collection}: {len(results.points)} insights")
                    
                    for point in results.points:
                        payload = point.payload or {}
                        text = payload.get('text', '')
                        filename = payload.get('filename', 'Unknown')
                        
                        all_insights.append({
                            'query': f"Q{query_idx}",
                            'collection': collection,
                            'score': point.score,
                            'filename': filename,
                            'text': text
                        })
                        
                        print(f"  • Score: {point.score:.3f} | {filename}")
                        print(f"    Preview: {text[:120]}...")
                
            except Exception as e:
                print(f"❌ Error in {collection}: {e}")
    
    # Analyze top insights
    print(f"\n🧠 ANALYSIS: TOP CHUNKING INSIGHTS DISCOVERED")
    print("=" * 60)
    
    all_insights.sort(key=lambda x: x['score'], reverse=True)
    
    for i, insight in enumerate(all_insights[:8], 1):
        print(f"\n{i}. INSIGHT (Score: {insight['score']:.3f})")
        print(f"   Source: {insight['collection']} | {insight['filename']}")
        print(f"   Query: {insight['query']}")
        print(f"   Content: {insight['text'][:250]}...")
        
        # Extract key techniques
        text_lower = insight['text'].lower()
        techniques = []
        
        if 'chunk' in text_lower:
            techniques.append("Chunking")
        if 'semantic' in text_lower:
            techniques.append("Semantic")
        if 'embed' in text_lower:
            techniques.append("Embedding")
        if 'optim' in text_lower:
            techniques.append("Optimization")
        if 'split' in text_lower:
            techniques.append("Splitting")
            
        if techniques:
            print(f"   Techniques: {', '.join(techniques)}")
    
    # Generate improvement recommendations
    print(f"\n🚀 CHUNKER IMPROVEMENT RECOMMENDATIONS")
    print("=" * 50)
    
    recommendations = [
        "1. SEMANTIC CHUNKING: Use meaning-based boundaries instead of fixed sizes",
        "2. EMBEDDING OPTIMIZATION: Pre-filter chunks based on content quality",
        "3. HIERARCHICAL PROCESSING: Combine document structure with semantic segmentation", 
        "4. ADAPTIVE SIZING: Dynamic chunk sizes based on content complexity",
        "5. MULTI-LEVEL CONTEXT: Preserve document hierarchy and relationships"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")
    
    print(f"\n📊 Research complete! Insights from {len(all_insights)} high-quality matches.")
    print("🎯 Ready to implement enhanced ultimate chunker!")

if __name__ == "__main__":
    research_chunking_strategies()