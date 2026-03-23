"""Deep-research email agent contract."""

from typing import Protocol

from sdr_agent.schemas import ReportData


class EmailAgent(Protocol):
    """Defines behavior for report-to-HTML conversion and SendGrid delivery."""

    async def send_report(self, report: ReportData) -> None:
        """Send the report as a formatted outbound email."""
        ...
