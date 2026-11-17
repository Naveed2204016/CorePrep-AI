# CorePrep AI — Developer Guide

> This is a supplementary developer guide for the `docs/` directory. It is intentionally separate from the root `README.md` and does not replace it.
>
> **Accuracy note:** This guide describes recommended engineering practices and the architecture documented for CorePrep AI. Verify exact module names, routes, environment-variable names, commands, and feature behavior against the current repository source before treating them as implementation facts.

## How to use this guide

Use this document when planning a feature, reviewing a pull request, debugging a workflow, or onboarding a contributor. It is organized by engineering concern rather than as a quick-start README.

## Scope

The guide covers frontend development, backend development, API design, persistence, authentication, AI provider integration, retrieval, document processing, testing, security, performance, accessibility, observability, release practices, and contribution workflows.

## Project context

CorePrep AI is documented as an AI-assisted learning and interview-preparation application. Its feature areas include learning roadmaps, job-description-oriented preparation, assessments, company preparation, and CV feedback. The documented technology choices include React, TypeScript, Vite, FastAPI, Pydantic, SQLAlchemy, MySQL, and configurable AI/retrieval components.

## Source of truth

The repository source code, dependency manifests, environment examples, migrations, and live API schema are authoritative. When this guide disagrees with the implementation, follow the implementation and update this guide.


# Product and feature planning

Turn a user need into a clearly scoped, testable product change.


## Key considerations

- Describe the user problem before proposing a technical solution.
- Identify the primary user and the task they are trying to complete.
- Define what success looks like from the user's perspective.
- Separate required behavior from optional enhancements.
- Document assumptions that have not yet been verified.
- Identify whether the change affects existing user data.
- Consider the effect on existing workflows and navigation.
- Prefer incremental delivery over a large, difficult-to-review change.
- Record known limitations rather than implying unsupported behavior.
- Confirm whether the feature requires authentication or authorization.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Frontend architecture

Keep the browser application modular, typed, accessible, and resilient to network conditions.


## Key considerations

- Use the existing component and routing conventions.
- Keep route-level page composition separate from reusable UI.
- Keep API communication in the established service layer where one exists.
- Use shared types for stable API contracts.
- Keep feature-specific state close to the feature unless it is genuinely shared.
- Avoid duplicating form validation rules across multiple components.
- Do not place private server credentials in browser-delivered code.
- Use semantic HTML elements for their intended purpose.
- Provide visible loading, empty, success, and error states.
- Keep components small enough to understand and test.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# React component design

Design components around clear responsibilities and predictable inputs.


## Key considerations

- Give each component one primary responsibility.
- Prefer explicit props over hidden dependencies.
- Use stable keys when rendering collections.
- Avoid mutating props or state directly.
- Keep derived values derived instead of storing redundant state.
- Use effects only for synchronization with external systems.
- Clean up subscriptions, timers, and event listeners.
- Do not suppress dependency warnings without understanding the consequence.
- Use memoization only when it addresses a measured or clear problem.
- Keep conditional rendering readable.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Frontend routing

Make navigation predictable and ensure protected views are actually protected by the backend.


## Key considerations

- Follow the route definitions already used in the application.
- Use clear route names and URL patterns.
- Handle unknown routes with a useful not-found page.
- Preserve navigation context when it improves the user journey.
- Do not rely on frontend route guards as the only authorization control.
- Check behavior when a user refreshes a nested route.
- Keep route-level loading behavior consistent.
- Verify browser back and forward navigation.
- Ensure links are keyboard accessible.
- Update navigation documentation when routes change.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Frontend forms

Build forms that help users submit valid information and recover from mistakes.


## Key considerations

- Label every input clearly.
- Associate help text and validation messages with the relevant field.
- Validate required values before submission.
- Validate again on the server; browser validation is not a security boundary.
- Preserve user-entered values when a recoverable error occurs.
- Disable or guard duplicate submissions.
- Show a clear submission state.
- Provide a useful success confirmation.
- Do not expose raw server stack traces in form errors.
- Support keyboard-only interaction.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Frontend state management

Choose the simplest state model that supports the feature.


## Key considerations

- Distinguish local component state from shared application state.
- Do not copy server data into multiple independent stores without a reason.
- Define how stale data is refreshed.
- Handle requests that finish after a component is no longer active.
- Prevent older responses from overwriting newer user selections.
- Keep authentication state handling consistent.
- Clear user-specific state when the user signs out.
- Represent loading and error states explicitly.
- Avoid storing secrets in persistent browser storage unless the design has been reviewed.
- Document complex state transitions.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Frontend API client

