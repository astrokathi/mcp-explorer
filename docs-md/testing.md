# Testing & Verification Guide

This page explains how to run automated unit and integration tests, as well as execute manual verification scripts to check system integrity, agent loops, and observability tracing.

---

## 🧪 1. Automated Testing (Pytest)

We use `pytest` (with `pytest-asyncio`) to run isolated configuration, loader, and integration tests.

### Running the Tests
To run the automated test suite, activate your virtual environment and execute `pytest`, ignoring the manual tests folder:
```bash
source venv/bin/activate
pytest --ignore=tests/manual
```

### Automated Test Suite Descriptions
*   **`tests/test_config.py`**: Verifies that environment variable profiles (`default`, `test`, `prod`) reload variables (like `OLLAMA_URL` and `MONGODB_URI`) correctly from their respective `.env` files.
*   **`tests/test_tool_loader.py`**: Validates the standard tools dynamic dynamic initializer, verifying the execution of Python code definitions inside `toolsConfig.json`.
*   **`tests/test_integration.py`**: Asserts successful connectivity with a running Ollama container and verifies that the `Agent` is created with the expected endpoints.

---

## 🛠️ 2. Manual Testing Scripts (`tests/manual/`)

Manual test scripts are divided into language folders to separate browser automation tests from diagnostic script tests.

### A. Python Verification Scripts (`tests/manual/python/`)

These scripts test specific API elements or simulate trace outputs directly inside the agent environment.

*   **`test_logging.py`**: Simulates two separate agent executions (one successful, one catching a tool division-by-zero boundary error) to verify that trace payloads and console logs are formatted correctly.
*   **`generate_trace.py`**: Runs a simple query through the ReAct agent, flushes the Langfuse callback client, and confirms trace logs.
*   **`generate_trace_simple.py`**: Directly invokes the Langfuse SDK to create a raw trace and span, verifying authorization keys.
*   **`verify_api.py` / `verify_api2.py`**: Connect to the local Langfuse API server endpoints via `requests` to fetch and print recent trace logs programmatically.
*   **`e2e_test.py`**: Launches the local Chainlit app in a background subprocess, uses Playwright Chromium to navigate to the web page, asserts successful UI render, and cleanly terminates the server.

### B. Node.js Browser Scripts (`tests/manual/js/`)

These use **Puppeteer** to simulate human browser interaction, click UI elements, submit inputs, and scrape outputs to verify E2E tracing.

*   **`debug_chainlit.js`**: Launches a headless browser, navigates to `http://localhost:8000`, types a query, dispatches a keydown `Enter` event, waits for agent response, and captures screenshots to `tests/manual/screenshots/`.
*   **`verify_puppeteer.js` / `verify_puppeteer_fix.js`**: Automate input submission in Chainlit, then log into the Langfuse dashboard at `http://localhost:3000` to verify that the trace for the submitted message exists in the database.
*   **`verify_traces.js`**: Inspects the Langfuse UI trace log table and prints the 5 most recent traces.
