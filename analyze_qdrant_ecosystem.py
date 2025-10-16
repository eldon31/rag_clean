#!/usr/bin/env python3
"""
Qdrant Ecosystem Analysis Tool
=============================

Deep analysis of the qdrant_ecosystem_768 collection to identify 
improvement opportunities and knowledge gaps.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

# Add project root to path
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent if CURRENT_DIR.name == "scripts" else CURRENT_DIR
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore

class QdrantEcosystemAnalyzer:
    """Comprehensive analyzer for the Qdrant ecosystem collection."""
    
    def __init__(self):
        self.embedder = None
        self.store = None
        self.analysis_results = {}
        
    async def initialize(self):
        """Initialize embedder and Qdrant connection."""
        print("🔧 Initializing Qdrant Ecosystem Analyzer...")
        
        # Initialize embedder
        embedder_config = EmbedderConfig(
            model_name="nomic-ai/CodeRankEmbed",
            device="cpu",
            batch_size=32
        )
        self.embedder = SentenceTransformerEmbedder(embedder_config)
        
        # Initialize Qdrant store
        config = QdrantStoreConfig(
            host="localhost",
            port=6333,
            collection_name="qdrant_ecosystem_768",
            vector_size=768,
            enable_quantization=True,
            prefer_grpc=False
        )
        self.store = QdrantStore(config)
        print("✅ Initialization complete!")
        
    async def analyze_topic_coverage(self) -> Dict[str, Any]:
        """Analyze what topics are covered in the collection."""
        print("\n📊 Analyzing Topic Coverage...")
        
        # Core Qdrant topics to analyze
        core_topics = [
            "vector search fundamentals",
            "collection management", 
            "indexing strategies",
            "query optimization",
            "performance tuning",
            "quantization techniques",
            "sparse embeddings",
            "hybrid search",
            "clustering and sharding",
            "memory management",
            "HNSW algorithm",
            "filtering and metadata",
            "batch operations",
            "backup and recovery",
            "monitoring and metrics",
            "API and SDK usage",
            "deployment strategies",
            "scalability patterns",
            "security best practices",
            "troubleshooting common issues"
        ]
        
        topic_analysis = {}
        
        for topic in core_topics:
            if self.embedder is None or self.store is None:
                continue
            embeddings = await self.embedder.embed_documents([topic])
            results = self.store.search(
                query_embedding=embeddings[0],
                limit=10,
                score_threshold=0.25
            )
            
            # Analyze results quality
            high_relevance = [r for r in results if r.get('score', 0) > 0.5]
            medium_relevance = [r for r in results if 0.3 <= r.get('score', 0) <= 0.5]
            low_relevance = [r for r in results if 0.25 <= r.get('score', 0) < 0.3]
            
            topic_analysis[topic] = {
                "total_results": len(results),
                "high_relevance": len(high_relevance),
                "medium_relevance": len(medium_relevance), 
                "low_relevance": len(low_relevance),
                "max_score": max([r.get('score', 0) for r in results], default=0),
                "avg_score": sum([r.get('score', 0) for r in results]) / len(results) if results else 0,
                "coverage_quality": self._assess_coverage_quality(high_relevance, medium_relevance, low_relevance)
            }
            
        return topic_analysis
        
    def _assess_coverage_quality(self, high, medium, low) -> str:
        """Assess the quality of coverage for a topic."""
        if len(high) >= 3:
            return "Excellent"
        elif len(high) >= 1 or len(medium) >= 3:
            return "Good"
        elif len(medium) >= 1 or len(low) >= 2:
            return "Fair"
        else:
            return "Poor"
            
    async def analyze_advanced_features(self) -> Dict[str, Any]:
        """Analyze coverage of advanced Qdrant features."""
        print("\n🚀 Analyzing Advanced Features Coverage...")
        
        advanced_features = [
            "payload indexing optimization",
            "custom distance metrics",
            "vector quantization techniques",
            "product quantization",
            "scalar quantization",
            "binary quantization",
            "on-disk storage optimization",
            "memory mapped files",
            "collection aliases",
            "snapshot management",
            "distributed deployment",
            "raft consensus",
            "multi-tenancy patterns",
            "custom scoring functions",
            "recommendation systems with qdrant",
            "real-time updates and consistency",
            "batch update strategies",
            "cluster management",
            "horizontal scaling",
            "performance benchmarking"
        ]
        
        advanced_analysis = {}
        
        for feature in advanced_features:
            query = f"how to implement {feature} in qdrant"
            embeddings = await self.embedder.embed_documents([query])
            results = self.store.search(
                query_embedding=embeddings[0],
                limit=5,
                score_threshold=0.3
            )
            
            advanced_analysis[feature] = {
                "implementation_guidance": len([r for r in results if r.get('score', 0) > 0.5]),
                "conceptual_coverage": len([r for r in results if 0.4 <= r.get('score', 0) <= 0.5]),
                "basic_mentions": len([r for r in results if 0.3 <= r.get('score', 0) < 0.4]),
                "best_score": max([r.get('score', 0) for r in results], default=0),
                "has_implementation": any(r.get('score', 0) > 0.5 for r in results)
            }
            
        return advanced_analysis
        
    async def analyze_performance_optimization(self) -> Dict[str, Any]:
        """Deep dive into performance optimization coverage."""
        print("\n⚡ Analyzing Performance Optimization Coverage...")
        
        perf_queries = [
            "qdrant search latency optimization",
            "memory usage optimization qdrant",
            "qdrant indexing performance tuning",
            "batch size optimization for qdrant",
            "qdrant query performance best practices",
            "reducing vector search response time",
            "qdrant resource utilization optimization",
            "concurrent search performance",
            "qdrant storage optimization techniques",
            "vector database performance monitoring"
        ]
        
        performance_analysis = {}
        
        for query in perf_queries:
            embeddings = await self.embedder.embed_documents([query])
            results = self.store.search(
                query_embedding=embeddings[0],
                limit=8,
                score_threshold=0.25
            )
            
            # Extract actionable insights
            actionable_results = []
            for result in results:
                content = result.get('content', '')
                score = result.get('score', 0)
                
                # Look for actionable content indicators
                actionable_indicators = [
                    'optimize', 'improve', 'reduce', 'increase', 'configure',
                    'setting', 'parameter', 'technique', 'strategy', 'method'
                ]
                
                has_actionable = any(indicator in content.lower() for indicator in actionable_indicators)
                
                if has_actionable and score > 0.3:
                    actionable_results.append({
                        'score': score,
                        'content_preview': content[:200] + "..." if len(content) > 200 else content,
                        'actionable_score': score * (1.2 if score > 0.5 else 1.0)
                    })
            
            performance_analysis[query] = {
                "total_results": len(results),
                "actionable_results": len(actionable_results),
                "best_score": max([r.get('score', 0) for r in results], default=0),
                "actionable_content": actionable_results[:3]  # Top 3 actionable results
            }
            
        return performance_analysis
        
    async def identify_knowledge_gaps(self) -> Dict[str, Any]:
        """Identify specific areas where knowledge might be lacking."""
        print("\n🔍 Identifying Knowledge Gaps...")
        
        # Critical areas that should have comprehensive coverage
        critical_areas = {
            "Production Deployment": [
                "qdrant production deployment checklist",
                "qdrant high availability setup",
                "qdrant disaster recovery planning",
                "qdrant monitoring in production"
            ],
            "Scaling and Performance": [
                "qdrant horizontal scaling strategies",
                "qdrant performance bottleneck identification",
                "qdrant capacity planning",
                "qdrant load balancing techniques"
            ],
            "Data Management": [
                "qdrant data migration strategies", 
                "qdrant backup and restore procedures",
                "qdrant version upgrade procedures",
                "qdrant data consistency guarantees"
            ],
            "Advanced Configuration": [
                "qdrant custom distance functions",
                "qdrant advanced filtering techniques",
                "qdrant multi-vector search patterns",
                "qdrant integration with external systems"
            ],
            "Troubleshooting": [
                "qdrant common error diagnosis",
                "qdrant performance debugging techniques",
                "qdrant memory leak investigation",
                "qdrant slow query optimization"
            ]
        }
        
        gap_analysis = {}
        
        for category, queries in critical_areas.items():
            category_results = []
            
            for query in queries:
                embeddings = await self.embedder.embed_documents([query])
                results = self.store.search(
                    query_embedding=embeddings[0],
                    limit=5,
                    score_threshold=0.4  # Higher threshold for critical areas
                )
                
                category_results.append({
                    "query": query,
                    "strong_matches": len([r for r in results if r.get('score', 0) > 0.6]),
                    "moderate_matches": len([r for r in results if 0.4 <= r.get('score', 0) <= 0.6]),
                    "best_score": max([r.get('score', 0) for r in results], default=0),
                    "has_comprehensive_coverage": any(r.get('score', 0) > 0.6 for r in results)
                })
            
            # Assess category gaps
            strong_coverage = sum(1 for r in category_results if r["has_comprehensive_coverage"])
            total_queries = len(queries)
            coverage_percentage = (strong_coverage / total_queries) * 100
            
            gap_analysis[category] = {
                "coverage_percentage": coverage_percentage,
                "queries_with_strong_coverage": strong_coverage,
                "total_queries": total_queries,
                "gap_severity": self._assess_gap_severity(coverage_percentage),
                "detailed_results": category_results
            }
            
        return gap_analysis
        
    def _assess_gap_severity(self, coverage_percentage: float) -> str:
        """Assess the severity of knowledge gaps."""
        if coverage_percentage >= 80:
            return "Low"
        elif coverage_percentage >= 60:
            return "Moderate" 
        elif coverage_percentage >= 40:
            return "High"
        else:
            return "Critical"
            
    async def generate_improvement_recommendations(self, 
                                                 topic_analysis: Dict,
                                                 advanced_analysis: Dict,
                                                 performance_analysis: Dict,
                                                 gap_analysis: Dict) -> Dict[str, Any]:
        """Generate specific recommendations for improving the collection."""
        print("\n💡 Generating Improvement Recommendations...")
        
        recommendations = {
            "high_priority": [],
            "medium_priority": [],
            "low_priority": [],
            "content_enhancement": [],
            "new_topics_needed": []
        }
        
        # Analyze topic coverage gaps
        poor_coverage_topics = [
            topic for topic, data in topic_analysis.items()
            if data["coverage_quality"] in ["Poor", "Fair"]
        ]
        
        # Analyze advanced features gaps
        missing_advanced_features = [
            feature for feature, data in advanced_analysis.items()
            if not data["has_implementation"]
        ]
        
        # Analyze critical gaps
        critical_gaps = [
            category for category, data in gap_analysis.items()
            if data["gap_severity"] in ["Critical", "High"]
        ]
        
        # Generate recommendations
        if critical_gaps:
            recommendations["high_priority"].extend([
                f"Add comprehensive content for {gap}" for gap in critical_gaps
            ])
            
        if poor_coverage_topics:
            recommendations["medium_priority"].extend([
                f"Enhance coverage for {topic}" for topic in poor_coverage_topics[:5]
            ])
            
        if missing_advanced_features:
            recommendations["content_enhancement"].extend([
                f"Add implementation guides for {feature}" for feature in missing_advanced_features[:10]
            ])
            
        # Performance optimization recommendations
        weak_perf_areas = [
            query for query, data in performance_analysis.items()
            if data["actionable_results"] < 2
        ]
        
        if weak_perf_areas:
            recommendations["medium_priority"].extend([
                f"Add actionable content for: {query}" for query in weak_perf_areas[:3]
            ])
            
        # Specific new topics based on analysis
        recommendations["new_topics_needed"] = [
            "Qdrant production deployment patterns",
            "Advanced quantization comparison and selection",
            "Real-world performance optimization case studies",
            "Qdrant ecosystem integration patterns",
            "Troubleshooting playbooks for common issues",
            "Migration strategies from other vector databases",
            "Cost optimization strategies for Qdrant deployments",
            "Security hardening for production Qdrant"
        ]
        
        return recommendations
        
    async def run_comprehensive_analysis(self):
        """Run the complete analysis suite."""
        print("🚀 Starting Comprehensive Qdrant Ecosystem Analysis")
        print("=" * 70)
        
        await self.initialize()
        
        # Run all analysis components
        topic_analysis = await self.analyze_topic_coverage()
        advanced_analysis = await self.analyze_advanced_features()
        performance_analysis = await self.analyze_performance_optimization()
        gap_analysis = await self.identify_knowledge_gaps()
        recommendations = await self.generate_improvement_recommendations(
            topic_analysis, advanced_analysis, performance_analysis, gap_analysis
        )
        
        # Generate comprehensive report
        report = {
            "collection_stats": {
                "total_vectors": 8108,
                "embedding_model": "nomic-ai/CodeRankEmbed",
                "vector_dimensions": 768
            },
            "analysis_timestamp": "2025-10-16",
            "topic_coverage": topic_analysis,
            "advanced_features": advanced_analysis,
            "performance_optimization": performance_analysis,
            "knowledge_gaps": gap_analysis,
            "improvement_recommendations": recommendations
        }
        
        # Save detailed report
        report_path = ROOT_DIR / "qdrant_ecosystem_analysis_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, indent=2, fp=f)
            
        await self.generate_summary_report(report)
        
        print(f"\n📊 Detailed analysis saved to: {report_path}")
        return report
        
    async def generate_summary_report(self, report: Dict):
        """Generate a human-readable summary report."""
        print("\n" + "=" * 70)
        print("📈 QDRANT ECOSYSTEM ANALYSIS SUMMARY")
        print("=" * 70)
        
        # Topic Coverage Summary
        topic_coverage = report["topic_coverage"]
        excellent_topics = [t for t, d in topic_coverage.items() if d["coverage_quality"] == "Excellent"]
        good_topics = [t for t, d in topic_coverage.items() if d["coverage_quality"] == "Good"]
        fair_topics = [t for t, d in topic_coverage.items() if d["coverage_quality"] == "Fair"]
        poor_topics = [t for t, d in topic_coverage.items() if d["coverage_quality"] == "Poor"]
        
        print(f"\n📊 TOPIC COVERAGE ANALYSIS:")
        print(f"  ✅ Excellent Coverage: {len(excellent_topics)} topics")
        print(f"  🟢 Good Coverage: {len(good_topics)} topics")
        print(f"  🟡 Fair Coverage: {len(fair_topics)} topics")
        print(f"  🔴 Poor Coverage: {len(poor_topics)} topics")
        
        if excellent_topics:
            print(f"\n  🌟 Strongest Topics: {', '.join(excellent_topics[:3])}")
        if poor_topics:
            print(f"  ⚠️ Weakest Topics: {', '.join(poor_topics[:3])}")
            
        # Advanced Features Summary
        advanced_features = report["advanced_features"]
        implemented_features = [f for f, d in advanced_features.items() if d["has_implementation"]]
        missing_features = [f for f, d in advanced_features.items() if not d["has_implementation"]]
        
        print(f"\n🚀 ADVANCED FEATURES ANALYSIS:")
        print(f"  ✅ Well Covered: {len(implemented_features)}/{len(advanced_features)}")
        print(f"  ❌ Need Implementation: {len(missing_features)}")
        
        # Knowledge Gaps Summary
        gap_analysis = report["knowledge_gaps"]
        critical_gaps = [c for c, d in gap_analysis.items() if d["gap_severity"] == "Critical"]
        high_gaps = [c for c, d in gap_analysis.items() if d["gap_severity"] == "High"]
        
        print(f"\n🔍 KNOWLEDGE GAPS ANALYSIS:")
        if critical_gaps:
            print(f"  🚨 Critical Gaps: {', '.join(critical_gaps)}")
        if high_gaps:
            print(f"  ⚠️ High Priority Gaps: {', '.join(high_gaps)}")
            
        # Performance Coverage
        perf_analysis = report["performance_optimization"]
        actionable_queries = [q for q, d in perf_analysis.items() if d["actionable_results"] >= 2]
        weak_queries = [q for q, d in perf_analysis.items() if d["actionable_results"] < 2]
        
        print(f"\n⚡ PERFORMANCE OPTIMIZATION ANALYSIS:")
        print(f"  ✅ Queries with Actionable Content: {len(actionable_queries)}")
        print(f"  ⚠️ Queries Needing More Content: {len(weak_queries)}")
        
        # Recommendations Summary
        recommendations = report["improvement_recommendations"]
        
        print(f"\n💡 TOP IMPROVEMENT RECOMMENDATIONS:")
        print(f"  🔥 High Priority: {len(recommendations['high_priority'])} items")
        for item in recommendations["high_priority"][:3]:
            print(f"    • {item}")
            
        print(f"\n  📈 Medium Priority: {len(recommendations['medium_priority'])} items")
        for item in recommendations["medium_priority"][:3]:
            print(f"    • {item}")
            
        print(f"\n  🆕 New Topics Needed: {len(recommendations['new_topics_needed'])} areas")
        for topic in recommendations["new_topics_needed"][:5]:
            print(f"    • {topic}")
            
        print("\n" + "=" * 70)
        print("🎯 NEXT STEPS:")
        print("1. Focus on critical knowledge gaps first")
        print("2. Add implementation guides for missing advanced features") 
        print("3. Enhance performance optimization content")
        print("4. Create production-ready deployment guides")
        print("5. Add more troubleshooting and best practices content")

async def main():
    """Main analysis function."""
    analyzer = QdrantEcosystemAnalyzer()
    
    try:
        report = await analyzer.run_comprehensive_analysis()
        print("\n🎉 Analysis completed successfully!")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())