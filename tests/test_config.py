import os
import importlib
from pathlib import Path

def test_load_config_default(monkeypatch):
    monkeypatch.delenv("MCP_ENV", raising=False)
    monkeypatch.delenv("OLLAMA_URL", raising=False)
    import config
    importlib.reload(config)
    assert config.CONFIG["ENV"] == "default"
    assert "localhost" in config.CONFIG["OLLAMA_URL"]

def test_load_config_test(monkeypatch):
    monkeypatch.setenv("MCP_ENV", "test")
    import config
    importlib.reload(config)
    assert config.CONFIG["ENV"] == "test"
