"""
A2A Protocol Utilities and Validation

This module provides utilities for A2A protocol validation,
testing, and compliance checking.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
import httpx
from datetime import datetime

logger = logging.getLogger(__name__)

class A2AProtocolValidator:
    """
    Validator for A2A protocol compliance and testing.
    """
    
    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip('/')
        self.client = httpx.AsyncClient()
    
    async def validate_server_health(self) -> Dict[str, Any]:
        """Validate basic server health and A2A compliance"""
        try:
            response = await self.client.get(f"{self.server_url}/health")
            
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "response_time": response.elapsed.total_seconds(),
                    "server_info": response.json() if response.content else None
                }
            else:
                return {
                    "status": "unhealthy", 
                    "status_code": response.status_code,
                    "error": response.text
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def validate_agent_registration(self) -> Dict[str, Any]:
        """Validate agent registration and discovery"""
        try:
            response = await self.client.get(f"{self.server_url}/agents")
            
            if response.status_code == 200:
                agents = response.json()
                return {
                    "status": "success",
                    "agents_found": len(agents.get("agents", [])),
                    "registered_agents": agents.get("agents", [])
                }
            else:
                return {
                    "status": "error",
                    "status_code": response.status_code,
                    "error": response.text
                }
                
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e)
            }
    
    async def test_knowledge_ingestion(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test knowledge ingestion endpoint"""
        try:
            response = await self.client.post(
                f"{self.server_url}/agents/kg_ingest",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            return {
                "status": "success" if response.status_code == 200 else "error",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.content else None,
                "error": response.text if response.status_code != 200 else None
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def test_knowledge_search(self, query: str, search_type: str = "hybrid") -> Dict[str, Any]:
        """Test knowledge search endpoint"""
        try:
            search_data = {
                "query": query,
                "type": search_type,
                "limit": 10
            }
            
            response = await self.client.post(
                f"{self.server_url}/agents/kg_search",
                json=search_data,
                headers={"Content-Type": "application/json"}
            )
            
            return {
                "status": "success" if response.status_code == 200 else "error",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.content else None,
                "error": response.text if response.status_code != 200 else None
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def test_system_status(self, detailed: bool = False) -> Dict[str, Any]:
        """Test system status endpoint"""
        try:
            status_data = {"detailed": detailed}
            
            response = await self.client.post(
                f"{self.server_url}/agents/kg_status",
                json=status_data,
                headers={"Content-Type": "application/json"}
            )
            
            return {
                "status": "success" if response.status_code == 200 else "error",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.content else None,
                "error": response.text if response.status_code != 200 else None
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run comprehensive A2A protocol compliance tests"""
        logger.info("Starting comprehensive A2A protocol tests")
        
        test_results = {
            "timestamp": datetime.now().isoformat(),
            "server_url": self.server_url,
            "tests": {}
        }
        
        # Test 1: Server Health
        logger.info("Testing server health...")
        test_results["tests"]["server_health"] = await self.validate_server_health()
        
        # Test 2: Agent Registration
        logger.info("Testing agent registration...")
        test_results["tests"]["agent_registration"] = await self.validate_agent_registration()
        
        # Test 3: Knowledge Ingestion
        logger.info("Testing knowledge ingestion...")
        test_data = {
            "data": "Ilya is a 34-year-old software engineer who lives in Tel Aviv. He is interested in buying a vineyard.",
            "format": "text",
            "options": {
                "extract_facts": True,
                "detect_connections": True,
                "notify_threshold": 0.7
            }
        }
        test_results["tests"]["knowledge_ingestion"] = await self.test_knowledge_ingestion(test_data)
        
        # Test 4: Knowledge Search
        logger.info("Testing knowledge search...")
        test_results["tests"]["knowledge_search"] = await self.test_knowledge_search("Ilya vineyard")
        
        # Test 5: System Status
        logger.info("Testing system status...")
        test_results["tests"]["system_status"] = await self.test_system_status(detailed=True)
        
        # Calculate overall success rate
        successful_tests = sum(1 for test in test_results["tests"].values() 
                             if test.get("status") == "success")
        total_tests = len(test_results["tests"])
        
        test_results["summary"] = {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "success_rate": successful_tests / total_tests if total_tests > 0 else 0,
            "overall_status": "pass" if successful_tests == total_tests else "fail"
        }
        
        logger.info(f"Tests completed: {successful_tests}/{total_tests} passed")
        return test_results
    
    async def close(self):
        """Clean up HTTP client"""
        await self.client.aclose()

class A2ATestData:
    """
    Test data generator for A2A protocol testing.
    """
    
    @staticmethod
    def get_sample_ingestion_data() -> List[Dict[str, Any]]:
        """Get sample data for ingestion testing"""
        return [
            {
                "data": "Alice is a 28-year-old data scientist who works at Google. She lives in Mountain View and is passionate about machine learning.",
                "format": "text",
                "options": {"extract_facts": True, "detect_connections": True}
            },
            {
                "data": {
                    "name": "Bob Johnson",
                    "age": 35,
                    "occupation": "Product Manager",
                    "company": "Microsoft",
                    "location": "Seattle"
                },
                "format": "json",
                "options": {"extract_facts": True, "detect_connections": False}
            },
            {
                "data": "Meeting Notes: Discussed the new AI project with the team. Key stakeholders include Sarah (Engineering Lead), Mike (Designer), and Lisa (PM). Timeline is 6 months.",
                "format": "text",
                "options": {"extract_facts": True, "detect_connections": True, "notify_threshold": 0.5}
            }
        ]
    
    @staticmethod
    def get_sample_search_queries() -> List[Dict[str, Any]]:
        """Get sample search queries for testing"""
        return [
            {"query": "data scientist", "type": "semantic", "limit": 5},
            {"query": "Google employees", "type": "graph", "limit": 10},
            {"query": "AI project timeline", "type": "hybrid", "limit": 3},
            {"query": "people in Seattle", "type": "semantic", "limit": 8}
        ]

async def run_a2a_validation(server_url: str = "http://localhost:8080") -> Dict[str, Any]:
    """
    Convenience function to run A2A protocol validation.
    
    Args:
        server_url: URL of the A2A server to validate
        
    Returns:
        Comprehensive test results
    """
    validator = A2AProtocolValidator(server_url)
    
    try:
        results = await validator.run_comprehensive_tests()
        return results
    finally:
        await validator.close()

# CLI interface for validation
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="A2A Protocol Validator")
    parser.add_argument("--server-url", default="http://localhost:8080",
                       help="A2A server URL to validate")
    parser.add_argument("--output", help="Output file for results (JSON)")
    
    args = parser.parse_args()
    
    async def main():
        results = await run_a2a_validation(args.server_url)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Results written to {args.output}")
        else:
            print(json.dumps(results, indent=2))
    
    asyncio.run(main())