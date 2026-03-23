"""Deep-research search agent contract."""

from typing import Protocol

from sdr_agent.schemas import WebSearchItem


class SearchAgent(Protocol):
    """Defines behavior for tool-backed web search summarization."""

    async def search(self, item: WebSearchItem) -> str:
        """Return a concise 2-3 paragraph summary for one targeted search."""
        ...
