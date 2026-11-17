# CorePrep AI — Architecture Overview

## Purpose
CorePrep AI is a learning, assessment, and interview-preparation platform. It combines a React frontend, a FastAPI backend, a relational database, and configurable AI and retrieval services.

## High-level request flow

1. A learner uses the React application.
2. The frontend sends an HTTP request to the FastAPI application.
3. The backend validates the request and applies authentication and business rules.
4. SQLAlchemy reads or writes application data in MySQL.
5. Where a feature requires generated content, the relevant service calls the configured language-model provider.
6. Where learning-material context is required, the retrieval service searches the configured knowledge corpus.
7. The backend validates the result and returns a structured response to the frontend.

## Main layers

| Layer | Responsibility | Main technologies |
|---|---|---|
| Presentation | Pages, forms, navigation, and user interactions | React, TypeScript, Vite |
| API | HTTP endpoints and request handling | FastAPI, Pydantic |
| Business services | Roadmaps, assessments, company preparation, CV review | Python service modules |
| Persistence | Relational data access | SQLAlchemy, MySQL |
| AI | Text generation and evaluation | Gemini API or Ollama |
| Retrieval | Finding relevant learning content | BM25; optional Qdrant and FastEmbed |

## Design notes
- The frontend and backend are separate applications and are started independently during local development.
- AI provider selection is environment-based (`LLM_PROVIDER`).
- Retrieval selection is environment-based (`RAG_BACKEND`).
- Keep credentials in local environment files. Do not commit real API keys, database passwords, or secret values.

## Related documentation
See `setup-guide.md`, `ai-and-rag-pipeline.md`, and `api-reference.md`.

> This document describes the architecture documented by the project README. Confirm implementation details against the current source before relying on this as a deployment specification.
