import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

def load_config():
    env = os.getenv("MCP_ENV", "default")
    
    if env == "test":
        env_file = ".env.test"
    elif env == "prod":
        env_file = ".env.prod"
    else:
        env_file = ".env"
        
    env_path = BASE_DIR / env_file
    load_dotenv(dotenv_path=env_path)
    
    return {
        "ENV": env,
        "OLLAMA_URL": os.getenv("OLLAMA_URL", "http://localhost:11434"),
        "MONGODB_URI": os.getenv("MONGODB_URI", "mongodb://localhost:27017/dev"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "DEBUG"),
        "MCP_CONFIG_PATH": BASE_DIR / "mcpConfig.json",
        "TOOLS_CONFIG_PATH": BASE_DIR / "toolsConfig.json"
    }

CONFIG = load_config()
