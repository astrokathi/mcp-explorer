from langchain_core.callbacks import BaseCallbackHandler
import uuid
from loguru import logger

class CustomAgentLogger(BaseCallbackHandler):
    """
    Custom console logger as requested to visualize the agent events.
    """
    def __init__(self):
        self.run_tree = {}

    def on_chain_start(self, serialized, prompts, **kwargs):
        run_id = kwargs.get("run_id") or str(uuid.uuid4())
        logger.info(f"[CHAIN START] ID: {run_id} | Initial Prompt: {prompts}")

    def on_tool_start(self, serialized, input_str, **kwargs):
        logger.info(f"  [TOOL START] Running Tool: {serialized.get('name')} with input: {input_str}")

    def on_tool_end(self, output, **kwargs):
        logger.info(f"  [TOOL END] Tool Output: {output}")

    def on_llm_end(self, response, **kwargs):
        token_usage = response.llm_output.get("token_usage", {}) if response.llm_output else {}
        logger.info(f"[LLM END] Generated Text. Tokens used: {token_usage}")
