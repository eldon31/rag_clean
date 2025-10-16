#!/usr/bin/env python3
"""
Quick Qdrant Ecosystem Coverage Analysis
=======================================
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path.cwd()))

from mcp_server.qdrant_mcp_simple import initialize_embedder, initialize_qdrant_stores, search_collection_impl

async def analyze_qdrant_coverage():
    """Analyze coverage of key Qdrant topics."""
    print("🔍 QDRANT ECOSYSTEM ANALYSIS")
    print("=" * 60)
    
    await initialize_embedder()
    await initialize_qdrant_stores()
    
    # Key areas to analyze
    analysis_areas = {
        "Core Functionality": [
            "vector search fundamentals",
            "collection management", 
            "indexing strategies",
            "query optimization"
        ],
        "Performance & Optimization": [
            "performance tuning qdrant",
            "quantization techniques",
            "memory optimization",
            "search latency reduction"
        ],
        "Advanced Features": [
            "sparse embeddings qdrant",
            "hybrid search implementation",
            "custom distance metrics",
            "payload indexing"
        ],
        "Production & Deployment": [
            "qdrant production deployment",
            "scalability patterns",
            "monitoring and metrics",
            "backup and recovery"
        ],
        "Integration & Development": [
            "qdrant API usage",
            "SDK best practices",
            "batch operations",
            "real-time updates"
        ]
    }
    
    overall_results = {}
    
    for category, topics in analysis_areas.items():
        print(f"\n📊 {category}")
        print("-" * 40)
        
        category_scores = []
        category_results = []
        
        for topic in topics:
            result = await search_collection_impl({
                "collection": "qdrant_ecosystem_768",
                "query": topic,
                "limit": 5,
                "score_threshold": 0.25
            })
            
            if "results" in result and result["results"]:
                scores = [r.get("score", 0) for r in result["results"]]
                max_score = max(scores)
                avg_score = sum(scores) / len(scores)
                high_quality = len([s for s in scores if s > 0.5])
                
                category_scores.extend(scores)
                
                # Assess coverage quality
                if high_quality >= 2:
                    quality = "🟢 Excellent"
                elif high_quality >= 1 or avg_score > 0.4:
                    quality = "🟡 Good"
                elif avg_score > 0.3:
                    quality = "🟠 Fair"
                else:
                    quality = "🔴 Poor"
                    
                print(f"  {topic:30} | {quality} | Max: {max_score:.3f} | Avg: {avg_score:.3f} | High: {high_quality}")
                
                category_results.append({
                    "topic": topic,
                    "max_score": max_score,
                    "avg_score": avg_score,
                    "high_quality_count": high_quality,
                    "quality": quality
                })
            else:
                print(f"  {topic:30} | 🔴 No Results")
                category_results.append({
                    "topic": topic,
                    "max_score": 0,
                    "avg_score": 0,
                    "high_quality_count": 0,
                    "quality": "🔴 Poor"
                })
        
        # Category summary
        if category_scores:
            cat_avg = sum(category_scores) / len(category_scores)
            cat_max = max(category_scores)
            high_quality_topics = len([r for r in category_results if r["high_quality_count"] > 0])
            
            print(f"\n  📈 Category Summary:")
            print(f"     Average Score: {cat_avg:.3f}")
            print(f"     Best Score: {cat_max:.3f}")
            print(f"     Topics with High Quality Results: {high_quality_topics}/{len(topics)}")
            
            overall_results[category] = {
                "average_score": cat_avg,
                "best_score": cat_max,
                "high_quality_topics": high_quality_topics,
                "total_topics": len(topics),
                "coverage_percentage": (high_quality_topics / len(topics)) * 100,
                "detailed_results": category_results
            }
    
    # Overall analysis
    print("\n" + "=" * 60)
    print("📈 OVERALL ANALYSIS SUMMARY")
    print("=" * 60)
    
    for category, data in overall_results.items():
        coverage = data["coverage_percentage"]
        print(f"\n🎯 {category}:")
        print(f"   Coverage: {coverage:.1f}% ({data['high_quality_topics']}/{data['total_topics']} topics)")
        print(f"   Average Score: {data['average_score']:.3f}")
        print(f"   Best Score: {data['best_score']:.3f}")
        
        if coverage >= 75:
            print("   Status: ✅ Strong coverage")
        elif coverage >= 50:
            print("   Status: 🟡 Moderate coverage")
        elif coverage >= 25:
            print("   Status: 🟠 Weak coverage")
        else:
            print("   Status: 🔴 Poor coverage")
    
    # Identify improvement areas
    print("\n🔧 IMPROVEMENT RECOMMENDATIONS:")
    print("-" * 40)
    
    weak_categories = [cat for cat, data in overall_results.items() if data["coverage_percentage"] < 50]
    moderate_categories = [cat for cat, data in overall_results.items() if 50 <= data["coverage_percentage"] < 75]
    
    if weak_categories:
        print(f"\n🚨 Priority 1 - Weak Coverage Areas:")
        for cat in weak_categories:
            print(f"   • {cat} ({overall_results[cat]['coverage_percentage']:.1f}% coverage)")
            # Show specific topics that need improvement
            poor_topics = [r["topic"] for r in overall_results[cat]["detailed_results"] if r["high_quality_count"] == 0]
            if poor_topics:
                print(f"     Missing: {', '.join(poor_topics[:3])}")
    
    if moderate_categories:
        print(f"\n⚠️ Priority 2 - Moderate Coverage Areas:")
        for cat in moderate_categories:
            print(f"   • {cat} ({overall_results[cat]['coverage_percentage']:.1f}% coverage)")
    
    # Specific content gaps
    print(f"\n💡 Specific Content Needed:")
    print("   • Production deployment checklists and patterns")
    print("   • Performance benchmarking and optimization guides") 
    print("   • Advanced quantization technique comparisons")
    print("   • Real-world integration examples")
    print("   • Troubleshooting and debugging guides")
    print("   • Migration and upgrade procedures")
    print("   • Security and access control patterns")
    
    print(f"\n🎯 Collection Status: {len(overall_results)} categories analyzed")
    total_coverage = sum(data["coverage_percentage"] for data in overall_results.values()) / len(overall_results)
    print(f"🎯 Overall Coverage Score: {total_coverage:.1f}%")
    
    if total_coverage >= 70:
        print("🎉 Overall Assessment: Strong knowledge base with room for enhancement")
    elif total_coverage >= 50:
        print("📈 Overall Assessment: Good foundation, needs targeted improvements")
    else:
        print("🔧 Overall Assessment: Significant enhancement opportunities exist")

if __name__ == "__main__":
    asyncio.run(analyze_qdrant_coverage())