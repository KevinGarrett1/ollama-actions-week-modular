from dataclasses import dataclass
from datetime import datetime
from .models import ModelRouter, run_model_query
from .storage import ResultStorage
from .config import load_config

@dataclass
class AnalysisResult:
    task_type: str
    model: str
    output: str
    timestamp: str


def analyze_content(content: str):
    config = load_config()
    router = ModelRouter(config)
    storage = ResultStorage()

    task = router.classify_task(content)
    model = router.select_model(task)
    prompt = config["prompts"].get(task, content)

    output = run_model_query(model, f"{prompt}\n\n{content}")
    result = AnalysisResult(
        task_type=task,
        model=model,
        output=output,
        timestamp=datetime.utcnow().isoformat(),
    )

    storage.save(result.__dict__)
    return result

def analyze_repository(path: str = "."):
    """
    Placeholder for repository-wide analysis.
    Implemented later in the Day 4 challenge.
    """
    raise NotImplementedError("analyze_repository is not implemented yet")
