"""Deep-research planner agent contract."""

from typing import Protocol

from sdr_agent.config import AppConfig
from sdr_agent.schemas import WebSearchPlan

PLANNER_INSTRUCTIONS = (
    "You are a helpful research planner. Given a user query, produce a focused web search plan "
    "that will best answer it. Return roughly the requested number of searches."
)


class PlannerResearchAgent(Protocol):
    """Defines behavior for planning targeted web searches."""

    async def plan(self, query: str, target_searches: int = 5) -> WebSearchPlan:
        """Return a structured web search plan for the provided query."""
        ...


class OpenAIPlannerResearchAgent:
    """OpenAI Agents SDK implementation of the deep-research planner contract."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._agent = self._build_agent()

    def _build_agent(self) -> object:
        try:
            from agents import Agent
        except ImportError as exc:
            raise RuntimeError(
                "OpenAI Agents SDK is required. Install with: pip install openai-agents"
            ) from exc

        model = self._config.planner_model or "gpt-4o-mini"
        return Agent(
            name="PlannerAgent",
            instructions=PLANNER_INSTRUCTIONS,
            model=model,
            output_type=WebSearchPlan,
        )

    async def plan(self, query: str, target_searches: int = 5) -> WebSearchPlan:
        """Generate a structured plan of targeted web searches."""
        try:
            from agents import Runner
        except ImportError as exc:
            raise RuntimeError(
                "OpenAI Agents SDK is required. Install with: pip install openai-agents"
            ) from exc

        prompt = f"Query: {query}\nTarget number of searches: {target_searches}"
        result = await Runner.run(self._agent, prompt)
        return result.final_output_as(WebSearchPlan)
