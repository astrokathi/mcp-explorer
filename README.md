# Nike Explorer 🚀

Nike Explorer is a local-first, multi-agent query and search system. It leverages LangChain and LangGraph for orchestration, Chainlit for a responsive chat UI, Ollama for local LLM inference (`gemma4:e4b`), and Model Context Protocol (MCP) servers to load dynamic capabilities.

Additionally, the system features out-of-the-box observability with Langfuse and console trace logging.

---

## 🏗️ Architecture Overview

```
                        ┌─────────────┐
                        │ Chainlit UI │
                        └──────┬──────┘
                               │
                        ┌──────▼──────┐
                        │ ReAct Agent │
                        └─┬─────────┬─┘
                          │         │
             ┌────────────▼┐       ┌▼────────────┐
             │ Standard    │       │ MCP Client  │
             │ Tools       │       │ (mcpConfig) │
             │ (toolsConfig│       └─────┬───────┘
             └─────────────┘             │
                               ┌─────────▼─────────┐
                               │ SQLite / Web /    │
                               │ Custom MCP Server │
                               └───────────────────┘
```

- **Chat Interface**: Built with Chainlit (`ui/app.py`) for streaming token responses and tool-call rendering.
- **Agent Loop**: A ReAct agent (`core/agent.py`) powered by `ChatOllama` executing search, retrieval, and calculations.
- **Dynamic MCP Integrations**: Loads tools from any configured MCP servers via `mcpConfig.json` dynamically using `core/mcp_loader.py`.
- **Standard Integrations**: Parses standard tools (like Wikipedia, Arxiv) and dynamic user agent setups from `toolsConfig.json` using `core/tool_loader.py`.
- **Observability Stack**: Integrated with a local Langfuse setup for full execution traces, span inputs/outputs, and latency monitoring.

---

## 📁 Project Structure

```
Nike_Explorer/
├── config.py             # Single configuration source of truth (MCP_ENV based)
├── docker-compose.yml    # Langfuse server, database, worker, redis, minio & app
├── docker-run.sh         # Quick start shell script for the Docker stack
├── Dockerfile            # Multi-stage container definition
├── pyproject.toml        # Dependency declarations (Python build system)
├── setup.sh              # Local virtualenv builder & dependencies installer
├── mcpConfig.json        # MCP server profiles configuration
├── toolsConfig.json      # Standard tool parameters configuration
├── docs/                 # Compiled static HTML site for GitHub Pages
├── docs-md/              # Source Markdown documentation files
│   └── walkthrough.md    # Detailed implementation walkthrough
├── core/
│   ├── agent.py          # ReAct Agent implementation
│   ├── logger.py         # Custom console callback tracer
│   ├── mcp_loader.py     # MCP Server connector and client adapter
│   └── tool_loader.py    # Standard tools dynamic initializer
├── ui/
│   └── app.py            # Chainlit application frontend logic
└── tests/
    ├── test_config.py       # Configuration unit tests
    ├── test_integration.py  # Agent and Ollama integration tests
    ├── test_tool_loader.py  # Dynamic loader tests
    └── manual/              # Manual testing files directory
        ├── screenshots/     # Puppeteer execution screenshots
        ├── js/              # Puppeteer UI submission scripts
        └── python/          # Python manual trace generation scripts
```

---

## 🚀 Getting Started

### Option A: Local Development

1. **Environment Setup**:
   Execute the setup script to initialize the virtual environment and install standard dependencies (including Playwright components):
   ```bash
   ./setup.sh
   ```

2. **Start the Application**:
   Activate your virtual environment and start the Chainlit server:
   ```bash
   source venv/bin/activate
   chainlit run ui/app.py
   ```

3. **Run Automated Tests**:
   ```bash
   source venv/bin/activate
   pytest --ignore=tests/manual
   ```

---

### Option B: Docker Compose Stack (With Langfuse Observability)

The Docker Stack starts **Langfuse Server**, **MinIO**, **Redis**, **ClickHouse**, **PostgreSQL**, and the **Nike Explorer App** in one cohesive network.

1. **Launch the Stack**:
   Run the helper script which auto-generates secure encryption secrets and starts the build:
   ```bash
   ./docker-run.sh
   ```

2. **Access Interfaces**:
   - **Chainlit Chat UI**: `http://localhost:8000`
   - **Langfuse Observability Board**: `http://localhost:3000` *(Login: `admin@langfuse.local` / `admin123`)*

3. **Test Observability Logging**:
   Verify traces are hitting the Langfuse pipeline by running the background test suite:
   ```bash
   # Execute inside the running app container
   docker compose exec -T nike-explorer-app python tests/manual/python/test_logging.py
   ```

---

## 🛡️ Git Configuration

This project is pre-configured with Git. Make sure to commit changes using standard guidelines:
- Local `.env` credentials are **never** committed (ignored via `.gitignore`).
- Dev screenshots under `tests/manual/screenshots/` and `.pytest_cache` folders are ignored.
