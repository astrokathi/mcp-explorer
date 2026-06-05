import pytest
from core.tool_loader import load_standard_tools
from pathlib import Path

def test_load_standard_tools_success(tmp_path):
    config_file = tmp_path / "toolsConfig.json"
    config_file.write_text('{"tools": ["wikipedia"]}')
    tools = load_standard_tools(str(config_file))
    assert len(tools) > 0
    assert tools[0].name == "wikipedia"

def test_load_standard_tools_empty(tmp_path):
    config_file = tmp_path / "toolsConfig.json"
    config_file.write_text('{}')
    tools = load_standard_tools(str(config_file))
    assert len(tools) == 0
