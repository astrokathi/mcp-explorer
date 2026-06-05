import chainlit as cl
from loguru import logger
import sys
from pathlib import Path

# Add project root to sys.path to allow importing config and core
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from config import CONFIG
from core.mcp_loader import MCPLoader
from core.tool_loader import load_standard_tools
from core.agent import Agent
from core.logger import CustomAgentLogger
from langfuse.langchain import CallbackHandler

@cl.on_chat_start
async def on_chat_start():
    logger.info(f"Starting chat session in {CONFIG['ENV']} environment")
    
    mcp_loader = MCPLoader(CONFIG["MCP_CONFIG_PATH"])
    cl.user_session.set("mcp_loader", mcp_loader)
    
    try:
        mcp_tools = await mcp_loader.initialize()
    except Exception as e:
        logger.error(f"Failed to load MCP tools: {e}")
        mcp_tools = []
        
    standard_tools = load_standard_tools(CONFIG["TOOLS_CONFIG_PATH"])
    
    all_tools = mcp_tools + standard_tools
    
    agent = Agent(CONFIG["OLLAMA_URL"], all_tools)
    cl.user_session.set("agent", agent)
    
    await cl.Message(content=f"Agent initialized with {len(all_tools)} tools.").send()

@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    if not agent:
        await cl.Message(content="Agent is not initialized yet.").send()
        return

    msg = cl.Message(content="")
    await msg.send()
    
    thread_id = cl.user_session.get("id")
    
    # Initialize callbacks
    custom_logger = CustomAgentLogger()
    langfuse_handler = CallbackHandler()
    callbacks = [custom_logger, langfuse_handler]
    
    try:
        async for event in agent.ainvoke(message.content, thread_id=thread_id, callbacks=callbacks):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                chunk = event.get("data", {}).get("chunk")
                if chunk and hasattr(chunk, "content"):
                    await msg.stream_token(chunk.content)
            elif kind == "on_tool_start":
                tool_name = event.get("name", "unknown")
                await cl.Message(content=f"🛠️ Using tool: {tool_name}").send()
    except Exception as e:
        import traceback
        logger.error(f"Error during agent invocation: {e}\n{traceback.format_exc()}")
        await cl.Message(content=f"Error: {e}").send()
    finally:
        if hasattr(langfuse_handler, 'last_trace_id') and langfuse_handler.last_trace_id:
            try:
                if hasattr(langfuse_handler, 'langfuse'):
                    langfuse_handler.langfuse.trace(
                        id=langfuse_handler.last_trace_id,
                        name="Nike Explorer Agent",
                        input=message.content
                    )
            except Exception as e:
                logger.error(f"Failed to update trace input: {e}")

        if hasattr(langfuse_handler, 'langfuse') and hasattr(langfuse_handler.langfuse, 'flush'):
            langfuse_handler.langfuse.flush()
        elif hasattr(langfuse_handler, 'flush'):
            langfuse_handler.flush()

    await msg.update()

@cl.on_chat_end
async def on_chat_end():
    mcp_loader = cl.user_session.get("mcp_loader")
    if mcp_loader:
        await mcp_loader.close()
