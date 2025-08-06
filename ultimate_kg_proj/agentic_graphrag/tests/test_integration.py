"""
Integration tests for the complete Agentic GraphRAG System.

These tests validate end-to-end workflows, component integration,
and system-level functionality.
"""

import pytest
import asyncio
import json
import httpx
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from agentic_graphrag.main import AgenticGraphRAGSystem
from agentic_graphrag.server.a2a_utils import A2AProtocolValidator
from agentic_graphrag.config import config

@pytest.fixture
async def mock_system():
    """Create a mock system with all components mocked"""
    with patch.multiple(
        'agentic_graphrag.main',
        AgenticGraphRAGServer=Mock,
        KnowledgeGraphAgent=Mock,
        extraction_pipeline=Mock(),
        connection_detector=Mock(),
        notification_manager=Mock()
    ) as mocks:
        # Setup mock behaviors
        server_mock = mocks['AgenticGraphRAGServer'].return_value
        server_mock.initialize = AsyncMock()
        server_mock.start = AsyncMock()
        server_mock.shutdown = AsyncMock()
        server_mock.set_kg_agent = Mock()
        server_mock.get_server_info.return_value = {
            "server_host": "localhost",
            "server_port": 8080,
            "uptime": 0,
            "requests_processed": 0
        }
        
        kg_agent_mock = mocks['KnowledgeGraphAgent'].return_value
        kg_agent_mock.initialize = AsyncMock()
        kg_agent_mock.cleanup = AsyncMock()
        kg_agent_mock.initialized = True
        kg_agent_mock.process_data = AsyncMock(return_value={
            "status": "success",
            "processing_time": 1.5,
            "facts_extracted": 3,
            "connections_found": 2
        })
        kg_agent_mock.get_status = AsyncMock(return_value={
            "initialized": True,
            "model": "gemini-2.0-flash"
        })
        
        # Setup extraction pipeline mock
        extraction_mock = mocks['extraction_pipeline']
        extraction_mock.extract_facts = AsyncMock()
        extraction_mock.get_statistics.return_value = {
            "total_extractions": 5,
            "successful_extractions": 4,
            "average_processing_time": 0.8
        }
        
        # Setup connection detector mock
        connection_mock = mocks['connection_detector']
        connection_mock.detect_connections = AsyncMock()
        connection_mock.get_statistics.return_value = {
            "total_detections": 3,
            "connections_found": 8,
            "high_relevance_connections": 2
        }
        
        # Setup notification manager mock
        notification_mock = mocks['notification_manager']
        notification_mock.test_all_channels = AsyncMock(return_value={
            "console": True,
            "file": True,
            "webhook": False
        })
        notification_mock.process_connections = AsyncMock(return_value={
            "status": "notifications_sent",
            "notifications_sent": 1
        })
        notification_mock.cleanup = AsyncMock()
        notification_mock.get_statistics.return_value = {
            "notifications_sent": 10,
            "channels_active": 2
        }
        
        system = AgenticGraphRAGSystem()
        yield system, mocks

class TestSystemInitialization:
    """Test system initialization and startup"""
    
    @pytest.mark.asyncio
    async def test_system_initialization(self, mock_system):
        """Test complete system initialization"""
        system, mocks = mock_system
        
        # Before initialization
        assert not system.initialized
        
        # Initialize
        success = await system.initialize()
        
        # Verify initialization
        assert success
        assert system.initialized
        
        # Verify components were initialized
        kg_agent_mock = mocks['KnowledgeGraphAgent'].return_value
        kg_agent_mock.initialize.assert_called_once()
        
        server_mock = mocks['AgenticGraphRAGServer'].return_value
        server_mock.initialize.assert_called_once()
        server_mock.set_kg_agent.assert_called_once()
        
        notification_mock = mocks['notification_manager']
        notification_mock.test_all_channels.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_system_initialization_failure(self, mock_system):
        """Test system initialization failure"""
        system, mocks = mock_system
        
        # Setup KG agent to fail initialization
        kg_agent_mock = mocks['KnowledgeGraphAgent'].return_value
        kg_agent_mock.initialize.side_effect = Exception("MCP connection failed")
        
        # Initialize should fail
        success = await system.initialize()
        
        assert not success
        assert not system.initialized
    
    @pytest.mark.asyncio
    async def test_config_validation_failure(self, mock_system):
        """Test initialization with invalid configuration"""
        system, mocks = mock_system
        
        # Mock config validation to fail
        with patch('agentic_graphrag.main.config.validate_config', return_value=False):
            success = await system.initialize()
        
        assert not success
        assert not system.initialized

