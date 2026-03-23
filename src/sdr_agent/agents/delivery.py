"""Delivery agent contract."""

from typing import Protocol

from sdr_agent.schemas import SummaryReport


class DeliveryAgent(Protocol):
    """Defines output delivery behavior (email/chat/doc systems)."""

    async def deliver(self, report: SummaryReport) -> None:
        """Deliver report to the target channel(s)."""
        ...

