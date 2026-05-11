# ADR-0001: Stack Selection

## Status

Accepted

## Context

The repository started empty, and the environment could not assume package installation. The lab needed a small but working system with tests and documentation.

## Decision

Use Python standard library for the backend, JSON file persistence, and a vanilla JavaScript frontend.

## Consequences

Positive:

- Zero dependency install for runtime
- Easy to inspect and explain
- Straightforward service-layer testing

Negative:

- Manual routing and response handling
- No automatic OpenAPI generation
- More boilerplate than a framework