Centralize API communication so error handling and authentication remain consistent.


## Key considerations

- Use the configured API base URL.
- Set content types correctly.
- Attach authentication information only where required.
- Handle non-success HTTP responses.
- Handle network errors and timeouts.
- Parse response bodies defensively.
- Keep request and response types synchronized with backend schemas.
- Do not log tokens or sensitive payloads.
- Make cancellation possible for long-running requests where appropriate.
- Keep retry behavior conservative and avoid retrying non-idempotent requests blindly.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Frontend styling and responsive design

Keep the interface readable and usable across supported screen sizes.


## Key considerations

- Follow the existing design tokens and styling approach.
- Prefer consistent spacing and typography.
- Check narrow mobile layouts.
- Check wide desktop layouts.
- Prevent horizontal overflow.
- Ensure dialogs fit within the viewport.
- Use clear focus indicators.
- Do not communicate status by color alone.
- Respect reduced-motion preferences.
- Check contrast for text and controls.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Frontend performance

Keep the initial experience responsive and avoid unnecessary work in the browser.


## Key considerations

- Measure before applying complex optimization.
- Split large route bundles when supported by the build setup.
- Compress and appropriately size images.
- Lazy-load content that is not immediately needed.
- Avoid unnecessary re-renders caused by unstable props.
- Paginate or virtualize large collections where appropriate.
- Debounce high-frequency search input when useful.
- Cancel obsolete requests.
- Keep large documents out of component state when avoidable.
- Inspect production build output periodically.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Backend architecture

Keep request handling, validation, business rules, and persistence responsibilities distinct.


## Key considerations

- Keep route handlers focused on HTTP concerns.
- Place reusable business logic in service modules where the project uses them.
- Validate request data before processing.
- Use dependency injection patterns already established by the application.
- Keep database access explicit.
- Handle external service failures at a clear boundary.
- Return consistent response structures.
- Use appropriate HTTP status codes.
- Do not leak internal exception details to clients.
- Keep configuration out of hard-coded source constants.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# FastAPI route design

Design API routes with clear resource semantics and stable contracts.


## Key considerations

- Choose HTTP methods according to the operation.
- Use consistent URL naming.
- Define request models for structured input.
- Define response models where appropriate.
- Declare authentication dependencies on protected routes.
- Validate resource ownership.
- Return suitable status codes.
- Document expected errors.
- Keep route handlers short enough to review.
- Update API documentation when the contract changes.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Pydantic schemas

Use explicit schemas to validate data crossing application boundaries.


## Key considerations

- Declare required and optional fields deliberately.
- Set sensible string length constraints.
- Constrain numeric ranges where applicable.
- Validate enumerated values.
- Normalize input only when normalization is part of the contract.
- Do not silently discard important user input.
- Separate public response schemas from internal database models.
- Keep schema names descriptive.
- Test invalid input as well as valid input.
- Review schema changes for backward compatibility.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Backend service layer

Keep feature-specific rules testable and independent from HTTP details.


## Key considerations

- Define service inputs and outputs clearly.
- Keep service functions focused.
- Reuse shared logic instead of copying it.
- Make external dependencies explicit.
- Avoid hidden global mutable state.
- Use transactions for related database changes.
- Raise meaningful domain errors.
- Keep provider-specific logic behind a small interface where practical.
- Write unit tests for important decision rules.
- Document non-obvious business constraints.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Database models

Keep relational models consistent with the data the application actually needs.


## Key considerations

- Use clear table and column names.
- Choose appropriate data types.
- Define foreign keys for real relationships.
- Add indexes for measured query patterns.
- Use uniqueness constraints where the business rule requires uniqueness.
- Define nullability intentionally.
- Be cautious when changing existing column semantics.
- Avoid storing derived data without a clear reason.
- Keep private user data access-controlled.
- Document significant model relationships.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Database transactions

Protect consistency when an operation changes multiple related records.


## Key considerations

- Identify the full set of writes belonging to one logical operation.
- Use a transaction where atomicity is required.
- Keep transactions as short as practical.
- Handle rollback paths.
- Do not perform slow external model calls while holding database locks.
- Consider concurrent updates.
- Use idempotency controls for retryable operations where appropriate.
- Test failure between related writes.
- Verify the final persisted state.
- Document unusual consistency requirements.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Database migrations

