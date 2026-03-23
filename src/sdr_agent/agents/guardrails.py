"""Guardrail agent contract for SDR and deep-research flows."""

from typing import Protocol

from sdr_agent.schemas import SummaryReport


class GuardrailsAgent(Protocol):
    """Defines validation checks before external delivery."""

    async def validate(self, report: SummaryReport) -> SummaryReport:
        """Return a validated or transformed report."""
        ...
