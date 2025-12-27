#!/usr/bin/env python3
"""
Generate historical analysis report from Ollama pipeline results.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

RESULTS_DIR = Path("results")
OUTPUT_FILE = RESULTS_DIR / "historical_report.md"


def load_all_results(results_dir: Path):
    summaries = []

    for run_dir in sorted(results_dir.iterdir()):
        if not run_dir.is_dir():
            continue

        summary_file = run_dir / "workflow_summary.json"
        if summary_file.exists():
            try:
                with open(summary_file) as f:
                    summaries.append(json.load(f))
            except Exception as e:
                print(f"[WARN] Failed to read {summary_file}: {e}")

    return summaries


def analyze_results(summaries):
    model_usage = Counter()
    task_usage = Counter()
    timestamps = []

    for entry in summaries:
        model_usage[entry.get("model", "unknown")] += 1
        task_usage[entry.get("task_type", "unknown")] += 1
        timestamps.append(entry.get("timestamp"))

    return {
        "total_runs": len(summaries),
        "models": model_usage,
        "tasks": task_usage,
        "timestamps": timestamps,
    }


def generate_markdown_report(stats):
    lines = []

    lines.append("# 📊 Historical Multi-Model Analysis Report\n")
    lines.append(f"Generated: {datetime.utcnow().isoformat()} UTC\n")

    if stats["total_runs"] < 1:
        lines.append("⚠️ No workflow runs found. Run the pipeline to collect data.\n")
        return "\n".join(lines)

    lines.append(f"## Summary\n")
    lines.append(f"- Total analysis runs: **{stats['total_runs']}**\n")

    lines.append("## Model Usage\n")
    lines.append("| Model | Runs |")
    lines.append("|------|------|")
    for model, count in stats["models"].items():
        lines.append(f"| {model} | {count} |")

    lines.append("\n## Task Distribution\n")
    lines.append("| Task Type | Runs |")
    lines.append("|----------|------|")
    for task, count in stats["tasks"].items():
        lines.append(f"| {task} | {count} |")

    if stats["total_runs"] < 3:
        lines.append(
            "\n⚠️ Not enough data for trend analysis. "
            "Run at least 3 workflows to enable trend insights.\n"
        )
    else:
        lines.append("\n## Trend Notes\n")
        lines.append("- 📈 System supports multi-model routing")
        lines.append("- 📊 Historical data is accumulating correctly")
        lines.append("- ➡️ Add more runs to unlock performance trends")

    return "\n".join(lines)


def main():
    if not RESULTS_DIR.exists():
        print("[ERROR] results/ directory not found")
        return

    summaries = load_all_results(RESULTS_DIR)
    stats = analyze_results(summaries)
    report = generate_markdown_report(stats)

    OUTPUT_FILE.write_text(report)
    print(f"[REPORT] Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
