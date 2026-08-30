# Backend Assessment Reference

## Backend & Server Fundamentals
Servers accept requests through sockets and execute work using processes, threads, event loops, or combinations. Concurrency model choices affect blocking, isolation, throughput, and failure behavior.
## REST API Design
Resources use stable identifiers and HTTP semantics; safe methods do not modify state and idempotent methods tolerate repetition. Pagination, versioning, filtering, and consistent errors are contract decisions.
## Validation & Error Handling
Validate untrusted boundaries and separate client errors from server failures. Responses should avoid internal leakage while logs retain correlation and diagnostic context.
## Authentication & Authorization
Authentication identifies a principal; authorization checks each requested action and resource. Tokens do not remove revocation, expiry, storage, CSRF, or ownership concerns.
## SQL & Database Design
Constraints preserve invariants and transactions define atomic business boundaries. Avoid N+1 queries, unbounded scans, and application-only enforcement of critical integrity.
## ORMs & Migrations
ORM identity maps and loading strategies influence queries and consistency. Safe migrations often expand, migrate data, switch code, and contract rather than applying breaking changes instantly.
## Caching
Cache-aside loads on misses; write-through updates cache with writes. Invalidation, TTL, stale reads, stampedes, serialization, and key design determine correctness.
## Background Jobs & Queues
Workers must handle duplicates, retries, poison messages, ordering, and partial failure. Idempotency makes at-least-once delivery manageable.
## File & Object Storage
Validate type and size without trusting filenames, stream large content, and avoid serving uploads as executable content. Signed URLs delegate limited temporary access.
## Backend Testing
Unit tests isolate logic, integration tests verify boundaries, and contract tests preserve service expectations. Deterministic fixtures and failure-path tests matter more than raw test count.
## Backend Security
Parameterized queries prevent SQL injection; object-level authorization prevents IDOR; egress controls reduce SSRF. Secrets belong in controlled stores, never logs or source.
## Logging & Observability
Structured logs support querying, metrics reveal trends, and traces connect distributed latency. Correlation IDs and careful PII handling are essential.
## Scalability & Reliability
Stateless instances scale horizontally, but databases and shared dependencies still constrain capacity. Timeouts, bounded retries, backpressure, and graceful shutdown prevent cascading failure.
## Containers & Deployment
Images should be reproducible, minimal, and non-root where possible. Readiness differs from liveness, and deployment must coordinate configuration, schema compatibility, and rollback.
## Backend Architecture
Layering and modular boundaries should protect business rules from infrastructure details. Monoliths, services, events, and CQRS each carry operational and consistency costs.
