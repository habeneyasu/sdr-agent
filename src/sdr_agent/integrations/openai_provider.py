"""OpenAI-compatible provider adapter for Agents SDK models."""

from sdr_agent.config import AppConfig


class OpenAIProvider:
    """Build model objects for an OpenAI-compatible endpoint."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config

    def resolve_model(self, model: str | None) -> object | str:
        """Return model string or OpenAIChatCompletionsModel for configured endpoint."""
        model_name = model or "gpt-4o-mini"

        if not self._config.openai_base_url:
            return model_name

        try:
            from agents import OpenAIChatCompletionsModel
        except ImportError as exc:
            raise RuntimeError(
                "OpenAI Agents SDK is required. Install with: pip install openai-agents"
            ) from exc

        client = self._build_client()
        return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

    def _build_client(self) -> object:
        try:
            import importlib

            openai_mod = importlib.import_module("openai")
        except ImportError as exc:
            raise RuntimeError("openai is required. Install with: pip install openai") from exc
        async_openai = openai_mod.AsyncOpenAI

        return async_openai(
            base_url=self._config.openai_base_url,
            api_key=self._config.openai_api_key,
        )

