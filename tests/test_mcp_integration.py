import asyncio
import os
import sys
from pathlib import Path

# Add project root to sys.path for direct script execution
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from google.adk.tools import McpToolset  # noqa: E402
from mcp import StdioServerParameters  # noqa: E402
from adk_coder.agent_factory import build_runner  # noqa: E402
from google.genai import types  # noqa: E402


async def main():
    print("🚀 Starting MCP Integration Trial...")

    # Define a simple MCP server (using the local mock_mcp_server.py)
    try:
        mcp_server = McpToolset(
            connection_params=StdioServerParameters(
                command=sys.executable,
                args=[str(project_root / "tests" / "mock_mcp_server.py")],
            ),
            tool_name_prefix="mcp_",
        )
        print("✅ MCP Toolset initialized.")
    except Exception as e:
        print(f"❌ Failed to initialize MCP Toolset: {e}")
        return

    # Build the runner with the MCP toolset
    try:
        runner = build_runner(extra_tools=[mcp_server])
        print("✅ Runner built with MCP support.")
    except Exception as e:
        print(f"❌ Failed to build runner: {e}")
        return

    # Simple task for the agent to verify it can see and use MCP tools
    prompt = "List all your available tools. Please tell me if you see any tools with 'mcp_' prefix."

    print(f"\n💬 Querying agent: '{prompt}'")

    new_message = types.Content(role="user", parts=[types.Part(text=prompt)])

    try:
        async for event in runner.run_async(
            user_id="mcp-test-user",
            session_id="mcp-test-session",
            new_message=new_message,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"🤖 Agent: {part.text}")

            for call in event.get_function_calls():
                print(f"🛠️ Executing tool: {call.name}({call.args})")

        print("\n✅ MCP integration trial complete.")
    except Exception as e:
        print(f"\n❌ Error during agent execution: {e}")


if __name__ == "__main__":
    if not os.environ.get("GOOGLE_API_KEY"):
        print(
            "⚠️  GOOGLE_API_KEY not found in environment. Please export it before running this script."
        )
        sys.exit(1)

    asyncio.run(main())
