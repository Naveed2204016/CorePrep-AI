"""JSON-generating LLM clients for local Ollama and hosted Groq models."""

import json
import os
from typing import Any, Protocol

import httpx
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
LLM_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", "45"))

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct")

GROQ_BASE_URL = os.getenv(
    "GROQ_BASE_URL",
    "https://api.groq.com/openai/v1",
)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")


class LLMError(RuntimeError):
    """Base exception for LLM provider failures."""


class LLMRateLimitError(LLMError):
    """Raised when the provider returns HTTP 429."""

    def __init__(
        self,
        message: str,
        *,
        retry_after: float = 5.0,
    ) -> None:
        super().__init__(message)
        self.retry_after = max(0.0, retry_after)


class LLMTransientError(LLMError):
    """Raised for retryable provider/network failures."""


class LLMRequestError(LLMError):
    """Raised for non-retryable request/configuration failures."""


class JSONGeneratingClient(Protocol):
    async def generate_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        schema_name: str,
        schema: dict[str, Any],
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        ...


class OllamaClient:
    async def generate_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        schema_name: str,
        schema: dict[str, Any],
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        del schema_name

        payload = {
            "model": OLLAMA_MODEL,
            "stream": False,
            "format": schema,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "options": {
                "temperature": temperature,
            },
        }

        try:
            async with httpx.AsyncClient(
                timeout=LLM_TIMEOUT_SECONDS
            ) as client:
                response = await client.post(
                    f"{OLLAMA_BASE_URL.rstrip('/')}/api/chat",
                    json=payload,
                )

        except httpx.TimeoutException as exc:
            raise LLMTransientError(
                "Ollama request timed out"
            ) from exc

        except httpx.RequestError as exc:
            raise LLMTransientError(
                f"Could not reach Ollama: {exc}"
            ) from exc

        if response.status_code >= 500:
            raise LLMTransientError(
                f"Ollama server error {response.status_code}: "
                f"{response.text[:1000]}"
            )

        if response.is_error:
            raise LLMRequestError(
                f"Ollama request failed with HTTP "
                f"{response.status_code}: "
                f"{response.text[:1000]}"
            )

        try:
            content = response.json()["message"]["content"]
            return json.loads(content)

        except (
            KeyError,
            TypeError,
            json.JSONDecodeError,
        ) as exc:
            raise LLMTransientError(
                "Ollama returned an invalid JSON response"
            ) from exc


class GroqClient:
    def __init__(self) -> None:
        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is required when LLM_PROVIDER=groq"
            )

    @staticmethod
    def _retry_after_seconds(
        response: httpx.Response,
    ) -> float:
        value = response.headers.get("retry-after")

        if not value:
            return 5.0

        try:
            return max(0.0, float(value))

        except ValueError:
            return 5.0

    async def generate_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        schema_name: str,
        schema: dict[str, Any],
        temperature: float = 0.2,
    ) -> dict[str, Any]:

        payload: dict[str, Any] = {
            "model": GROQ_MODEL,
            "temperature": temperature,

            # Strict Structured Outputs.
            # qwen/qwen3.8-27b currently supports strict JSON Schema mode.
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": schema_name,
                    "strict": True,
                    "schema": schema,
                },
            },

            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        }

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(
                timeout=LLM_TIMEOUT_SECONDS
            ) as client:

                response = await client.post(
                    f"{GROQ_BASE_URL.rstrip('/')}/chat/completions",
                    headers=headers,
                    json=payload,
                )

        except httpx.TimeoutException as exc:
            raise LLMTransientError(
                "Groq request timed out"
            ) from exc

        except httpx.RequestError as exc:
            raise LLMTransientError(
                f"Could not reach Groq: {exc}"
            ) from exc

        # Rate limiting must be handled separately.
        if response.status_code == 429:
            retry_after = self._retry_after_seconds(
                response
            )

            raise LLMRateLimitError(
                (
                    "Groq rate limit reached; "
                    f"retry after {retry_after:.2f}s"
                ),
                retry_after=retry_after,
            )

        # Temporary Groq-side errors.
        if response.status_code >= 500:
            raise LLMTransientError(
                f"Groq server error "
                f"{response.status_code}: "
                f"{response.text[:1000]}"
            )

        # 400 / 401 / 403 etc.
        # Repeating the same bad request will not solve it.
        if response.is_error:
            raise LLMRequestError(
                f"Groq request failed with HTTP "
                f"{response.status_code}: "
                f"{response.text[:2000]}"
            )

        try:
            body = response.json()

            content = (
                body["choices"][0]["message"]["content"]
            )

            return json.loads(content)

        except (
            KeyError,
            IndexError,
            TypeError,
            json.JSONDecodeError,
        ) as exc:

            raise LLMTransientError(
                "Groq returned an invalid structured response"
            ) from exc


def get_llm() -> JSONGeneratingClient:
    if LLM_PROVIDER == "ollama":
        return OllamaClient()

    if LLM_PROVIDER == "groq":
        return GroqClient()

    raise ValueError(
        f"Unsupported LLM_PROVIDER={LLM_PROVIDER!r}; "
        "expected 'ollama' or 'groq'"
    )