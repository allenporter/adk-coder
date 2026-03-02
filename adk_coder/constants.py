"""Centralized constants for adk-coder to ensure consistency across modules."""

# The main application identifier used for session storage and Pydantic validation.
# MUST be a valid Python identifier (no hyphens).
APP_NAME = "adk_coder"

# Default Gemini model if none is specified by the user or project settings.
DEFAULT_MODEL = "gemini-3-flash-preview"

# Default history persistence settings.
DEFAULT_SESSION_ID_LENGTH = 8
