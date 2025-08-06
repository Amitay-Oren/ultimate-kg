"""
Knowledge Graph Agent with MCP Integration

This module implements the main KG Agent that interfaces with Cognee GraphRAG
system via MCP tools and coordinates multi-agent workflows.
"""

import asyncio
import logging
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams
from google.genai import types

from config import config

# Configure logging
logger = logging.getLogger(__name__)

# KG Agent instruction prompt
KG_AGENT_PROMPT = """You are the Knowledge Graph Coordinator, an intelligent agent that manages knowledge processing through MCP tools connected to a Cognee GraphRAG system.

Your primary responsibilities:
1. **Data Processing**: Use the 'cognify' tool to process and store various data formats (text, JSON, PDF, CSV) into the knowledge graph
2. **Knowledge Search**: Use the 'search' tool to query existing knowledge across multiple databases (Neo4j, LanceDB, SQLite)
3. **Code Analysis**: Use the 'codify' tool to analyze code repositories and extract dependency relationships
4. **Data Management**: Use 'list_data', 'delete', and 'prune' tools for knowledge lifecycle management
5. **Connection Detection**: Analyze relationships between new and existing knowledge to identify interesting connections

Available MCP Tools:
- cognify: Process documents/data into knowledge graphs
- search: Query knowledge base with semantic, graph, and hybrid search
- codify: Analyze code repositories for dependencies and relationships
- list_data: Show processed datasets and their status
- delete: Remove specific data entries from the knowledge base
- prune: Reset/clean the entire knowledge base

When processing data:
1. First use 'cognify' to store the data in the knowledge graph
2. Then use 'search' to find related existing knowledge
3. Analyze connections and relationships
4. Report findings with relevance scores

Always provide structured responses with:
- Processing status and results
- Facts extracted or knowledge found
- Connections detected with relevance scores
- Recommendations for further processing

Be thorough in analyzing connections but concise in responses. Focus on actionable insights and meaningful relationships.
"""

