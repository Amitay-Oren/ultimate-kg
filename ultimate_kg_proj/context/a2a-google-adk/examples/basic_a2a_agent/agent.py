"""
Basic A2A-compatible Google ADK Agent

This example demonstrates how to create a simple A2A-compatible agent
using Google ADK with Vertex AI integration.
"""

import asyncio
import logging
from typing import Dict, Any, List
from dataclasses import dataclass

from a2a_sdk import A2AServer, A2ACompatibleAgent
from google.cloud import aiplatform
from google_adk import GoogleADKAgent, VertexAIModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class A2ACapabilities:
    """Agent capabilities for A2A discovery"""
    tasks: List[str]
    tools: List[str] 
    models: List[str]
    protocols: List[str]
    platform: str

class BasicA2AGooogleADKAgent(A2ACompatibleAgent):
    """
    Basic A2A-compatible agent using Google ADK and Vertex AI
    
    This agent can:
    - Handle A2A protocol requests
    - Process text with Vertex AI models
    - Integrate with Google ADK tools
    - Communicate with agents on other platforms
    """
    
    def __init__(self, name: str, model: str = "gemini-1.5-pro"):
        super().__init__(name)
        self.model_name = model
        self.vertex_ai_model = None
        self.capabilities = A2ACapabilities(
            tasks=["text_generation", "text_analysis", "question_answering"],
            tools=["vertex_ai", "google_search", "text_processing"],
            models=[model],
            protocols=["a2a-v1.0"],
            platform="google-adk"
        )
        
    async def initialize(self):
        """Initialize the agent with Google Cloud and Vertex AI"""
        try:
            # Initialize Vertex AI
            aiplatform.init()
            self.vertex_ai_model = VertexAIModel(self.model_name)
            logger.info(f"Initialized agent '{self.name}' with model {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Return agent capabilities for A2A discovery"""
        return {
            "agent_id": self.name,
            "platform": self.capabilities.platform,
            "protocols": self.capabilities.protocols,
            "supported_tasks": self.capabilities.tasks,
            "available_tools": self.capabilities.tools,
            "models": self.capabilities.models,
            "version": "1.0.0",
            "description": "A2A-compatible Google ADK agent with Vertex AI integration"
        }
    
    async def handle_a2a_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming A2A protocol requests
        
        Args:
            request: A2A protocol request containing task details
            
        Returns:
            A2A protocol response with results
        """
        try:
            task_type = request.get("task_type")
            content = request.get("content", "")
            context = request.get("context", {})
            
            logger.info(f"Handling A2A request: {task_type}")
            
            # Route to appropriate handler based on task type
            if task_type == "text_generation":
                result = await self._handle_text_generation(content, context)
            elif task_type == "text_analysis":
                result = await self._handle_text_analysis(content, context)
            elif task_type == "question_answering":
                result = await self._handle_question_answering(content, context)
            else:
                result = await self._handle_generic_request(content, context)
            
            return {
                "status": "success",
                "agent_id": self.name,
                "platform": self.capabilities.platform,
                "result": result,
                "metadata": {
                    "model_used": self.model_name,
                    "processing_time": "calculated_processing_time"
                }
            }
            
        except Exception as e:
            logger.error(f"Error handling A2A request: {e}")
            return {
                "status": "error",
                "agent_id": self.name,
                "platform": self.capabilities.platform,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def _handle_text_generation(self, content: str, context: Dict[str, Any]) -> str:
        """Handle text generation requests using Vertex AI"""
        prompt = f"Generate text based on: {content}"
        if context.get("style"):
            prompt += f" Style: {context['style']}"
        
        response = await self.vertex_ai_model.generate_text(prompt)
        return response.text
    
    async def _handle_text_analysis(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle text analysis requests"""
        prompt = f"Analyze the following text and provide insights: {content}"
        
        response = await self.vertex_ai_model.generate_text(prompt)
        
        return {
            "analysis": response.text,
            "word_count": len(content.split()),
            "character_count": len(content),
            "analysis_type": context.get("analysis_type", "general")
        }
    
    async def _handle_question_answering(self, content: str, context: Dict[str, Any]) -> str:
        """Handle question answering requests"""
        question = content
        background_context = context.get("background", "")
        
        prompt = f"Question: {question}"
        if background_context:
            prompt = f"Context: {background_context}\n\n{prompt}"
        
        response = await self.vertex_ai_model.generate_text(prompt)
        return response.text
    
    async def _handle_generic_request(self, content: str, context: Dict[str, Any]) -> str:
        """Handle generic requests when task type is not specified"""
        prompt = f"Process this request: {content}"
        
        response = await self.vertex_ai_model.generate_text(prompt)
        return response.text

async def main():
    """
    Example usage of BasicA2AGooogleADKAgent
    """
    # Create and initialize agent
    agent = BasicA2AGooogleADKAgent("basic-google-adk-agent")
    await agent.initialize()
    
    # Create A2A server
    server = A2AServer(host="localhost", port=8080)
    
    # Register agent with server
    await server.register_agent(agent)
    
    logger.info("A2A server started with Google ADK agent")
    logger.info(f"Agent capabilities: {await agent.get_capabilities()}")
    
    # Start server (this would run indefinitely in production)
    try:
        await server.start()
    except KeyboardInterrupt:
        logger.info("Shutting down A2A server")
        await server.shutdown()

if __name__ == "__main__":
    asyncio.run(main())