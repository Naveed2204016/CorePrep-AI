import asyncio
import unittest
from unittest.mock import patch

from app.core.llm_config import LLMRateLimitError
from app.services import roadmap_service as module


class SucceedsAfterRateLimit:
    def __init__(self):
        self.calls = 0

    async def generate_json(self, **kwargs):
        self.calls += 1
        if self.calls == 1:
            raise LLMRateLimitError("rate limited", retry_after=0)
        return {"ok": True}


class RoadmapRetryTests(unittest.TestCase):
    def test_retries_provider_rate_limit(self):
        provider = SucceedsAfterRateLimit()
        service = module.RoadmapGenerationService()

        with (
            patch.object(module, "get_llm", return_value=provider),
            patch.object(module.asyncio, "sleep", return_value=None),
        ):
            result = asyncio.run(service._generate_json_with_retry(test=True))

        self.assertEqual(result, {"ok": True})
        self.assertEqual(provider.calls, 2)


if __name__ == "__main__":
    unittest.main()
