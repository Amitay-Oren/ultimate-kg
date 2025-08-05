## FEATURE:

- Agentic GraphRAG system built with Google ADK agents exposed via A2A Protocol endpoints
- KG Agent that interfaces with Cognee GraphRAG system (Neo4j + LanceDB + SQLite) for unified knowledge storage
- Fact extraction agents that parse unstructured data (documents, chat, facts) into structured triplets and relationships
- Automatic connection detection between new data and existing knowledge graph
- A2A-compatible endpoints for external scouting systems to feed data
- Notification system that alerts users when interesting connections are discovered

## EXAMPLES:

In the `cognee-graphrag/` and `google-adk/` folders, there are working implementations to understand:

- `cognee-graphrag/examples/mcp_server_setup.py` - Complete MCP setup for GraphRAG system
- `cognee-graphrag/config/` - Multi-database configuration patterns (Neo4j, LanceDB, SQLite)
- `google-adk/examples/kg_broker_agent/` - Agent that interfaces with knowledge graphs via MCP
- `google-adk/examples/orchestrator_agent/` - Multi-agent coordination patterns
- `google-adk/examples/parallel_extraction_system/` - Parallel fact extraction workflows

Don't copy these examples directly, but use them to understand GraphRAG integration patterns, agent coordination, and MCP tool usage.

## DOCUMENTATION:

**A2A Protocol:**
- https://a2a-protocol.org/latest/ - A2A Protocol specification and overview
- https://a2a-protocol.org/latest/tutorials/python - Python implementation tutorials
- https://github.com/a2aproject/a2a-python - A2A Python SDK documentation
- https://github.com/a2aproject/a2a-samples/tree/main/samples/python - Python A2A examples

**Google ADK:**
- https://google.github.io/adk-docs/ - Official Google ADK documentation
- https://github.com/google/adk-samples/tree/main/python - Google ADK Python examples

**Cognee GraphRAG:**
- https://docs.cognee.ai/ - Cognee documentation for knowledge graph operations
- https://spec.modelcontextprotocol.io/ - MCP specification for tool integration

## OTHER CONSIDERATIONS:

- Include A2A server setup with proper agent endpoint configuration using the A2A Python SDK
- KG Agent should handle both read (search) and write (cognify) operations to the GraphRAG system
- Fact extraction agents should support multiple input formats: large documents, chat messages, structured data, web content
- Connection detection should automatically create relationships and trigger notifications when connections exceed relevance threshold
- Include proper error handling for A2A protocol communication and GraphRAG system failures
- Use environment-based configuration for database connections, API keys, and A2A server settings
- Include example scouting system integration showing how external systems send data to A2A endpoints
- Notification system should support multiple channels (console, file, webhook) for connection alerts
- Virtual environment and dependency management using standard Python practices
- Use python-dotenv for environment variable management across A2A servers and ADK agents