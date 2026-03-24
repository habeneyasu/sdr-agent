"""Deep-research search agent contract."""

from typing import Protocol

from sdr_agent.config import AppConfig
from sdr_agent.integrations.openai_provider import OpenAIProvider
from sdr_agent.schemas import WebSearchItem

SEARCH_INSTRUCTIONS = (
    "You are a research assistant. Given a search term, search the web and produce a concise "
    "summary of key findings. The summary must be 2-3 short paragraphs and under 300 words. "
    "Capture signal over noise and avoid extra commentary."
)


class SearchAgent(Protocol):
    """Defines behavior for tool-backed web search summarization."""

    async def search(self, item: WebSearchItem) -> str:
        """Return a concise 2-3 paragraph summary for one targeted search."""
        ...


class OpenAISearchAgent:
    """OpenAI Agents SDK implementation of the deep-research search contract."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._provider = OpenAIProvider(config)
        self._agent = self._build_agent()

    def _build_agent(self) -> object:
        try:
            from agents import Agent, ModelSettings, WebSearchTool
        except ImportError as exc:
            raise RuntimeError(
                "OpenAI Agents SDK is required. Install with: pip install openai-agents"
            ) from exc

        model = self._provider.resolve_model(self._config.search_model or "gpt-4o-mini")
        return Agent(
            name="SearchAgent",
            instructions=SEARCH_INSTRUCTIONS,
            tools=[WebSearchTool(search_context_size="low")],
            model=model,
            model_settings=ModelSettings(tool_choice="required"),
        )

    async def search(self, item: WebSearchItem) -> str:
        """Run one targeted web search and return a concise summary string."""
        try:
            from agents import Runner
        except ImportError as exc:
            raise RuntimeError(
                "OpenAI Agents SDK is required. Install with: pip install openai-agents"
            ) from exc

        prompt = f"Search term: {item.query}\nReason for searching: {item.reason}"
        result = await Runner.run(self._agent, prompt)
        return str(result.final_output)