Evolve the schema in a controlled and reviewable way.


## Key considerations

- Use the migration mechanism already adopted by the repository.
- Do not edit production schema manually as a substitute for a migration.
- Review generated migration scripts before applying them.
- Plan data backfills explicitly.
- Consider deployment order for application and schema changes.
- Back up important data before risky changes.
- Test migrations against a disposable development database.
- Consider rollback limitations.
- Do not remove columns before confirming they are unused.
- Document operational steps for high-risk migrations.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Authentication

Verify identity consistently for operations that require a signed-in user.


## Key considerations

- Use the authentication mechanism implemented by the project.
- Hash passwords using a maintained password-hashing library.
- Never store plaintext passwords.
- Validate token signatures and expiry.
- Keep signing secrets private.
- Handle expired and invalid tokens consistently.
- Do not expose tokens in logs.
- Invalidate or rotate credentials according to the system design.
- Protect OAuth callback configuration.
- Test sign-in, sign-out, and expired-session behavior.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Authorization

Authentication identifies a user; authorization decides what that user may access.


## Key considerations

- Check ownership for user-specific records.
- Do not trust a user ID supplied by the browser without verification.
- Apply authorization in backend code.
- Check permissions on read, update, and delete operations.
- Consider access to uploaded documents.
- Test attempts to access another user's resource.
- Keep administrative privileges separate.
- Use least privilege for service accounts.
- Return safe responses for unauthorized access.
- Review authorization whenever a route or data relationship changes.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# File uploads

Treat uploaded files as untrusted input.


## Key considerations

- Enforce maximum upload sizes.
- Validate allowed file types.
- Do not trust the filename extension alone.
- Generate safe storage names.
- Store files outside executable locations.
- Restrict access to private uploads.
- Clean up temporary files.
- Handle malformed and empty documents.
- Limit parsing time and memory use.
- Do not include uploaded personal documents in logs.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# AI provider abstraction

Keep provider configuration and provider-specific behavior manageable.


## Key considerations

- Use the provider-selection mechanism already present.
- Keep API keys in environment configuration.
- Do not expose provider credentials to the frontend.
- Use timeouts for provider requests.
- Handle rate limits and temporary failures.
- Validate provider responses.
- Record model and provider metadata when needed for reproducibility.
- Keep provider-specific request formatting isolated.
- Make fallback behavior explicit.
- Test error paths without calling a live provider.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Prompt engineering

Treat prompts as versioned application behavior, not informal text.


## Key considerations

- State the task clearly.
- Specify the expected output format.
- Provide only relevant context.
- Separate trusted instructions from untrusted user content.
- Do not assume the model will follow every instruction.
- Validate structured output after generation.
- Test prompts with normal and adversarial inputs.
- Review prompt changes against representative examples.
- Avoid including unnecessary personal data.
- Record meaningful prompt changes in code review.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Retrieval-augmented generation

Use retrieved material to provide task-relevant context to generation.


## Key considerations

- Identify the source collection for each feature.
- Chunk documents in a repeatable way.
- Preserve useful metadata such as title and source.
- Choose retrieval settings based on evaluation.
- Inspect retrieval quality separately from generation quality.
- Limit context to relevant passages.
- Handle empty retrieval results.
- Do not present retrieved text as verified when its source is untrusted.
- Refresh indexes when source documents change.
- Protect private or user-specific documents from cross-user retrieval.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# BM25 retrieval

Use lexical retrieval where term matching is useful and supported by the project.


## Key considerations

- Normalize text consistently.
- Preserve important technical terms.
- Review tokenization behavior.
- Evaluate results with representative queries.
- Check performance as the corpus grows.
- Handle documents with little text.
- Keep document identifiers stable.
- Review ranking when source material changes.
- Do not assume lexical matching understands semantic equivalence.
- Compare retrieval results against expected relevant documents.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Vector retrieval

Use vector search only where the project has configured and evaluated it.


## Key considerations

- Use the embedding model configured by the application.
- Keep embedding dimensions consistent with the collection.
- Re-embed documents when the embedding model changes.
- Store source metadata with each vector.
- Choose similarity settings based on evaluation.
- Handle missing or unavailable vector services.
- Secure vector database access.
- Keep indexes isolated by environment.
- Monitor indexing failures.
- Compare vector retrieval against the lexical baseline.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# AI output evaluation

Evaluate generated content for usefulness, correctness, and format compliance.


