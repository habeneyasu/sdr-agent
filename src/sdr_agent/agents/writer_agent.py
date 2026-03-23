"""Deep-research writer agent contract."""

from typing import Protocol

from sdr_agent.schemas import ReportData


class WriterResearchAgent(Protocol):
    """Defines behavior for long-form report synthesis."""

    async def write(self, query: str, search_summaries: list[str]) -> ReportData:
        """Return a report with summary, markdown body, and follow-up questions."""
        ...
