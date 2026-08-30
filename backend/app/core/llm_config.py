"""JSON-generating LLM clients for local Ollama and hosted Groq models."""

import json
import os
from typing import Any, Protocol

import httpx
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
LLM_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", "180"))

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct")

GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.6-27b")


class JSONGeneratingClient(Protocol):
    async def generate_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        schema_name: str,
        schema: dict[str, Any],
        temperature: float = 0.2,
    ) -> dict[str, Any]: ...


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
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "options": {"temperature": temperature},
        }
        async with httpx.AsyncClient(timeout=LLM_TIMEOUT_SECONDS) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL.rstrip('/')}/api/chat", json=payload
            )
            response.raise_for_status()
            content = response.json()["message"]["content"]
        return json.loads(content)


class GroqClient:
    def __init__(self) -> None:
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required when LLM_PROVIDER=groq")

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
        schema_instruction = (
            "\nReturn only one valid JSON object matching this JSON Schema exactly:\n"
            + json.dumps(schema, separators=(",", ":"))
        )
        payload: dict[str, Any] = {
            "model": GROQ_MODEL,
            "temperature": temperature,
            "reasoning_effort": "none",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt + schema_instruction},
                {"role": "user", "content": user_prompt},
            ],
        }
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=LLM_TIMEOUT_SECONDS) as client:
            response = await client.post(
                f"{GROQ_BASE_URL.rstrip('/')}/chat/completions",
                headers=headers,
                json=payload,
            )
            # Some Groq models reject complex generations in JSON Object Mode
            # even though the same model accepts simpler JSON requests. Retry
            # once with prompt-enforced JSON; Pydantic still validates the
            # returned object at the service boundary.
            if response.status_code == 400:
                first_error = response.text[:2000]
                payload.pop("response_format", None)
                response = await client.post(
                    f"{GROQ_BASE_URL.rstrip('/')}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                if response.is_error:
                    raise RuntimeError(
                        "Groq rejected both JSON-mode and standard requests. "
                        f"JSON-mode response: {first_error}; "
                        f"retry response: {response.text[:2000]}"
                    )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)


def get_llm() -> JSONGeneratingClient:
    if LLM_PROVIDER == "ollama":
        return OllamaClient()
    if LLM_PROVIDER == "groq":
        return GroqClient()
    raise ValueError(
        f"Unsupported LLM_PROVIDER={LLM_PROVIDER!r}; expected 'ollama' or 'groq'"
    )
