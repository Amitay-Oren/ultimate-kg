#!/usr/bin/env python3
"""
Claude Code Workflow Examples for Cognee MCP.

This file demonstrates common workflows and usage patterns 
when using Cognee through MCP tools in Claude Code.

Note: This is a reference file showing example conversations.
The actual MCP tools are used through Claude Code interface.
"""

import json
from pathlib import Path
from typing import Dict, List, Any


class WorkflowExamples:
    """Examples of Claude Code workflows using Cognee MCP tools."""
    
    def __init__(self):
        self.workflows = self._define_workflows()
    
    def _define_workflows(self) -> Dict[str, Any]:
        """Define common workflow patterns."""
        
        return {
            "document_analysis": {
                "name": "Document Analysis Workflow",
                "description": "Process and analyze documents to extract insights",
                "steps": [
                    {
                        "user": "Process the research papers in ./documents/ using cognify",
                        "claude_action": "Uses cognify tool",
                        "expected_result": "Documents processed, entities extracted, stored in knowledge base"
                    },
                    {
                        "user": "What are the main themes in machine learning research?",
                        "claude_action": "Uses search tool with vector similarity",
                        "expected_result": "Identifies key themes like deep learning, reinforcement learning, etc."
                    },
                    {
                        "user": "Show me connections between different research groups",
                        "claude_action": "Uses search tool with graph traversal",
                        "expected_result": "Maps relationships between researchers and institutions"
                    }
                ],
                "tools_used": ["cognify", "search"],
                "databases_involved": ["Neo4j", "LanceDB", "SQLite"]
            },
            
            "knowledge_extraction": {
                "name": "Knowledge Extraction from Code",
                "description": "Analyze codebase structure and extract knowledge",
                "steps": [
                    {
                        "user": "Analyze the Python codebase in ./src/ using codify",
                        "claude_action": "Uses codify tool",
                        "expected_result": "Code structure analyzed, functions and classes mapped"
                    },
                    {
                        "user": "What are the main dependencies in this project?",
                        "claude_action": "Uses search tool to find dependency information",
                        "expected_result": "Lists key dependencies and their relationships"
                    },
                    {
                        "user": "Find functions that handle database operations",
                        "claude_action": "Uses search with code-specific queries",
                        "expected_result": "Identifies database-related functions and their usage"
                    }
                ],
                "tools_used": ["codify", "search"],
                "databases_involved": ["Neo4j", "SQLite"]
            },
            
            "research_synthesis": {
                "name": "Research Paper Synthesis",
                "description": "Synthesize information across multiple research papers",
                "steps": [
                    {
                        "user": "Process all papers in ./research_library/ with cognify",
                        "claude_action": "Uses cognify tool on document collection",
                        "expected_result": "Large document collection processed and indexed"
                    },
                    {
                        "user": "What are the latest trends in transformer architectures?",
                        "claude_action": "Uses search with temporal and topic filters",
                        "expected_result": "Identifies recent developments in transformer research"
                    },
                    {
                        "user": "Compare different attention mechanisms across papers",
                        "claude_action": "Uses combined search to find and compare concepts",
                        "expected_result": "Comparative analysis of attention mechanisms"
                    },
                    {
                        "user": "Create a timeline of important developments",
                        "claude_action": "Uses graph queries to build temporal relationships",
                        "expected_result": "Chronological timeline of research developments"
                    }
                ],
                "tools_used": ["cognify", "search", "list_data"],
                "databases_involved": ["Neo4j", "LanceDB", "SQLite"]
            },
            
            "data_management": {
                "name": "Knowledge Base Management",
                "description": "Manage and maintain the knowledge base",
                "steps": [
                    {
                        "user": "Show me what data is currently in the system",
                        "claude_action": "Uses list_data tool",
                        "expected_result": "Overview of processed documents and datasets"
                    },
                    {
                        "user": "Remove outdated documents from last year",
                        "claude_action": "Uses delete tool with date filters",
                        "expected_result": "Specified documents removed from knowledge base"
                    },
                    {
                        "user": "Reset the entire knowledge base for fresh start",
                        "claude_action": "Uses prune tool",
                        "expected_result": "All data cleared from databases"
                    }
                ],
                "tools_used": ["list_data", "delete", "prune"],
                "databases_involved": ["Neo4j", "LanceDB", "SQLite"]
            },
            
            "hybrid_search": {
                "name": "Advanced Hybrid Search Patterns",
                "description": "Complex search strategies combining multiple approaches",
                "steps": [
                    {
                        "user": "Find documents about neural networks but also show related concepts",
                        "claude_action": "Uses search tool with combined vector + graph strategy",
                        "expected_result": "Neural network docs plus related concepts like backpropagation, CNNs"
                    },
                    {
                        "user": "What research connects computer vision and natural language processing?",
                        "claude_action": "Uses graph search to find interdisciplinary connections",
                        "expected_result": "Papers on multimodal models, vision-language transformers"
                    },
                    {
                        "user": "Show me the research ecosystem around attention mechanisms",
                        "claude_action": "Uses graph traversal with multiple hops",
                        "expected_result": "Network of related concepts, researchers, and applications"
                    }
                ],
                "tools_used": ["search"],
                "databases_involved": ["Neo4j", "LanceDB"]
            }
        }
    
    def print_workflow(self, workflow_name: str):
        """Print a specific workflow example."""
        if workflow_name not in self.workflows:
            print(f"❌ Workflow '{workflow_name}' not found")
            return
        
        workflow = self.workflows[workflow_name]
        
        print(f"🔄 {workflow['name']}")
        print("=" * (len(workflow['name']) + 3))
        print(f"📋 {workflow['description']}")
        print()
        
        print("💬 Example Conversation:")
        for i, step in enumerate(workflow['steps'], 1):
            print(f"\n{i}. You: \"{step['user']}\"")
            print(f"   Claude: {step['claude_action']}")
            print(f"   Result: {step['expected_result']}")
        
        print(f"\n🛠️  Tools Used: {', '.join(workflow['tools_used'])}")
        print(f"🗄️  Databases: {', '.join(workflow['databases_involved'])}")
    
    def print_all_workflows(self):
        """Print all workflow examples."""
        print("🤖 Claude Code + Cognee MCP Workflow Examples")
        print("=" * 50)
        print()
        
        for name, workflow in self.workflows.items():
            self.print_workflow(name)
            print("\n" + "-" * 50 + "\n")
    
    def save_workflows_as_json(self, output_file: str = "workflows.json"):
        """Save workflows as JSON for reference."""
        output_path = Path(output_file)
        output_path.write_text(json.dumps(self.workflows, indent=2))
        print(f"💾 Workflows saved to: {output_path}")


