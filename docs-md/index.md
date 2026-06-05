# MCP Explorer

Welcome to the **MCP Explorer** developer documentation!

MCP Explorer is a state-of-the-art, local-first agentic query interface built with Python and LangChain. It uses a **ReAct (Reasoning and Acting)** loop powered by local large language models (such as `gemma4:e4b` via Ollama) to autonomously invoke tools, query external APIs, search databases, and format results.

The system is equipped with **Model Context Protocol (MCP)** clients to connect to remote or local MCP servers dynamically and query resources in real time.

---

## 🌟 Key Features

*   **Local-First Agent Core**: Run LLMs locally using [Ollama](https://ollama.com) (defaulting to the `gemma4:e4b` model) with zero latency or remote API dependency.
*   **Dynamic Model Context Protocol (MCP) Loader**: Automatically discover, load, and authenticate tools from multiple MCP servers dynamically using configurations in `mcpConfig.json`.
*   **Standard Tools Extension**: Load and dynamically configure parameters (like custom user agents or endpoints) for classic tools (Wikipedia, Arxiv) defined dynamically in `toolsConfig.json`.
*   **Interactive Chat UI**: A responsive, real-time streaming web dashboard built using **Chainlit** for developer conversations.
*   **Observability Pipeline**: Automatic tracking of every message, prompt, LLM invocation, tool execution, token usage, and error boundary using **Langfuse**.
*   **Dockerized Stack**: Run the entire system—including database backends, workers, and visualization dashboards—using a simple `./docker-run.sh` script.

---

## 🗺️ High-Level System Architecture

The workflow follows a standard ReAct loop:

```
    [User Inputs Query]
             │
             ▼
   [Chainlit App Session]
             │
             ▼
      [ReAct Agent] <───(Reads Configs: env / toolsConfig.json)
             │
     ┌───────┴───────┐
     ▼               ▼
[Run Standard]  [Run MCP Server]
   [Tools]          [Tools]
     │               │
     └───────┬───────┘
             ▼
     [Agent Formulates] ───(Callback)───► [Langfuse Traces Logged]
       [Response]
             │
             ▼
     [Stream to UI]
```

---

## 📂 Next Steps
Navigate through the tabs above or click the links below to continue learning:
*   [Getting Started](setup.md) — Learn how to set up the environment and run the code.
*   [Configuration Guide](configuration.md) — Understand every env variable and JSON parameter.
*   [Technical Architecture](architecture.md) — Dive deep into agent loops and MCP protocol.
*   [Component Breakdown](components.md) — Technical details of the Python codebase.
*   [Testing & Verification](testing.md) — Learn to execute automated and manual browser tests.
