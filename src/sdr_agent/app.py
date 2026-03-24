"""Application entrypoint for SDR-first Gradio experience."""

from collections.abc import AsyncIterator

from sdr_agent.agents.research_manager import ResearchManager
from sdr_agent.config import AppConfig, ensure_openai_env_aliases
from sdr_agent.manager import SDRManager
from sdr_agent.schemas import ResearchQuery


def _runtime_config() -> AppConfig:
    """Load runtime config with OpenRouter/OpenAI env aliasing applied."""
    ensure_openai_env_aliases()
    return AppConfig.from_env()


async def run_sdr(topic: str) -> AsyncIterator[str]:
    """Generate and deliver one SDR email from a business topic."""
    manager = SDRManager(config=_runtime_config())
    yield "Generating SDR outreach email..."
    result = await manager.run(ResearchQuery(topic=topic))
    yield "Sending email..."
    yield "Done."
    for section in result.sections:
        yield f"## {section.heading}\n\n{section.content}"


async def run_research(query: str) -> AsyncIterator[str]:
    """Stream deep research progress for a UI text input query."""
    manager = ResearchManager(config=_runtime_config())
    async for chunk in manager.run(query):
        yield chunk


def build_app() -> object:
    """Build and return a Gradio Blocks UI."""
    try:
        import gradio as gr
    except ImportError as exc:
        raise RuntimeError("Gradio is required. Install with: pip install gradio") from exc

    with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as app:
        gr.Markdown("# SDR Agent")
        gr.Markdown(
            "Create and send professional outbound SDR emails. "
            "Deep research is available in the secondary tab."
        )
        with gr.Tabs():
            with gr.Tab("SDR Outreach", id="sdr"):
                topic_box = gr.Textbox(label="Company/product/topic for outreach")
                sdr_button = gr.Button("Generate & Send", variant="primary")
                sdr_output = gr.Markdown(label="SDR Email")
                sdr_button.click(fn=run_sdr, inputs=topic_box, outputs=sdr_output)
                topic_box.submit(fn=run_sdr, inputs=topic_box, outputs=sdr_output)

            with gr.Tab("Deep Research", id="research"):
                query_box = gr.Textbox(label="What topic would you like to research?")
                run_button = gr.Button("Run Research")
                report_box = gr.Markdown(label="Report")
                run_button.click(fn=run_research, inputs=query_box, outputs=report_box)
                query_box.submit(fn=run_research, inputs=query_box, outputs=report_box)

    return app


def launch() -> None:
    """Launch the Gradio UI with optional AppConfig host/port overrides."""
    try:
        from dotenv import load_dotenv
    except ImportError as exc:
        raise RuntimeError("python-dotenv is required. Install with: pip install python-dotenv") from exc

    load_dotenv(override=True)
    config = _runtime_config()
    app = build_app()
    app.launch(
        inbrowser=True,
        server_name=config.gradio_server_name,
        server_port=config.gradio_server_port,
    )


if __name__ == "__main__":
    launch()
