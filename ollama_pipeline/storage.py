"""
Storage utilities for Ollama pipeline
"""

import json
from pathlib import Path
from datetime import datetime


class DirectoryManager:
    """Handles timestamped directory creation"""

    def __init__(self, base_dir="results"):
        self.base_dir = Path(base_dir)

    def create_run_dir(self):
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        run_dir = self.base_dir / timestamp
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir


class ResultStorage:
    """Stores analysis results to disk"""

    def __init__(self, base_dir="results"):
        self.dir_manager = DirectoryManager(base_dir)

    def save(self, result_dict: dict):
        run_dir = self.dir_manager.create_run_dir()
        output_file = run_dir / "analysis.json"

        with open(output_file, "w") as f:
            json.dump(result_dict, f, indent=2)

        print(f"[STORAGE] Saved results to {output_file}")
        return output_file
