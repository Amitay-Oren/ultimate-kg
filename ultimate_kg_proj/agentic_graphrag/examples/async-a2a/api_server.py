#!/usr/bin/env python3
"""
Flask API wrapper for the Graphiti MCP Agent
Exposes the agent functionality via HTTP endpoints for easy access from Claude Code
"""

import asyncio
import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import our agent
from agent import async_main

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route('/query', methods=['POST'])
def query_agent():
    """
    Query the Graphiti knowledge graph via the MCP agent
    
    Expected JSON payload:
    {
        "query": "What do you know about the user?"
    }
    
    Returns:
    {
        "query": "original query",
        "response": "agent response",
        "status": "success"
    }
    """
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing 'query' field in JSON payload",
                "status": "error"
            }), 400
        
        query = data['query']
        
        # Capture the agent's response
        original_stdout = sys.stdout
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            # Run the async agent
            asyncio.run(async_main(query))
            
            # Get the captured output
            output = captured_output.getvalue()
            sys.stdout = original_stdout
            
            # Extract just the assistant response from the output
            lines = output.split('\n')
            assistant_response = ""
            for line in lines:
                if line.startswith("Assistant: "):
                    assistant_response = line[11:]  # Remove "Assistant: " prefix
                    break
            
            if not assistant_response:
                assistant_response = "No response received from agent"
            
            return jsonify({
                "query": query,
                "response": assistant_response,
                "status": "success"
            })
            
        except Exception as e:
            sys.stdout = original_stdout
            return jsonify({
                "query": query,
                "error": f"Agent execution failed: {str(e)}",
                "status": "error"
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": f"Request processing failed: {str(e)}",
            "status": "error"
        }), 500

@app.route('/query', methods=['GET'])
def query_agent_get():
    """
    Query via GET request with query parameter for simple curl usage
    
    Usage: curl "http://localhost:8080/query?q=What+do+you+know+about+the+user"
    """
    try:
        query = request.args.get('q', 'What do you know about the user?')
        
        # Use the same logic as POST but with GET parameter
        original_stdout = sys.stdout
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            asyncio.run(async_main(query))
            output = captured_output.getvalue()
            sys.stdout = original_stdout
            
            lines = output.split('\n')
            assistant_response = ""
            for line in lines:
                if line.startswith("Assistant: "):
                    assistant_response = line[11:]
                    break
            
            if not assistant_response:
                assistant_response = "No response received from agent"
            
            return jsonify({
                "query": query,
                "response": assistant_response,
                "status": "success"
            })
            
        except Exception as e:
            sys.stdout = original_stdout
            return jsonify({
                "query": query,
                "error": f"Agent execution failed: {str(e)}",
                "status": "error"
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": f"Request processing failed: {str(e)}",
            "status": "error"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Graphiti MCP Agent API",
        "version": "1.0.0"
    })

@app.route('/', methods=['GET'])
def home():
    """API documentation"""
    return jsonify({
        "service": "Graphiti MCP Agent API",
        "version": "1.0.0",
        "endpoints": {
            "POST /query": "Query the knowledge graph with JSON payload: {'query': 'your question'}",
            "GET /query?q=<query>": "Query the knowledge graph with URL parameter",
            "GET /health": "Health check",
            "GET /": "This documentation"
        },
        "examples": {
            "curl_post": "curl -X POST http://localhost:8080/query -H 'Content-Type: application/json' -d '{\"query\": \"What do you know about the user?\"}'",
            "curl_get": "curl 'http://localhost:8080/query?q=What+are+my+hobbies'"
        }
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    print(f"Starting Graphiti MCP Agent API server on {host}:{port}")
    print(f"Health check: http://{host}:{port}/health")
    print(f"Documentation: http://{host}:{port}/")
    
    app.run(host=host, port=port, debug=debug)