"""Deep-research email agent contract and OpenAI implementation."""

from typing import Protocol

from sdr_agent.config import AppConfig
from sdr_agent.integrations.openai_provider import OpenAIProvider
from sdr_agent.schemas import ReportData

EMAIL_INSTRUCTIONS = (
    "You send a professional HTML email from a markdown report. "
    "Create a clear subject line, convert markdown to readable HTML, and send exactly one email."
)


class EmailAgent(Protocol):
    """Defines behavior for report-to-HTML conversion and SendGrid delivery."""

    async def send_report(self, report: ReportData) -> None:
        """Send the report as a formatted outbound email."""
        ...


class OpenAIEmailAgent:
    """OpenAI Agents SDK implementation for HTML email delivery."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._provider = OpenAIProvider(config)
        self._agent = self._build_agent()

    def _build_agent(self) -> object:
        try:
            from agents import Agent, function_tool
        except ImportError as exc:
            raise RuntimeError(
                "OpenAI Agents SDK is required. Install with: pip install openai-agents"
            ) from exc

        @function_tool
        def send_email(subject: str, html_body: str) -> str:
            """Send one HTML email via SendGrid."""
            if not self._config.sendgrid_api_key:
                raise RuntimeError("Missing SENDGRID_API_KEY in AppConfig.")
            if not self._config.mail_from or not self._config.mail_to:
                raise RuntimeError("Missing mail_from/mail_to in AppConfig.")
            try:
                import importlib

                sendgrid_mod = importlib.import_module("sendgrid")
                mail_mod = importlib.import_module("sendgrid.helpers.mail")
            except ImportError as exc:
                raise RuntimeError("sendgrid is required. Install with: pip install sendgrid") from exc

            client = sendgrid_mod.SendGridAPIClient(api_key=self._config.sendgrid_api_key)
            message = mail_mod.Mail(
                mail_mod.Email(self._config.mail_from),
                mail_mod.To(self._config.mail_to),
                subject,
                mail_mod.Content("text/html", html_body),
            ).get()
            client.client.mail.send.post(request_body=message)
            return "success"

        model = self._provider.resolve_model(self._config.email_model or "gpt-4o-mini")
        return Agent(
            name="EmailAgent",
            instructions=EMAIL_INSTRUCTIONS,
            tools=[send_email],
            model=model,
        )

    async def send_report(self, report: ReportData) -> None:
        """Convert markdown report to HTML and send using tool-enabled agent."""
        try:
            from agents import Runner
        except ImportError as exc:
            raise RuntimeError(
                "OpenAI Agents SDK is required. Install with: pip install openai-agents"
            ) from exc

        await Runner.run(self._agent, report.markdown_report)
