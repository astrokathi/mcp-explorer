# Codebase Component Breakdown

This document provides a breakdown of each Python file in the MCP Explorer codebase, explaining its significance and architectural role.

---

## 🛠️ Configuration & Core Files

### 1. `config.py`
The central configuration hub of the application. It manages dynamic configuration reloading based on environments.
*   **Significance**: Loads variables from `.env`, `.env.test`, or `.env.prod` depending on the value of the `MCP_ENV` environment variable (falling back to `.env` if undefined).
*   **Key Objects**: `CONFIG` (dictionary housing `OLLAMA_URL`, `MONGODB_URI`, `LOG_LEVEL`, and pathways to tools/MCP configuration files).

### 2. `core/agent.py`
The brain of the system.
*   **Significance**: Defines the custom `Agent` class wrapper. It instantiates `ChatOllama` utilizing the `gemma4:e4b` model and binds it to a list of dynamically resolved tools using LangGraph's `create_react_agent`.
*   **Key Methods**:
    *   `ainvoke(prompt, thread_id, callbacks)`: Starts the agent as an asynchronous generator utilizing `astream_events` to yield granular execution events (model responses, token outputs, tool inputs/outputs) back to the caller.

### 3. `core/logger.py`
The diagnostic tracing console callback.
*   **Significance**: Extends LangChain's `BaseCallbackHandler` to format and print colored, structured execution logs directly to the system CLI.
*   **Key Methods**:
    *   `on_chain_start()` / `on_chain_end()`: Logs execution boundaries of sub-graphs.
    *   `on_tool_start()` / `on_tool_end()`: Traces the exact input and outputs of standard/MCP tool execution.

---

## 🔌 Loader Components

### 4. `core/mcp_loader.py`
Connects the agent to external tool suites using the Model Context Protocol.
*   **Significance**: Parses `mcpConfig.json`, spawns each configured MCP server (e.g. SQLite, local scripts) as an independent OS process, establishes stdin/stdout channels, and maps their exposed JSON-RPC tools into LangChain compatible tool interfaces.

### 5. `core/tool_loader.py`
The dynamic initializer for standard LangChain integrations.
*   **Significance**: Resolves issues with third-party tools that require code-level adjustments (such as configuring User-Agent credentials for Wikipedia or overriding Arxiv query parameters).
*   **Key Methods**:
    *   `load_standard_tools(config_path)`: Reads `toolsConfig.json`, compiles and executes the `tool_inits` Python code snippets dynamically via `exec()`, then registers these standard tools into the agent scope.

---

## 🖥️ User Interface

### 6. `ui/app.py`
The frontend coordinator.
*   **Significance**: Orchestrates Chainlit's user lifecycle events.
*   **Workflow**:
    *   `@cl.on_chat_start`: Initializes tools, establishes MCP servers context, and instantiates the `Agent` object.
    *   `@cl.on_message`: Triggers `agent.ainvoke`, streaming response tokens in real-time to the user's browser. In the `finally` block, it parses the underlying `langfuse_handler.last_trace_id` and manually updates the trace payload in Langfuse (assigning trace input and the name `"MCP Explorer Agent"`).
