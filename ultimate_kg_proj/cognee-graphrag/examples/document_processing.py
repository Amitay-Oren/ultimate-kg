#!/usr/bin/env python3
"""
Document Processing Workflow Examples for Cognee MCP.

This example demonstrates how document processing works through
the Cognee MCP server when using Claude Code. This simulates
the workflow that happens behind the scenes when you use MCP tools.
"""

import asyncio
import tempfile
from pathlib import Path
from typing import List
import os

# Add src to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent))

from src.graphrag import GraphRAG, GraphRAGConfig


def create_sample_documents() -> List[Path]:
    """Create sample documents for processing."""
    
    sample_texts = {
        "ai_research.txt": """
        Artificial Intelligence and Machine Learning Research

        Machine learning is a subset of artificial intelligence that focuses on algorithms 
        that can learn and make decisions from data. Deep learning, a subset of machine 
        learning, uses neural networks with multiple layers to process complex patterns.

        Key researchers in this field include Geoffrey Hinton, who pioneered deep learning 
        techniques, and Yann LeCun, who developed convolutional neural networks. 
        Andrew Ng has made significant contributions to online learning and reinforcement learning.

        The applications of AI are vast, including natural language processing, computer vision, 
        and autonomous vehicles. Companies like OpenAI, Google DeepMind, and Anthropic are 
        leading the development of large language models.

        Current challenges include model interpretability, bias in AI systems, and 
        the computational requirements for training large models.
        """,
        
        "tech_companies.txt": """
        Technology Company Analysis

        Google (Alphabet Inc.) is a multinational technology company specializing in 
        internet services and products. The company was founded by Larry Page and 
        Sergey Brin while they were students at Stanford University.

        Microsoft Corporation is led by CEO Satya Nadella and has been a pioneer in 
        personal computing and cloud services. The company's Azure cloud platform 
        competes directly with Amazon Web Services (AWS).

        Apple Inc., under the leadership of Tim Cook, focuses on consumer electronics 
        and has built a comprehensive ecosystem of devices and services. The company's 
        iPhone revolutionized the smartphone industry.

        Tesla, led by Elon Musk, has disrupted the automotive industry with electric 
        vehicles and autonomous driving technology. The company also operates in 
        energy storage and solar panel manufacturing.
        """,
        
        "scientific_concepts.txt": """
        Scientific Concepts and Relationships

        Quantum mechanics is a fundamental theory in physics that describes the behavior 
        of matter and energy at atomic and subatomic scales. Key principles include 
        wave-particle duality and quantum entanglement.

        Albert Einstein contributed to quantum theory but famously disagreed with some 
        interpretations, stating "God does not play dice with the universe." His work 
        on relativity theory revolutionized our understanding of space and time.

        Marie Curie was a pioneering physicist and chemist who discovered the elements 
        polonium and radium. She was the first woman to win a Nobel Prize and the 
        first person to win Nobel Prizes in two different scientific fields.

        DNA (deoxyribonucleic acid) carries genetic information in living organisms. 
        The double helix structure was discovered by James Watson, Francis Crick, 
        and Rosalind Franklin, revolutionizing molecular biology.
        """
    }
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp(prefix="cognee_docs_"))
    print(f"📁 Creating sample documents in: {temp_dir}")
    
    document_paths = []
    for filename, content in sample_texts.items():
        file_path = temp_dir / filename
        file_path.write_text(content.strip())
        document_paths.append(file_path)
        print(f"✅ Created: {filename}")
    
    return document_paths


async def main():
    """Document processing demonstration."""
    print("📄 Cognee GraphRAG Document Processing Example")
    print("=" * 55)
    
    # Step 1: Create GraphRAG instance
    print("\n1️⃣  Initializing GraphRAG System")
    config = GraphRAGConfig(
        chunk_size=500,  # Smaller chunks for better entity extraction
        chunk_overlap=50,
        max_concurrent_documents=2,
        vector_top_k=10
    )
    
    graphrag = GraphRAG(config)
    success = await graphrag.initialize()
    
    if not success:
        print("❌ Failed to initialize GraphRAG")
        return
    
    # Step 2: Create sample documents
    print("\n2️⃣  Creating Sample Documents")
    document_paths = create_sample_documents()
    
    # Step 3: Add documents to the system
    print("\n3️⃣  Adding Documents to GraphRAG")
    add_result = await graphrag.add_documents(document_paths)
    
    if add_result.get("status") != "success":
        print(f"❌ Failed to add documents: {add_result.get('error')}")
        await graphrag.close()
        return
    
    print(f"✅ Added {add_result.get('documents_added')} documents")
    
    # Step 4: Process documents
    print("\n4️⃣  Processing Documents (Entity & Relationship Extraction)")
    print("⏳ This may take a few minutes depending on document size...")
    
    process_result = await graphrag.process_documents()
    
    if process_result.get("status") != "success":
        print(f"❌ Failed to process documents: {process_result.get('error')}")
        await graphrag.close()
        return
    
    print("✅ Document processing completed!")
    
    # Step 5: Check system statistics
    print("\n5️⃣  System Statistics After Processing")
    stats = await graphrag.get_statistics()
    
    if stats.get("status") == "success":
        print("📊 Updated Database Statistics:")
        for db_name, db_stats in stats.get("databases", {}).items():
            print(f"  {db_name.upper()}:")
            for key, value in db_stats.items():
                print(f"    {key}: {value}")
    
    # Step 6: Test basic searches
    print("\n6️⃣  Testing Search Functionality")
    
    test_queries = [
        "machine learning and AI",
        "Google and technology companies", 
        "quantum mechanics and physics",
        "Nobel Prize winners",
    ]
    
    for query in test_queries:
        print(f"\n🔍 Searching: '{query}'")
        
        # Try vector search
        vector_result = await graphrag.search(query, search_type="vector", top_k=3)
        if vector_result.get("status") == "success":
            results = vector_result.get("results", [])
            print(f"  📈 Vector search: {len(results)} results")
            for i, result in enumerate(results[:2], 1):
                # Display basic info about each result
                result_text = str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
                print(f"    {i}. {result_text}")
        
        # Try combined search
        combined_result = await graphrag.search(query, search_type="combined", top_k=3)
        if combined_result.get("status") == "success":
            results = combined_result.get("results", [])
            vector_count = combined_result.get("vector_count", 0)
            graph_count = combined_result.get("graph_count", 0)
            print(f"  🔗 Combined search: {len(results)} results (V:{vector_count}, G:{graph_count})")
    
    # Step 7: Cleanup
    print("\n7️⃣  Cleanup")
    
    # Remove temporary documents
    for doc_path in document_paths:
        doc_path.unlink()
    document_paths[0].parent.rmdir()
    print("🗑️  Removed temporary documents")
    
    # Close GraphRAG
    await graphrag.close()
    
    print("\n✅ Document processing example completed successfully!")
    print("\nWhat happened:")
    print("1. Sample documents were created with entities and relationships")
    print("2. Documents were added to the GraphRAG system")
    print("3. Cognee processed documents and extracted:")
    print("   - Text chunks stored in LanceDB (vector embeddings)")
    print("   - Entities and relationships stored in Neo4j (knowledge graph)")
    print("   - Metadata and status stored in SQLite (relational data)")
    print("4. Search functionality was tested across all databases")
    print("\nNext: Run graphrag_queries.py for advanced search patterns")


if __name__ == "__main__":
    asyncio.run(main())