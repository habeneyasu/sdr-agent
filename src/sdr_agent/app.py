"""Application entrypoint for a Gradio-based deep research UI."""

from collections.abc import AsyncIterator

from sdr_agent.agents.research_manager import ResearchManager
from sdr_agent.config import AppConfig


async def run(query: str) -> AsyncIterator[str]:
    """Stream deep research progress for a UI text input query."""
    manager = ResearchManager(config=AppConfig())
    async for chunk in manager.run(query):
        yield chunk


def build_app() -> object:
    """Build and return a Gradio Blocks UI."""
    try:
        import gradio as gr
    except ImportError as exc:
        raise RuntimeError("Gradio is required. Install with: pip install gradio") from exc

    with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as app:
        gr.Markdown("# Deep Research")
        query_box = gr.Textbox(label="What topic would you like to research?")
        run_button = gr.Button("Run", variant="primary")
        report_box = gr.Markdown(label="Report")

        run_button.click(fn=run, inputs=query_box, outputs=report_box)
        query_box.submit(fn=run, inputs=query_box, outputs=report_box)

    return app


def launch() -> None:
    """Launch the Gradio UI with optional AppConfig host/port overrides."""
    config = AppConfig()
    app = build_app()
    app.launch(
        inbrowser=True,
        server_name=config.gradio_server_name,
        server_port=config.gradio_server_port,
    )
