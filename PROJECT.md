# PROJECT.md

## Project Name

`ClipLink` - a minimal URL shortener for short-lived sharing links.

## Problem

People often need a short link for sharing a long URL in chat or notes. For a small team or classroom demo, a lightweight self-hosted tool is enough.

## Goal

Build a small web application that demonstrates an AI-assisted workflow while still remaining understandable and fully reviewable by a student.

## Assignment Fit

This topic matches the lab requirement for a small system with at least 3 meaningful features. It is also small enough to support clear ADRs, AI session logs, tests, and reflection without turning the repository into a framework-heavy demo.

## Scope

Included:

- Create a short URL from a long URL
- Optional expiration time for each short link
- Redirect endpoint that counts clicks
- Dashboard to list links and see usage data
- Delete link action
- JSON file persistence

Excluded:

- User accounts
- QR code generation
- Production-grade database
- Analytics beyond click counts
- Distributed deployment

## Milestones

1. Define project scope, repository intent, and assignment alignment. ✓
2. Compare stack options and justify the selected stack. ✓
3. Draft architecture and repository structure before further build commits. ✓
4. Implement domain model, repository, and service layer. ✓
5. Add HTTP endpoints and minimal frontend. ✓
6. Write unit tests covering service behaviour and edge cases. ✓
7. Complete AI usage report, self-evaluation, and submission polish. ✓

## Primary Users

- Student creating demo links
- Reviewer checking functionality quickly

## Success Criteria

- At least 3 core features work end-to-end
- Code remains readable without hidden framework magic
- Tests cover service-layer behavior and edge cases
- Documents clearly show how AI was used and verified

## Risks

- Weak validation could allow invalid URLs
- Expiration logic can be mishandled if time parsing is inconsistent
- Short code collisions must be prevented

## Mitigations

- Validate URL scheme before saving
- Centralize time handling in the service layer
- Retry short code generation until a unique code is found
