"""Orchestration for the deep-research multi-agent workflow."""

import asyncio
import os
from collections.abc import AsyncIterator

from sdr_agent.agents.email_agent import EmailAgent, OpenAIEmailAgent
from sdr_agent.agents.guardrails import BasicDeepResearchGuardrails, DeepResearchGuardrailsAgent
from sdr_agent.agents.planner_agent import OpenAIPlannerResearchAgent, PlannerResearchAgent
from sdr_agent.agents.search_agent import OpenAISearchAgent, SearchAgent
from sdr_agent.agents.writer_agent import OpenAIWriterResearchAgent, WriterResearchAgent
from sdr_agent.config import AppConfig
from sdr_agent.schemas import ReportData, WebSearchItem, WebSearchPlan


class ResearchManager:
    """Coordinates planning, search, writing, and email delivery."""

    def __init__(
        self,
        config: AppConfig | None = None,
        planner: PlannerResearchAgent | None = None,
        searcher: SearchAgent | None = None,
        writer: WriterResearchAgent | None = None,
        emailer: EmailAgent | None = None,
        guardrails: DeepResearchGuardrailsAgent | None = None,
    ) -> None:
        self._config = config or AppConfig()
        self._planner = planner or OpenAIPlannerResearchAgent(self._config)
        self._searcher = searcher or OpenAISearchAgent(self._config)
        self._writer = writer or OpenAIWriterResearchAgent(self._config)
        self._emailer = emailer or OpenAIEmailAgent(self._config)
        self._guardrails = guardrails or BasicDeepResearchGuardrails()

    async def run(self, query: str) -> AsyncIterator[str]:
        """Stream progress updates and final markdown report."""
        trace_context, trace_link = self._build_trace_context()
        if trace_link:
            yield trace_link

        if trace_context is None:
            async for chunk in self._execute_pipeline(query):
                yield chunk
            return

        with trace_context:
            async for chunk in self._execute_pipeline(query):
                yield chunk

    async def _execute_pipeline(self, query: str) -> AsyncIterator[str]:
        yield "Planning searches..."
        search_plan = await self.plan_searches(query)

        yield "Running searches..."
        search_results = await self.perform_searches(search_plan)

        yield "Writing report..."
        report = await self.write_report(query, search_results)
        report = await self._guardrails.validate_report(report)

        preview = self._build_email_preview(report)
        yield preview

        yield "Sending email..."
        await self.send_email(report)

        yield "Done."
        yield report.markdown_report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Create a structured plan of targeted searches for the input query."""
        return await self._planner.plan(query=query, target_searches=5)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Run planned searches concurrently and return search summaries."""
        tasks = [asyncio.create_task(self._search_item(item)) for item in search_plan.searches]
        results: list[str] = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result:
                results.append(result)
        return results

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Synthesize search summaries into a long-form report payload."""
        return await self._writer.write(query=query, search_summaries=search_results)

    async def send_email(self, report: ReportData) -> None:
        """Deliver report through the configured outbound channel."""
        await self._emailer.send_report(report)

    async def _search_item(self, item: WebSearchItem) -> str | None:
        """Run one search item and tolerate per-item failures."""
        try:
            return await self._searcher.search(item)
        except Exception:
            return None

    @staticmethod
    def _build_trace_context() -> tuple[object | None, str | None]:
        """Build optional trace context and trace link."""
        # OpenAI trace export expects an OpenAI API key. When running on OpenRouter
        # credentials, skip trace creation to avoid noisy non-fatal 401 errors.
        base_url = (os.getenv("OPENAI_BASE_URL") or "").lower()
        api_key = os.getenv("OPENAI_API_KEY") or ""
        if "openrouter.ai" in base_url or api_key.startswith("sk-or-v1"):
            return None, None

        try:
            from agents import gen_trace_id, trace
        except ImportError:
            return None, None

        trace_id = gen_trace_id()
        trace_link = f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
        return trace("Research trace", trace_id=trace_id), trace_link

    @staticmethod
    def _build_email_preview(report: ReportData) -> str:
        """Return a UI-friendly email preview snippet before sending."""
        subject = report.short_summary.strip().split(".")[0][:90] or "Research Update"
        body_preview = report.markdown_report.strip()[:500]
        return (
            "### Email Preview\n"
            f"**Subject:** {subject}\n\n"
            f"{body_preview}\n\n"
            "_Preview truncated before send._"
        )
