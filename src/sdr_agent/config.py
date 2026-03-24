"""Configuration contracts for SDR and Deep Research workflows."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration container.
    """

    # OpenAI-compatible provider/model configuration
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    planner_model: str | None = None
    search_model: str | None = None
    writer_model: str | None = None
    email_model: str | None = None

    # Email delivery configuration
    sendgrid_api_key: str | None = None
    mail_from: str | None = None
    mail_to: str | None = None

    # App/UI runtime configuration
    gradio_server_name: str | None = None
    gradio_server_port: int | None = None

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load configuration from environment variables."""
        openai_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        openai_base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENROUTER_BASE_URL")
        return cls(
            openai_api_key=openai_api_key,
            openai_base_url=openai_base_url,
            planner_model=os.getenv("PLANNER_MODEL") or os.getenv("MODEL_DEFAULT"),
            search_model=os.getenv("SEARCH_MODEL") or os.getenv("MODEL_DEFAULT"),
            writer_model=os.getenv("WRITER_MODEL") or os.getenv("MODEL_DEFAULT"),
            email_model=os.getenv("EMAIL_MODEL") or os.getenv("MODEL_DEFAULT"),
            sendgrid_api_key=os.getenv("SENDGRID_API_KEY"),
            mail_from=os.getenv("MAIL_FROM"),
            mail_to=os.getenv("MAIL_TO"),
            gradio_server_name=os.getenv("GRADIO_SERVER_NAME"),
            gradio_server_port=_parse_int(os.getenv("GRADIO_SERVER_PORT")),
        )


def ensure_openai_env_aliases() -> None:
    """Mirror OpenRouter env vars to OpenAI names for SDKs that require OPENAI_*."""
    if not os.getenv("OPENAI_API_KEY") and os.getenv("OPENROUTER_API_KEY"):
        os.environ["OPENAI_API_KEY"] = os.environ["OPENROUTER_API_KEY"]
    if not os.getenv("OPENAI_BASE_URL") and os.getenv("OPENROUTER_BASE_URL"):
        os.environ["OPENAI_BASE_URL"] = os.environ["OPENROUTER_BASE_URL"]


def _parse_int(value: str | None) -> int | None:
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None
