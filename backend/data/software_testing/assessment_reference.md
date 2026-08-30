# Software Testing and QA Assessment Reference

## Testing Fundamentals
Testing samples behavior to reveal risk and defects; it cannot prove absence of all defects. Verification asks whether the product was built correctly, while validation asks whether the right product was built.
## Test Strategy & Planning
Strategy prioritizes quality risks, scope, levels, environments, data, ownership, and exit evidence. A plan should adapt as risk and information change.
## Test Case Design
Equivalence partitioning samples classes, boundary analysis targets edges, decision tables cover rule combinations, and state testing covers transitions. More cases are not automatically better coverage.
## Unit Testing
Unit tests should be fast, deterministic, isolated enough to locate failures, and focused on behavior. Excessive implementation mocking makes refactoring unnecessarily expensive.
## Integration Testing
Integration tests verify real boundaries such as databases, services, serialization, and configuration. They complement rather than replace focused unit and end-to-end tests.
## System & End-to-End Testing
E2E tests validate complete workflows but are slower and more failure-prone. Keep a focused high-value set with controlled data and strong diagnostics.
## Regression, Smoke & Sanity Testing
Regression checks changed and related behavior, smoke checks whether a build is testable, and sanity checks a focused change. These labels describe scope and purpose, not automation level.
## Black-Box & White-Box Testing
Black-box design derives cases from behavior and requirements; white-box design uses code structure and paths. High code coverage does not prove strong assertions or requirement coverage.
## API Testing
Test contracts, status, schemas, authorization, validation, boundaries, idempotency, concurrency, and failures. A successful status code alone is insufficient.
## UI Test Automation
Prefer semantic stable locators, explicit observable assertions, isolated data, and automatic waits. Fixed sleeps and implementation selectors create flaky tests.
## Performance Testing
Load tests expected demand, stress finds limits, spike tests sudden changes, and endurance exposes long-term degradation. Results require representative workloads and monitored resources.
## Security Testing
Test identity, object authorization, input handling, sessions, configuration, dependencies, and business abuse. Automated scanning cannot replace threat-informed manual investigation.
## Defect Management
Useful reports contain environment, reproducible steps, expected and actual outcomes, evidence, severity, and impact. Severity measures consequence; priority reflects scheduling choice.
## Testing in CI/CD
Pipelines run fast checks early, parallelize safely, retain evidence, and prevent unsafe promotion. Quarantining flaky tests needs ownership and repair deadlines.
## Quality Metrics & Risk-Based Testing
Prioritize likelihood times impact and use metrics as signals, not targets. Coverage, pass rate, and defect counts can mislead without context and escape analysis.
