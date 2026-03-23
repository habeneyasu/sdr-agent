"""Configuration contracts for SDR and Deep Research workflows."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration container.

    Skeleton only: env loading/parsing is intentionally omitted.
    """

    # Provider/model configuration
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
