#!/usr/bin/env python3
"""
Basic Chat Agent Example using Google Agent Development Kit (ADK)

This example demonstrates how to create a simple conversational agent using Google ADK
with environment-based configuration and basic conversation handling.
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables
load_dotenv()

def create_basic_chat_agent():
    """
    Create a basic conversational agent using Google ADK.
    
    Returns:
        Agent: A configured Google ADK agent for conversation
    """
    
    agent = Agent(
        name="basic_chat_assistant",
        model=os.getenv("ADK_MODEL", "gemini-2.0-flash"),
        instruction=(
            "You are a helpful and friendly conversational assistant. "
            "Engage in natural conversation, answer questions clearly, "
            "and provide helpful information. Be concise but informative."
        ),
        description="A basic conversational agent for general chat and assistance"
    )
    
    return agent

def main():
    """Main function to run the basic chat agent."""
    
    print("🤖 Google ADK Basic Chat Agent")
    print("=" * 40)
    print("Type 'exit' to end the conversation\n")
    
    # Create the agent
    agent = create_basic_chat_agent()
    
    # Start conversation loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit condition
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Agent: Goodbye! Have a great day! 👋")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Get agent response
            response = agent.run(user_input)
            print(f"Agent: {response}")
            print()  # Add blank line for readability
            
        except KeyboardInterrupt:
            print("\n\nAgent: Goodbye! Have a great day! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.\n")

if __name__ == "__main__":
    main()