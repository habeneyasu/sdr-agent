"""Application entrypoint skeleton for a Gradio-based deep research UI."""

from collections.abc import AsyncIterator

from sdr_agent.agents.research_manager import ResearchManager


async def run(query: str) -> AsyncIterator[str]:
    """Stream deep research progress for a UI text input query."""
    raise NotImplementedError("Skeleton only: wire Gradio callback in project phase.")


def build_app() -> object:
    """Return a UI app object (e.g., Gradio Blocks) for interactive deep research."""
    _ = ResearchManager
    raise NotImplementedError("Skeleton only: implement UI composition in project phase.")
