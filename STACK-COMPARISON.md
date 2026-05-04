# STACK-COMPARISON.md

## Compared Options

### Option 1: FastAPI + SQLite + simple HTML

Pros:

- Modern API tooling
- Strong request validation
- Good OpenAPI support

Cons:

- Requires external dependencies
- More setup for an empty environment
- Slight risk if package install or environment setup fails during the lab window

### Option 2: Node.js + Express + lowdb

Pros:

- Popular web stack
- Easy JSON APIs
- Flexible frontend integration

Cons:

- Dependency install required
- Slightly more moving parts for a small lab
- Runtime and tooling choices would need additional explanation during review

### Option 3: Python standard library + JSON + vanilla JS

Pros:

- No third-party installation needed
- Easy to run in constrained environments
- Encourages understanding every layer

Cons:

- Manual routing and validation
- No built-in OpenAPI generation
- More boilerplate than a framework

## Evaluation Criteria

The stack was compared using these criteria:

- setup risk in an empty repository
- ease of explaining the code during oral review
- support for 3-5 features without overengineering
- testability of the business logic
- fit for AI-assisted incremental commits and documentation

## Decision Matrix

| Option | Setup Risk | Explainability | Testability | Lab Fit |
| --- | --- | --- | --- | --- |
| FastAPI + SQLite | Medium | High | High | Medium |
| Node + Express | Medium | Medium | Medium | Medium |
| Python stdlib + JSON | Low | High | High | High |

## Chosen Stack

Option 3: Python standard library + JSON + vanilla JavaScript.

## Why This Stack Won

- The repository started empty, so a zero-dependency stack lowers execution risk.
- The lab emphasizes AI workflow, review, and architectural reasoning more than framework usage.
- The service layer can still be cleanly tested and extended.
- A reviewer can open every file and understand the system quickly.
- The smaller stack also makes it easier to split the work into honest multi-day commits without hiding important logic inside framework defaults.
