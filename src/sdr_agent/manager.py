"""Orchestration for the SDR sales workflow."""

from sdr_agent.agents.email_agent import OpenAIEmailAgent
from sdr_agent.agents.guardrails import GuardrailsAgent
from sdr_agent.config import AppConfig
from sdr_agent.integrations.openai_provider import OpenAIProvider
from sdr_agent.schemas import ReportData, ResearchQuery, SectionSummary, SummaryReport

SDR_EMAIL_INSTRUCTIONS = (
    "You are an expert B2B SaaS Sales Development Representative. "
    "Draft one professional outbound cold email tailored to the user's topic. "
    "Keep it concise, credible, and conversion-focused. Include: subject line, opening hook, "
    "value proposition, proof point, and clear CTA."
)


class SDRManager:
    """Generate and deliver professional SDR outbound emails."""

    def __init__(
        self,
        config: AppConfig | None = None,
        guardrails: GuardrailsAgent | None = None,
    ) -> None:
        self._config = config or AppConfig()
        self._provider = OpenAIProvider(self._config)
        self._agent = self._build_agent()
        self._emailer = OpenAIEmailAgent(self._config)
        self._guardrails = guardrails

    async def run(self, query: ResearchQuery) -> SummaryReport:
        """Execute SDR workflow and return a structured sales report/email package."""
        email_body = await self._generate_email(topic=query.topic)
        subject = self._extract_subject(email_body)
        summary = SummaryReport(
            title=f"SDR Outreach Email: {query.topic}",
            executive_summary="Generated one professional outbound email and dispatched via delivery agent.",
            sections=[SectionSummary(heading=subject, content=email_body)],
            sources=[],
            follow_up_questions=[],
        )
        if self._guardrails is not None:
            summary = await self._guardrails.validate(summary)
        await self._emailer.send_report(report=self._to_report_data(email_body))
        return summary

    def _build_agent(self) -> object:
        try:
            from agents import Agent
        except ImportError as exc:
            raise RuntimeError(
                "OpenAI Agents SDK is required. Install with: pip install openai-agents"
            ) from exc
        model = self._provider.resolve_model(self._config.email_model or "gpt-4o-mini")
        return Agent(
            name="SDREmailAgent",
            instructions=SDR_EMAIL_INSTRUCTIONS,
            model=model,
        )

    async def _generate_email(self, topic: str) -> str:
        try:
            from agents import Runner
        except ImportError as exc:
            raise RuntimeError(
                "OpenAI Agents SDK is required. Install with: pip install openai-agents"
            ) from exc
        prompt = (
            f"Target topic: {topic}\n"
            "Write one polished B2B SDR outreach email in markdown. "
            "Start with a Subject: line."
        )
        result = await Runner.run(self._agent, prompt)
        return str(result.final_output)

    @staticmethod
    def _extract_subject(email_body: str) -> str:
        for line in email_body.splitlines():
            normalized = line.strip()
            if normalized.lower().startswith("subject:"):
                return normalized.split(":", 1)[1].strip() or "SDR Outreach Email"
        return "SDR Outreach Email"

    @staticmethod
    def _to_report_data(email_body: str) -> ReportData:
        return ReportData(
            short_summary="Generated one professional outbound email and dispatched it.",
            markdown_report=email_body,
            follow_up_questions=[],
        )