class TestDataProcessingWorkflow:
    """Test complete data processing workflows"""
    
    @pytest.mark.asyncio
    async def test_complete_data_processing_workflow(self, mock_system):
        """Test complete data processing from ingestion to notification"""
        system, mocks = mock_system
        await system.initialize()
        
        # Setup mock extraction results
        from agentic_graphrag.agents.schemas import (
            FactExtractionOutput, ExtractedFact, ProcessingStatus, 
            DataFormat, FactType, ConnectionDetectionOutput, DetectedConnection, ConnectionScore
        )
        
        extracted_facts = [
            ExtractedFact(
                fact="Alice is a software engineer",
                confidence=0.95,
                fact_type=FactType.PERSON,
                entities=["Alice"],
                source_context="Alice is a software engineer at Google"
            ),
            ExtractedFact(
                fact="Alice works at Google",
                confidence=0.90,
                fact_type=FactType.RELATIONSHIP,
                entities=["Alice", "Google"],
                source_context="Alice is a software engineer at Google"
            )
        ]
        
        extraction_result = FactExtractionOutput(
            facts=extracted_facts,
            total_facts=2,
            processing_time=1.2,
            data_format=DataFormat.TEXT,
            extraction_method="text_specialized_processor",
            status=ProcessingStatus.COMPLETED
        )
        
        # Setup mock connection detection results
        detected_connections = [
            DetectedConnection(
                source_fact="Alice is a software engineer",
                target_fact="Alice works at Google",
                relationship="Employment relationship",
                score=ConnectionScore(
                    score=0.85,
                    confidence=0.90,
                    reasoning="Strong employment relationship",
                    connection_type="factual"
                ),
                evidence=["Both facts mention Alice and her profession"]
            )
        ]
        
        connection_result = ConnectionDetectionOutput(
            connections=detected_connections,
            total_connections=1,
            high_relevance_connections=detected_connections,
            threshold_used=0.7,
            processing_time=0.8,
            status=ProcessingStatus.COMPLETED
        )
        
        # Setup mocks
        extraction_mock = mocks['extraction_pipeline']
        extraction_mock.extract_facts.return_value = extraction_result
        
        connection_mock = mocks['connection_detector']
        connection_mock.detect_connections.return_value = connection_result
        
        # Process data
        data = {
            "data": "Alice is a software engineer at Google",
            "format": "text",
            "options": {
                "extract_facts": True,
                "detect_connections": True,
                "notify_threshold": 0.7
            }
        }
        
        result = await system.process_data(data)
        
        # Verify workflow execution
        assert result["status"] == "success"
        assert result["facts_extracted"] == 2
        assert result["connections_found"] == 1
        assert result["high_relevance_connections"] == 1
        assert result["notifications_sent"] == 1
        assert "processing_time" in result
        
        # Verify components were called
        extraction_mock.extract_facts.assert_called_once()
        connection_mock.detect_connections.assert_called_once()
        
        notification_mock = mocks['notification_manager']
        notification_mock.process_connections.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_data_processing_without_connections(self, mock_system):
        """Test data processing with connection detection disabled"""
        system, mocks = mock_system
        await system.initialize()
        
        # Setup extraction mock only
        from agentic_graphrag.agents.schemas import FactExtractionOutput, ProcessingStatus, DataFormat
        
        extraction_result = FactExtractionOutput(
            facts=[],
            total_facts=1,
            processing_time=0.5,
            data_format=DataFormat.TEXT,
            extraction_method="text_processor",
            status=ProcessingStatus.COMPLETED
        )
        
        extraction_mock = mocks['extraction_pipeline']
        extraction_mock.extract_facts.return_value = extraction_result
        
        # Process data without connection detection
        data = {
            "data": "Bob works at Microsoft",
            "format": "text",
            "options": {
                "extract_facts": True,
                "detect_connections": False
            }
        }
        
        result = await system.process_data(data)
        
        # Verify results
        assert result["status"] == "success"
        assert result["facts_extracted"] == 1
        assert result["connections_found"] == 0
        assert result["notifications_sent"] == 0
        
        # Verify connection detection was not called
        connection_mock = mocks['connection_detector']
        connection_mock.detect_connections.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_data_processing_error_handling(self, mock_system):
        """Test data processing error handling"""
        system, mocks = mock_system
        await system.initialize()
        
        # Setup extraction to fail
        extraction_mock = mocks['extraction_pipeline']
        extraction_mock.extract_facts.side_effect = Exception("Extraction failed")
        
        data = {
            "data": "test data",
            "format": "text"
        }
        
        result = await system.process_data(data)
        
        # Verify error handling
        assert result["status"] == "error"
        assert "Extraction failed" in result["error"]
        assert result["facts_extracted"] == 0
        assert result["connections_found"] == 0
        assert "processing_time" in result

