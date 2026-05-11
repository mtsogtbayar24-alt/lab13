# ADR-0002: JSON Persistence and Expiration Enforcement

## Status

Accepted

## Context

The project needs persistence and time-based link invalidation, but it remains intentionally small for a coursework lab.

## Decision

- Persist link records in a local JSON file through a repository abstraction.
- Enforce expiration in the service layer so all access paths use the same rule.

## Rationale

- JSON persistence keeps the environment lightweight and understandable.
- A repository abstraction avoids tying the service directly to file I/O.
- Expiration is a business rule, so placing it in the service layer keeps the HTTP layer thin.

## Consequences

Positive:

- Small operational footprint
- Easy unit testing for expiration behavior
- Future migration path to SQLite or another store

Negative:

- Concurrency guarantees are limited
- JSON is not ideal for larger datasets
