# AI-Assisted Software Construction Lab 13

This repository contains a complete submission scaffold for Lab 13.

## Assignment Notes

- Course: `F.CSM311 Программ хангамжийн бүтээлт`
- Submission type: AI-assisted mini project with planning, build, and reflection deliverables
- Current repository focus: define the project scope clearly before the main implementation history begins
- Git history goal: keep commits small, explainable, and distributed over multiple working days

## Project

The chosen topic is `URL shortener` with a minimal web UI and a Python standard-library backend.

## Features

- Create short URLs with an optional expiration timestamp
- Redirect through short codes and increment click counters
- List, filter, inspect, and delete saved links
- Persist data to a local JSON file

## Run

```bash
python3 app.py
```

Open `http://127.0.0.1:8000`.

## Test

```bash
python3 -m unittest discover -s tests -v
```

## Repository Guide

- `PROJECT.md`: scope and product definition
- `ARCHITECTURE.md`: architecture and Mermaid diagram
- `STACK-COMPARISON.md`: stack tradeoff analysis
- `CLAUDE.md`: collaboration rules for AI-assisted work
- `adr/`: architectural decisions
- `ai-logs/`: summarized AI sessions
- `.claude/commands/`: custom slash commands
- `src/`: application code
- `static/`: frontend assets
- `tests/`: automated tests
