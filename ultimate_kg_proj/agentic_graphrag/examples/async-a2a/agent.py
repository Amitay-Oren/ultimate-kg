# agent.py (modify get_tools_async and other parts as needed)
# ./adk_agent_samples/mcp_agent/agent.py
import os
import asyncio
import warnings
import logging
import sys
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, SseConnectionParams

# Suppress warnings and set logging level
warnings.filterwarnings("ignore", category=UserWarning)
logging.getLogger().setLevel(logging.ERROR)

# Load environment variables from .env file in the parent directory
# Place this near the top, before using env vars like API keys
load_dotenv('../.env')

# Ensure TARGET_FOLDER_PATH is an absolute path for the MCP server.
TARGET_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "C:/Users/Amitay Oren/graphiti/mcp_server")

# --- Step 1: Agent Definition ---
async def get_agent_async():
  """Creates an ADK Agent equipped with tools from the MCP Server."""
  toolset = MCPToolset(
      # Use StdioServerParameters for local process communication
      #tool_filter=['read_file', 'list_directory'] # Optional: filter specific tools
      # For remote servers, you would use SseServerParams instead:
      connection_params=SseConnectionParams(url="http://127.0.0.1:8000/sse")
      
  )

  # Use in an agent
  root_agent = LlmAgent(
      model='gemini-2.5-flash-lite', # Adjust model name if needed based on availability
      name='graphiti_assistant',
      instruction='You are a helpful agent who can provide interesting facts about the user from a graph database.',
      tools=[toolset], # Provide the MCP tools to the ADK agent
  )
  return root_agent, toolset

# --- Step 2: Main Execution Logic ---
async def async_main(query=None):
  session_service = InMemorySessionService()
  # Artifact service might not be needed for this example
  artifacts_service = InMemoryArtifactService()

  session = await session_service.create_session(
      state={}, app_name='graphiti_mcp_app', user_id='user_graphiti'
  )

  # Use command line argument or default query
  if query is None:
    query = "What do you know about the user?"
  
  print(f"User Query: '{query}'")
  content = types.Content(role='user', parts=[types.Part(text=query)])

  root_agent, toolset = await get_agent_async()

  runner = Runner(
      app_name='graphiti_mcp_app',
      agent=root_agent,
      artifact_service=artifacts_service, # Optional
      session_service=session_service,
  )

  print("Running agent...")
  events_async = runner.run_async(
      session_id=session.id, user_id=session.user_id, new_message=content
  )

  final_response = ""
  async for event in events_async:
    # Only print text responses from the model
    if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts'):
      for part in event.content.parts:
        if hasattr(part, 'text') and part.text:
          final_response = part.text
          print(f"Assistant: {part.text}")
        # Skip function calls and other non-text parts
  
  if not final_response:
    print("No text response received from the agent.")

  # Cleanup is handled automatically by the agent framework
  # But you can also manually close if needed:
  print("Closing MCP server connection...")
  await toolset.close()
  print("Cleanup complete.")

if __name__ == '__main__':
  try:
    # Get query from command line arguments
    if len(sys.argv) > 1:
      query = ' '.join(sys.argv[1:])  # Join all arguments after script name
    else:
      query = None
    
    asyncio.run(async_main(query))
  except Exception as e:
    print(f"An error occurred: {e}")