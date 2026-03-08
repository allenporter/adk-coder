from unittest.mock import patch
from adk_coder.mcp import get_mcp_toolsets
from google.adk.tools.mcp_tool import StreamableHTTPConnectionParams
from mcp import StdioServerParameters


def test_get_mcp_toolsets_stdio():
    settings = {
        "mcpServers": {
            "test-stdio": {
                "type": "stdio",
                "command": "python",
                "args": ["-m", "mcp_server"],
            }
        }
    }
    with patch("adk_coder.mcp.McpToolset") as MockToolset:
        toolsets = get_mcp_toolsets(settings)
        assert len(toolsets) == 1
        MockToolset.assert_called_once()
        args, kwargs = MockToolset.call_args
        params = kwargs["connection_params"]
        assert isinstance(params, StdioServerParameters)
        assert params.command == "python"
        assert params.args == ["-m", "mcp_server"]


def test_get_mcp_toolsets_http():
    settings = {
        "mcpServers": {"test-http": {"type": "http", "url": "https://example.com/mcp"}}
    }
    with patch("adk_coder.mcp.McpToolset") as MockToolset:
        toolsets = get_mcp_toolsets(settings)
        assert len(toolsets) == 1
        MockToolset.assert_called_once()
        args, kwargs = MockToolset.call_args
        params = kwargs["connection_params"]
        assert isinstance(params, StreamableHTTPConnectionParams)
        assert params.url == "https://example.com/mcp"


def test_get_mcp_toolsets_legacy():
    settings = {
        "mcp_servers": {"legacy-stdio": {"command": "python", "args": ["-m", "legacy"]}}
    }
    with patch("adk_coder.mcp.McpToolset") as MockToolset:
        toolsets = get_mcp_toolsets(settings)
        assert len(toolsets) == 1
        MockToolset.assert_called_once()
        params = MockToolset.call_args.kwargs["connection_params"]
        assert isinstance(params, StdioServerParameters)


def test_get_mcp_toolsets_invalid():
    settings = {
        "mcpServers": {
            "invalid": {
                "type": "stdio"
                # missing command
            }
        }
    }
    with patch("adk_coder.mcp.McpToolset") as MockToolset:
        toolsets = get_mcp_toolsets(settings)
        assert len(toolsets) == 0
        MockToolset.assert_not_called()
