import os
import yaml
from pathlib import Path

# Minimal defaults to keep the system alive if config.yaml is missing
DEFAULT_CONFIG = {
    "models": {
        "default": "llama3.2:1b",
        "classifier": "llama3.2:1b",
    },
    "model_assignments": {},
    "prompts": {},
    "thresholds": {
        "max_response_time": 60,
        "min_response_length": 0,
    },
}

def load_config(path: str = "config.yaml") -> dict:
    """
    Load configuration from YAML file, apply defaults,
    and allow environment variable overrides.
    """
    config = DEFAULT_CONFIG.copy()

    config_path = Path(path)

    if config_path.exists():
        with open(config_path, "r") as f:
            file_config = yaml.safe_load(f) or {}

        # Shallow merge: top-level keys override defaults
        for key, value in file_config.items():
            config[key] = value

    # Environment variable overrides (highest priority)
    if os.getenv("OLLAMA_MODEL"):
        config["models"]["default"] = os.getenv("OLLAMA_MODEL")

    if os.getenv("OLLAMA_TIMEOUT"):
        config["thresholds"]["max_response_time"] = int(os.getenv("OLLAMA_TIMEOUT"))

    return config
