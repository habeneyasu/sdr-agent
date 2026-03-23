"""Orchestration skeleton for the deep-research multi-agent workflow."""

from collections.abc import AsyncIterator

from sdr_agent.schemas import ReportData, WebSearchPlan


class ResearchManager:
    """Coordinates planning, search, writing, and email delivery."""

    async def run(self, query: str) -> AsyncIterator[str]:
        """Stream progress updates and final markdown report."""
        raise NotImplementedError("Skeleton only: implement orchestration in project phase.")

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Create a structured plan of targeted searches for the input query."""
        raise NotImplementedError("Skeleton only: implement planning in project phase.")

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Run planned searches concurrently and return search summaries."""
        raise NotImplementedError("Skeleton only: implement retrieval in project phase.")

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Synthesize search summaries into a long-form report payload."""
        raise NotImplementedError("Skeleton only: implement writing in project phase.")

    async def send_email(self, report: ReportData) -> None:
        """Deliver report through the configured outbound channel."""
        raise NotImplementedError("Skeleton only: implement delivery in project phase.")
