import asyncio
import json
import unittest
from unittest.mock import patch

from app.services import company_evaluation_service as module


class PartialBatchLLM:
    async def generate_json(self, **kwargs):
        marker = "QUESTIONS AND ANSWERS:\n"
        payload_text = kwargs["user_prompt"].split(marker, 1)[1].split(
            "\n\nReturn exactly", 1
        )[0]
        payload = json.loads(payload_text)
        # Simulate a provider omitting the last result from multi-item batches.
        returned = payload[:-1] if len(payload) > 1 else payload
        return {
            "answers": [
                {
                    "question_id": item["question_id"],
                    "score": 9 if item["user_answer"] else 4,
                    "status": "correct" if item["user_answer"] else "incorrect",
                    "feedback": "The response was evaluated against the expected concepts.",
                    "suggested_answer": "This is a complete technically correct suggested answer.",
                }
                for item in returned
            ]
        }


class FailsOnceLLM(PartialBatchLLM):
    def __init__(self):
        self.calls = 0

    async def generate_json(self, **kwargs):
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("temporary provider failure")
        return await super().generate_json(**kwargs)


class CompanyEvaluationServiceTests(unittest.TestCase):
    def test_retries_missing_items_and_returns_every_question(self):
        questions = [
            {
                "question_id": question_id,
                "question": f"Question {question_id}",
                "reference_answer": f"Reference {question_id}",
                "user_answer": "Learner answer" if question_id in {1, 3} else "",
            }
            for question_id in range(1, 21)
        ]

        with patch.object(module, "get_llm", return_value=PartialBatchLLM()):
            result = asyncio.run(
                module.CompanyEvaluationService().evaluate(
                    company_name="Example", questions=questions
                )
            )

        self.assertEqual(
            [item.question_id for item in result], list(range(1, 21))
        )
        self.assertEqual(result[0].score, 9)
        self.assertEqual(result[2].score, 9)
        self.assertTrue(
            all(
                item.score == 0
                for item in result
                if item.question_id not in {1, 3}
            )
        )
        self.assertTrue(all(item.suggested_answer for item in result))

    def test_retries_a_temporary_provider_failure(self):
        provider = FailsOnceLLM()
        questions = [{
            "question_id": 1,
            "question": "What is a race condition?",
            "reference_answer": "Concurrent access creates timing-dependent behavior.",
            "user_answer": "It is caused by unsafe concurrent access.",
        }]

        with (
            patch.object(module, "get_llm", return_value=provider),
            patch.object(module.asyncio, "sleep", return_value=None),
        ):
            result = asyncio.run(
                module.CompanyEvaluationService().evaluate(
                    company_name="Example", questions=questions
                )
            )

        self.assertEqual(len(result), 1)
        self.assertGreaterEqual(provider.calls, 2)


if __name__ == "__main__":
    unittest.main()
