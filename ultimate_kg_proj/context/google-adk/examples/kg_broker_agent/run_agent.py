#!/usr/bin/env python3
import subprocess
import sys
import os

def run_agent_with_venv(query):
    # Change to the script directory
    script_dir = r"/mnt/c/projects/cc-a2a-agents/kg_broker_cc"
    venv_python = r"/mnt/c/projects/cc-a2a-agents/venv/Scripts/python.exe"
    agent_script = r"/mnt/c/projects/cc-a2a-agents/kg_broker_cc/agent.py"
    
    # Run the agent script with the virtual environment Python via cmd.exe
    win_venv_python = r"C:\projects\cc-a2a-agents\venv\Scripts\python.exe"
    win_agent_script = r"C:\projects\cc-a2a-agents\kg_broker_cc\agent.py"
    win_script_dir = r"C:\projects\cc-a2a-agents\kg_broker_cc"
    
    cmd = ["cmd.exe", "/c", win_venv_python, win_agent_script, query]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr, file=sys.stderr)
        return result.returncode
    except Exception as e:
        print(f"Error running agent: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_agent.py 'your query here'")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    sys.exit(run_agent_with_venv(query))