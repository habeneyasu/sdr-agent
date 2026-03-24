"""Deep-research writer agent contract and OpenAI implementation."""

from typing import Protocol

from sdr_agent.config import AppConfig
from sdr_agent.schemas import ReportData

WRITER_INSTRUCTIONS = (
    "You are a senior researcher. Given the original query and a set of concise web summaries, "
    "produce a detailed markdown report (>= 1000 words). Start with a short 2-3 sentence summary, "
    "then a well-structured, thorough report in markdown, and finally 5-8 follow-up questions."
)


class WriterResearchAgent(Protocol):
    """Defines behavior for long-form report synthesis."""

    async def write(self, query: str, search_summaries: list[str]) -> ReportData:
        """Return a report with summary, markdown body, and follow-up questions."""
        ...


class OpenAIWriterResearchAgent:
    """OpenAI Agents SDK implementation of the deep-research writer contract."""

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

        model = self._config.writer_model or "gpt-4o-mini"
        return Agent(
            name="WriterAgent",
            instructions=WRITER_INSTRUCTIONS,
            model=model,
            output_type=ReportData,
        )

    async def write(self, query: str, search_summaries: list[str]) -> ReportData:
        """Synthesize long-form markdown report from search summaries."""
        try:
            from agents import Runner
        except ImportError as exc:
            raise RuntimeError(
                "OpenAI Agents SDK is required. Install with: pip install openai-agents"
            ) from exc

        prompt = (
            f"Original query: {query}\n"
            f"Summarized search results: {search_summaries}"
        )
        result = await Runner.run(self._agent, prompt)
        return result.final_output_as(ReportData)
