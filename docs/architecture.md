# Technical Architecture & Tracing

This page explains the internal mechanics of the MCP Explorer agentic system, covering ReAct loops, Model Context Protocol (MCP) transport, and observability integration.

---

## 🔁 The ReAct Agent Loop
The agent core utilizes the **ReAct (Reasoning and Acting)** framework to solve tasks iteratively:

1.  **Reasoning**: The model (e.g. `gemma4:e4b`) analyzes the user's prompt and decides which tool (if any) to call, along with the required parameters.
2.  **Acting**: The agent framework intercepts this decision and executes the tool locally or via MCP.
3.  **Observation**: The tool output is appended to the message history, and the model evaluates if the answer is complete or if further actions are required.

This cycle continues dynamically until the model provides a final output.

```
       ┌─────────────────────────────┐
       │     Human Input Message     │
       └──────────────┬──────────────┘
                      │
                      ▼
        ┌───────────────────────────┐
  ┌───► │   LLM Reasoning Step      │
  │     └─────────────┬─────────────┘
  │                   │
  │             [Decision]
  │             /        \
  │      [Tool Call]   [Final Answer] ──► [Respond to User]
  │           │
  │           ▼
  │     ┌───────────┐
  │     │ Tool Exec │
  │     └─────┬─────┘
  │           │
  │     [Observation]
  └───────────┘
```

---

## 🔌 Model Context Protocol (MCP) Integration
The Model Context Protocol allows the agent to communicate with separate external tools running as independent subprocesses.

- **Process Isolation**: MCP servers run as isolated child processes (spawned via commands like `npx`, `uvx`, or python scripts).
- **Communication Transport**: Communication between the agent client and the server happens over standard streams (`stdin` and `stdout`) using JSON-RPC v2.0 packets.
- **Resource/Tool Discovery**: On startup, the client queries the servers for available capabilities and wraps them as standard LangChain tools, mapping them directly into the LLM's bind options.

---

## 📊 Tracing & Observability with Langfuse

To ensure we can audit agent decisions, latencies, and tool errors, the app integrates **Langfuse** at the lowest engine level.

### Execution Hooks
We implement two separate LangChain callbacks inside the execution scope:
1.  **`CustomAgentLogger`**: Prints colored log outlines directly to the container console, indicating when chains start, when tools execute, and when LLMs output text.
2.  **`LangchainCallbackHandler`**: Automatically sends details (prompts, tool parameters, token usage metrics, latency) to the Langfuse backend database.

### Trace Injection Fixes
During streaming operations (using `astream_events`), LangGraph's default integration might submit empty names or empty inputs to the root trace. To resolve this, `ui/app.py` intercepts the session teardown:
*   On session completion (in the `finally` block), the handler's `last_trace_id` is retrieved.
*   The Langfuse client is called manually to update the root trace name to `"MCP Explorer Agent"` and inject the initial user prompt as the trace input payload.
*   A client flush is triggered immediately to ensure no data is lost during streaming cut-offs.
