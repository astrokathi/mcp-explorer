# Code & Prompts Examples

This page provides practical examples of prompts, JSON configurations, and procedures for extending the capabilities of your MCP Explorer.

---

## 💬 1. Example User Prompts

You can enter these queries into the Chainlit chat input to test the system's reasoning loop:

### Standard Tools Queries
*   *Prompt*: `use wikipedia and search for Rabindranath Tagore`
    *   **Agent Flow**: Decides to execute the `wikipedia` tool, scrapes the summary of Tagore, and uses the text to answer.
*   *Prompt*: `use arxiv and search for papers on Transformer architectures`
    *   **Agent Flow**: Decides to run the `arxiv` tool, fetches recent publications matching the query, and formats the abstracts in Markdown.

### Combined Tool Queries
*   *Prompt*: `Search wikipedia for the formula of water, then search arxiv for recent papers detailing water purification techniques using that formula.`
    *   **Agent Flow**: Executes a sequential tool-calling chain (first Wikipedia, then uses the extracted data to formulate an Arxiv search query).

---

## 🔌 2. Adding a Custom MCP Server

You can extend the agent's capabilities by adding server definitions to `mcpConfig.json`.

### Example: SQLite MCP Server
To allow the agent to read, write, and query a local database:

1.  Open `mcpConfig.json` in your workspace.
2.  Add the SQLite server profile to the `mcpServers` object:
    ```json
    {
      "mcpServers": {
        "sqlite": {
          "command": "uvx",
          "args": [
            "mcp-server-sqlite",
            "--db-path",
            "/Users/kathi.s/NKExplorer/Nike_Explorer/dev.db"
          ]
        }
      }
    }
    ```
3.  Restart your Chainlit server or rebuild the Docker container.
4.  Ask the agent: `Show the tables in the SQLite database and list their schemas.` The agent will call the SQLite server tools dynamically.

---

## 🛠️ 3. Adding a Dynamic Tool Initialization

If a new tool requires specific configuration (like environment keys or User-Agents) before loading:

1.  Open `toolsConfig.json`.
2.  Add a new block under `tool_inits`:
    ```json
    {
      "tool_inits": [
        {
          "name": "my_custom_tool",
          "method": "import os\nos.environ['MY_CUSTOM_TOOL_KEY'] = 'my_secret_api_key'\nprint('Custom tool loaded successfully!')"
        }
      ]
    }
    ```
3.  The loader will execute the `method` script block via `exec()` before registering the tool, resolving any setup dependencies dynamically.
