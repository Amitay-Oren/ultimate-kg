#!/usr/bin/env python3
"""
Clean startup script for Agentic GraphRAG A2A Server

This script provides a simple way to start the A2A server without
dealing with Python module import complexities.
"""

import asyncio
import logging
from server.a2a_server import AgenticGraphRAGServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Start the Agentic GraphRAG A2A Server"""
    logger.info("🚀 Starting Agentic GraphRAG A2A Server...")
    
    try:
        server = AgenticGraphRAGServer()
        await server.start()
    except KeyboardInterrupt:
        logger.info("👋 Server shutdown requested by user")
        if 'server' in locals():
            await server.shutdown()
    except Exception as e:
        logger.error(f"❌ Server failed to start: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())