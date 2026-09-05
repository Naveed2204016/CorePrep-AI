import json
import unittest
from unittest.mock import patch

from app.core import llm_config


class FakeResponse:
    def __init__(self, *, status_code=200, body=None, headers=None):
        self.status_code = status_code
        self._body = body or {}
        self.headers = headers or {}
        self.text = json.dumps(self._body)

    @property
    def is_error(self):
        return self.status_code >= 400

    def json(self):
        return self._body


class FakeAsyncClient:
    response = None
    last_request = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    async def post(self, url, *, headers, json):
        type(self).last_request = (url, headers, json)
        return type(self).response


class GeminiClientTests(unittest.IsolatedAsyncioTestCase):
    async def test_generates_and_parses_structured_json(self):
        expected = {"answers": [{"question_id": 1, "score": 8}]}
        FakeAsyncClient.response = FakeResponse(body={
            "candidates": [{
                "content": {"parts": [{"text": json.dumps(expected)}]}
            }]
        })

        with (
            patch.object(llm_config, "GEMINI_API_KEY", "test-key"),
            patch.object(llm_config.httpx, "AsyncClient", FakeAsyncClient),
        ):
            result = await llm_config.GeminiClient().generate_json(
                system_prompt="system",
                user_prompt="user",
                schema_name="evaluation",
                schema={"type": "object"},
            )

        self.assertEqual(result, expected)
        url, headers, payload = FakeAsyncClient.last_request
        self.assertIn("gemini-3.5-flash-lite:generateContent", url)
        self.assertEqual(headers["x-goog-api-key"], "test-key")
        self.assertEqual(
            payload["generationConfig"]["responseMimeType"],
            "application/json",
        )
        self.assertEqual(
            payload["generationConfig"]["responseJsonSchema"],
            {"type": "object"},
        )

    async def test_maps_rate_limit_to_retryable_error(self):
        FakeAsyncClient.response = FakeResponse(
            status_code=429,
            body={"error": {"message": "quota exceeded"}},
            headers={"retry-after": "7"},
        )

        with (
            patch.object(llm_config, "GEMINI_API_KEY", "test-key"),
            patch.object(llm_config.httpx, "AsyncClient", FakeAsyncClient),
        ):
            with self.assertRaises(llm_config.LLMRateLimitError) as raised:
                await llm_config.GeminiClient().generate_json(
                    system_prompt="system",
                    user_prompt="user",
                    schema_name="evaluation",
                    schema={"type": "object"},
                )

        self.assertEqual(raised.exception.retry_after, 7)


if __name__ == "__main__":
    unittest.main()
