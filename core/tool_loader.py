import json
from loguru import logger
from langchain_community.agent_toolkits.load_tools import load_tools

def load_standard_tools(config_path):
    logger.info(f"Loading tools config from {config_path}")
    with open(config_path, "r") as f:
        config = json.load(f)
        
    tool_names = config.get("tools", [])
    if not tool_names:
        logger.warning("No standard tools configured.")
        return []
        
    # Dynamically execute any tool-specific initialization logic from JSON
    tool_inits = config.get("tool_inits", {})
    for tool_name in tool_names:
        init_code = tool_inits.get(tool_name)
        if init_code:
            try:
                exec(init_code, globals(), locals())
                logger.info(f"Executed JSON-defined dynamic initialization for tool: {tool_name}")
            except Exception as e:
                logger.error(f"Failed to execute init code for {tool_name}: {e}")

    try:
        tools = load_tools(tool_names)
        logger.info(f"Loaded {len(tools)} standard tools.")
        return tools
    except Exception as e:
        logger.error(f"Failed to load tools: {e}")
        return []