## Key considerations

- Create representative test prompts.
- Include edge cases and ambiguous requests.
- Check factual claims against trusted references.
- Check structured output validity.
- Track provider and model versions.
- Measure latency and failure rates.
- Review output quality with human evaluation when needed.
- Do not rely on one aggregate metric alone.
- Document known model limitations.
- Re-run evaluations after prompt, model, or retrieval changes.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Roadmap feature

Keep roadmap creation and editing understandable and reviewable.


## Key considerations

- Define the input needed to create a roadmap.
- Validate the learner's goal and constraints.
- Represent roadmap topics consistently.
- Make draft and confirmed states clear.
- Allow users to review generated content.
- Persist updates safely.
- Check ownership on all roadmap operations.
- Handle partial generation failures.
- Test empty and unusually large roadmaps.
- Keep the user informed about generation progress.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Assessment feature

Make practice and assessment flows predictable, fair, and testable.


## Key considerations

- Define question formats explicitly.
- Validate submitted answers.
- Keep scoring rules consistent.
- Prevent duplicate submissions where needed.
- Associate results with the correct user.
- Handle interrupted attempts.
- Present feedback clearly.
- Test boundary cases in scoring.
- Keep answer keys private when appropriate.
- Review accessibility of timers and controls.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Company preparation feature

Organize preparation content around a target role without overstating certainty.


## Key considerations

- Make company and role context explicit.
- Distinguish verified source material from generated suggestions.
- Allow learners to edit or dismiss suggestions.
- Keep company content maintainable.
- Do not imply that generated questions are actual confidential interview questions.
- Handle missing company information gracefully.
- Test search and filtering behavior.
- Protect saved preparation history.
- Review stale company information.
- Explain uncertainty where appropriate.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# CV review feature

Provide constructive document feedback without inventing user credentials.


## Key considerations

- Explain what document types are supported.
- Validate uploads before parsing.
- Protect personal information.
- Give actionable suggestions rather than unsupported claims.
- Never fabricate experience or qualifications.
- Let the user review every suggested edit.
- Handle scanned or unreadable documents gracefully.
- Set limits on file size and processing time.
- Remove temporary files according to the data-handling design.
- Test parsing failures and empty documents.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Logging and observability

Make failures diagnosable without collecting unnecessary sensitive data.


## Key considerations

- Use structured logs where supported.
- Include request correlation identifiers where practical.
- Do not log passwords or tokens.
- Do not log full private documents.
- Record provider failures safely.
- Monitor API latency.
- Monitor database errors.
- Track background task failures.
- Set appropriate log retention.
- Keep production debug output disabled.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Testing strategy

Build confidence through tests at multiple levels.


## Key considerations

- Unit-test isolated business rules.
- Test schema validation.
- Test API route behavior.
- Test database persistence.
- Test authentication and authorization boundaries.
- Mock external AI providers in deterministic tests.
- Test retrieval with a small known corpus.
- Test frontend user interactions.
- Run build and lint scripts.
- Document checks that cannot be automated.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# API integration testing

Verify that frontend and backend agree on the contract.


## Key considerations

- Use representative request payloads.
- Verify success response shapes.
- Verify validation error shapes.
- Verify unauthorized behavior.
- Verify missing-resource behavior.
- Verify timeout and network failure behavior.
- Verify pagination if supported.
- Check CORS in a browser environment.
- Keep test credentials isolated.
- Update contract tests when the API changes.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Accessibility

Make the application usable by people with different interaction needs.


## Key considerations

- Use semantic landmarks.
- Label form controls.
- Support keyboard navigation.
- Provide visible focus.
- Ensure dialogs manage focus appropriately.
- Use accessible names for icon-only buttons.
- Announce important asynchronous status changes.
- Do not rely only on color.
- Check text and control contrast.
- Respect reduced-motion preferences.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Performance

Optimize measured bottlenecks while preserving maintainability.


## Key considerations

- Measure frontend bundle size.
- Measure slow API endpoints.
- Inspect database query counts.
- Paginate large result sets.
- Cache only data with clear invalidation rules.
- Limit retrieval context.
- Set sensible provider timeouts.
- Avoid unnecessary repeated model calls.
- Use background work for long tasks when the architecture supports it.
- Document performance trade-offs.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Deployment

Prepare configuration and infrastructure deliberately for each environment.


## Key considerations