def demonstrate_mcp_tool_patterns():
    """Show common MCP tool usage patterns."""
    
    print("🔧 Common MCP Tool Patterns")
    print("=" * 35)
    
    patterns = {
        "cognify": {
            "description": "Process documents into knowledge base",
            "examples": [
                "Use cognify to process documents in ./papers/",
                "Process the PDF files in ./research/ with cognify",
                "Use cognify on the text files in this directory"
            ],
            "parameters": [
                "data: File path or directory to process",
                "extract_entities: Boolean to extract entities (default: true)",
                "build_graph: Boolean to build knowledge graph (default: true)"
            ]
        },
        
        "search": {
            "description": "Query the knowledge base",
            "examples": [
                "Search for information about machine learning algorithms",
                "Find connections between neural networks and deep learning",
                "Search the knowledge base for papers about transformers"
            ],
            "parameters": [
                "query: Search query string",
                "search_type: 'vector', 'graph', or 'combined'",
                "limit: Maximum number of results"
            ]
        },
        
        "codify": {
            "description": "Analyze code repositories",
            "examples": [
                "Use codify to analyze the Python code in ./src/",
                "Analyze the repository structure with codify",
                "Process the codebase using codify to extract dependencies"
            ],
            "parameters": [
                "repository: Path to code repository",
                "analyze_dependencies: Boolean to extract dependencies"
            ]
        },
        
        "list_data": {
            "description": "Show available datasets",
            "examples": [
                "List all processed documents",
                "Show me what data is in the knowledge base",
                "What datasets are currently available?"
            ],
            "parameters": []
        }
    }
    
    for tool_name, info in patterns.items():
        print(f"\n🛠️  {tool_name.upper()}")
        print(f"   {info['description']}")
        print("   Examples:")
        for example in info['examples']:
            print(f"   • \"{example}\"")
        if info['parameters']:
            print("   Parameters:")
            for param in info['parameters']:
                print(f"   • {param}")


def create_troubleshooting_guide():
    """Create a troubleshooting guide for common MCP issues."""
    
    print("🚨 Troubleshooting Common Issues")
    print("=" * 40)
    
    issues = {
        "Claude Code can't find MCP tools": {
            "symptoms": [
                "No cognee tools appear in Claude Code",
                "MCP server not connecting",
                "Tools list is empty"
            ],
            "solutions": [
                "Check that MCP server is running: ps aux | grep server.py",
                "Verify settings.json path and configuration",
                "Ensure 'cwd' in settings.json points to cognee-mcp directory",
                "Restart Claude Code after changing settings"
            ]
        },
        
        "cognify tool fails to process documents": {
            "symptoms": [
                "Error when processing documents",
                "No entities extracted",
                "Database connection errors"
            ],
            "solutions": [
                "Check that document path exists and is accessible",
                "Verify database connections (Neo4j running, etc.)",
                "Check LLM_API_KEY is set correctly",
                "Look at MCP server logs for specific errors"
            ]
        },
        
        "search tool returns no results": {
            "symptoms": [
                "Empty search results",
                "No matches found for queries",
                "Search appears to work but finds nothing"
            ],
            "solutions": [
                "Ensure documents have been processed with cognify first",
                "Check that knowledge base contains relevant data using list_data",
                "Try different search types (vector vs graph vs combined)",
                "Verify embeddings are being generated correctly"
            ]
        },
        
        "Performance is slow": {
            "symptoms": [
                "MCP tools take long time to respond",
                "Document processing is very slow",
                "Search queries timeout"
            ],
            "solutions": [
                "Check database performance (Neo4j memory, etc.)",
                "Optimize embedding model choice",
                "Process documents in smaller batches",
                "Monitor system resources during operations"
            ]
        }
    }
    
    for issue, details in issues.items():
        print(f"\n❌ {issue}")
        print("   Symptoms:")
        for symptom in details['symptoms']:
            print(f"   • {symptom}")
        print("   Solutions:")
        for solution in details['solutions']:
            print(f"   • {solution}")


def main():
    """Main function to demonstrate all examples."""
    
    # Show workflow examples
    examples = WorkflowExamples()
    examples.print_all_workflows()
    
    # Show tool patterns
    demonstrate_mcp_tool_patterns()
    
    # Show troubleshooting
    create_troubleshooting_guide()
    
    # Save workflows for reference
    examples.save_workflows_as_json("cognee_workflows.json")
    
    print("\n🎯 Summary")
    print("=" * 15)
    print("This file shows example workflows for using Cognee through Claude Code.")
    print("The actual interactions happen in Claude Code using the MCP tools.")
    print("Use these patterns as a guide for your own document analysis workflows.")


if __name__ == "__main__":
    main()