class TestSystemStatus:
    """Test system status and monitoring"""
    
    @pytest.mark.asyncio
    async def test_system_status(self, mock_system):
        """Test comprehensive system status"""
        system, mocks = mock_system
        await system.initialize()
        system.start_time = datetime.now()
        system.running = True
        
        status = await system.get_system_status()
        
        # Verify system status
        assert status["system"]["status"] == "running"
        assert status["system"]["initialized"] == True
        assert status["system"]["version"] == "0.1.0"
        assert "uptime" in status["system"]
        
        # Verify component statuses
        assert "a2a_server" in status["components"]
        assert "kg_agent" in status["components"]
        assert "extraction_pipeline" in status["components"]
        assert "connection_detector" in status["components"]
        assert "notification_manager" in status["components"]
        
        # Verify configuration
        assert status["configuration"]["a2a_port"] == config.a2a.port
        assert status["configuration"]["mcp_server_url"] == config.mcp.server_url
    
    @pytest.mark.asyncio
    async def test_system_statistics_tracking(self, mock_system):
        """Test system statistics tracking"""
        system, mocks = mock_system
        await system.initialize()
        
        # Process some data to update statistics
        from agentic_graphrag.agents.schemas import FactExtractionOutput, ProcessingStatus, DataFormat
        
        extraction_result = FactExtractionOutput(
            facts=[],
            total_facts=3,
            processing_time=1.0,
            data_format=DataFormat.TEXT,
            extraction_method="test",
            status=ProcessingStatus.COMPLETED
        )
        
        extraction_mock = mocks['extraction_pipeline']
        extraction_mock.extract_facts.return_value = extraction_result
        
        # Process multiple requests
        for i in range(3):
            await system.process_data({
                "data": f"test data {i}",
                "format": "text"
            })
        
        # Check statistics
        assert system.stats["requests_processed"] == 3
        assert system.stats["facts_extracted"] == 9  # 3 facts × 3 requests
        assert system.stats["last_activity"] is not None

class TestSystemTesting:
    """Test system testing functionality"""
    
    @pytest.mark.asyncio
    async def test_system_tests_success(self, mock_system):
        """Test successful system tests"""
        system, mocks = mock_system
        
        # Mock successful A2A validation
        with patch('agentic_graphrag.main.run_a2a_validation') as mock_a2a_validation:
            mock_a2a_validation.return_value = {
                "summary": {"overall_status": "pass"}
            }
            
            # Setup successful data processing
            from agentic_graphrag.agents.schemas import FactExtractionOutput, ProcessingStatus, DataFormat
            
            extraction_result = FactExtractionOutput(
                facts=[],
                total_facts=1,
                processing_time=0.5,
                data_format=DataFormat.TEXT,
                extraction_method="test",
                status=ProcessingStatus.COMPLETED
            )
            
            extraction_mock = mocks['extraction_pipeline']
            extraction_mock.extract_facts.return_value = extraction_result
            
            # Run tests
            results = await system.run_system_tests()
            
            # Verify test results
            assert results["summary"]["overall_status"] == "pass"
            assert results["summary"]["passed_tests"] == results["summary"]["total_tests"]
            
            # Verify individual tests
            assert results["tests"]["configuration"]["status"] == "pass"
            assert results["tests"]["initialization"]["status"] == "pass"
            assert results["tests"]["data_processing"]["status"] == "pass"
    
    @pytest.mark.asyncio
    async def test_system_tests_with_failures(self, mock_system):
        """Test system tests with some failures"""
        system, mocks = mock_system
        
        # Setup notification channels to fail
        notification_mock = mocks['notification_manager']
        notification_mock.test_all_channels.return_value = {
            "console": True,
            "file": False,  # Failed
            "webhook": False  # Failed
        }
        
        # Run tests
        results = await system.run_system_tests()
        
        # Verify partial success
        assert results["summary"]["overall_status"] == "fail"
        assert results["summary"]["passed_tests"] < results["summary"]["total_tests"]
        
        # Verify notification test marked as partial
        assert results["tests"]["notification_channels"]["status"] == "partial"