- Separate development, test, and production configuration.
- Use secure secret management.
- Enable HTTPS.
- Restrict CORS to trusted origins.
- Disable debug mode.
- Configure database backups.
- Monitor service health.
- Set resource limits for file processing.
- Plan database migrations.
- Document rollback and recovery procedures.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Git collaboration

Keep project history useful to teammates and future maintainers.


## Key considerations

- Create a branch for a focused change.
- Check git status before staging.
- Review the diff before committing.
- Do not commit generated caches or local environments.
- Use accurate commit messages.
- Split unrelated work into separate commits.
- Do not rewrite shared history without coordination.
- Resolve merge conflicts carefully.
- Include test information in pull requests.
- Never manipulate commit statistics with meaningless changes.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Release management

Make releases traceable and recoverable.


## Key considerations

- Identify the set of changes included.
- Confirm tests and builds have run.
- Review dependency changes.
- Review environment changes.
- Check migration requirements.
- Prepare release notes.
- Confirm monitoring is available.
- Define rollback steps.
- Communicate known limitations.
- Verify the deployed health endpoint.


## Review checklist

- [ ] The change matches the current repository conventions.
- [ ] Inputs and outputs are validated.
- [ ] Failure behavior is considered.
- [ ] Security and privacy implications are reviewed.
- [ ] Relevant tests or manual verification are recorded.
- [ ] Documentation is updated when behavior changes.


# Change Playbook: Adding a frontend page

This playbook gives a review sequence for the change type: **Adding a frontend page**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Adding a reusable component

This playbook gives a review sequence for the change type: **Adding a reusable component**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Adding a form

This playbook gives a review sequence for the change type: **Adding a form**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Adding a backend endpoint

This playbook gives a review sequence for the change type: **Adding a backend endpoint**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Changing a response schema

This playbook gives a review sequence for the change type: **Changing a response schema**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Adding a database field

This playbook gives a review sequence for the change type: **Adding a database field**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Changing authentication behavior

This playbook gives a review sequence for the change type: **Changing authentication behavior**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Adding a retrieval source

This playbook gives a review sequence for the change type: **Adding a retrieval source**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Changing an AI prompt

This playbook gives a review sequence for the change type: **Changing an AI prompt**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Adding a model provider

This playbook gives a review sequence for the change type: **Adding a model provider**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Changing file upload handling

This playbook gives a review sequence for the change type: **Changing file upload handling**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Adding an assessment type

This playbook gives a review sequence for the change type: **Adding an assessment type**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Changing roadmap generation

This playbook gives a review sequence for the change type: **Changing roadmap generation**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Adding a company-preparation workflow

This playbook gives a review sequence for the change type: **Adding a company-preparation workflow**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Improving CV parsing

This playbook gives a review sequence for the change type: **Improving CV parsing**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Adding notifications

This playbook gives a review sequence for the change type: **Adding notifications**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Adding pagination

This playbook gives a review sequence for the change type: **Adding pagination**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Adding search filters

This playbook gives a review sequence for the change type: **Adding search filters**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Changing error handling

This playbook gives a review sequence for the change type: **Changing error handling**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Change Playbook: Adding automated tests

This playbook gives a review sequence for the change type: **Adding automated tests**. Adapt it to the existing implementation rather than creating a parallel architecture.


## Suggested workflow

1. Find the existing implementation and read related tests.
2. Identify the user-visible behavior that should change.
3. Identify affected frontend, backend, data, and configuration layers.
4. Define valid input, invalid input, and expected output.
5. Check authentication and authorization requirements.
6. Implement the smallest coherent change.
7. Add or update automated tests where practical.
8. Run the relevant project checks.
9. Review the diff for secrets and unrelated edits.
10. Update the relevant documentation.
11. Write a commit message that accurately describes the change.


## Review checklist

- [ ] No unsupported feature behavior is claimed.
- [ ] Existing workflows remain compatible or migration is documented.
- [ ] Error and loading states are handled.
- [ ] Sensitive information is protected.
- [ ] The change can be reviewed independently.


# Pre-commit review

Use this checklist before completing the **pre-commit review** stage.


## Review checklist

- [ ] Run git status.
- [ ] Inspect the staged diff.
- [ ] Remove local environment files.
- [ ] Remove API keys and credentials.
- [ ] Remove database dumps and private documents.
- [ ] Remove temporary debugging output.
- [ ] Confirm the commit message matches the change.
- [ ] Confirm generated files are intentional.
- [ ] Confirm documentation is not misleading.
- [ ] Confirm tests are reported accurately.


