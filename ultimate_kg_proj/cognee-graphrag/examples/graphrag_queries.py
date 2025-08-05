#!/usr/bin/env python3
"""
Advanced GraphRAG query patterns example.

This example demonstrates:
1. Different search strategies (vector, graph, combined)
2. Complex query patterns
3. Result analysis and ranking
4. Multi-hop reasoning patterns
"""

import asyncio
from pathlib import Path
from typing import Dict, Any, List
import json

# Add src to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent))

from src.graphrag import GraphRAG, GraphRAGConfig


class QueryAnalyzer:
    """Analyze and rank query results."""
    
    @staticmethod
    def analyze_results(results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze search results and provide insights."""
        if results.get("status") != "success":
            return {"error": results.get("error", "Unknown error")}
        
        search_results = results.get("results", [])
        analysis = {
            "total_results": len(search_results),
            "search_type": results.get("search_type", "unknown"),
            "query": results.get("query", ""),
        }
        
        if results.get("search_type") == "combined":
            analysis["vector_count"] = results.get("vector_count", 0)
            analysis["graph_count"] = results.get("graph_count", 0)
            analysis["coverage"] = {
                "vector_ratio": analysis["vector_count"] / max(analysis["total_results"], 1),
                "graph_ratio": analysis["graph_count"] / max(analysis["total_results"], 1)
            }
        
        return analysis
    
    @staticmethod
    def extract_entities(results: List[Any]) -> List[str]:
        """Extract mentioned entities from results."""
        entities = set()
        for result in results:
            result_str = str(result).lower()
            # Simple entity extraction (in real implementation, use NER)
            common_entities = [
                "machine learning", "artificial intelligence", "deep learning",
                "google", "microsoft", "apple", "tesla", "openai",
                "einstein", "marie curie", "geoffrey hinton", "andrew ng",
                "quantum mechanics", "dna", "neural networks"
            ]
            for entity in common_entities:
                if entity in result_str:
                    entities.add(entity)
        return list(entities)


async def run_query_analysis(graphrag: GraphRAG, query: str, search_types: List[str]):
    """Run comprehensive query analysis."""
    print(f"\n🔍 Analyzing Query: '{query}'")
    print("-" * 60)
    
    analyzer = QueryAnalyzer()
    results_by_type = {}
    
    # Run different search types
    for search_type in search_types:
        print(f"  Running {search_type} search...")
        result = await graphrag.search(query, search_type=search_type, top_k=8)
        results_by_type[search_type] = result
        
        # Analyze results
        analysis = analyzer.analyze_results(result)
        print(f"    📊 {search_type.title()} Results: {analysis.get('total_results', 0)}")
        
        if search_type == "combined" and analysis.get("coverage"):
            coverage = analysis["coverage"]
            print(f"    📈 Vector: {coverage['vector_ratio']:.1%}, Graph: {coverage['graph_ratio']:.1%}")
    
    # Compare results across search types
    print("\n  🔄 Cross-Search Analysis:")
    for search_type, result in results_by_type.items():
        if result.get("status") == "success":
            entities = analyzer.extract_entities(result.get("results", []))
            print(f"    {search_type.title()}: {len(entities)} entities - {', '.join(entities[:3])}{'...' if len(entities) > 3 else ''}")
    
    return results_by_type


async def demonstrate_query_patterns(graphrag: GraphRAG):
    """Demonstrate various GraphRAG query patterns."""
    
    query_patterns = {
        "Entity-Focused Queries": [
            "What do you know about Geoffrey Hinton and deep learning?",
            "Tell me about Google and its founders",
            "What are the contributions of Marie Curie to science?"
        ],
        
        "Relationship Queries": [
            "How are machine learning and neural networks related?",
            "What is the connection between Einstein and quantum mechanics?",
            "How do Tesla and autonomous vehicles relate?"
        ],
        
        "Comparative Queries": [
            "Compare Google and Microsoft as technology companies",
            "What are the differences between classical and quantum physics?",
            "How do different AI researchers approach machine learning?"
        ],
        
        "Multi-Domain Queries": [  
            "How do physics concepts relate to AI development?",
            "What connections exist between technology companies and scientific research?",
            "How has scientific discovery influenced modern technology?"
        ]
    }
    
    # Test different search strategies
    search_strategies = ["vector", "graph", "combined"]
    
    for category, queries in query_patterns.items():
        print(f"\n{'='*20} {category} {'='*20}")
        
        for query in queries:
            await run_query_analysis(graphrag, query, search_strategies)
            
            # Add some spacing
            print()


async def benchmark_search_performance(graphrag: GraphRAG):
    """Benchmark different search approaches."""
    print("\n🏃 Search Performance Benchmarking")
    print("=" * 50)
    
    benchmark_queries = [
        "machine learning algorithms",
        "technology company leaders", 
        "scientific discoveries",
        "artificial intelligence applications",
        "quantum physics principles"
    ]
    
    import time
    
    performance_results = []
    
    for query in benchmark_queries:
        print(f"\n⏱️  Benchmarking: '{query}'")
        
        search_times = {}
        
        for search_type in ["vector", "graph", "combined"]:
            start_time = time.time()
            result = await graphrag.search(query, search_type=search_type, top_k=5)
            end_time = time.time()
            
            search_time = end_time - start_time
            search_times[search_type] = search_time
            result_count = len(result.get("results", []))
            
            print(f"  {search_type.title()}: {search_time:.3f}s ({result_count} results)")
        
        performance_results.append({
            "query": query,
            "times": search_times,
            "fastest": min(search_times.values()),
            "slowest": max(search_times.values())
        })
    
    # Performance summary
    print(f"\n📊 Performance Summary:")
    avg_times = {"vector": 0, "graph": 0, "combined": 0}
    
    for result in performance_results:
        for search_type, time_taken in result["times"].items():
            avg_times[search_type] += time_taken
    
    for search_type in avg_times:
        avg_times[search_type] /= len(performance_results)
        print(f"  {search_type.title()} average: {avg_times[search_type]:.3f}s")
    
    fastest_method = min(avg_times.keys(), key=lambda k: avg_times[k])
    print(f"  🏆 Fastest overall: {fastest_method.title()}")


async def main():
    """Advanced GraphRAG query demonstration."""
    print("🔍 Cognee GraphRAG Advanced Query Patterns")
    print("=" * 50)
    
    # Initialize GraphRAG
    print("\n1️⃣  Initializing GraphRAG System")
    config = GraphRAGConfig(
        vector_top_k=10,
        graph_depth=2,
        combine_results=True
    )
    
    graphrag = GraphRAG(config)
    success = await graphrag.initialize()
    
    if not success:
        print("❌ Failed to initialize GraphRAG")
        print("💡 Tip: Run document_processing.py first to populate the system with data")
        return
    
    # Check if we have data
    stats = await graphrag.get_statistics()
    if stats.get("status") == "success":
        db_stats = stats.get("databases", {})
        total_data = sum([
            db_stats.get("sqlite", {}).get("documents", 0),
            db_stats.get("neo4j", {}).get("nodes", 0),
            sum(db_stats.get("lancedb", {}).get("table_rows", {}).values())
        ])
        
        if total_data == 0:
            print("⚠️  No data found in the system")
            print("💡 Run document_processing.py first to add and process documents")
            await graphrag.close()
            return
        
        print(f"✅ Found data in system: {total_data} total items")
    
    # Demonstrate query patterns
    print("\n2️⃣  Demonstrating Query Patterns")
    await demonstrate_query_patterns(graphrag)
    
    # Benchmark performance
    print("\n3️⃣  Performance Benchmarking")
    await benchmark_search_performance(graphrag)
    
    # Advanced analytics
    print("\n4️⃣  Advanced Analytics Example")
    
    # Multi-step reasoning example
    reasoning_query = "How might AI researchers like Geoffrey Hinton influence technology companies like Google?"
    
    print(f"\n🧠 Multi-Step Reasoning: '{reasoning_query}'")
    
    # Step 1: Find AI researchers
    ai_researchers = await graphrag.search("Geoffrey Hinton AI researchers", search_type="graph", top_k=5)
    print(f"  Step 1 - AI Researchers: {len(ai_researchers.get('results', []))} found")
    
    # Step 2: Find technology companies
    tech_companies = await graphrag.search("Google technology companies", search_type="vector", top_k=5)
    print(f"  Step 2 - Tech Companies: {len(tech_companies.get('results', []))} found")
    
    # Step 3: Combined reasoning
    combined_reasoning = await graphrag.search(reasoning_query, search_type="combined", top_k=8)
    print(f"  Step 3 - Combined Analysis: {len(combined_reasoning.get('results', []))} insights")
    
    # Extract key insights
    if combined_reasoning.get("status") == "success":
        entities = QueryAnalyzer.extract_entities(combined_reasoning.get("results", []))
        print(f"  🔑 Key Entities: {', '.join(entities[:5])}")
    
    # Cleanup
    await graphrag.close()
    
    print("\n✅ Advanced query patterns demonstration completed!")
    print("\nKey Insights:")
    print("1. Vector search excels at semantic similarity")
    print("2. Graph search finds related entities and relationships")
    print("3. Combined search provides comprehensive coverage")
    print("4. Multi-step reasoning enables complex analysis")
    print("\nNext: Run mcp_integration.py to test Claude Code integration")


if __name__ == "__main__":
    asyncio.run(main())