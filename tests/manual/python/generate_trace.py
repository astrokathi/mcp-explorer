import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from config import CONFIG
from core.tool_loader import load_standard_tools
from langfuse.langchain import CallbackHandler
from core.agent import Agent
import os

async def main():
    print("Initializing Langfuse Callback...")
    langfuse_handler = CallbackHandler()
    
    print("Loading Tools...")
    tools = load_standard_tools(CONFIG["TOOLS_CONFIG_PATH"])
    
    print("Initializing Agent...")
    agent = Agent(CONFIG["OLLAMA_URL"], tools)
    
    print("Invoking Agent...")
    try:
        async for event in agent.ainvoke(
            prompt="Hello! This is a test trace!",
            callbacks=[langfuse_handler]
        ):
            pass
        print("Agent responded!")
    except Exception as e:
        print(f"Agent error: {e}")
        
    print("Flushing Langfuse...")
    langfuse_handler._langfuse_client.flush()
    print("Done!")

asyncio.run(main())
