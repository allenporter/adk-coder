import asyncio
import os
import sys
import json
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from adk_coder.agent_factory import build_runner  # noqa: E402
from google.genai import types  # noqa: E402


async def main():
    print("🚀 Starting Config-based MCP Integration Trial...")

    # Define the mock settings with an MCP server
    mcp_config = {
        "mcpServers": {
            "mock": {
                "type": "stdio",
                "command": sys.executable,
                "args": [str(project_root / "tests" / "mock_mcp_server.py")],
            }
        }
    }

    # Create a local .adk/settings.json for this test
    adk_dir = project_root / ".adk"
    adk_dir.mkdir(exist_ok=True)
    settings_path = adk_dir / "settings.json"

    original_settings = None
    if settings_path.exists():
        original_settings = settings_path.read_text()

    import logging

    logging.basicConfig(level=logging.DEBUG)

    try:
        settings_path.write_text(json.dumps(mcp_config, indent=2))
        print(f"✅ Created local settings with MCP config at {settings_path}")

        # Build the runner - it should now automatically pick up the MCP server
        runner = build_runner(permission_mode="auto")
        print("✅ Runner built (should have auto-loaded MCP tools).")

        # Query the agent to verify it sees the mock MCP tool
        prompt = "List your tools. Do you see 'echo'?"
        print(f"\n💬 Querying agent: '{prompt}'")

        new_message = types.Content(role="user", parts=[types.Part(text=prompt)])

        async for event in runner.run_async(
            user_id="config-mcp-test",
            session_id="config-mcp-session",
            new_message=new_message,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"🤖 Agent: {part.text}")

            for call in event.get_function_calls():
                print(f"🛠️ Executing tool: {call.name}")

    finally:
        # Restore original settings
        if original_settings:
            settings_path.write_text(original_settings)
        else:
            settings_path.unlink(missing_ok=True)
        print("\n🧹 Cleaned up test settings.")


if __name__ == "__main__":
    if not os.environ.get("GOOGLE_API_KEY"):
        print("⚠️  GOOGLE_API_KEY not found in environment.")
        sys.exit(1)

    asyncio.run(main())
