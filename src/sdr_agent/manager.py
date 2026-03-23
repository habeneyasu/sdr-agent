"""Orchestration skeleton for the SDR sales workflow."""

from sdr_agent.schemas import ResearchQuery, SummaryReport


class SDRManager:
    """Coordinates SDR planner, retrieval, writer, guardrails, and delivery stages."""

    async def run(self, query: ResearchQuery) -> SummaryReport:
        """Execute SDR workflow and return a structured sales report/email package."""
        raise NotImplementedError("Skeleton only: implement orchestration in project phase.")

