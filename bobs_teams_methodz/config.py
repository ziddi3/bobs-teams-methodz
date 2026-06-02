"""
Bob's Teams Methodz - Centralized Configuration
Loads environment variables safely from .env files or system environment.
NEVER hardcode secrets — this module is the single source of truth for all config.
"""

import os
from typing import Optional

# Attempt to load .env file via python-dotenv (optional dependency)
try:
    from dotenv import load_dotenv, find_dotenv
    # Load from .env in the project root (walking up from this file)
    _env_path = find_dotenv(usecwd=True)
    if _env_path:
        load_dotenv(_env_path, override=False)
except ImportError:
    # python-dotenv not available; rely on system env vars only
    pass


# ---------------------------------------------------------------------------
# Public config helpers — every module should call these instead of
# os.environ.get(...) directly so that .env loading is guaranteed to have
# happened at least once before any value is read.
# ---------------------------------------------------------------------------

def get_workspace() -> str:
    """Return the root workspace directory (defaults to /workspace)."""
    return os.environ.get("BOB_WORKSPACE", "/workspace")


def get_github_token() -> Optional[str]:
    """Return the GitHub personal-access token (or None if unset)."""
    return os.environ.get("GITHUB_TOKEN")


def get_ai_model_api_key() -> Optional[str]:
    """Return the primary AI model API key (Groq) (or None if unset)."""
    return os.environ.get("AI_MODEL_API_KEY")


def get_xai_api_key() -> Optional[str]:
    """Return the xAI / Grok API key (or None if unset)."""
    return os.environ.get("XAI_API_KEY")


def get_required_key(name: str) -> str:
    """
    Fetch an environment variable that *must* exist.
    Raises a clear RuntimeError if it is missing, so the user sees a
    helpful message instead of a cryptic NoneType error downstream.
    """
    value = os.environ.get(name)
    if value is None:
        raise RuntimeError(
            f"Required environment variable '{name}' is not set. "
            f"Please add it to your .env file or system environment."
        )
    return value


# Convenience: expose package-level constants
PACKAGE_DIR = "bobs_teams_methodz"
BRAND = "Bob's Teams Methodz"
TAGLINE = "The Only Methodz"
VERSION = "1.0.0"
