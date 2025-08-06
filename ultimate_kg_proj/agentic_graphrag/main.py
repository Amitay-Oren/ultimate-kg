"""
Main Agentic GraphRAG System Integration

This module integrates all components of the Agentic GraphRAG system:
- A2A Server for external communication
- KG Agent with MCP integration for Cognee GraphRAG operations
- Fact Extraction Pipeline for multi-format data processing  
- Connection Detection System for relationship analysis
- Notification Manager for user alerts

Usage:
    python main.py                    # Start complete system
    python main.py --test-only        # Run system tests only
    python main.py --config-check     # Validate configuration only
"""

import asyncio
import logging
import signal
import sys
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from .server.a2a_server import AgenticGraphRAGServer
from .agents.kg_agent import KnowledgeGraphAgent
from .agents.extraction_pipeline import extraction_pipeline
from .agents.connection_detector import connection_detector
from .agents.notification_manager import notification_manager
from .config import config
from .server.a2a_utils import run_a2a_validation

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.google_cloud.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/agentic_graphrag.log') if Path('logs').exists() else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

class AgenticGraphRAGSystem:
    """
    Main system class that orchestrates all components of the Agentic GraphRAG system.
    
    This class provides the complete integration of A2A server, KG agent, fact extraction,
    connection detection, and notification management.
    """
    
    def __init__(self):
        # Core components
        self.a2a_server = AgenticGraphRAGServer()
        self.kg_agent = KnowledgeGraphAgent()
        self.extraction_pipeline = extraction_pipeline
        self.connection_detector = connection_detector
        self.notification_manager = notification_manager
        
        # System state
        self.initialized = False
        self.running = False
        self.start_time = None
        self.shutdown_event = asyncio.Event()
        
        # System statistics
        self.stats = {
            "start_time": None,
            "requests_processed": 0,
            "facts_extracted": 0,
            "connections_detected": 0,
            "notifications_sent": 0,
            "errors": 0,
            "last_activity": None
        }
        
        # Register shutdown handlers
        self._register_shutdown_handlers()
    
    def _register_shutdown_handlers(self):
        """Register signal handlers for graceful shutdown"""
        for sig in [signal.SIGTERM, signal.SIGINT]:
            signal.signal(sig, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.shutdown_event.set()
    
    async def initialize(self) -> bool:
        """
        Initialize all system components.
        
        Returns:
            True if initialization successful, False otherwise
        """
        logger.info("Initializing Agentic GraphRAG System")
        
        try:
            # Validate configuration
            if not config.validate_config():
                logger.error("Configuration validation failed")
                return False
            
            # Initialize KG Agent first (requires MCP server)
            logger.info("Initializing Knowledge Graph Agent...")
            await self.kg_agent.initialize()
            
            # Initialize A2A Server
            logger.info("Initializing A2A Server...")
            await self.a2a_server.initialize()
            
            # Connect KG Agent to A2A Server
            self.a2a_server.set_kg_agent(self.kg_agent)
            
            # Test notification channels
            logger.info("Testing notification channels...")
            channel_results = await self.notification_manager.test_all_channels()
            working_channels = sum(1 for result in channel_results.values() if result)
            logger.info(f"Notification channels: {working_channels}/{len(channel_results)} working")
            
            # Update system statistics
            self.stats["start_time"] = datetime.now().isoformat()
            self.initialized = True
            
            logger.info("Agentic GraphRAG System initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"System initialization failed: {e}")
            return False
    
    async def start(self):
        """Start the complete system"""
        if not self.initialized:
            success = await self.initialize()
            if not success:
                raise RuntimeError("System initialization failed")
        
        logger.info("Starting Agentic GraphRAG System")
        
        try:
            self.start_time = datetime.now()
            self.running = True
            
            # Start A2A server
            await self.a2a_server.start()
            
            logger.info(f"🚀 Agentic GraphRAG System is running!")
            logger.info(f"   A2A Server: http://{config.a2a.host}:{config.a2a.port}")
            logger.info(f"   MCP Server: {config.mcp.server_url}")
            logger.info(f"   Google Cloud Project: {config.google_cloud.project_id}")
            logger.info(f"   Notification Threshold: {config.notifications.threshold}")
            
            # Wait for shutdown signal
            await self.shutdown_event.wait()
            
        except Exception as e:
            logger.error(f"System startup failed: {e}")
            raise
        finally:
            await self.shutdown()
    
    async def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main data processing workflow that coordinates all components.
        
        Args:
            data: Dictionary containing data, format, and processing options
            
        Returns:
            Complete processing results
        """
        start_time = datetime.now()
        self.stats["requests_processed"] += 1
        self.stats["last_activity"] = start_time.isoformat()
        
        try:
            logger.info(f"Starting data processing workflow: {data.get('format', 'unknown')} format")
            
            # Step 1: Extract facts using the extraction pipeline
            logger.debug("Step 1: Extracting facts...")
            data_text = data.get("data", "")
            data_format = data.get("format", "text")
            options = data.get("options", {})
            
            extraction_result = await self.extraction_pipeline.extract_facts(
                data_text, 
                data_format, 
                options
            )
            
            self.stats["facts_extracted"] += extraction_result.total_facts
            
            # Step 2: Store facts in GraphRAG via KG Agent
            logger.debug("Step 2: Storing facts in knowledge graph...")
            storage_result = await self.kg_agent.process_data(data)
            
            # Step 3: Detect connections if enabled
            connections_result = None
            if options.get("detect_connections", True):
                logger.debug("Step 3: Detecting connections...")
                
                # Get existing knowledge context (simplified)
                existing_knowledge = "Sample existing knowledge from the knowledge graph"
                
                connections_result = await self.connection_detector.detect_connections(
                    extraction_result.facts,
                    existing_knowledge,
                    options
                )
                
                self.stats["connections_detected"] += connections_result.total_connections
                
                # Step 4: Process connections for notifications
                if connections_result.high_relevance_connections:
                    logger.debug("Step 4: Processing notifications...")
                    notification_result = await self.notification_manager.process_connections(
                        connections_result.high_relevance_connections
                    )
                    self.stats["notifications_sent"] += notification_result.get("notifications_sent", 0)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Build comprehensive result
            result = {
                "status": "success",
                "processing_time": processing_time,
                "processed_at": start_time.isoformat(),
                
                # Fact extraction results
                "facts_extracted": extraction_result.total_facts,
                "extraction_status": extraction_result.status.value,
                "extraction_time": extraction_result.processing_time,
                
                # Storage results
                "storage_status": storage_result.get("status", "unknown"),
                "storage_time": storage_result.get("processing_time", 0),
                
                # Connection detection results
                "connections_found": connections_result.total_connections if connections_result else 0,
                "high_relevance_connections": len(connections_result.high_relevance_connections) if connections_result else 0,
                "connection_detection_time": connections_result.processing_time if connections_result else 0,
                
                # Notification results
                "notifications_sent": self.stats["notifications_sent"] - (self.stats["notifications_sent"] - (notification_result.get("notifications_sent", 0) if 'notification_result' in locals() else 0)),
                
                # Detailed results for debugging
                "detailed_results": {
                    "extraction": extraction_result.dict() if hasattr(extraction_result, 'dict') else str(extraction_result),
                    "storage": storage_result,
                    "connections": connections_result.dict() if connections_result and hasattr(connections_result, 'dict') else str(connections_result),
                    "notifications": locals().get("notification_result", {})
                }
            }
            
            logger.info(f"Data processing completed: {result['facts_extracted']} facts, {result['connections_found']} connections in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Data processing failed: {e}")
            
            return {
                "status": "error",
                "error": str(e),
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "processed_at": start_time.isoformat(),
                "facts_extracted": 0,
                "connections_found": 0,
                "notifications_sent": 0
            }
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        uptime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        # Get component statuses
        kg_agent_status = await self.kg_agent.get_status() if self.kg_agent.initialized else {"initialized": False}
        a2a_server_info = self.a2a_server.get_server_info()
        extraction_stats = self.extraction_pipeline.get_statistics()
        connection_stats = self.connection_detector.get_statistics()
        notification_stats = self.notification_manager.get_statistics()
        
        return {
            "system": {
                "status": "running" if self.running else "stopped",
                "initialized": self.initialized,
                "uptime": uptime,
                "version": "0.1.0"
            },
            "statistics": self.stats,
            "components": {
                "a2a_server": {
                    "status": "running" if self.running else "stopped",
                    **a2a_server_info
                },
                "kg_agent": kg_agent_status,
                "extraction_pipeline": extraction_stats,
                "connection_detector": connection_stats,
                "notification_manager": notification_stats
            },
            "configuration": {
                "a2a_port": config.a2a.port,
                "mcp_server_url": config.mcp.server_url,
                "google_cloud_project": config.google_cloud.project_id,
                "notification_threshold": config.notifications.threshold,
                "enabled_channels": list(config.notifications.channels)
            }
        }
    
    async def run_system_tests(self) -> Dict[str, Any]:
        """Run comprehensive system tests"""
        logger.info("Running system tests...")
        
        test_results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {}
        }
        
        try:
            # Test 1: Configuration validation
            test_results["tests"]["configuration"] = {
                "status": "pass" if config.validate_config() else "fail"
            }
            
            # Test 2: Component initialization
            if not self.initialized:
                init_success = await self.initialize()
                test_results["tests"]["initialization"] = {
                    "status": "pass" if init_success else "fail"
                }
            else:
                test_results["tests"]["initialization"] = {"status": "pass"}
            
            # Test 3: A2A server validation (if running)
            if self.running:
                a2a_results = await run_a2a_validation(f"http://{config.a2a.host}:{config.a2a.port}")
                test_results["tests"]["a2a_validation"] = {
                    "status": "pass" if a2a_results.get("summary", {}).get("overall_status") == "pass" else "fail",
                    "details": a2a_results
                }
            
            # Test 4: Notification channels
            channel_results = await self.notification_manager.test_all_channels()
            test_results["tests"]["notification_channels"] = {
                "status": "pass" if all(channel_results.values()) else "partial",
                "details": channel_results
            }
            
            # Test 5: Sample data processing
            test_data = {
                "data": "Test fact: Alice is a software engineer at TechCorp.",
                "format": "text",
                "options": {"extract_facts": True, "detect_connections": False}
            }
            
            processing_result = await self.process_data(test_data)
            test_results["tests"]["data_processing"] = {
                "status": "pass" if processing_result.get("status") == "success" else "fail",
                "details": processing_result
            }
            
            # Calculate overall status
            passed_tests = sum(1 for test in test_results["tests"].values() if test.get("status") == "pass")
            total_tests = len(test_results["tests"])
            
            test_results["summary"] = {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "success_rate": passed_tests / total_tests if total_tests > 0 else 0,
                "overall_status": "pass" if passed_tests == total_tests else "fail"
            }
            
            logger.info(f"System tests completed: {passed_tests}/{total_tests} passed")
            return test_results
            
        except Exception as e:
            logger.error(f"System tests failed: {e}")
            test_results["error"] = str(e)
            test_results["summary"] = {"overall_status": "error"}
            return test_results
    
    async def shutdown(self):
        """Gracefully shutdown all system components"""
        logger.info("Shutting down Agentic GraphRAG System...")
        
        self.running = False
        
        try:
            # Shutdown components in reverse order
            await self.notification_manager.cleanup()
            await self.kg_agent.cleanup()
            await self.a2a_server.shutdown()
            
            logger.info("System shutdown completed")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

async def main():
    """Main entry point for the Agentic GraphRAG System"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agentic GraphRAG System")
    parser.add_argument("--test-only", action="store_true", help="Run tests only, don't start server")
    parser.add_argument("--config-check", action="store_true", help="Validate configuration only")
    parser.add_argument("--port", type=int, help="Override A2A server port")
    
    args = parser.parse_args()
    
    # Override port if specified
    if args.port:
        config.a2a.port = args.port
    
    # Configuration check only
    if args.config_check:
        valid = config.validate_config()
        print(f"Configuration: {'VALID' if valid else 'INVALID'}")
        return 0 if valid else 1
    
    # Create system instance
    system = AgenticGraphRAGSystem()
    
    try:
        # Test-only mode
        if args.test_only:
            results = await system.run_system_tests()
            print(f"Test Results: {results['summary']['overall_status'].upper()}")
            print(f"Passed: {results['summary']['passed_tests']}/{results['summary']['total_tests']}")
            return 0 if results['summary']['overall_status'] == 'pass' else 1
        
        # Normal startup
        await system.start()
        return 0
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
        return 0
    except Exception as e:
        logger.error(f"System error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))