"""Tests for agent_factory module: build_runner() and build_adk_agent()."""

from pathlib import Path
from unittest.mock import MagicMock, patch


@patch("adk_coder.agent_factory.get_session_db_path", return_value="/tmp/test.db")
@patch("adk_coder.agent_factory.find_project_root")
@patch("adk_coder.agent_factory.load_settings", return_value={})
@patch("adk_coder.agent_factory.build_adk_agent")
def test_build_runner_returns_runner(
    mock_build_agent: MagicMock,
    mock_settings: MagicMock,
    mock_root: MagicMock,
    mock_db_path: MagicMock,
) -> None:
    """build_runner() should assemble and return a Runner with expected config."""
    mock_agent = MagicMock(name="fake_agent")
    mock_build_agent.return_value = mock_agent

    mock_runner_cls = MagicMock(name="RunnerClass")
    mock_app_cls = MagicMock(name="AppClass")
    mock_session_cls = MagicMock(name="SessionClass")

    with (
        patch("adk_coder.policy.CustomPolicyEngine"),
        patch("adk_coder.policy.SecurityPlugin") as mock_sec,
        patch("google.adk.apps.app.App", mock_app_cls),
        patch("google.adk.runners.Runner", mock_runner_cls),
        patch(
            "google.adk.sessions.sqlite_session_service.SqliteSessionService",
            mock_session_cls,
        ),
    ):
        from adk_coder.agent_factory import build_runner

        runner = build_runner()

    # Verify Runner was constructed
    mock_runner_cls.assert_called_once()
    call_kwargs = mock_runner_cls.call_args[1]
    assert call_kwargs["auto_create_session"] is True
    assert runner == mock_runner_cls.return_value

    # Verify App was constructed with the agent and security plugin
    mock_app_cls.assert_called_once()
    app_kwargs = mock_app_cls.call_args[1]
    assert app_kwargs["root_agent"] == mock_agent
    assert mock_sec.return_value in app_kwargs["plugins"]


@patch("adk_coder.agent_factory.get_session_db_path", return_value="/tmp/test.db")
@patch("adk_coder.agent_factory.find_project_root")
@patch("adk_coder.agent_factory.load_settings", return_value={})
@patch("adk_coder.agent_factory.build_adk_agent")
def test_build_runner_passes_model_through(
    mock_build_agent: MagicMock,
    mock_settings: MagicMock,
    mock_root: MagicMock,
    mock_db_path: MagicMock,
) -> None:
    """build_runner(model=...) should forward the model to build_adk_agent()."""
    with (
        patch("adk_coder.policy.CustomPolicyEngine"),
        patch("adk_coder.policy.SecurityPlugin"),
        patch("google.adk.apps.app.App"),
        patch("google.adk.runners.Runner"),
        patch("google.adk.sessions.sqlite_session_service.SqliteSessionService"),
    ):
        from adk_coder.agent_factory import build_runner

        build_runner(model="gemini-2.0-flash")

    mock_build_agent.assert_called_once_with("gemini-2.0-flash", workspace_path=None)


@patch("adk_coder.agent_factory.get_session_db_path", return_value="/tmp/test.db")
@patch("adk_coder.agent_factory.find_project_root")
@patch("adk_coder.agent_factory.load_settings", return_value={})
@patch("adk_coder.agent_factory.build_adk_agent")
def test_build_runner_uses_permission_mode(
    mock_build_agent: MagicMock,
    mock_settings: MagicMock,
    mock_root: MagicMock,
    mock_db_path: MagicMock,
) -> None:
    """build_runner(permission_mode=...) should create a matching CustomPolicyEngine."""
    with (
        patch("adk_coder.policy.CustomPolicyEngine") as mock_policy,
        patch("adk_coder.policy.SecurityPlugin"),
        patch("google.adk.apps.app.App"),
        patch("google.adk.runners.Runner"),
        patch("google.adk.sessions.sqlite_session_service.SqliteSessionService"),
    ):
        from adk_coder.agent_factory import build_runner
        from adk_coder.policy import PermissionMode

        build_runner(permission_mode="auto")

    mock_policy.assert_called_once()
    call_kwargs = mock_policy.call_args[1]
    assert call_kwargs["mode"] == PermissionMode("auto")


@patch("adk_coder.agent_factory.get_session_db_path", return_value="/tmp/test.db")
@patch("adk_coder.agent_factory.find_project_root")
@patch("adk_coder.agent_factory.load_settings", return_value={})
@patch("adk_coder.agent_factory.build_adk_agent")
def test_build_runner_passes_workspace_path(
    mock_build_agent: MagicMock,
    mock_settings: MagicMock,
    mock_root: MagicMock,
    mock_db_path: MagicMock,
) -> None:
    """build_runner(workspace_path=...) should forward it to build_adk_agent() and find_project_root()."""
    ws = Path("/srv/workspaces/my-project")

    with (
        patch("adk_coder.policy.CustomPolicyEngine"),
        patch("adk_coder.policy.SecurityPlugin"),
        patch("google.adk.apps.app.App"),
        patch("google.adk.runners.Runner"),
        patch("google.adk.sessions.sqlite_session_service.SqliteSessionService"),
    ):
        from adk_coder.agent_factory import build_runner

        build_runner(workspace_path=ws)

    mock_build_agent.assert_called_once_with(None, workspace_path=ws)


def test_build_adk_agent_passes_workspace_path() -> None:
    """build_adk_agent(workspace_path=...) should forward it to find_project_root() and discover_skills()."""
    ws = Path("/srv/workspaces/my-project")
    fake_root = Path("/srv/workspaces/my-project")

    with (
        patch(
            "adk_coder.agent_factory.find_project_root", return_value=fake_root
        ) as mock_root,
        patch(
            "adk_coder.agent_factory.load_settings",
            return_value={"default_model": "test-model"},
        ),
        patch("adk_coder.skills.discover_skills", return_value=[]) as mock_skills,
        patch("adk_coder.tools.get_essential_tools", return_value=[]),
        patch("adk_coder.retry_gemini.AdkRetryGemini"),
        patch("google.adk.agents.llm_agent.LlmAgent"),
        patch("google.adk.planners.BuiltInPlanner"),
        patch("google.genai.types"),
    ):
        from adk_coder.agent_factory import build_adk_agent

        build_adk_agent(workspace_path=ws)

    mock_root.assert_called_once_with(ws)
    mock_skills.assert_called_once_with(ws)
