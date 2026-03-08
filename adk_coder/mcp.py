import logging
from typing import Any
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool import StreamableHTTPConnectionParams
from mcp import StdioServerParameters

logger = logging.getLogger(__name__)

MCP_SERVERS_KEY = "mcpServers"
MCP_SERVERS_LEGACY_KEY = "mcp_servers"


def get_mcp_toolsets(settings: dict[str, Any]) -> list[McpToolset]:
    """Returns a list of McpToolset objects from the given settings."""
    mcp_toolsets = []
    mcp_config = settings.get("mcpServers") or settings.get("mcp_servers")

    if mcp_config and isinstance(mcp_config, dict):
        for name, cfg in mcp_config.items():
            if not isinstance(cfg, dict):
                continue

            mcp_type = cfg.get("type")
            try:
                params = None
                # Determine params based on explicit type or legacy field detection
                if mcp_type == "http" or "url" in cfg:
                    if "url" not in cfg:
                        logger.warning(
                            "Invalid HTTP MCP config for %s: missing 'url'", name
                        )
                        continue
                    params = StreamableHTTPConnectionParams(
                        url=cfg["url"],
                        headers=cfg.get("headers"),
                        timeout=cfg.get("timeout", 5.0),
                    )
                elif mcp_type == "stdio" or "command" in cfg:
                    if "command" not in cfg:
                        logger.warning(
                            "Invalid Stdio MCP config for %s: missing 'command'", name
                        )
                        continue
                    params = StdioServerParameters(
                        command=cfg["command"],
                        args=cfg.get("args", []),
                        env=cfg.get("env"),
                    )

                if params:
                    mcp_toolset = McpToolset(
                        connection_params=params,
                        tool_name_prefix=f"{name}_" if len(mcp_config) > 1 else None,
                    )
                    mcp_toolsets.append(mcp_toolset)
                    logger.debug(
                        "Loaded MCP toolset: %s (type: %s)", name, mcp_type or "legacy"
                    )
            except Exception as e:
                logger.error("Failed to load MCP toolset %s: %s", name, e)
    return mcp_toolsets
