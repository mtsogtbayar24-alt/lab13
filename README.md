# ClipLink — Lab 13 Submission

URL shortener built for `F.CSM311 Программ хангамжийн бүтээлт` Lab 13 (AI-Assisted Software Construction).

## Features

- Create short URLs with an optional expiration timestamp
- Redirect through short codes and increment click counters
- List, filter (all / active / expired), inspect, and delete links
- Persist data to a local JSON file — zero runtime dependencies

## Run

```bash
python3 app.py
```

Open `http://127.0.0.1:8000`.

## Test

```bash
python3 -m unittest discover -s tests -v
```

22 tests, all passing.

## Repository Structure

| Path | Purpose |
|---|---|
| `PROJECT.md` | Scope and product definition |
| `ARCHITECTURE.md` | Architecture and Mermaid diagrams |
| `STACK-COMPARISON.md` | Stack tradeoff analysis and decision matrix |
| `CLAUDE.md` | AI collaboration rules and build guardrails |
| `adr/` | Architectural decision records |
| `ai-logs/` | Summarized AI build sessions |
| `AI-USAGE-REPORT.md` | Honest reflection on AI usage |
| `SELF-EVALUATION.md` | Self-evaluation answers |
| `src/` | Backend application code |
| `static/` | Frontend assets (HTML, JS, CSS) |
| `tests/` | Automated unit tests |

## Stack

- Python 3 standard library (no third-party packages)
- Vanilla JavaScript frontend
- JSON file persistence
