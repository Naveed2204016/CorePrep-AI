# API Reference

## Overview
CorePrep AI exposes REST endpoints through FastAPI. The documented API prefix is `/api/v1`.

The tables below summarize endpoints listed in the project README. Confirm request and response schemas in the corresponding backend route modules before integrating a client.

## Authentication

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/auth/signup` | Register a user |
| POST | `/api/v1/auth/login` | Authenticate and issue a JWT |
| GET | `/api/v1/auth/google` | Start Google OAuth |
| GET | `/api/v1/auth/google/callback` | Handle the OAuth callback |

## Roadmaps

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/roadmaps/generate` | Generate a topic-based roadmap |
| POST | `/api/v1/roadmaps/generate-from-job` | Generate a roadmap from a job-description PDF |
| GET | `/api/v1/roadmaps` | List confirmed roadmaps |
| GET | `/api/v1/roadmaps/{roadmap_id}` | Retrieve a roadmap |
| DELETE | `/api/v1/roadmaps/{roadmap_id}` | Delete a roadmap |
| POST | `/api/v1/roadmaps/{roadmap_id}/suggest-edit` | Suggest edits to a draft |
| POST | `/api/v1/roadmaps/{roadmap_id}/confirm` | Confirm and activate a roadmap |

## Interactive API documentation
When the backend is running locally, FastAPI normally provides interactive documentation at:

```text
http://localhost:8000/docs
```

The project README also documents a health endpoint at `/health`.

## Authentication guidance
Protected endpoints use Bearer-token authentication according to the project documentation. Do not put real tokens in examples, screenshots, issues, or committed files.

## Keeping this reference accurate
When an endpoint changes:
1. Update the route implementation.
2. Update request/response schemas.
3. Verify the endpoint in the interactive API documentation.
4. Update this reference in the same change.
