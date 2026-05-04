# ARCHITECTURE.md

## Overview

The system is a small layered web application built with the Python standard library.

```mermaid
flowchart TD
    Browser["Browser UI"] --> Server["HTTP Server"]
    Server --> Router["Request Handlers"]
    Router --> Service["ShortLinkService"]
    Service --> Repo["JsonLinkRepository"]
    Repo --> Data["data/links.json"]
```

## System Boundary

- External actor: browser user
- Internal system: HTTP server, domain service, JSON repository
- Storage boundary: local file persistence in `data/links.json`

## Layers

- `static/`: HTML, CSS, and JavaScript user interface
- `server.py`: HTTP routing and JSON/redirect responses
- `service.py`: domain rules, validation, expiration, click counting
- `repository.py`: persistence abstraction over a JSON file

## Component Responsibilities

- Browser UI: sends create/list/delete requests and renders link data
- HTTP server: maps routes, parses payloads, returns JSON or redirect responses
- Service layer: validates URLs, generates short codes, enforces expiration rules
- Repository layer: loads and saves serialized link records
- Data file: stores the current system state in a simple format for the lab

## Data Flow

1. The browser sends API requests to the HTTP server.
2. Route handlers deserialize input and call the service.
3. The service validates input, applies business rules, and updates domain state.
4. The repository writes changes to `data/links.json`.
5. The server returns JSON responses or HTTP redirects.

## Request Scenarios

### Create Link

```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant H as HTTP Server
    participant S as ShortLinkService
    participant R as JsonLinkRepository
    participant D as links.json

    U->>B: submit long URL
    B->>H: POST /api/links
    H->>S: create_link(...)
    S->>R: list_links()
    R->>D: read records
    S->>R: save_links(...)
    R->>D: write records
    H-->>B: 201 Created
```

### Redirect and Click Tracking

```mermaid
sequenceDiagram
    participant B as Browser
    participant H as HTTP Server
    participant S as ShortLinkService
    participant R as JsonLinkRepository
    participant D as links.json

    B->>H: GET /r/{code}
    H->>S: resolve_link(code)
    S->>R: list_links()
    R->>D: read records
    S->>R: save_links(updated clicks)
    R->>D: write records
    H-->>B: 302 redirect
```

## Design Decisions

- Keep business logic out of the HTTP layer so tests stay simple.
- Use a repository abstraction even for JSON storage so future migration stays clean.
- Use plain JavaScript on the frontend to minimize setup cost and keep the code inspectable.
- Keep the architecture intentionally small so it remains explainable during oral review.