class KnowledgeGraphAgent:
    """
    Knowledge Graph Agent that coordinates GraphRAG operations via MCP tools.
    
    This agent serves as the main interface between the A2A server and the
    Cognee GraphRAG system, handling data processing, search, and connection detection.
    """
    
    def __init__(self):
        self.toolset: Optional[MCPToolset] = None
        self.agent: Optional[LlmAgent] = None
        self.runner: Optional[Runner] = None
        self.session_service: Optional[InMemorySessionService] = None
        self.session = None
        self.initialized = False
        self.processing_stats = {
            "requests_processed": 0,
            "data_items_processed": 0,
            "searches_performed": 0,
            "connections_detected": 0,
            "last_activity": None
        }
        
    async def initialize(self):
        """Initialize KG Agent with MCP toolset and Google ADK components"""
        logger.info("Initializing Knowledge Graph Agent")
        
        try:
            # Create MCP toolset for Cognee GraphRAG operations
            self.toolset = MCPToolset(
                connection_params=SseConnectionParams(url=config.mcp.server_url)
            )
            
            # Create LLM Agent with knowledge graph capabilities
            self.agent = LlmAgent(
                #model=config.google_cloud.model,
                model="gemini-2.0-flash",
                name='kg_coordinator',
                instruction=KG_AGENT_PROMPT,
                tools=[self.toolset]
            )
            
            # Create session service for agent execution
            self.session_service = InMemorySessionService()
            
            # Create session
            self.session = await self.session_service.create_session(
                state={}, 
                app_name='agentic_graphrag',
                user_id='system'
            )
            
            # Create runner for agent execution
            self.runner = Runner(
                app_name='agentic_graphrag',
                agent=self.agent,
                session_service=self.session_service
            )
            
            self.initialized = True
            logger.info("Knowledge Graph Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Knowledge Graph Agent: {e}")
            raise
    
    async def process_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the knowledge graph pipeline.
        
        Args:
            request_data: Dictionary containing data, format, and options
            
        Returns:
            Processing results with facts, connections, and statistics
        """
        if not self.initialized:
            raise RuntimeError("KG Agent not initialized")
        
        start_time = datetime.now()
        self.processing_stats["requests_processed"] += 1
        self.processing_stats["last_activity"] = start_time.isoformat()
        
        try:
            data = request_data.get("data", "")
            data_format = request_data.get("format", "text")
            options = request_data.get("options", {})
            
            extract_facts = options.get("extract_facts", True)
            detect_connections = options.get("detect_connections", True)
            notify_threshold = options.get("notify_threshold", config.notifications.threshold)
            
            logger.info(f"Processing data: format={data_format}, extract_facts={extract_facts}, detect_connections={detect_connections}")
            
            # Construct processing instruction
            processing_instruction = f"""
            Process the following {data_format} data using the available MCP tools:
            
            Data: {data}
            
            Instructions:
            1. Use the 'cognify' tool to process and store this data in the knowledge graph
            2. {"Extract facts and entities from the data" if extract_facts else "Store data without detailed fact extraction"}
            3. {"Use 'search' to find related existing knowledge and detect connections" if detect_connections else "Skip connection detection"}
            4. {"Score connections and highlight those above " + str(notify_threshold) + " relevance" if detect_connections else ""}
            5. Provide a structured summary of the processing results
            
            Return a JSON response with:
            - processing_status: success/error
            - facts_extracted: number of facts processed
            - storage_result: results from cognify operation
            - connections_found: number of connections detected (if enabled)
            - high_relevance_connections: connections above threshold (if enabled)
            - processing_time: time taken
            """
            
            # Execute agent processing
            content = types.Content(role='user', parts=[types.Part(text=processing_instruction)])
            
            events_async = self.runner.run_async(
                session_id=self.session.id,
                user_id=self.session.user_id,
                new_message=content
            )
            
            # Collect agent response
            response_text = ""
            async for event in events_async:
                if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text += part.text
            
            # Parse agent response
            try:
                # Try to extract JSON from response
                if "{" in response_text:
                    json_start = response_text.find("{")
                    json_end = response_text.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        agent_result = json.loads(response_text[json_start:json_end])
                    else:
                        raise ValueError("No valid JSON found")
                else:
                    raise ValueError("No JSON in response")
            except (json.JSONDecodeError, ValueError):
                # Fallback: create structured response from text
                agent_result = {
                    "processing_status": "completed",
                    "facts_extracted": 0,
                    "storage_result": response_text,
                    "connections_found": 0,
                    "high_relevance_connections": [],
                    "raw_response": response_text
                }
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Update statistics
            self.processing_stats["data_items_processed"] += 1
            if detect_connections:
                connections_found = agent_result.get("connections_found", 0)
                self.processing_stats["connections_detected"] += connections_found
            
            # Build final response
            result = {
                "status": agent_result.get("processing_status", "completed"),
                "facts_extracted": agent_result.get("facts_extracted", 0),
                "storage_result": agent_result.get("storage_result", "Data processed successfully"),
                "connections_found": agent_result.get("connections_found", 0) if detect_connections else 0,
                "high_relevance_connections": agent_result.get("high_relevance_connections", []) if detect_connections else [],
                "processing_time": processing_time,
                "processed_at": start_time.isoformat(),
                "agent_response": response_text[:500] + "..." if len(response_text) > 500 else response_text
            }
            
            # Add notification trigger if high relevance connections found
            if detect_connections and result["high_relevance_connections"]:
                result["notifications_sent"] = len(result["high_relevance_connections"])
            else:
                result["notifications_sent"] = 0
            
            logger.info(f"Data processing completed: {result['facts_extracted']} facts, {result['connections_found']} connections")
            return result
            
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            return {
                "status": "error",
                "error": str(e),
                "facts_extracted": 0,
                "connections_found": 0,
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "processed_at": start_time.isoformat()
            }
    
    async def search_knowledge(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search the knowledge graph using various strategies.
        
        Args:
            request_data: Dictionary containing query, type, limit, and filters
            
        Returns:
            Search results with metadata
        """
        if not self.initialized:
            raise RuntimeError("KG Agent not initialized")
        
        start_time = datetime.now()
        self.processing_stats["searches_performed"] += 1
        self.processing_stats["last_activity"] = start_time.isoformat()
        
        try:
            query = request_data.get("query", "")
            search_type = request_data.get("type", "hybrid")
            limit = min(request_data.get("limit", 10), 100)  # Cap at 100
            filters = request_data.get("filters", {})
            
            logger.info(f"Searching knowledge: query='{query}', type={search_type}, limit={limit}")
            
            # Construct search instruction
            search_instruction = f"""
            Search the knowledge graph using the 'search' MCP tool with the following parameters:
            
            Query: "{query}"
            Search Type: {search_type}
            Limit: {limit}
            Filters: {json.dumps(filters) if filters else "None"}
            
            Instructions:
            1. Use the 'search' tool to query the knowledge base
            2. Include semantic similarity, graph relationships, and metadata
            3. Rank results by relevance to the query
            4. Provide context and explanation for each result
            
            Return a JSON response with:
            - search_status: success/error
            - results: array of search results with scores and context
            - total_count: total number of results found
            - search_strategy: actual search strategy used
            - related_concepts: related concepts that might interest the user
            """
            
            # Execute agent search
            content = types.Content(role='user', parts=[types.Part(text=search_instruction)])
            
            events_async = self.runner.run_async(
                session_id=self.session.id,
                user_id=self.session.user_id,
                new_message=content
            )
            
            # Collect agent response
            response_text = ""
            async for event in events_async:
                if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text += part.text
            
            # Parse agent response
            try:
                if "{" in response_text:
                    json_start = response_text.find("{")
                    json_end = response_text.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        agent_result = json.loads(response_text[json_start:json_end])
                    else:
                        raise ValueError("No valid JSON found")
                else:
                    raise ValueError("No JSON in response")
            except (json.JSONDecodeError, ValueError):
                # Fallback: create structured response
                agent_result = {
                    "search_status": "completed",
                    "results": [{"content": response_text, "score": 0.5, "source": "agent_response"}],
                    "total_count": 1,
                    "search_strategy": search_type,
                    "related_concepts": []
                }
            
            # Calculate search time
            search_time = (datetime.now() - start_time).total_seconds()
            
            # Build final response
            result = {
                "results": agent_result.get("results", []),
                "total_count": agent_result.get("total_count", len(agent_result.get("results", []))),
                "search_time": search_time,
                "search_type": agent_result.get("search_strategy", search_type),
                "query": query,
                "searched_at": start_time.isoformat(),
                "related_concepts": agent_result.get("related_concepts", []),
                "agent_response": response_text[:300] + "..." if len(response_text) > 300 else response_text
            }
            
            logger.info(f"Search completed: {result['total_count']} results in {search_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error searching knowledge: {e}")
            return {
                "results": [],
                "total_count": 0,
                "search_time": (datetime.now() - start_time).total_seconds(),
                "search_type": search_type,
                "query": query,
                "error": str(e),
                "searched_at": start_time.isoformat()
            }
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current status of the KG Agent"""
        return {
            "initialized": self.initialized,
            "mcp_server_url": config.mcp.server_url,
            #"model": config.google_cloud.model,
            "model": "gemini-2.0-flash",
            "statistics": self.processing_stats.copy(),
            "tools_available": ["cognify", "search", "codify", "list_data", "delete", "prune"] if self.initialized else []
        }
    
    async def list_knowledge_data(self) -> Dict[str, Any]:
        """List all data in the knowledge base"""
        if not self.initialized:
            raise RuntimeError("KG Agent not initialized")
        
        try:
            instruction = "Use the 'list_data' MCP tool to show all processed datasets and their status. Provide a comprehensive overview of the knowledge base contents."
            
            content = types.Content(role='user', parts=[types.Part(text=instruction)])
            
            events_async = self.runner.run_async(
                session_id=self.session.id,
                user_id=self.session.user_id,
                new_message=content
            )
            
            response_text = ""
            async for event in events_async:
                if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text += part.text
            
            return {
                "status": "success",
                "data_overview": response_text,
                "retrieved_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error listing knowledge data: {e}")
            return {
                "status": "error",
                "error": str(e),
                "retrieved_at": datetime.now().isoformat()
            }
    
    async def cleanup(self):
        """Clean up resources"""
        if self.toolset:
            try:
                await self.toolset.close()
                logger.info("MCP toolset connection closed")
            except Exception as e:
                logger.error(f"Error closing MCP toolset: {e}")
        
        self.initialized = False