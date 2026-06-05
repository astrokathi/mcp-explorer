import asyncio
import sys
from pathlib import Path
import os
from loguru import logger

project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from config import CONFIG
from core.agent import Agent
from core.logger import CustomAgentLogger
from langfuse.langchain import CallbackHandler
from core.tool_loader import load_standard_tools

async def main():
    logger.info("Initializing Agent directly for logging tests...")
    
    # Ensure env vars are set for Langfuse
    os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY", "pk-lf-123456")
    os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY", "sk-lf-123456")
    os.environ["LANGFUSE_HOST"] = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
    
    custom_logger = CustomAgentLogger()
    langfuse_handler = CallbackHandler()
    callbacks = [custom_logger, langfuse_handler]
    
    tools = load_standard_tools(CONFIG["TOOLS_CONFIG_PATH"])
    agent = Agent(CONFIG["OLLAMA_URL"], tools)
    
    # Test 1: Success Scenario
    prompt = "What is the capital of France?"
    logger.info(f"--- Running Test 1 (Success): {prompt} ---")
    try:
        async for event in agent.ainvoke(prompt, thread_id="test_thread_1", callbacks=callbacks):
            pass
        logger.info("Test 1 Finished. Check Langfuse dashboard for successful trace.")
    except Exception as e:
        logger.error(f"Test 1 Failed: {e}")
        
    # Test 2: Potential Error/Tool failure scenario
    prompt = "Please force an error or divide by zero."
    logger.info(f"--- Running Test 2 (Potential Failure): {prompt} ---")
    try:
        async for event in agent.ainvoke(prompt, thread_id="test_thread_2", callbacks=callbacks):
            pass
        logger.info("Test 2 Finished.")
    except Exception as e:
        logger.error(f"Test 2 Caught Exception: {e}")
        
    logger.info("Flushing Langfuse logs...")
    langfuse_handler._langfuse_client.flush()
    logger.info("Script completed. Open http://localhost:3000 to view traces.")

if __name__ == "__main__":
    asyncio.run(main())
