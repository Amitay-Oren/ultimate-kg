"""
Unit tests for Knowledge Graph Agent with MCP Integration.

These tests validate the KG agent's MCP toolset integration,
data processing capabilities, and knowledge search functionality.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from agentic_graphrag.agents.kg_agent import KnowledgeGraphAgent
from agentic_graphrag.config import config

@pytest.fixture
def mock_mcp_toolset():
    """Create a mock MCP toolset"""
    toolset = Mock()
    toolset.close = AsyncMock()
    return toolset

@pytest.fixture
def mock_llm_agent():
    """Create a mock LLM agent"""
    agent = Mock()
    return agent

@pytest.fixture
def mock_runner():
    """Create a mock runner"""
    runner = Mock()
    runner.run_async = AsyncMock()
    return runner

@pytest.fixture
def mock_session_service():
    """Create a mock session service"""
    service = Mock()
    service.create_session = AsyncMock()
    return service

@pytest.fixture
def mock_session():
    """Create a mock session"""
    session = Mock()
    session.id = "test-session-123"
    session.user_id = "system"
    return session

class TestKGAgentInitialization:
    """Test KG agent initialization and setup"""
    
    @pytest.mark.asyncio
    @patch('agentic_graphrag.agents.kg_agent.MCPToolset')
    @patch('agentic_graphrag.agents.kg_agent.LlmAgent')
    @patch('agentic_graphrag.agents.kg_agent.InMemorySessionService')
    @patch('agentic_graphrag.agents.kg_agent.Runner')
    async def test_agent_initialization(self, mock_runner_class, mock_session_service_class, 
                                      mock_llm_agent_class, mock_mcp_toolset_class):
        """Test successful KG agent initialization"""
        # Setup mocks
        mock_toolset = Mock()
        mock_mcp_toolset_class.return_value = mock_toolset
        
        mock_agent = Mock()
        mock_llm_agent_class.return_value = mock_agent
        
        mock_session_service = Mock()
        mock_session = Mock()
        mock_session.id = "test-session"
        mock_session.user_id = "system"
        mock_session_service.create_session.return_value = mock_session
        mock_session_service_class.return_value = mock_session_service
        
        mock_runner = Mock()
        mock_runner_class.return_value = mock_runner
        
        # Create and initialize agent
        kg_agent = KnowledgeGraphAgent()
        
        # Before initialization
        assert not kg_agent.initialized
        assert kg_agent.toolset is None
        assert kg_agent.agent is None
        assert kg_agent.runner is None
        
        # Initialize
        await kg_agent.initialize()
        
        # After initialization
        assert kg_agent.initialized
        assert kg_agent.toolset is not None
        assert kg_agent.agent is not None
        assert kg_agent.runner is not None
        assert kg_agent.session is not None
        
        # Verify MCP toolset creation
        mock_mcp_toolset_class.assert_called_once()
        
        # Verify LLM agent creation
        mock_llm_agent_class.assert_called_once()
        call_args = mock_llm_agent_class.call_args
        assert call_args[1]['model'] == config.google_cloud.model
        assert call_args[1]['name'] == 'kg_coordinator'
        assert 'MCP tools' in call_args[1]['instruction']
        
        # Verify session creation
        mock_session_service.create_session.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('agentic_graphrag.agents.kg_agent.MCPToolset')
    async def test_initialization_failure(self, mock_mcp_toolset_class):
        """Test KG agent initialization failure"""
        # Setup mock to raise exception
        mock_mcp_toolset_class.side_effect = Exception("MCP connection failed")
        
        kg_agent = KnowledgeGraphAgent()
        
        # Initialization should raise exception
        with pytest.raises(Exception, match="MCP connection failed"):
            await kg_agent.initialize()
        
        # Agent should not be initialized
        assert not kg_agent.initialized

class TestDataProcessing:
    """Test data processing functionality"""
    
    @pytest.fixture
    async def initialized_kg_agent(self, mock_mcp_toolset, mock_llm_agent, 
                                  mock_runner, mock_session_service, mock_session):
        """Create an initialized KG agent with mocks"""
        with patch.multiple(
            'agentic_graphrag.agents.kg_agent',
            MCPToolset=Mock(return_value=mock_mcp_toolset),
            LlmAgent=Mock(return_value=mock_llm_agent),
            InMemorySessionService=Mock(return_value=mock_session_service),
            Runner=Mock(return_value=mock_runner)
        ):
            mock_session_service.create_session.return_value = mock_session
            
            kg_agent = KnowledgeGraphAgent()
            await kg_agent.initialize()
            return kg_agent
    
    @pytest.mark.asyncio
    async def test_successful_data_processing(self, initialized_kg_agent):
        """Test successful data processing workflow"""
        # Setup mock runner response
        mock_event = Mock()
        mock_event.content = Mock()
        mock_event.content.parts = [Mock()]
        mock_event.content.parts[0].text = json.dumps({
            "processing_status": "success",
            "facts_extracted": 3,
            "storage_result": "Data stored successfully",
            "connections_found": 2,
            "high_relevance_connections": [
                {"source": "fact1", "target": "fact2", "score": 0.85}
            ]
        })
        
        initialized_kg_agent.runner.run_async.return_value = AsyncMock()
        initialized_kg_agent.runner.run_async.return_value.__aiter__ = AsyncMock(
            return_value=[mock_event]
        )
        
        # Process data
        request_data = {
            "data": "Alice is a software engineer at Google",
            "format": "text",
            "options": {
                "extract_facts": True,
                "detect_connections": True,
                "notify_threshold": 0.7
            }
        }
        
        result = await initialized_kg_agent.process_data(request_data)
        
        # Verify result
        assert result["status"] == "success"
        assert result["facts_extracted"] == 3
        assert result["connections_found"] == 2
        assert result["high_relevance_connections"] == [
            {"source": "fact1", "target": "fact2", "score": 0.85}
        ]
        assert "processing_time" in result
        assert "processed_at" in result
        
        # Verify statistics updated
        assert initialized_kg_agent.processing_stats["requests_processed"] == 1
        assert initialized_kg_agent.processing_stats["data_items_processed"] == 1
    
    @pytest.mark.asyncio
    async def test_data_processing_with_connection_detection_disabled(self, initialized_kg_agent):
        """Test data processing with connection detection disabled"""
        # Setup mock runner response
        mock_event = Mock()
        mock_event.content = Mock()
        mock_event.content.parts = [Mock()]
        mock_event.content.parts[0].text = json.dumps({
            "processing_status": "success",
            "facts_extracted": 2,
            "storage_result": "Data stored successfully"
        })
        
        initialized_kg_agent.runner.run_async.return_value = AsyncMock()
        initialized_kg_agent.runner.run_async.return_value.__aiter__ = AsyncMock(
            return_value=[mock_event]
        )
        
        # Process data without connection detection
        request_data = {
            "data": "Bob works at Microsoft",
            "format": "text",
            "options": {
                "extract_facts": True,
                "detect_connections": False
            }
        }
        
        result = await initialized_kg_agent.process_data(request_data)
        
        # Verify result
        assert result["status"] == "success"
        assert result["facts_extracted"] == 2
        assert result["connections_found"] == 0
        assert result["high_relevance_connections"] == []
    
    @pytest.mark.asyncio
    async def test_data_processing_error(self, initialized_kg_agent):
        """Test data processing error handling"""
        # Setup mock runner to raise exception
        initialized_kg_agent.runner.run_async.side_effect = Exception("Processing failed")
        
        request_data = {
            "data": "test data",
            "format": "text"
        }
        
        result = await initialized_kg_agent.process_data(request_data)
        
        # Verify error result
        assert result["status"] == "error"
        assert "Processing failed" in result["error"]
        assert result["facts_extracted"] == 0
        assert result["connections_found"] == 0
        assert "processing_time" in result
    
    @pytest.mark.asyncio
    async def test_uninitialized_agent_processing(self):
        """Test data processing with uninitialized agent"""
        kg_agent = KnowledgeGraphAgent()
        
        request_data = {"data": "test", "format": "text"}
        
        with pytest.raises(RuntimeError, match="KG Agent not initialized"):
            await kg_agent.process_data(request_data)

class TestKnowledgeSearch:
    """Test knowledge search functionality"""
    
    @pytest.mark.asyncio
    async def test_successful_knowledge_search(self, initialized_kg_agent):
        """Test successful knowledge search"""
        # Setup mock runner response
        mock_event = Mock()
        mock_event.content = Mock()
        mock_event.content.parts = [Mock()]
        mock_event.content.parts[0].text = json.dumps({
            "search_status": "success",
            "results": [
                {"content": "Alice is a software engineer", "score": 0.95, "source": "knowledge_base"},
                {"content": "Bob works at Google", "score": 0.87, "source": "knowledge_base"}
            ],
            "total_count": 2,
            "search_strategy": "hybrid",
            "related_concepts": ["programming", "technology", "employment"]
        })
        
        initialized_kg_agent.runner.run_async.return_value = AsyncMock()
        initialized_kg_agent.runner.run_async.return_value.__aiter__ = AsyncMock(
            return_value=[mock_event]
        )
        
        # Search knowledge
        request_data = {
            "query": "software engineer",
            "type": "hybrid",
            "limit": 10,
            "filters": {"department": "engineering"}
        }
        
        result = await initialized_kg_agent.search_knowledge(request_data)
        
        # Verify result
        assert result["total_count"] == 2
        assert result["search_type"] == "hybrid"
        assert result["query"] == "software engineer"
        assert len(result["results"]) == 2
        assert result["results"][0]["score"] == 0.95
        assert result["related_concepts"] == ["programming", "technology", "employment"]
        assert "search_time" in result
        assert "searched_at" in result
        
        # Verify statistics updated
        assert initialized_kg_agent.processing_stats["searches_performed"] == 1
    
    @pytest.mark.asyncio
    async def test_search_with_invalid_response(self, initialized_kg_agent):
        """Test search with invalid JSON response"""
        # Setup mock runner with invalid JSON response
        mock_event = Mock()
        mock_event.content = Mock()
        mock_event.content.parts = [Mock()]
        mock_event.content.parts[0].text = "This is not valid JSON response"
        
        initialized_kg_agent.runner.run_async.return_value = AsyncMock()
        initialized_kg_agent.runner.run_async.return_value.__aiter__ = AsyncMock(
            return_value=[mock_event]
        )
        
        request_data = {
            "query": "test query",
            "type": "semantic"
        }
        
        result = await initialized_kg_agent.search_knowledge(request_data)
        
        # Should fallback gracefully
        assert result["total_count"] == 1
        assert result["query"] == "test query"
        assert len(result["results"]) == 1
        assert "This is not valid JSON response" in result["results"][0]["content"]
    
    @pytest.mark.asyncio
    async def test_search_error_handling(self, initialized_kg_agent):
        """Test search error handling"""
        # Setup mock runner to raise exception
        initialized_kg_agent.runner.run_async.side_effect = Exception("Search failed")
        
        request_data = {
            "query": "test query",
            "type": "semantic"
        }
        
        result = await initialized_kg_agent.search_knowledge(request_data)
        
        # Verify error result
        assert result["results"] == []
        assert result["total_count"] == 0
        assert "Search failed" in result["error"]
        assert result["query"] == "test query"

class TestAgentStatus:
    """Test agent status and statistics"""
    
    @pytest.mark.asyncio
    async def test_uninitialized_agent_status(self):
        """Test status of uninitialized agent"""
        kg_agent = KnowledgeGraphAgent()
        
        status = await kg_agent.get_status()
        
        assert not status["initialized"]
        assert status["tools_available"] == []
        assert status["statistics"]["requests_processed"] == 0
    
    @pytest.mark.asyncio
    async def test_initialized_agent_status(self, initialized_kg_agent):
        """Test status of initialized agent"""
        status = await initialized_kg_agent.get_status()
        
        assert status["initialized"]
        assert status["mcp_server_url"] == config.mcp.server_url
        assert status["model"] == config.google_cloud.model
        assert "cognify" in status["tools_available"]
        assert "search" in status["tools_available"]
    
    @pytest.mark.asyncio
    async def test_list_knowledge_data(self, initialized_kg_agent):
        """Test listing knowledge data"""
        # Setup mock runner response
        mock_event = Mock()
        mock_event.content = Mock()
        mock_event.content.parts = [Mock()]
        mock_event.content.parts[0].text = "Knowledge base contains 150 documents and 3000 facts"
        
        initialized_kg_agent.runner.run_async.return_value = AsyncMock()
        initialized_kg_agent.runner.run_async.return_value.__aiter__ = AsyncMock(
            return_value=[mock_event]
        )
        
        result = await initialized_kg_agent.list_knowledge_data()
        
        assert result["status"] == "success"
        assert "150 documents" in result["data_overview"]
        assert "retrieved_at" in result

class TestAgentCleanup:
    """Test agent cleanup and resource management"""
    
    @pytest.mark.asyncio
    async def test_agent_cleanup(self, initialized_kg_agent):
        """Test proper agent cleanup"""
        # Verify agent is initialized
        assert initialized_kg_agent.initialized
        assert initialized_kg_agent.toolset is not None
        
        # Cleanup
        await initialized_kg_agent.cleanup()
        
        # Verify cleanup
        assert not initialized_kg_agent.initialized
        initialized_kg_agent.toolset.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_cleanup_with_toolset_error(self, initialized_kg_agent):
        """Test cleanup when toolset.close() raises exception"""
        # Setup toolset to raise exception on close
        initialized_kg_agent.toolset.close.side_effect = Exception("Close failed")
        
        # Cleanup should not raise exception
        await initialized_kg_agent.cleanup()
        
        # Agent should still be marked as not initialized
        assert not initialized_kg_agent.initialized

@pytest.mark.integration
class TestKGAgentIntegration:
    """Integration tests for KG agent functionality"""
    
    @pytest.mark.asyncio
    async def test_complete_workflow(self, initialized_kg_agent):
        """Test complete workflow from data processing to search"""
        # Setup mock responses for both operations
        process_event = Mock()
        process_event.content = Mock()
        process_event.content.parts = [Mock()]
        process_event.content.parts[0].text = json.dumps({
            "processing_status": "success",
            "facts_extracted": 2,
            "storage_result": "Stored successfully",
            "connections_found": 1
        })
        
        search_event = Mock()
        search_event.content = Mock()
        search_event.content.parts = [Mock()]
        search_event.content.parts[0].text = json.dumps({
            "search_status": "success",
            "results": [{"content": "Found relevant data", "score": 0.9}],
            "total_count": 1
        })
        
        # Setup different responses for different calls
        call_count = 0
        async def mock_run_async(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return AsyncMock(__aiter__=AsyncMock(return_value=[process_event]))()
            else:
                return AsyncMock(__aiter__=AsyncMock(return_value=[search_event]))()
        
        initialized_kg_agent.runner.run_async = mock_run_async
        
        # Step 1: Process data
        process_result = await initialized_kg_agent.process_data({
            "data": "Charlie is a data scientist at StartupCorp",
            "format": "text",
            "options": {"extract_facts": True, "detect_connections": True}
        })
        
        assert process_result["status"] == "success"
        assert process_result["facts_extracted"] == 2
        
        # Step 2: Search for the data
        search_result = await initialized_kg_agent.search_knowledge({
            "query": "Charlie data scientist",
            "type": "hybrid",
            "limit": 5
        })
        
        assert search_result["total_count"] == 1
        assert search_result["results"][0]["score"] == 0.9
        
        # Verify statistics
        stats = initialized_kg_agent.processing_stats
        assert stats["requests_processed"] == 1
        assert stats["searches_performed"] == 1