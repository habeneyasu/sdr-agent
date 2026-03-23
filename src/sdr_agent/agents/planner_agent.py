"""Deep-research planner agent contract."""

from typing import Protocol

from sdr_agent.schemas import WebSearchPlan


class PlannerResearchAgent(Protocol):
    """Defines behavior for planning targeted web searches."""

    async def plan(self, query: str, target_searches: int = 5) -> WebSearchPlan:
        """Return a structured web search plan for the provided query."""
        ...
