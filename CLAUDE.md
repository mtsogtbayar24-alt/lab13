# CLAUDE.md

## Project Context

This repository is for Lab 13: AI-Assisted Software Construction.

## Build Commands

- Run app: `python3 app.py`
- Run tests: `python3 -m unittest discover -s tests -v`

## Conventions

- Keep core business logic in `src/url_shortener/service.py`
- Keep HTTP-specific behavior in `src/url_shortener/server.py`
- Prefer small functions with explicit names
- Use only standard-library dependencies unless explicitly approved
- Keep commits focused on one idea at a time so the lab history stays explainable
- Prefer documentation-first commits before large implementation jumps

## Review Expectations

- Validate generated code before accepting it
- Check input validation and error handling
- Prefer readable code over clever abstractions
- Add or update tests whenever business rules change
- If AI proposes a broad refactor, reduce it to the smallest safe next step first

## No-Go Zones

- Do not introduce hidden network calls
- Do not hardcode secrets
- Do not bypass tests after changing service behavior
- Do not store invalid URLs or silently ignore repository errors

## Documentation Rules

- Update ADRs when a meaningful architecture decision changes
- Summarize important AI sessions in `ai-logs/`
- Keep documentation synchronized with actual behavior
- Record planning assumptions before implementation if a requirement is ambiguous

## Build Guardrails

- Start with documents and decisions before adding many source files
- Keep the URL shortener scope limited to features already approved in `PROJECT.md`
- Avoid introducing libraries that would weaken the zero-dependency rationale in `STACK-COMPARISON.md`
