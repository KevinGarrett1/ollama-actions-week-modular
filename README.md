# Multi-Model Analysis Pipeline (Day 4 AM Challenge)

## Overview

This project implements a **multi-model AI analysis pipeline** using Ollama, evolving a single-model workflow into a configurable, reusable, and historically analyzable system.

The pipeline classifies incoming content, routes it to specialized language models, stores structured results in timestamped directories, and generates historical reports across workflow runs.

This work builds directly on the Day 4 lab and fulfills the **Day 4 AM Challenge** requirements.

---

## Problem Addressed

The initial lab workflow had several limitations:

- A single AI model handled all tasks regardless of context
- Python files were modular but not reusable as a package
- Results were saved but not analyzed across runs
- Behavior was hardcoded, making changes brittle

This challenge resolves those issues by introducing **intelligent routing**, **shared modules**, **configuration-driven behavior**, and **historical reporting**.

---

## Key Outcomes

### 1. Proper Python Package Architecture

The pipeline is implemented as a reusable Python package:

ollama_pipeline/
├── init.py
├── models.py
├── storage.py
├── analysis.py
└── config.py

markdown
Copy code

- Modules import and reuse each other cleanly
- A public API is exposed via `__init__.py`
- Any script or workflow can import the pipeline

**Outcome:** The code behaves like a real internal library, not a collection of loose scripts.

---

### 2. Configuration-Driven Behavior

All runtime behavior is driven by `config.yaml`, including:

- Model assignments per task type
- Prompt templates
- Performance thresholds

Environment variables can override defaults:

- `OLLAMA_MODEL`
- `OLLAMA_TIMEOUT`

**Outcome:** No hardcoded behavior. Models and prompts can be changed without modifying code.

---

### 3. Intelligent Model Routing

The `ModelRouter` class:

- Uses a lightweight classifier model to determine task type
- Routes content to specialized models:
  - `documentation`
  - `code_review`
  - `bug_analysis`
- Logs classification and routing decisions

Example output:

[ROUTER] Classified task as 'documentation'
[ROUTER] Selected model 'llama3.2:1b' for task 'documentation'

yaml
Copy code

**Outcome:** The pipeline selects the right model for the right job.

---

### 4. Centralized Model Execution

All Ollama interactions live in `models.py`:

- `run_model_query()` executes model calls
- Execution timing is logged
- Failures raise a custom `OllamaError`

**Outcome:** A single, auditable entry point for AI execution logic.

---

### 5. Structured Result Storage

Results are persisted through a shared storage layer:

- Timestamped directories under `results/`
- Each run generates a `workflow_summary.json`
- Storage logic is isolated and reusable

Example:

results/
├── 20251227-184827/
│ └── workflow_summary.json
├── 20251227-185635/
│ └── workflow_summary.json

yaml
Copy code

**Outcome:** Results are consistent, machine-readable, and easy to analyze.

---

### 6. Analysis Orchestration

The `analyze_content()` function coordinates:

- Task classification
- Model selection
- AI execution
- Result persistence

Results are returned as a structured `AnalysisResult` dataclass.

**Outcome:** A clean orchestration layer that can scale to multi-file or parallel analysis.

---

### 7. Historical Reporting

The script `scripts/generate_report.py`:

- Scans all historical workflow summaries
- Aggregates run statistics
- Generates a markdown report with:
  - Run counts
  - Model usage
  - Execution timing trends

Output example:

results/historical_report.md

yaml
Copy code

If insufficient data exists, the report degrades gracefully.

**Outcome:** Leadership can observe trends across runs instead of isolated outputs.

---

## CLI-Only Compliance

All work was completed using the command line:

- File creation via shell tools and editors
- Local testing via `python -c`
- Git operations via CLI

No browser-based file editing or UI workflows were used.

**Outcome:** Fully compliant with challenge constraints.

---

## Verification Commands

```bash
# Verify package imports
python -c "from ollama_pipeline import ModelRouter, ResultStorage; print('Imports work')"

# Run a sample analysis
python -c "from ollama_pipeline.analysis import analyze_content; analyze_content('This is documentation text')"

# Generate historical report
python scripts/generate_report.py
Organizational Use
This pipeline is designed to integrate into an organization’s existing CI/CD environment.

Common use cases include:

Pull request analysis

Documentation quality checks

Periodic repository audits

AI-assisted DevOps workflows

Teams can extend the router, adjust configuration, or integrate reporting outputs into dashboards without restructuring the system.

Summary
This project transforms a basic AI workflow into a production-style multi-model pipeline with:

Intelligent task routing

Reusable architecture

Configuration-driven behavior

Historical insight across runs

It demonstrates how AI-powered automation can be structured, scalable, and operationally meaningful.

yaml
Copy code

---
