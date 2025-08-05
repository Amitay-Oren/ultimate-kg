# Push Notification Hook System

This module provides persistent push notification capabilities for Claude Code via ntfy.sh, complementing the existing voice notification system for remote monitoring of development activities.

## Features

- **Context-aware notifications** - 100+ different messages based on file types, commands, and operations
- **Message variations** - Random selection from multiple notification options for variety  
- **Dual hook architecture** - Works alongside voice notifications for comprehensive feedback
- **Priority levels** - Different urgency levels (1-5) for different hook types
- **Custom tags** - Emoji indicators and custom tag support for notification categories
- **Graceful fallbacks** - Always provides a notification even if specific mappings are missing
- **Module-specific logging** - Independent debug logging system prevents conflicts
- **Cross-platform support** - Mobile, tablet, and desktop notifications via ntfy.sh

## Quick Start

### 1. Subscribe to Notifications

Subscribe to the ntfy.sh topic on your mobile device or desktop:
- **Mobile**: Install ntfy app, subscribe to `claude-code-notifications`
- **Desktop**: Visit https://ntfy.sh/claude-code-notifications in browser
- **Custom topic**: Use any topic name in configuration

### 2. Configuration

Push notifications are configured in `.claude/settings.json` alongside voice notifications for comprehensive feedback:

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [
        {"command": "uv run .claude/hooks/voice_notifications/handler.py --voice=alfred"},
        {"command": "uv run .claude/hooks/push_notifications/handler.py --topic=claude-code-notifications"}
      ]
    }],
    "Notification": [{
      "hooks": [
        {"command": "uv run .claude/hooks/voice_notifications/handler.py --voice=alfred"},
        {"command": "uv run .claude/hooks/push_notifications/handler.py --topic=claude-code-notifications --priority=4 --tags=🔔"}
      ]
    }],
    "PreToolUse": [{
      "hooks": [
        {"command": "uv run .claude/hooks/voice_notifications/handler.py --voice=alfred"},
        {"command": "uv run .claude/hooks/push_notifications/handler.py --topic=claude-code-notifications --priority=2"}
      ]
    }]
  }
}
```

### 3. Customization

#### Change Topic Name
Edit the `--topic` parameter in `.claude/settings.json`:
```bash
--topic=my-custom-topic
```

#### Adjust Priorities
- **Stop hooks**: Priority 3 (default)
- **PreToolUse hooks**: Priority 2 (low priority)
- **Notification hooks**: Priority 4 (high priority)

#### Custom Server
Use your own ntfy.sh server:
```bash
--server=https://my-ntfy-server.com
```

## Testing

### Manual Testing

Test individual hook events:

```bash
# Test Stop hook
echo '{"hook_event_name": "Stop"}' | uv run .claude/hooks/push_notifications/handler.py --topic=test-notifications

# Test permission request
echo '{"hook_event_name": "Notification", "message": "Permission required"}' | uv run .claude/hooks/push_notifications/handler.py --topic=test-notifications

# Test file operation  
echo '{"hook_event_name": "PostToolUse", "tool_name": "Read", "tool_input": {"file_path": "example.py"}}' | uv run .claude/hooks/push_notifications/handler.py --topic=test-notifications
```

### Automated Testing

Run the comprehensive test suite:

```bash
# Basic tests
uv run .claude/hooks/push_notifications/test.py --topic=test-notifications

