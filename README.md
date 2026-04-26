# LLM Prompt Chaining - Research Assistant Pipeline

A CLI research assistant that answers complex qeustions by chaining a sequence of LLM prompts, parsing structural outputs at each step, and compiling a final report.

---

## Context

This project implements a **prompt chaining** pattern: rather than asking a single LLM prompt to do everything, the question is broken down into a sequence of focused steps, each building on the output of the previous one. This improves reliability and output quality by keeping each prompt narrow and well-defined.

The pipeline runs in three steps: (a) decompose the question into sub-questions, (b) research each sub-question individually, (c) synthesise all findings into a structured report. Structured outputs are enforced at every step using Pydantic models, and transient LLM failures are handled with automatic retries.

The pipeline is built with **LangChain** for LLM orchestration and targets the **HuggingFace Inferece API** (free tier) using **DeepSeek-R1**, requiring no local GPU and no paid API subscription.

---

## Objectives

- Implement a multi-step prompt chain where each step receives and produces a typed, validated output.
- Enforce structured JSON outputs from the LLM using Pydantic schemas.
- Handle transient inference failures gracefully with an automatic retry mechanism.
- Keep pipeline modular, each step as an independent, testable unit.

---

## Project Structure

```
LLM-prompt-chaining/
|-- .env                    # HF API token (git-ignore)
|-- .gitignore
|-- requirements.txt
|-- main.py                 # CLI entry point
└-- pipeline/
    |-- __init__.py
    |-- chain.py            # LLM client, retry logic, JSON parsing, pipeline orchestration
    |-- models.py           # Pydantic output schemas for each pipeline step
    └-- steps/
        |-- __init__.py
        |-- decompose.py    # Step 1: break the main research question into sub-question
        |-- research.py     # Step 2: answer each sub-question individually
        └-- synthesize.py   # Step 3: compile all findings into a final report
```

---

## Requirements

- Python 3.10+
- A free [HuggingFace](https://huggingface.co) account and API token

---

## Usage

### 1. Set up the environment

```bash
python -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Confiture your API token

Create a `.env`file in the project root:

```
HF_API_TOKEN=hf_xxxxxxxxxxxxxxxxx
```

Generate a token at huggingface.co → Settings → Access Tokens.

### 3. Run the pipeline

```bash
python main.py "What are the environmental impact of electric vehicles?"
```

### 4. Example output

```
# Comprehensive Analysis of Electric Vehicle Environmental Impacts

Electric vehicles (EVs) generally offer lower lifecycle greenhouse gas emissions than internal combustion engine vehicles (ICEVs), though their environmental benefits...

## Findings

**What are the greenhouse gas emissions associated with the entire lifecycle of electric vehicles (including manufacturing, use, and end-of-life) compared to conventional internal combustion engine vehicles?**
EVs have higher manufacturing emissions (primarily from battery production) but significantly lower use-phase emissions...

**How does the source of electricity used to charge electric vehicles influence their overall environmental impact, particularly in terms of air pollution and carbon footprint?**
Electricity sources critically determine EV impacts: charging from fossil-heavy grids (e.g., coal) increases greenhouse gas emissions and air pollutants (SO₂, NOx, PM)...

...
```

---

## Tech Stack

| **Component**      | **Technology**                                  |
|--------------------|-------------------------------------------------|
| LLM Model          | DeepSeek-R1 (`deepseek-ai/DeepSeek-R1`)         |
| LLM Orchestration  | LangChain + LangChain-HuggingFace               |
| Output Validation  | Pydantic v2                                     |
| Language           | Python 3.10+                                    |