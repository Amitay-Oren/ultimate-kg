from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams
#from utils.custom_adk_patches import CustomMCPToolset  # Uncomment if you actually need it
from parallel_extraction.agent import processing_agent_tool
from .prompt import orchestrator_prompt


def create_orchestrator_agent():
    name = "orchestrator_agent"
    model = "gemini-2.5-pro"
    description = "AN advanced user facing agent that chats with the user and gathers facts from the user and sends them to the knowledge graph broker, and generates queries."
    instruction = orchestrator_prompt
    tools = [
        processing_agent_tool
    ]

    return LlmAgent(
        name=name,
        model=model,
        description=description,
        instruction=instruction,
        tools=tools,
    )

root_agent = create_orchestrator_agent()
