# Nike_Explorer Walkthrough

## Overview
I have successfully implemented the "Nike_Explorer" local-first multi-agent system. The system uses LangChain for orchestration, Chainlit for the UI, and connects to a local Ollama instance (`gemma4:e4b`).

> [!NOTE]
> All project code is located at: `[Nike_Explorer](file:///Users/kathi.s/NKExplorer/Nike_Explorer)`

## Key Components

### Architecture & Setup
- **Environment Management**: Implemented strict environment separation with `.env`, `.env.test`, and `.env.prod`. 
- **Configuration Hub**: [config.py](file:///Users/kathi.s/NKExplorer/Nike_Explorer/config.py) serves as the single source of truth, loading variables dynamically based on the `MCP_ENV` system environment variable.
- **Agent Orchestration**: [core/agent.py](file:///Users/kathi.s/NKExplorer/Nike_Explorer/core/agent.py) defines a LangGraph `create_react_agent` that uses `ChatOllama` to talk to `http://localhost:11434`.

### Dynamic Loading
- **MCP Servers**: [mcpConfig.json](file:///Users/kathi.s/NKExplorer/Nike_Explorer/mcpConfig.json) configures servers. [core/mcp_loader.py](file:///Users/kathi.s/NKExplorer/Nike_Explorer/core/mcp_loader.py) uses `langchain-mcp-adapters` to initialize the `MultiServerMCPClient` and keep the connection context active across requests.
- **Standard Tools**: [toolsConfig.json](file:///Users/kathi.s/NKExplorer/Nike_Explorer/toolsConfig.json) manages standard tools. [core/tool_loader.py](file:///Users/kathi.s/NKExplorer/Nike_Explorer/core/tool_loader.py) parses and initializes these standard LangChain tools using `load_tools()`.

### User Interface
- **Chainlit App**: [ui/app.py](file:///Users/kathi.s/NKExplorer/Nike_Explorer/ui/app.py) handles the user chat session, managing tool initialization on start, creating the `Agent` object, and streaming token responses and tool usages directly to the browser.

## Testing & Verification

### End-to-End Test
I've provided a complete Playwright script ([e2e_test.py](file:///Users/kathi.s/NKExplorer/Nike_Explorer/tests/manual/python/e2e_test.py)) which:
1. Spawns the Chainlit server as a subprocess background task.
2. Waits for it to become ready.
3. Uses Playwright headless Chromium to navigate to the locally hosted URL.
4. Verifies the successful render of the Chainlit application UI.
5. Terminate the server subprocess cleanly.

### Unit & Integration Tests
I created comprehensive pytest test suites:
- `tests/test_config.py`: Verifies environment switching behavior.
- `tests/test_tool_loader.py`: Ensures standard tools are properly mocked and loaded.
- `tests/test_integration.py`: Validates the `Agent` object's instantiation with correctly passed Ollama URIs using the test environment (`.env.test`).

## How to Run

1. Open your terminal in the project directory.
2. Execute the provided setup script:
   ```bash
   ./setup.sh
   ```
   *This will create the `venv`, install packages from `pyproject.toml`, and fetch Playwright browser binaries.*
3. Start the application:
   ```bash
   source venv/bin/activate
   chainlit run ui/app.py
   ```
4. Or, run the tests:
   ```bash
   source venv/bin/activate
   pytest --ignore=tests/manual
   ```

## Observability & Docker Integration

I have updated the architecture to include full observability with Langfuse and integrated everything into a Docker Compose stack.

### Logging & Tracing
- **Custom Logger**: A custom console-based logger (`CustomAgentLogger`) directly into the LangChain `Agent.ainvoke` runtime (in `ui/app.py` and `core/agent.py`). This captures all agent executions, tools utilized, token counts, latency, and success/failure logs, sending them to the Langfuse board.

### Langfuse Integration Fixes
- Addressed `LangchainCallbackHandler` object missing `flush` attribute error by implementing a fallback `hasattr` check to call `langfuse_handler.langfuse.flush()` safely during the teardown block of `app.py`.
- Wrote and ran a headless `puppeteer` script (`verify_traces.js`) which logged into the Langfuse Dashboard at `http://localhost:3000`, navigated to the Nike Explorer project, and successfully validated that recent queries and LLM replies were being traced and stored correctly.

### Results
- The Docker environment is now cohesive, with `.env` driving both the app and langfuse configurations uniformly.
- The Chainlit UI reliably connects to Ollama, correctly instantiates the ReAct agent, invokes `wikipedia` search, retrieves results without Wikipedia blocking the scraper, and returns the formulated response back to the user.
- Every chat message correctly pushes trace logs to the Langfuse ClickHouse backend over `host-gateway`.

### Docker Stack
- **docker-compose.yml**: Added to orchestrate `langfuse-server` and `db` (Postgres) alongside our newly Dockerized `nike-explorer-app` Chainlit application. 
- **docker-run.sh**: A launch script that auto-generates your secure `SALT`, `ENCRYPTION_KEY`, and `NEXTAUTH_SECRET`, applies them to `.env.docker`, and builds/spins up the stack.

## How to Run the Docker Stack

1. **Spin up the Environment:**
   Navigate into the project directory and execute the runner script:
   ```bash
   cd /Users/kathi.s/NKExplorer/Nike_Explorer
   ./docker-run.sh
   ```

2. **Access the Application & Dashboard:**
   - **Langfuse Visualization Board**: Go to `http://localhost:3000`. Set up your project to get your real `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY`, then update them in the generated `.env.docker` file.
   - **Chainlit UI**: Go to `http://localhost:8000`.

3. **Test the Logging Visualization:**
   Run the dedicated script to test traces appearing in the Langfuse dashboard:
   ```bash
   source venv/bin/activate
   python tests/manual/python/test_logging.py
   ```
   *This script runs two separate threads (one successful and one failure) to generate dummy traffic for your Langfuse board.*
