"""
Unit tests for A2A Server functionality.

These tests validate the A2A server implementation, endpoint registration,
request handling, and protocol compliance.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from agentic_graphrag.server.a2a_server import AgenticGraphRAGServer
from agentic_graphrag.config import config

@pytest.fixture
async def a2a_server():
    """Create a test A2A server instance"""
    server = AgenticGraphRAGServer()
    await server.initialize()
    yield server
    await server.shutdown()

@pytest.fixture
def mock_kg_agent():
    """Create a mock KG agent"""
    agent = Mock()
    agent.process_data = AsyncMock(return_value={
        "status": "success",
        "facts_extracted": 5,
        "connections_found": 3,
        "processing_time": 1.5,
        "notifications_sent": 1
    })
    agent.search_knowledge = AsyncMock(return_value={
        "results": [{"content": "test result", "score": 0.85}],
        "total_count": 1,
        "search_time": 0.5
    })
    agent.get_status = AsyncMock(return_value={
        "initialized": True,
        "model": "gemini-2.0-flash"
    })
    return agent

class TestA2AServerInitialization:
    """Test A2A server initialization and setup"""
    
    @pytest.mark.asyncio
    async def test_server_initialization(self):
        """Test basic server initialization"""
        server = AgenticGraphRAGServer()
        
        # Before initialization
        assert server.server is None
        assert server.kg_agent is None
        assert len(server.registered_agents) == 0
        
        # Initialize
        await server.initialize()
        
        # After initialization
        assert server.server is not None
        assert len(server.registered_agents) == 3  # kg_ingest, kg_search, kg_status
        assert "kg_ingest" in server.registered_agents
        assert "kg_search" in server.registered_agents
        assert "kg_status" in server.registered_agents
        
        await server.shutdown()
    
    @pytest.mark.asyncio
    async def test_agent_registration(self, a2a_server):
        """Test agent endpoint registration"""
        registered_agents = a2a_server.registered_agents
        
        # Check all required agents are registered
        assert "kg_ingest" in registered_agents
        assert "kg_search" in registered_agents
        assert "kg_status" in registered_agents
        
        # Check agent capabilities
        kg_ingest = registered_agents["kg_ingest"]
        assert kg_ingest["capabilities"].agent_id == "kg_ingest"
        assert "document_processing" in kg_ingest["capabilities"].capabilities
        assert "fact_extraction" in kg_ingest["capabilities"].capabilities
        
    @pytest.mark.asyncio
    async def test_kg_agent_connection(self, a2a_server, mock_kg_agent):
        """Test KG agent connection to A2A server"""
        # Before connection
        assert a2a_server.kg_agent is None
        
        # Connect KG agent
        a2a_server.set_kg_agent(mock_kg_agent)
        
        # After connection
        assert a2a_server.kg_agent is not None
        assert a2a_server.kg_agent == mock_kg_agent

class TestKnowledgeIngestion:
    """Test knowledge ingestion endpoint"""
    
    @pytest.mark.asyncio
    async def test_valid_ingestion_request(self, a2a_server, mock_kg_agent):
        """Test valid knowledge ingestion request"""
        a2a_server.set_kg_agent(mock_kg_agent)
        
        # Create mock request
        request = Mock()
        request.id = "test-request-1"
        request.content = Mock()
        request.content.text = json.dumps({
            "data": "Alice is a software engineer at Google",
            "format": "text",
            "options": {"extract_facts": True, "detect_connections": True}
        })
        
        # Handle request
        response = await a2a_server.handle_knowledge_ingestion(request)
        
        # Verify response
        assert response.status == "success"
        assert response.request_id == "test-request-1"
        
        # Verify KG agent was called
        mock_kg_agent.process_data.assert_called_once()
        call_args = mock_kg_agent.process_data.call_args[0][0]
        assert call_args["data"] == "Alice is a software engineer at Google"
        assert call_args["format"] == "text"
    
    @pytest.mark.asyncio
    async def test_invalid_ingestion_request(self, a2a_server):
        """Test invalid knowledge ingestion request"""
        # Create mock request without content
        request = Mock()
        request.id = "test-request-2"
        request.content = None
        
        # Handle request
        response = await a2a_server.handle_knowledge_ingestion(request)
        
        # Verify error response
        assert response.status == "error"
        assert response.request_id == "test-request-2"
        assert "Missing request content" in response.content.text
    
    @pytest.mark.asyncio
    async def test_ingestion_without_kg_agent(self, a2a_server):
        """Test ingestion request when KG agent is not available"""
        # Create valid request but no KG agent
        request = Mock()
        request.id = "test-request-3"
        request.content = Mock()
        request.content.text = json.dumps({"data": "test data", "format": "text"})
        
        # Handle request
        response = await a2a_server.handle_knowledge_ingestion(request)
        
        # Verify error response
        assert response.status == "error"
        assert "Knowledge Graph agent not available" in response.content.text

class TestKnowledgeSearch:
    """Test knowledge search endpoint"""
    
    @pytest.mark.asyncio
    async def test_valid_search_request(self, a2a_server, mock_kg_agent):
        """Test valid knowledge search request"""
        a2a_server.set_kg_agent(mock_kg_agent)
        
        # Create mock request
        request = Mock()
        request.id = "test-search-1"
        request.content = Mock()
        request.content.text = json.dumps({
            "query": "software engineer",
            "type": "semantic",
            "limit": 10
        })
        
        # Handle request
        response = await a2a_server.handle_knowledge_search(request)
        
        # Verify response
        assert response.status == "success"
        assert response.request_id == "test-search-1"
        
        # Verify KG agent was called
        mock_kg_agent.search_knowledge.assert_called_once()
        call_args = mock_kg_agent.search_knowledge.call_args[0][0]
        assert call_args["query"] == "software engineer"
        assert call_args["type"] == "semantic"
    
    @pytest.mark.asyncio
    async def test_search_without_query(self, a2a_server, mock_kg_agent):
        """Test search request without query"""
        a2a_server.set_kg_agent(mock_kg_agent)
        
        # Create request without query
        request = Mock()
        request.id = "test-search-2"
        request.content = Mock()
        request.content.text = json.dumps({"type": "semantic"})
        
        # Handle request
        response = await a2a_server.handle_knowledge_search(request)
        
        # Verify error response
        assert response.status == "error"
        assert "Missing 'query' field" in response.content.text

class TestSystemStatus:
    """Test system status endpoint"""
    
    @pytest.mark.asyncio
    async def test_basic_status_request(self, a2a_server):
        """Test basic system status request"""
        # Create basic status request
        request = Mock()
        request.id = "test-status-1"
        request.content = Mock()
        request.content.text = "{}"
        
        # Handle request
        response = await a2a_server.handle_system_status(request)
        
        # Verify response
        assert response.status == "success"
        response_data = json.loads(response.content.text)
        assert response_data["status"] == "healthy"
        assert "uptime" in response_data
        assert "version" in response_data
    
    @pytest.mark.asyncio
    async def test_detailed_status_request(self, a2a_server, mock_kg_agent):
        """Test detailed system status request"""
        a2a_server.set_kg_agent(mock_kg_agent)
        
        # Create detailed status request
        request = Mock()
        request.id = "test-status-2"
        request.content = Mock()
        request.content.text = json.dumps({"detailed": True})
        
        # Handle request
        response = await a2a_server.handle_system_status(request)
        
        # Verify response
        assert response.status == "success"
        response_data = json.loads(response.content.text)
        assert "registered_agents" in response_data
        assert "configuration" in response_data
        assert "kg_agent_status" in response_data

class TestServerInfo:
    """Test server information and statistics"""
    
    @pytest.mark.asyncio
    async def test_server_info(self, a2a_server):
        """Test server information retrieval"""
        info = a2a_server.get_server_info()
        
        # Verify basic info
        assert "server_host" in info
        assert "server_port" in info
        assert "network_mode" in info
        assert "protocol_version" in info
        assert "uptime" in info
        assert "registered_agents" in info
        assert info["registered_agents"] == 3  # kg_ingest, kg_search, kg_status
    
    @pytest.mark.asyncio
    async def test_request_counting(self, a2a_server, mock_kg_agent):
        """Test that requests are properly counted"""
        a2a_server.set_kg_agent(mock_kg_agent)
        
        initial_count = a2a_server.request_count
        
        # Make a request
        request = Mock()
        request.id = "test-count"
        request.content = Mock()
        request.content.text = json.dumps({"data": "test", "format": "text"})
        
        await a2a_server.handle_knowledge_ingestion(request)
        
        # Verify count increased
        assert a2a_server.request_count == initial_count + 1
        
        # Check agent-specific counts
        assert a2a_server.registered_agents["kg_ingest"]["requests"] == 1

class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.mark.asyncio
    async def test_kg_agent_error_handling(self, a2a_server):
        """Test handling of KG agent errors"""
        # Create mock KG agent that raises exception
        mock_kg_agent = Mock()
        mock_kg_agent.process_data = AsyncMock(side_effect=Exception("Processing failed"))
        a2a_server.set_kg_agent(mock_kg_agent)
        
        # Create request
        request = Mock()
        request.id = "test-error"
        request.content = Mock()
        request.content.text = json.dumps({"data": "test", "format": "text"})
        
        # Handle request
        response = await a2a_server.handle_knowledge_ingestion(request)
        
        # Verify error response
        assert response.status == "error"
        assert "Processing failed" in response.content.text
    
    @pytest.mark.asyncio
    async def test_malformed_json_handling(self, a2a_server, mock_kg_agent):
        """Test handling of malformed JSON requests"""
        a2a_server.set_kg_agent(mock_kg_agent)
        
        # Create request with malformed JSON
        request = Mock()
        request.id = "test-malformed"
        request.content = Mock()
        request.content.text = "{ invalid json }"
        
        # Handle request - should fallback to treating as text
        response = await a2a_server.handle_knowledge_ingestion(request)
        
        # Should still work with fallback handling
        assert response.status == "success"
        
        # Verify fallback data was used
        mock_kg_agent.process_data.assert_called_once()
        call_args = mock_kg_agent.process_data.call_args[0][0]
        assert call_args["data"] == "{ invalid json }"
        assert call_args["format"] == "text"

@pytest.mark.integration
class TestA2AIntegration:
    """Integration tests for A2A server functionality"""
    
    @pytest.mark.asyncio
    async def test_complete_workflow(self, a2a_server, mock_kg_agent):
        """Test complete workflow from ingestion to search"""
        a2a_server.set_kg_agent(mock_kg_agent)
        
        # Step 1: Ingest data
        ingest_request = Mock()
        ingest_request.id = "workflow-ingest"
        ingest_request.content = Mock()
        ingest_request.content.text = json.dumps({
            "data": "John Doe is a data scientist at TechCorp",
            "format": "text",
            "options": {"extract_facts": True, "detect_connections": True}
        })
        
        ingest_response = await a2a_server.handle_knowledge_ingestion(ingest_request)
        assert ingest_response.status == "success"
        
        # Step 2: Search for data
        search_request = Mock()
        search_request.id = "workflow-search" 
        search_request.content = Mock()
        search_request.content.text = json.dumps({
            "query": "data scientist",
            "type": "hybrid",
            "limit": 5
        })
        
        search_response = await a2a_server.handle_knowledge_search(search_request)
        assert search_response.status == "success"
        
        # Step 3: Check system status
        status_request = Mock()
        status_request.id = "workflow-status"
        status_request.content = Mock()
        status_request.content.text = json.dumps({"detailed": True})
        
        status_response = await a2a_server.handle_system_status(status_request)
        assert status_response.status == "success"
        
        # Verify all requests were processed
        assert a2a_server.request_count >= 3