# Pull request review

Use this checklist before completing the **pull request review** stage.


## Review checklist

- [ ] Is the purpose clear?
- [ ] Is the implementation scoped?
- [ ] Are important edge cases covered?
- [ ] Are permissions checked?
- [ ] Are error messages safe?
- [ ] Are tests included or explained?
- [ ] Are configuration changes documented?
- [ ] Are screenshots included when they clarify a UI change?
- [ ] Are breaking changes identified?
- [ ] Can another developer maintain the result?


# AI feature review

Use this checklist before completing the **ai feature review** stage.


## Review checklist

- [ ] Is the model provider configured securely?
- [ ] Is the prompt task clear?
- [ ] Is untrusted content separated from instructions?
- [ ] Is retrieved context relevant?
- [ ] Is model output validated?
- [ ] Are provider failures handled?
- [ ] Is latency acceptable?
- [ ] Is sensitive data minimized?
- [ ] Is output uncertainty communicated?
- [ ] Has representative output been reviewed?


# Database change review

Use this checklist before completing the **database change review** stage.


## Review checklist

- [ ] Is a migration required?
- [ ] Are defaults safe?
- [ ] Are nullability changes understood?
- [ ] Are indexes justified?
- [ ] Are foreign keys correct?
- [ ] Is data backfill required?
- [ ] Is rollback possible?
- [ ] Has the migration been tested?
- [ ] Are concurrent writes considered?
- [ ] Is access to the data authorized?


# Release readiness

Use this checklist before completing the **release readiness** stage.


## Review checklist

- [ ] Build succeeds.
- [ ] Relevant tests pass.
- [ ] Environment variables are documented.
- [ ] Secrets are configured outside source control.
- [ ] Database migration plan is ready.
- [ ] Health checks are available.
- [ ] Logs avoid sensitive data.
- [ ] Backups are configured.
- [ ] Rollback is understood.
- [ ] Known limitations are communicated.


# Command and Configuration Reference

The following commands are examples based on the documented stack. Confirm actual package scripts, entry points, and supported versions in the repository before running them.

## Git inspection

```bash
git status
git diff
git diff --staged
git log --oneline
git branch
```

## Backend virtual environment examples

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Frontend examples

```bash
npm install
npm run
npm run dev
```

Use the scripts actually declared in `frontend/package.json`.

## Database example

```sql
CREATE DATABASE coreprep_ai
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

## Example environment placeholders

```dotenv
DATABASE_URL=mysql+pymysql://USER:PASSWORD@localhost:3306/coreprep_ai
LLM_PROVIDER=gemini
RAG_BACKEND=bm25
```

These are illustrative placeholders, not a complete or guaranteed configuration. Consult the project's `.env.example` and configuration code for the exact variable names and accepted values.

## Example commit messages

```text
docs: add developer guide
feat: validate assessment submissions
fix: handle provider timeout errors
test: cover roadmap service behavior
refactor: simplify API client
```


# Glossary


## API

An application programming interface used by clients to communicate with a service.

## Authentication

The process of verifying who a user or service is.

## Authorization

The process of deciding what an authenticated identity is allowed to do.

## BM25

A lexical information-retrieval ranking method.

## CORS

A browser security mechanism that controls cross-origin requests.

## CRUD

Create, read, update, and delete operations.

## Embedding

A numerical representation of content used for similarity search.

## FastAPI

A Python framework for building APIs.

## JWT

A signed token format commonly used to carry claims between systems.

## Migration

A versioned change to a database schema or data.

## MySQL

A relational database management system.

## ORM

A mapping layer between application objects and relational database records.

## Pydantic

A Python library for data parsing and validation.

## Qdrant

A vector search engine and database.

## RAG

Retrieval-augmented generation, where retrieved material is supplied as context to a generative model.

## React

A JavaScript library for building user interfaces.

## SQLAlchemy

A Python SQL toolkit and ORM.

## TypeScript

A typed superset of JavaScript.

## Vite

A frontend development server and build tool.

## Validation

Checking that data conforms to expected rules.

## Vector search

Retrieval based on similarity between vector representations.


# Final maintenance principle

A large document is useful only when it helps people work accurately. Keep this guide aligned with the implementation, remove obsolete instructions, and prefer verified details over assumptions. Do not add meaningless code or documentation solely to increase GitHub line counts. Meaningful commits should represent real improvements that another contributor can understand and review.
