# Model Context Protocol (MCP) Support

`adk-coder` supports external tool servers via the **Model Context Protocol (MCP)**. This allows you to extend the agent's capabilities with any MCP-compliant server (e.g., specialized databases, API integrations, or local scripts).

## CLI-Based Management (Easiest)

You can manage your global MCP server connections directly from the CLI using the `mcp` command group.

### List Servers
```bash
adk-coder mcp list
```

### Add a Server (Local)
```bash
# adk-coder mcp add <name> <command> [args...]
adk-coder mcp add everything npx -y @modelcontextprotocol/server-everything
```

### Add a Server (Remote)
```bash
# adk-coder mcp add <name> <url>
adk-coder mcp add my-remote https://example.com/mcp
```

### Remove a Server
```bash
adk-coder mcp remove everything
```

## Configuration-Based Setup

You can also manually specify MCP servers in your `settings.json` (either global at `~/.adk/settings.json` or project-local at `.adk/settings.json`). This is useful for project-specific tools.

Example `local` server:
```json
{
  "mcpServers": {
    "everything": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-everything"]
    }
  }
}
```

Example `remote` server (Streamable HTTP):
```json
{
  "mcpServers": {
    "my-remote": {
      "type": "http",
      "url": "https://example.com/mcp"
    }
  }
}
```

If you have multiple MCP servers, `adk-coder` will automatically prefix their tool names with the server name (e.g., `everything_echo`) to avoid collisions.

## Programmatic Usage

If you are building a custom agent script, you can also manually instantiate an `McpToolset` and pass it to `extra_tools`.

```python
from google.adk.tools import McpToolset
from mcp import StdioServerParameters
from adk_coder.agent_factory import build_runner

# Define the MCP server connection
mcp_server = McpToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-everything"],
        env=None
    )
)

# Build the runner with the MCP toolset
runner = build_runner(
    extra_tools=[mcp_server]
)
```

## Manual Trial

A sample script is provided in `tests/test_mcp_integration.py` which demonstrates connecting to a simple MCP server and verifying that the agent can use its tools.

### Running the Trial

1. Ensure you have the `mcp` Python package installed (it should be installed as a dependency of `google-adk`).
2. Run the test script:

```bash
python tests/test_mcp_integration.py
```

## Advanced Configuration

You can filter which tools from the MCP server are exposed to the agent using the `tool_filter` argument:

```python
mcp_server = McpToolset(
    connection_params=...,
    tool_filter=["allowed_tool_1", "allowed_tool_2"]
)
```

You can also add a prefix to MCP tool names to avoid collisions with built-in tools:

```python
mcp_server = McpToolset(
    connection_params=...,
    tool_name_prefix="mcp_"
)
```