# Debug mode
uv run .claude/hooks/push_notifications/test.py --topic=test-notifications --debug
```

### Debugging

Enable debug logging:
```bash
echo '{"hook_event_name": "Stop"}' | uv run .claude/hooks/push_notifications/handler.py --topic=test-notifications --debug
```

Check debug logs:
```bash
cat .claude/hooks/push_notifications/debug.log
```

## Architecture

### Files Structure
```
.claude/hooks/push_notifications/
├── handler.py                     # Main notification handler (440+ lines)
├── notification_mapping.json     # Message mappings with 100+ variations
├── test.py                       # Comprehensive test suite
├── debug.log                     # Module-specific logging
└── README.md                     # This documentation
```

### Hook Events Supported

- **Stop**: Task completion with multiple message variations
- **SubagentStop**: Subagent task completion tracking
- **Notification**: Permission requests, idle timeouts, general notifications
- **PreToolUse**: Context-aware tool operation notifications
- **PostToolUse**: Operation completion notifications
- **UserPromptSubmit**: User input acknowledgment

### Context-Aware Patterns

**File Operations:**
- Python files: "Editing Python code"
- JavaScript/TypeScript: "Modifying JavaScript file"
- Documentation: "Updating documentation"
- Configuration: "Changing settings"

**Bash Commands:**
- Git operations: "Pushing to remote", "Staging files"
- Package management: "Installing dependencies"
- System commands: "Running system command"

## Message Variations

The system includes 100+ different notification messages with variations for:

- **Stop events**: "Task completed", "Work finished", "Request fulfilled"
- **Permission requests**: "Authorization needed", "Requesting permission"
- **File operations**: Different messages for Python, JS, docs, config files
- **Git operations**: Specific messages for status, commit, push, pull
- **Package management**: NPM, UV, pip command notifications

## Integration with Voice Notifications

Push notifications work seamlessly alongside the existing Alfred voice notifications in a dual hook architecture:

- **Voice notifications**: Immediate audio feedback during active development work
- **Push notifications**: Persistent mobile/desktop notifications for remote monitoring
- **Shared intelligence**: Both systems use similar context-aware patterns and message variations
- **Independent logging**: Each system maintains its own debug log to prevent conflicts
- **Graceful fallbacks**: Systems operate independently - if one fails, the other continues
- **Unified configuration**: Both hooks configured together in `.claude/settings.json`

## Configuration Options

### Command Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--topic` | *required* | ntfy.sh topic name |
| `--server` | `https://ntfy.sh` | Server URL |
| `--priority` | `3` | Priority level (1-5) |
| `--tags` | `🤖` | Emoji tags |
| `--debug` | `false` | Verbose logging |

### Hook Configuration Examples

**Stop hooks only:**
```json
"Stop": [{
  "hooks": [{
    "command": "uv run .claude/hooks/push_notifications/handler.py --topic=claude-code --priority=4"
  }]
}]
```

**High-priority notifications:**
```json
"Notification": [{
  "hooks": [{
    "command": "uv run .claude/hooks/push_notifications/handler.py --topic=urgent-alerts --priority=5 --tags=🚨"
  }]
}]
```

**Custom server:**
```json
"Stop": [{
  "hooks": [{
    "command": "uv run .claude/hooks/push_notifications/handler.py --topic=my-topic --server=https://my-server.com"
  }]
}]
```

## Dependencies

- **Python**: 3.13+ (with native type annotations)
- **httpx**: HTTP client for ntfy.sh API calls (installed via `uv add httpx`)
- **pathlib**: Modern file path handling (Python standard library)
- **json**: Hook data processing (Python standard library)
- **uv**: Python package manager and script runner
- **random**: Message variation selection (Python standard library)

## Troubleshooting

### Common Issues

1. **No notifications received**
   - Check topic subscription in ntfy app/browser
   - Verify topic name matches configuration
   - Check debug logs for errors

2. **Handler fails to start**
   - Ensure httpx is installed: `uv add httpx`
   - Check Python version compatibility
   - Review debug logs

3. **Network errors**
   - Verify internet connectivity
   - Test with curl: `curl -d "test" ntfy.sh/your-topic`
   - Check server URL if using custom server

### Debug Information

All operations are logged to `.claude/hooks/push_notifications/debug.log` with comprehensive context:
- Hook event details with timestamps and emojis
- Notification mapping results and message selection
- HTTP request/response information and status codes
- Error messages and stack traces for troubleshooting
- Performance timing information for optimization
- Context-aware pattern matching details

### Log Analysis

View recent activity:
```bash
tail -f .claude/hooks/push_notifications/debug.log
```

Search for errors:
```bash
grep "ERROR" .claude/hooks/push_notifications/debug.log
```

Filter by hook type:
```bash
grep "Stop" .claude/hooks/push_notifications/debug.log
```