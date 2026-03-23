"""Typed schemas for SDR and Deep Research contracts."""

from pydantic import BaseModel, Field


class ResearchQuery(BaseModel):
    """Input contract for a research or summary request."""

    topic: str = Field(description="Primary topic or question to research and summarize.")


class SectionSummary(BaseModel):
    """A single section in a generated summary."""

    heading: str = Field(description="Section heading.")
    content: str = Field(description="Section body content in markdown.")


class SummaryReport(BaseModel):
    """Output contract for final summaries."""

    title: str = Field(description="Summary title.")
    executive_summary: str = Field(description="Short summary for quick readers.")
    sections: list[SectionSummary] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list, description="Source links or citations.")
    follow_up_questions: list[str] = Field(default_factory=list)


class WebSearchItem(BaseModel):
    """One planned search for deep research."""

    reason: str = Field(description="Why this search helps answer the user query.")
    query: str = Field(description="Search term for web retrieval.")


class WebSearchPlan(BaseModel):
    """Planner output for deep research."""

    searches: list[WebSearchItem] = Field(
        default_factory=list,
        description="A list of targeted searches to run.",
    )


class ReportData(BaseModel):
    """Writer output for deep research."""

    short_summary: str = Field(description="A short 2-3 sentence summary of findings.")
    markdown_report: str = Field(description="Long-form markdown report, ideally >= 1000 words.")
    follow_up_questions: list[str] = Field(default_factory=list)

