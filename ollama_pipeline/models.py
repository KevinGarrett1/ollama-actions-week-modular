"""
Model operations and routing for Ollama pipeline
"""

import time


class OllamaError(Exception):
    """Custom exception for Ollama operations"""
    def __init__(self, message, model=None):
        super().__init__(message)
        self.model = model


def run_model_query(model: str, prompt: str, timeout: int = 60) -> str:
    """
    Temporary stub for model execution.
    This will be replaced with real Ollama subprocess calls later.
    """
    print(f"[MODEL] Running model '{model}'")
    time.sleep(0.5)
    return f"Mock response from {model} for prompt: {prompt[:60]}..."


class ModelRouter:
    """
    Routes tasks to appropriate models using configuration
    """

    def __init__(self, config: dict):
        self.config = config
        self.assignments = config.get("model_assignments", {})
        self.models = config.get("models", {})

    def classify_task(self, content: str) -> str:
        """
        Temporary classifier.
        Uses simple heuristics until AI-based classification is added.
        """
        lowered = content.lower()

        if "def " in lowered or "class " in lowered:
            task = "code_review"
        elif "bug" in lowered or "error" in lowered:
            task = "bug_analysis"
        else:
            task = "documentation"

        print(f"[ROUTER] Classified task as '{task}'")
        return task

    def select_model(self, task_type: str) -> str:
        """
        Select appropriate model for task type.
        """
        model = self.assignments.get(
            task_type,
            self.models.get("default")
        )

        print(f"[ROUTER] Selected model '{model}' for task '{task_type}'")
        return model
