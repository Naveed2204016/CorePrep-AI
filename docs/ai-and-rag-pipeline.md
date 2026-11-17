# AI and Retrieval-Augmented Generation Pipeline

## AI providers
CorePrep AI documents two language-model options:

- **Google Gemini** — hosted model API.
- **Ollama** — local model runtime, with Qwen 2.5 7B Instruct documented as a supported model.

The provider is selected through the `LLM_PROVIDER` environment variable. Provider-specific configuration belongs in the backend environment file.

## Retrieval-augmented generation
The retrieval service supplies relevant learning material as context for supported generation tasks.

Documented flow:
1. Read subject-specific Markdown material from `backend/data/`.
2. Split material into smaller chunks.
3. Search for chunks relevant to the learner's request.
4. Add retrieved context to the model prompt.
5. Generate and validate a structured response.

## Retrieval backends

| Backend | Role | Configuration |
|---|---|---|
| BM25 | Default lexical retrieval | `RAG_BACKEND=bm25` or the project's default |
| Qdrant + FastEmbed | Optional vector retrieval | `RAG_BACKEND=vector` |

The README documents `BAAI/bge-small-en-v1.5` as the embedding model for the optional vector setup.

## Configuration example

```text
LLM_PROVIDER=gemini
RAG_BACKEND=bm25
```

Use the exact supported values and defaults in the current backend configuration code. Do not copy secrets into this documentation.

## Reliability considerations
- Treat retrieved text as context, not as automatically verified truth.
- Validate generated output against the application's Pydantic schemas.
- Handle provider timeouts and malformed responses.
- Keep learning documents organized and review their accuracy.
- Avoid logging private prompts, tokens, or uploaded personal documents.

## Feature use
The README describes AI/RAG support for learning roadmaps, assessments, company interview preparation, and CV feedback. The precise service flow can differ by feature; inspect the corresponding service module when changing behavior.
