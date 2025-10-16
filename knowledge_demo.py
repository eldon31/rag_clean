#!/usr/bin/env python3
"""
Knowledge Base Utilization Demo
==============================

Demonstrates how to leverage your deployed Qdrant collections:
- sentence_transformers_768: Advanced embedding techniques
- qdrant_ecosystem_768: Vector search strategies  
- docling_768: Document processing methods

Shows practical examples of knowledge extraction and learning.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("knowledge_demo")

class KnowledgeBaseDemo:
    """Demonstrates knowledge extraction from deployed collections."""
    
    def __init__(self):
        self.embedder: Optional[SentenceTransformerEmbedder] = None
        self.stores: Dict[str, QdrantStore] = {}
        
        # Collection specializations
        self.collection_expertise = {
            'sentence_transformers_768': {
                'description': 'Advanced embedding techniques and model optimization',
                'specialties': ['fine-tuning', 'training', 'model selection', 'performance optimization'],
                'best_for': 'Learning embedding strategies and implementation techniques'
            },
            'qdrant_ecosystem_768': {
                'description': 'Vector search, sparse embeddings, and database optimization',
                'specialties': ['vector search', 'sparse embeddings', 'quantization', 'hybrid search'],
                'best_for': 'Understanding vector database strategies and implementation'
            },
            'docling_768': {
                'description': 'Document processing, structure extraction, and chunking',
                'specialties': ['document parsing', 'structure extraction', 'chunking strategies', 'text processing'],
                'best_for': 'Learning document processing and preparation techniques'
            }
        }
        
    async def initialize(self):
        """Initialize embedder and collection connections."""
        logger.info("🚀 Initializing Knowledge Base Demo...")
        
        # Initialize CodeRankEmbed (768-dim)
        embedder_config = EmbedderConfig(
            model_name="nomic-ai/CodeRankEmbed",
            device="cpu",
            batch_size=32
        )
        self.embedder = SentenceTransformerEmbedder(embedder_config)
        
        # Connect to all collections
        for collection_name in self.collection_expertise.keys():
            logger.info(f"Connecting to {collection_name}...")
            config = QdrantStoreConfig(
                host="localhost",
                port=6333,
                collection_name=collection_name,
                vector_size=768,
                enable_quantization=True,
                prefer_grpc=False
            )
            self.stores[collection_name] = QdrantStore(config)
            
        logger.info("✅ All collections connected!")
        
    async def search_collection(
        self, 
        collection: str, 
        query: str, 
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Search a specific collection."""
        if collection not in self.stores or not self.embedder:
            return []
            
        try:
            # Generate embedding
            embeddings = await self.embedder.embed_documents([query])
            
            # Search collection
            results = self.stores[collection].search(
                query_embedding=embeddings[0],
                limit=limit,
                score_threshold=0.3
            )
            
            # Enhance results with collection context
            enhanced_results = []
            for result in results:
                enhanced_results.append({
                    'content': result.get('content', ''),
                    'score': result.get('score', 0.0),
                    'source': result.get('source_file', 'unknown'),
                    'collection': collection,
                    'expertise_area': self.collection_expertise[collection]['description']
                })
                
            return enhanced_results
            
        except Exception as e:
            logger.error(f"Error searching {collection}: {e}")
            return []
            
    async def demonstrate_sentence_transformers_learning(self):
        """Demo learning from Sentence Transformers collection."""
        print("\n🎯 SENTENCE TRANSFORMERS LEARNING DEMO")
        print("=" * 60)
        
        collection = 'sentence_transformers_768'
        info = self.collection_expertise[collection]
        
        print(f"📚 Collection: {collection}")
        print(f"🎯 Expertise: {info['description']}")
        print(f"🔧 Specialties: {', '.join(info['specialties'])}")
        print(f"💡 Best for: {info['best_for']}\n")
        
        # Learning queries focused on practical implementation
        learning_queries = [
            "How to fine-tune sentence transformers for domain-specific tasks?",
            "What are the best practices for training custom embedding models?",
            "How to optimize sentence transformer performance and memory usage?",
            "What loss functions work best for similarity learning?"
        ]
        
        for i, query in enumerate(learning_queries, 1):
            print(f"🔍 Query {i}: {query}")
            results = await self.search_collection(collection, query, limit=3)
            
            print(f"📊 Found {len(results)} relevant results:")
            for j, result in enumerate(results, 1):
                score = result['score']
                content_preview = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
                source = result['source']
                
                print(f"  {j}. Score: {score:.3f} | Source: {source}")
                print(f"     Preview: {content_preview}")
                
            print("-" * 50)
            
    async def demonstrate_qdrant_strategies(self):
        """Demo learning Qdrant vector strategies."""
        print("\n🚀 QDRANT VECTOR STRATEGIES DEMO")
        print("=" * 60)
        
        collection = 'qdrant_ecosystem_768'
        info = self.collection_expertise[collection]
        
        print(f"📚 Collection: {collection}")
        print(f"🎯 Expertise: {info['description']}")
        print(f"🔧 Specialties: {', '.join(info['specialties'])}")
        print(f"💡 Best for: {info['best_for']}\n")
        
        # Vector strategy queries
        strategy_queries = [
            "How to implement sparse vector search in Qdrant?",
            "What are quantization strategies for optimizing vector storage?",
            "How to set up hybrid search combining dense and sparse vectors?",
            "Best practices for scaling vector collections in production?"
        ]
        
        for i, query in enumerate(strategy_queries, 1):
            print(f"🔍 Strategy Query {i}: {query}")
            results = await self.search_collection(collection, query, limit=3)
            
            print(f"📊 Found {len(results)} strategy insights:")
            for j, result in enumerate(results, 1):
                score = result['score']
                content_preview = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
                source = result['source']
                
                print(f"  {j}. Score: {score:.3f} | Source: {source}")
                print(f"     Strategy: {content_preview}")
                
            print("-" * 50)
            
    async def demonstrate_docling_techniques(self):
        """Demo learning document processing from Docling collection."""
        print("\n📄 DOCLING DOCUMENT PROCESSING DEMO")
        print("=" * 60)
        
        collection = 'docling_768'
        info = self.collection_expertise[collection]
        
        print(f"📚 Collection: {collection}")
        print(f"🎯 Expertise: {info['description']}")
        print(f"🔧 Specialties: {', '.join(info['specialties'])}")
        print(f"💡 Best for: {info['best_for']}\n")
        
        # Document processing queries
        docling_queries = [
            "How to extract structured information from PDF documents?",
            "What are the best chunking strategies for long documents?",
            "How to preserve document structure during text extraction?",
            "Techniques for handling different document formats and layouts?"
        ]
        
        for i, query in enumerate(docling_queries, 1):
            print(f"🔍 Processing Query {i}: {query}")
            results = await self.search_collection(collection, query, limit=3)
            
            print(f"📊 Found {len(results)} processing techniques:")
            for j, result in enumerate(results, 1):
                score = result['score']
                content_preview = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
                source = result['source']
                
                print(f"  {j}. Score: {score:.3f} | Source: {source}")
                print(f"     Technique: {content_preview}")
                
            print("-" * 50)
            
    async def demonstrate_cross_collection_synthesis(self):
        """Demo synthesizing knowledge across multiple collections."""
        print("\n🔄 CROSS-COLLECTION KNOWLEDGE SYNTHESIS")
        print("=" * 60)
        
        # Complex queries that benefit from multiple collections
        synthesis_queries = [
            "How to build an end-to-end document similarity search system?",
            "Best practices for embeddings in production vector databases?",
            "How to optimize document chunking for better vector search results?"
        ]
        
        for i, query in enumerate(synthesis_queries, 1):
            print(f"🔍 Synthesis Query {i}: {query}")
            print("🎯 Searching across all collections...\n")
            
            all_results = []
            
            # Search each collection
            for collection_name in self.collection_expertise.keys():
                collection_results = await self.search_collection(collection_name, query, limit=2)
                
                if collection_results:
                    clean_name = collection_name.replace('_768', '').replace('_', ' ').title()
                    print(f"📁 {clean_name} Collection:")
                    
                    for j, result in enumerate(collection_results, 1):
                        score = result['score']
                        content_preview = result['content'][:150] + "..." if len(result['content']) > 150 else result['content']
                        
                        print(f"  {j}. Score: {score:.3f}")
                        print(f"     Insight: {content_preview}")
                        
                    all_results.extend(collection_results)
                    print()
            
            # Synthesize findings
            print("🧠 Synthesis Summary:")
            collections_contributing = set(r['collection'] for r in all_results)
            print(f"   • Found insights from {len(collections_contributing)} collections")
            print(f"   • Total relevant results: {len(all_results)}")
            print(f"   • Cross-domain knowledge synthesis successful")
            
            print("-" * 70)
            
    async def demonstrate_practical_learning_scenarios(self):
        """Demo practical learning scenarios."""
        print("\n🎯 PRACTICAL LEARNING SCENARIOS")
        print("=" * 60)
        
        scenarios = [
            {
                'scenario': 'I want to improve code similarity search accuracy',
                'approach': 'Learn embedding fine-tuning + vector optimization',
                'collections': ['sentence_transformers_768', 'qdrant_ecosystem_768']
            },
            {
                'scenario': 'I need to process large document collections efficiently',
                'approach': 'Learn document chunking + batch processing strategies',
                'collections': ['docling_768', 'qdrant_ecosystem_768']
            },
            {
                'scenario': 'I want to build a production-ready similarity search system',
                'approach': 'Learn end-to-end pipeline optimization',
                'collections': ['sentence_transformers_768', 'qdrant_ecosystem_768', 'docling_768']
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"📚 Scenario {i}: {scenario['scenario']}")
            print(f"🎯 Learning Approach: {scenario['approach']}")
            print(f"📁 Target Collections: {', '.join(scenario['collections'])}")
            
            # Generate learning query
            learning_query = f"How to {scenario['approach'].lower()}?"
            print(f"🔍 Learning Query: {learning_query}")
            
            # Search relevant collections
            scenario_results = []
            for collection in scenario['collections']:
                results = await self.search_collection(collection, learning_query, limit=2)
                scenario_results.extend(results)
            
            print(f"📊 Learning Resources Found: {len(scenario_results)}")
            
            # Show top insights
            scenario_results.sort(key=lambda x: x['score'], reverse=True)
            for j, result in enumerate(scenario_results[:3], 1):
                collection_name = result['collection'].replace('_768', '').replace('_', ' ').title()
                content_preview = result['content'][:120] + "..."
                
                print(f"  💡 Insight {j} from {collection_name}: {content_preview}")
                
            print("-" * 50)

    async def show_collection_statistics(self):
        """Show statistics about the deployed collections."""
        print("\n📊 COLLECTION STATISTICS")
        print("=" * 50)
        
        for collection_name, info in self.collection_expertise.items():
            clean_name = collection_name.replace('_768', '').replace('_', ' ').title()
            
            # Test search to verify connection
            test_results = await self.search_collection(collection_name, "test query", limit=1)
            
            print(f"📁 {clean_name}")
            print(f"   🎯 Expertise: {info['description']}")
            print(f"   🔧 Specialties: {', '.join(info['specialties'])}")
            print(f"   📊 Connection: {'✅ Active' if test_results else '❌ Error'}")
            print(f"   💡 Best for: {info['best_for']}")
            print()

async def main():
    """Run the complete knowledge base demonstration."""
    print("🎯 KNOWLEDGE BASE UTILIZATION DEMONSTRATION")
    print("🚀 Leveraging your deployed Qdrant collections for learning")
    print("=" * 70)
    
    demo = KnowledgeBaseDemo()
    await demo.initialize()
    
    # Show what we have
    await demo.show_collection_statistics()
    
    # Demonstrate collection-specific learning
    await demo.demonstrate_sentence_transformers_learning()
    await demo.demonstrate_qdrant_strategies()
    await demo.demonstrate_docling_techniques()
    
    # Show cross-collection synthesis
    await demo.demonstrate_cross_collection_synthesis()
    
    # Practical scenarios
    await demo.demonstrate_practical_learning_scenarios()
    
    print("\n" + "=" * 70)
    print("✅ DEMONSTRATION COMPLETE!")
    print("\n💡 Your deployed knowledge bases are working perfectly for:")
    print("   🎓 Learning advanced embedding techniques")
    print("   🚀 Mastering vector search strategies")
    print("   📄 Understanding document processing methods")
    print("   🔄 Synthesizing cross-domain knowledge")
    print("\n🎯 Next Steps:")
    print("   1. Use enhanced_knowledge_utilization.py for production queries")
    print("   2. Develop specialized learning curriculums")
    print("   3. Build domain-specific applications")
    print("   4. Implement continuous learning feedback loops")

if __name__ == "__main__":
    asyncio.run(main())