class TestSystemShutdown:
    """Test system shutdown and cleanup"""
    
    @pytest.mark.asyncio
    async def test_graceful_shutdown(self, mock_system):
        """Test graceful system shutdown"""
        system, mocks = mock_system
        await system.initialize()
        system.running = True
        
        # Shutdown
        await system.shutdown()
        
        # Verify shutdown
        assert not system.running
        
        # Verify components were cleaned up
        notification_mock = mocks['notification_manager']
        notification_mock.cleanup.assert_called_once()
        
        kg_agent_mock = mocks['KnowledgeGraphAgent'].return_value
        kg_agent_mock.cleanup.assert_called_once()
        
        server_mock = mocks['AgenticGraphRAGServer'].return_value
        server_mock.shutdown.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_shutdown_with_errors(self, mock_system):
        """Test shutdown with component errors"""
        system, mocks = mock_system
        await system.initialize()
        system.running = True
        
        # Setup cleanup to fail
        notification_mock = mocks['notification_manager']
        notification_mock.cleanup.side_effect = Exception("Cleanup failed")
        
        # Shutdown should complete despite errors
        await system.shutdown()
        
        assert not system.running

@pytest.mark.integration
@pytest.mark.slow
class TestRealIntegration:
    """Real integration tests (require actual services)"""
    
    @pytest.mark.skipif(not config.validate_config(), reason="Configuration not valid")
    @pytest.mark.asyncio
    async def test_a2a_protocol_validation(self):
        """Test A2A protocol validation against real server"""
        # This test requires a running A2A server
        validator = A2AProtocolValidator("http://localhost:8080")
        
        try:
            # Test basic connectivity
            health_result = await validator.validate_server_health()
            
            # Test is informational - may pass or fail depending on server availability
            print(f"A2A Server Health: {health_result}")
            
        except Exception as e:
            pytest.skip(f"A2A server not available: {e}")
        finally:
            await validator.close()
    
    @pytest.mark.skipif(not config.validate_config(), reason="Configuration not valid")
    @pytest.mark.asyncio
    async def test_http_endpoint_integration(self):
        """Test HTTP endpoints if server is running"""
        try:
            async with httpx.AsyncClient() as client:
                # Test status endpoint
                response = await client.post(
                    "http://localhost:8080/agents/kg_status",
                    json={"detailed": False},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"Server Status: {data}")
                else:
                    pytest.skip(f"Server returned {response.status_code}")
                    
        except Exception as e:
            pytest.skip(f"HTTP integration test failed: {e}")

# Performance tests
@pytest.mark.performance
class TestPerformance:
    """Performance tests for system components"""
    
    @pytest.mark.asyncio
    async def test_concurrent_processing(self, mock_system):
        """Test concurrent data processing performance"""
        system, mocks = mock_system
        await system.initialize()
        
        # Setup fast mock responses
        from agentic_graphrag.agents.schemas import FactExtractionOutput, ProcessingStatus, DataFormat
        
        extraction_result = FactExtractionOutput(
            facts=[],
            total_facts=1,
            processing_time=0.1,
            data_format=DataFormat.TEXT,
            extraction_method="fast_test",
            status=ProcessingStatus.COMPLETED
        )
        
        extraction_mock = mocks['extraction_pipeline']
        extraction_mock.extract_facts.return_value = extraction_result
        
        # Process multiple requests concurrently
        tasks = []
        for i in range(10):
            task = system.process_data({
                "data": f"concurrent test data {i}",
                "format": "text"
            })
            tasks.append(task)
        
        start_time = datetime.now()
        results = await asyncio.gather(*tasks)
        end_time = datetime.now()
        
        # Verify all requests succeeded
        assert all(result["status"] == "success" for result in results)
        
        # Check processing time (should be reasonable for concurrent processing)
        total_time = (end_time - start_time).total_seconds()
        assert total_time < 5.0  # Should complete within 5 seconds
        
        print(f"Processed 10 concurrent requests in {total_time:.2f}s")