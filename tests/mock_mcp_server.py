from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("EchoServer")


@mcp.tool()
async def echo(message: str) -> str:
    """Echoes the message back to the user."""
    return f"Echo from MCP: {message}"


if __name__ == "__main__":
    mcp.run()
