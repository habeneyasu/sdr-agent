"""Guardrail agent contract for SDR and deep-research flows."""

from typing import Protocol

from sdr_agent.schemas import ReportData, SummaryReport


class GuardrailsAgent(Protocol):
    """Defines validation checks before external delivery."""

    async def validate(self, report: SummaryReport) -> SummaryReport:
        """Return a validated or transformed report."""
        ...


class DeepResearchGuardrailsAgent(Protocol):
    """Defines validation checks for deep-research report payloads."""

    async def validate_report(self, report: ReportData) -> ReportData:
        """Return a validated deep-research report."""
        ...


class BasicDeepResearchGuardrails:
    """Minimal report sanity checks before email delivery."""

    async def validate_report(self, report: ReportData) -> ReportData:
        markdown = report.markdown_report.strip()
        if not markdown:
            raise ValueError("Report markdown is empty.")
        if len(markdown) < 500:
            raise ValueError("Report markdown is too short for delivery.")
        return report
