#!/usr/bin/env python3
"""
Test script for Push Notification Hook System
=============================================

Tests various hook event scenarios to ensure push notifications work correctly.

Usage:
  python test.py --topic=test-notifications
  python test.py --topic=test-notifications --debug
"""

import json
import sys
import argparse
import subprocess
from pathlib import Path

def run_test_case(test_name: str, test_data: dict, topic: str, debug: bool = False) -> bool:
    """Run a single test case for push notifications."""
    print(f"\n🧪 Testing: {test_name}")
    
    # Convert test data to JSON
    json_input = json.dumps(test_data)
    
    # Prepare command
    script_path = Path(__file__).parent / "handler.py"
    cmd = ["uv", "run", str(script_path), "--topic", topic]
    
    if debug:
        cmd.append("--debug")
    
    try:
        # Run the handler with test data
        result = subprocess.run(
            cmd,
            input=json_input,
            text=True,
            capture_output=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ {test_name} - Success")
            if debug:
                print(f"   stdout: {result.stdout}")
            return True
        else:
            print(f"❌ {test_name} - Failed")
            print(f"   stderr: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_name} - Timeout")
        return False
    except Exception as e:
        print(f"💥 {test_name} - Exception: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test push notification hook system')
    parser.add_argument('--topic', default='test-notifications', help='ntfy.sh topic for testing')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    topic = args.topic
    debug = args.debug
    
    print(f"🚀 Testing Push Notification Hook System")
    print(f"📱 Topic: {topic}")
    print(f"🐛 Debug: {debug}")
    
    # Test cases based on CLAUDE.md examples
    test_cases = [
        # Basic Stop hook
        ("Stop Hook", {
            "hook_event_name": "Stop"
        }),
        
        # SubagentStop hook
        ("SubagentStop Hook", {
            "hook_event_name": "SubagentStop",
            "stop_hook_active": False
        }),
        
        # Notification - Permission request
        ("Permission Request", {
            "hook_event_name": "Notification",
            "message": "Claude Code is requesting permission to use the Bash tool"
        }),
        
        # Notification - Idle timeout
        ("Idle Timeout", {
            "hook_event_name": "Notification",
            "message": "Claude Code is waiting for your input"
        }),
        
        # Notification - General
        ("General Notification", {
            "hook_event_name": "Notification",
            "message": "General system notification"
        }),
        
        # Python file read
        ("Python File Read", {
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/path/to/script.py"}
        }),
        
        # Git command
        ("Git Status", {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "git status"}
        }),
        
        # Task completion
        ("Task Complete", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Edit",
            "tool_input": {"file_path": "/path/to/file.js"}
        }),
        
        # Unknown hook (fallback test)
        ("Unknown Hook", {
            "hook_event_name": "UnknownEvent",
            "tool_name": "UnknownTool"
        }),
    ]
    
    # Run all test cases
    passed = 0
    total = len(test_cases)
    
    for test_name, test_data in test_cases:
        if run_test_case(test_name, test_data, topic, debug):
            passed += 1
    
    # Results
    print(f"\n📊 Test Results:")
    print(f"   Passed: {passed}/{total}")
    print(f"   Failed: {total - passed}/{total}")
    
    if passed == total:
        print(f"🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"⚠️ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()