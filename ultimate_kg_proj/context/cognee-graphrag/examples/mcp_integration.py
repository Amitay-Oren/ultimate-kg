#!/usr/bin/env python3
"""
MCP (Model Context Protocol) integration example for Cognee GraphRAG.

This example demonstrates:
1. Setting up MCP server configuration
2. Testing MCP tools through Python (simulating Claude Code interaction)
3. GraphRAG operations via MCP protocol
4. Integration patterns with Claude Code
"""

import asyncio
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import time

# Add src to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent))


class MCPSimulator:
    """Simulate MCP interactions for testing."""
    
    def __init__(self):
        self.server_process = None
        self.temp_files = []
    
    def create_mcp_settings(self) -> Path:
        """Create Claude Code MCP settings configuration."""
        
        # Find the cognee-mcp directory (assuming it's in the parent directory structure)
        current_dir = Path(__file__).parent.parent
        possible_paths = [
            current_dir / "cognee" / "cognee-mcp",
            current_dir.parent / "cognee" / "cognee-mcp",
            Path.home() / "cognee" / "cognee-mcp",
        ]
        
        cognee_mcp_path = None
        for path in possible_paths:
            if path.exists():
                cognee_mcp_path = path
                break
        
        if not cognee_mcp_path:
            print("⚠️  Cognee MCP server not found. Please clone and setup:")
            print("   git clone https://github.com/topoteretes/cognee.git")
            print("   cd cognee/cognee-mcp && uv sync")
            return None
        
        settings = {
            "mcpServers": {
                "cognee": {
                    "command": "uv",
                    "args": ["run", "python", str(cognee_mcp_path / "src" / "server.py")],
                    "cwd": str(cognee_mcp_path),
                    "env": {
                        "OPENAI_API_KEY": "${OPENAI_API_KEY}"
                    }
                }
            }
        }
        
        # Create temporary settings file
        settings_file = Path(tempfile.mktemp(suffix="_mcp_settings.json"))
        settings_file.write_text(json.dumps(settings, indent=2))
        self.temp_files.append(settings_file)
        
        return settings_file
    
    def simulate_mcp_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate an MCP tool call."""
        
        print(f"🔧 Simulating MCP tool call: {tool_name}")
        print(f"   Parameters: {json.dumps(parameters, indent=2)}")
        
        # Simulate different tool responses based on Cognee MCP server
        if tool_name == "cognify":
            return {
                "status": "success",
                "message": f"Processed {parameters.get('data', 'unknown')} successfully",
                "entities_extracted": 25,
                "relationships_found": 18,
                "processing_time": "2.3s"
            }
        
        elif tool_name == "search":
            query = parameters.get("query", "")
            search_type = parameters.get("search_type", "combined")
            
            # Simulate search results
            mock_results = [
                {
                    "id": "doc_1",
                    "content": f"Mock result for '{query}' - Content about {query} with relevant information.",
                    "relevance_score": 0.85,
                    "source": "document_1.txt"
                },
                {
                    "id": "entity_1", 
                    "type": "entity",
                    "name": query.split()[0] if query else "Entity",
                    "relationships": ["relates_to", "is_part_of"],
                    "relevance_score": 0.78
                }
            ]
            
            return {
                "status": "success",
                "query": query,
                "search_type": search_type,
                "results": mock_results[:parameters.get("limit", 5)],
                "total_found": len(mock_results)
            }
        
        elif tool_name == "list_data":
            return {
                "status": "success",
                "datasets": [
                    {"name": "ai_research.txt", "size": "2.1KB", "processed": True},
                    {"name": "tech_companies.txt", "size": "1.8KB", "processed": True},
                    {"name": "scientific_concepts.txt", "size": "2.4KB", "processed": True}
                ],
                "total_documents": 3
            }
        
        elif tool_name == "delete":
            return {
                "status": "success",
                "message": f"Deleted {parameters.get('data_id', 'unknown')} successfully",
                "affected_items": 1
            }
        
        elif tool_name == "prune":
            return {
                "status": "success", 
                "message": "Memory reset completed",
                "items_removed": {
                    "documents": 3,
                    "entities": 25,
                    "relationships": 18,
                    "embeddings": 47
                }
            }
        
        elif tool_name == "codify":
            return {
                "status": "success",
                "message": f"Code analysis completed for {parameters.get('repository', 'unknown')}",
                "analysis": {
                    "files_analyzed": 15,
                    "functions_found": 42,
                    "classes_found": 8,
                    "dependencies": ["asyncio", "pathlib", "typing"]
                }
            }
        
        else:
            return {
                "status": "error",
                "message": f"Unknown tool: {tool_name}"
            }
    
    def cleanup(self):
        """Clean up temporary files."""
        for temp_file in self.temp_files:
            try:
                temp_file.unlink()
            except:
                pass


async def demonstrate_mcp_integration():
    """Demonstrate MCP integration patterns."""
    
    print("🔌 MCP Integration Demonstration")
    print("=" * 40)
    
    simulator = MCPSimulator()
    
    try:
        # Step 1: Create MCP configuration
        print("\n1️⃣  Creating MCP Configuration")
        settings_file = simulator.create_mcp_settings()
        
        if settings_file:
            print(f"✅ Created MCP settings at: {settings_file}")
            print("💡 Add this configuration to your Claude Code settings.json")
            
            # Show the configuration
            settings_content = settings_file.read_text()
            print("\n📄 MCP Configuration:")
            print(settings_content)
        else:
            print("⚠️  Could not create MCP configuration")
            return
        
        # Step 2: Simulate MCP tool interactions
        print("\n2️⃣  Simulating MCP Tool Interactions")
        
        # Test cognify tool
        print("\n🧠 Testing 'cognify' tool (document processing):")
        cognify_result = simulator.simulate_mcp_tool_call("cognify", {
            "data": "./examples/sample_documents/",
            "extract_entities": True,
            "build_graph": True
        })
        print(f"   Result: {json.dumps(cognify_result, indent=2)}")
        
        # Test search tool
        print("\n🔍 Testing 'search' tool:")
        search_queries = [
            {"query": "machine learning", "search_type": "vector", "limit": 3},
            {"query": "technology companies", "search_type": "graph", "limit": 3},
            {"query": "AI researchers", "search_type": "combined", "limit": 5}
        ]
        
        for query_params in search_queries:
            search_result = simulator.simulate_mcp_tool_call("search", query_params)
            print(f"   Query: '{query_params['query']}' ({query_params['search_type']})")
            print(f"   Found: {search_result.get('total_found', 0)} results")
        
        # Test list_data tool
        print("\n📋 Testing 'list_data' tool:")
        list_result = simulator.simulate_mcp_tool_call("list_data", {})
        print(f"   Datasets: {list_result.get('total_documents', 0)} documents")
        for dataset in list_result.get('datasets', []):
            print(f"     - {dataset['name']} ({dataset['size']})")
        
        # Test codify tool
        print("\n📝 Testing 'codify' tool (code analysis):")
        codify_result = simulator.simulate_mcp_tool_call("codify", {
            "repository": "./src/",
            "analyze_dependencies": True
        })
        analysis = codify_result.get('analysis', {})
        print(f"   Files analyzed: {analysis.get('files_analyzed', 0)}")
        print(f"   Functions found: {analysis.get('functions_found', 0)}")
        print(f"   Dependencies: {', '.join(analysis.get('dependencies', []))}")
        
        # Step 3: Demonstrate Claude Code integration patterns
        print("\n3️⃣  Claude Code Integration Patterns")
        
        integration_examples = [
            {
                "scenario": "Document Analysis Workflow",
                "claude_prompt": "Analyze the documents in my project and extract key entities",
                "mcp_tools": ["list_data", "cognify", "search"],
                "expected_flow": [
                    "Claude lists available data",
                    "Claude processes documents with cognify",
                    "Claude searches for extracted entities"
                ]
            },
            {
                "scenario": "Research Question Answering",
                "claude_prompt": "What do you know about machine learning researchers?",
                "mcp_tools": ["search"],
                "expected_flow": [
                    "Claude searches with vector similarity",
                    "Claude searches graph relationships", 
                    "Claude combines results for comprehensive answer"
                ]
            },
            {
                "scenario": "Code Repository Analysis",
                "claude_prompt": "Analyze my codebase and find related concepts",
                "mcp_tools": ["codify", "search"],
                "expected_flow": [
                    "Claude analyzes code structure",
                    "Claude searches for related documentation",
                    "Claude provides integrated analysis"
                ]
            }
        ]
        
        for example in integration_examples:
            print(f"\n🎯 Scenario: {example['scenario']}")
            print(f"   User: \"{example['claude_prompt']}\"")
            print(f"   Tools: {', '.join(example['mcp_tools'])}")
            print("   Expected Flow:")
            for i, step in enumerate(example['expected_flow'], 1):
                print(f"     {i}. {step}")
        
        # Step 4: Best practices
        print("\n4️⃣  MCP Integration Best Practices")
        
        best_practices = [
            "✅ Use environment variables for API keys and sensitive config",
            "✅ Implement proper error handling in MCP tool responses", 
            "✅ Provide clear tool descriptions for Claude to understand capabilities",
            "✅ Use structured outputs for better Claude integration",
            "✅ Implement timeout handling for long-running operations",
            "✅ Log MCP interactions for debugging and monitoring",
            "✅ Test MCP tools independently before Claude integration",
            "✅ Use resource URIs for consistent data access patterns"
        ]
        
        for practice in best_practices:
            print(f"   {practice}")
        
        # Step 5: Troubleshooting guide
        print("\n5️⃣  Common Issues & Solutions")
        
        troubleshooting = {
            "Connection Issues": [
                "Check if Cognee MCP server is running",
                "Verify environment variables are set correctly",
                "Ensure network connectivity to databases"
            ],
            "Performance Issues": [
                "Monitor database query execution times",
                "Optimize vector search parameters",
                "Use connection pooling for database access"
            ],
            "Data Issues": [
                "Verify documents are properly processed",
                "Check entity extraction quality",
                "Validate relationship mappings"
            ]
        }
        
        for issue_type, solutions in troubleshooting.items():
            print(f"\n   🚨 {issue_type}:")
            for solution in solutions:
                print(f"     - {solution}")
    
    finally:
        # Cleanup
        simulator.cleanup()
    
    print("\n✅ MCP integration demonstration completed!")
    print("\nNext Steps:")
    print("1. Clone and setup Cognee MCP server")
    print("2. Add MCP configuration to Claude Code settings")
    print("3. Test integration with real Claude Code session")
    print("4. Monitor performance and optimize as needed")


async def main():
    """Main MCP integration example."""
    await demonstrate_mcp_integration()


if __name__ == "__main__":
    asyncio.run(main())