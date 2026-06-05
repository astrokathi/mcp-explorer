import json
from loguru import logger
from langchain_mcp_adapters.client import MultiServerMCPClient

class MCPLoader:
    def __init__(self, config_path):
        self.config_path = config_path
        self.client = None

    async def initialize(self):
        logger.info(f"Loading MCP config from {self.config_path}")
        with open(self.config_path, "r") as f:
            config = json.load(f)
        
        mcp_servers = config.get("mcpServers", {})
        if not mcp_servers:
            logger.warning("No MCP servers configured.")
            return []

        server_config = {}
        for name, srv in mcp_servers.items():
            server_config[name] = {
                "command": srv.get("command"),
                "args": srv.get("args", []),
                "transport": "stdio"
            }

        self.client = MultiServerMCPClient(server_config)
        tools = await self.client.get_tools()
        logger.info(f"Loaded {len(tools)} MCP tools.")
        return tools

    async def close(self):
        if self.client:
            pass # MultiServerMCPClient doesn't require explicit close in 0.1.0
