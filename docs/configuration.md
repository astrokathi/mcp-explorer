# Configuration Reference Guide

This document describes all environment variables and configuration files (`toolsConfig.json` and `mcpConfig.json`) used to control the runtime behavior of the MCP Explorer.

---

## 🔑 Environment Variables

These variables are defined in your local `.env` file (for bare-metal execution) or `.env.docker` (in the Docker Stack).

### Core Services Settings

| Variable Name | Default Value | Description |
| :--- | :--- | :--- |
| `OLLAMA_URL` | `http://localhost:11434` | The HTTP endpoint where your local Ollama server is running. Inside Docker containers, this is overridden to `http://host.docker.internal:11434`. |
| `MONGODB_URI` | `mongodb://localhost:27017/dev` | Connection URI for the MongoDB server used by the agent memory. |
| `LOG_LEVEL` | `DEBUG` | System verbosity logging level. Options are `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. |

### Langfuse Observatory Connection

| Variable Name | Target UI Location | Description |
| :--- | :--- | :--- |
| `LANGFUSE_PUBLIC_KEY` | Settings -> API Credentials | Public API Key generated from the Langfuse project console to authenticate traces. |
| `LANGFUSE_SECRET_KEY` | Settings -> API Credentials | Secret API Key paired with the public key. Keep this private! |
| `LANGFUSE_HOST` | - | The HTTP host address of the Langfuse server. For local dev, this is `http://localhost:3000`. Inside Docker, the app container connects via `http://langfuse-server:3000`. |

### Docker Stack Internal Secrets

These variables are auto-generated when running `./docker-run.sh` to secure your internal Postgres and session cookies:

*   `NEXTAUTH_SECRET`: Used by NextAuth to sign secure session tokens in the Langfuse dashboard.
*   `SALT`: Secure string used by Langfuse to encrypt project variables.
*   `ENCRYPTION_KEY`: A 64-character hexadecimal key used by the Langfuse backend to encrypt credential records stored in Postgres.

---

## 🛠️ Configuration Files

### 1. `toolsConfig.json`
Manages standard LangChain tools and their initialization methods.

Example structure:
```json
{
  "tool_inits": [
    {
      "name": "wikipedia",
      "method": "from urllib.request import Request\nimport wikipedia\n# Configure user agent dynamically\n"
    },
    {
      "name": "arxiv",
      "method": "import arxiv\n# Configure arxiv parameters dynamically\n"
    }
  ]
}
```

- **`name`**: The name of the package/module loaded dynamically.
- **`method`**: Dynamic Python script lines loaded and executed via `exec()` inside `core/tool_loader.py` to initialize parameters (e.g. setting custom User-Agents) before loading.

### 2. `mcpConfig.json`
Defines the connection parameters for Model Context Protocol (MCP) servers.

Example structure:
```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/app/dev.db"]
    }
  }
}
```

- **`command`**: The execution binary (e.g., `npx`, `uvx`, `python3`, `node`).
- **`args`**: Arguments passed to the command line to startup the server.
- **`env`**: (Optional) Key-value pairs for environment variables passed to the sub-process.
