from loguru import logger
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

class Agent:
    def __init__(self, ollama_url: str, all_tools: list):
        self.ollama_url = ollama_url
        self.tools = all_tools
        
        logger.info(f"Initializing ChatOllama with URL {self.ollama_url}")
        self.llm = ChatOllama(
            model="gemma4:e4b",
            base_url=self.ollama_url,
            temperature=0
        )
        
        logger.info(f"Creating ReAct agent with {len(self.tools)} tools")
        self.app = create_react_agent(self.llm, tools=self.tools)

    async def ainvoke(self, prompt: str, thread_id: str = "default_thread", callbacks=None):
        config = {"configurable": {"thread_id": thread_id}}
        if callbacks:
            config["callbacks"] = callbacks
            
        inputs = {"messages": [HumanMessage(content=prompt)]}
        
        logger.info(f"Invoking agent with prompt: {prompt}")
        
        async for event in self.app.astream_events(inputs, config=config, version="v1"):
            yield event
