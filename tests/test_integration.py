import pytest
import os
from core.agent import Agent
from langchain_ollama import ChatOllama

@pytest.mark.asyncio
async def test_ollama_connection(monkeypatch):
    monkeypatch.setenv("MCP_ENV", "test")
    import config
    import importlib
    importlib.reload(config)
    
    agent = Agent(config.CONFIG["OLLAMA_URL"], [])
    assert agent.ollama_url == config.CONFIG["OLLAMA_URL"]
    assert isinstance(agent.llm, ChatOllama)
    assert agent.llm.base_url == config.CONFIG["OLLAMA_URL"]
