# SDR Agent for B2B SaaS

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/OpenAI-Agents_SDK-412991)](https://openai.github.io/openai-agents-python/)
[![UI](https://img.shields.io/badge/UI-Gradio-FF4B4B?logo=gradio&logoColor=white)](https://www.gradio.app/)
[![Provider](https://img.shields.io/badge/Provider-OpenRouter-6C47FF)](https://openrouter.ai/)

This repository provides an SDR-focused business application to generate and send professional outbound emails for B2B SaaS teams.

Secondary capability:
- **Deep Research Workflow:** plan, execute concurrent web research, synthesize findings, validate output, and deliver by email.

The platform is built on the OpenAI Agents SDK and supports OpenAI-compatible endpoints, including OpenRouter.

Current maturity: **SDR workflow is the primary interactive flow in the UI**; **Deep Research is available as a secondary tab**.

## Business Value

- Accelerates research and outbound preparation for lean GTM teams.
- Reduces time-to-insight through automation of discovery and synthesis.
- Improves consistency with structured outputs and pre-delivery guardrails.
- Supports scalable delivery operations through a reusable agent pipeline.

## Capability Overview

- **SDR (primary)**
  - generate one professional outbound cold email from a business topic
  - apply guardrail validation hooks (optional)
  - send final email via SendGrid-enabled delivery agent
  - run directly from the default Gradio experience
- **Deep Research (secondary)**
  - query planning and targeted search orchestration
  - concurrent research execution
  - long-form report generation
  - guardrail validation prior to distribution
  - email preview and SendGrid dispatch

## Model Transparency

The system uses OpenRouter-compatible models across planning, search, writing, and delivery steps. Typical configurations include GPT-4o-class and Claude-class models, selected through:

- `MODEL_DEFAULT`
- `PLANNER_MODEL`
- `SEARCH_MODEL`
- `WRITER_MODEL`
- `EMAIL_MODEL`

## Demo and Screenshots

- Live demo: add your deployed Gradio URL here, for example `[Live Demo](https://your-space-or-domain)`
- Recommended attachment folder: `data/screenshots/`
- Example screenshot set:
  - `SDR Outreach.png`
    ![SDR Outreach tab output showing a generated professional outbound email](data/screenshots/SDR%20Outreach.png "SDR output")
  - `SDR Deap Research.png`
    ![Deep Research tab output showing a generated GTM strategy report](data/screenshots/SDR%20Deap%20Research.png "Deep Research output")

## Architecture

- `src/sdr_agent/app.py`: SDR-first Gradio entrypoint and runtime bootstrap
- `src/sdr_agent/agents/research_manager.py`: deep-research orchestration
- `src/sdr_agent/manager.py`: SDR orchestration and outbound email generation
- `src/sdr_agent/agents/planner_agent.py`: planning agent
- `src/sdr_agent/agents/search_agent.py`: web search summarization agent
- `src/sdr_agent/agents/writer_agent.py`: report synthesis agent
- `src/sdr_agent/agents/email_agent.py`: email formatting and SendGrid delivery
- `src/sdr_agent/agents/guardrails.py`: validation contracts and baseline checks
- `src/sdr_agent/config.py`: environment-driven config and OpenRouter/OpenAI aliasing
- `src/sdr_agent/integrations/openai_provider.py`: OpenAI-compatible model adapter

## Configuration

Create `.env` (see `env.example`) with at least:

- `OPENROUTER_API_KEY`
- `OPENROUTER_BASE_URL` (for example `https://openrouter.ai/api/v1`)
- `SENDGRID_API_KEY`
- `MAIL_FROM`
- `MAIL_TO`

Optional runtime controls supported by the app:

- `MODEL_DEFAULT`
- `PLANNER_MODEL`
- `SEARCH_MODEL`
- `WRITER_MODEL`
- `EMAIL_MODEL`
- `GRADIO_SERVER_NAME`
- `GRADIO_SERVER_PORT`

Operational note:
- The app auto-maps `OPENROUTER_*` to `OPENAI_*` for SDK compatibility.

## Run with uv

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
uv run python -m sdr_agent.app
```

## Validation Workflow

1. Launch the Gradio interface.
2. In the SDR tab, enter an outreach topic and run `Generate & Send`.
3. Confirm staged execution for SDR:
   - email generation
   - delivery
4. Confirm receipt at `MAIL_TO`.
5. Optional: validate Deep Research tab flow:
   - planning
   - concurrent search
   - report generation
   - email preview
   - delivery completion

## Security and Governance

- Keep credentials in `.env` or a managed secret store.
- Do not commit secrets to source control.
- Verify `MAIL_FROM` in SendGrid before production use.
- Tracing is automatically disabled for OpenRouter credentials to avoid OpenAI trace-auth noise.
