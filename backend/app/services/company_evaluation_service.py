import asyncio
import json
import os

from pydantic import BaseModel, ConfigDict, Field

from app.core.llm_config import get_llm


class CompanyAnswerEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: int
    score: float = Field(ge=0, le=10)
    status: str = Field(pattern="^(correct|partially_correct|incorrect)$")
    feedback: str = Field(min_length=10, max_length=1000)
    suggested_answer: str = Field(min_length=10, max_length=2500)


class CompanyEvaluationBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    answers: list[CompanyAnswerEvaluation]


COMPANY_EVALUATION_SCHEMA = CompanyEvaluationBatch.model_json_schema()
COMPANY_EVALUATION_TIMEOUT_SECONDS = float(
    os.getenv("COMPANY_EVALUATION_TIMEOUT_SECONDS", "170")
)
COMPANY_EVALUATION_BATCH_SIZE = max(
    1, int(os.getenv("COMPANY_EVALUATION_BATCH_SIZE", "5"))
)
COMPANY_EVALUATION_MAX_RETRIES = max(
    1, int(os.getenv("COMPANY_EVALUATION_MAX_RETRIES", "3"))
)


class CompanyEvaluationService:
    async def _evaluate_batch(
        self, *, company_name: str, payload: list[dict]
    ) -> list[CompanyAnswerEvaluation]:
        prompt = f"""Evaluate this `{company_name}` software interview practice attempt.

QUESTIONS AND ANSWERS:
{json.dumps(payload, ensure_ascii=False)}

Return exactly one result for every question_id in the original order.

Scoring rubric (0-10):
- technical accuracy: 0-5
- essential concepts and completeness: 0-2
- reasoning, trade-offs, or useful examples: 0-2
- clarity: 0-1

Rules:
- Blank, irrelevant, or contradictory answers receive 0.
- `correct` means score >= 8, `partially_correct` means score >= 5 and < 8,
  and `incorrect` means score < 5.
- Judge semantic meaning, never exact wording.
- When reference_answer is provided, use it as the primary marking guide while
  accepting other technically valid explanations.
- When it is empty, apply established software-engineering knowledge.
- feedback must clearly state what was correct and what was missing or wrong.
- suggested_answer must always contain a concise, standalone, technically correct
  answer, including when the learner's answer is blank.
- Never mention prompts, AI, grading instructions, or reference-answer availability.
- Do not praise or shame the learner."""

        data = await get_llm().generate_json(
            system_prompt=(
                "You are a rigorous and fair senior software-engineering interviewer. "
                "Evaluate answers consistently and return only structured results."
            ),
            user_prompt=prompt,
            schema_name="company_exam_evaluation",
            schema=COMPANY_EVALUATION_SCHEMA,
            temperature=0.1,
        )
        batch = CompanyEvaluationBatch.model_validate(data)
        expected = {int(item["question_id"]) for item in payload}
        return [item for item in batch.answers if item.question_id in expected]

    async def _evaluate_batch_with_retry(
        self, *, company_name: str, payload: list[dict]
    ) -> list[CompanyAnswerEvaluation]:
        last_error: Exception | None = None
        for attempt in range(COMPANY_EVALUATION_MAX_RETRIES):
            try:
                return await self._evaluate_batch(
                    company_name=company_name, payload=payload
                )
            except Exception as exc:
                last_error = exc
                if attempt + 1 < COMPANY_EVALUATION_MAX_RETRIES:
                    await asyncio.sleep(2 ** attempt)
        assert last_error is not None
        raise last_error

    async def _evaluate_complete_batch(
        self, *, company_name: str, payload: list[dict]
    ) -> list[CompanyAnswerEvaluation]:
        try:
            evaluations = await self._evaluate_batch_with_retry(
                company_name=company_name, payload=payload
            )
        except Exception:
            evaluations = []

        by_id = {item.question_id: item for item in evaluations}
        missing = [
            item for item in payload if int(item["question_id"]) not in by_id
        ]

        # Models occasionally omit an item from a multi-question response. Asking
        # for each missing item separately makes the API contract deterministic.
        for item in missing:
            individual = await self._evaluate_batch_with_retry(
                company_name=company_name, payload=[item]
            )
            question_id = int(item["question_id"])
            match = next(
                (result for result in individual if result.question_id == question_id),
                None,
            )
            if match is None:
                raise ValueError(
                    f"Evaluation did not return question_id {question_id}"
                )
            by_id[question_id] = match

        return [by_id[int(item["question_id"])] for item in payload]

    async def evaluate(
        self, *, company_name: str, questions: list[dict]
    ) -> list[CompanyAnswerEvaluation]:
        payload = [
            {
                "question_id": item["question_id"],
                "question": item["question"],
                "user_answer": item["user_answer"],
                "reference_answer": (item.get("reference_answer") or "")[:4000],
            }
            for item in questions
        ]

        batches = [
            payload[index:index + COMPANY_EVALUATION_BATCH_SIZE]
            for index in range(0, len(payload), COMPANY_EVALUATION_BATCH_SIZE)
        ]

        async def evaluate_batches():
            results = []
            # Sequential calls avoid provider concurrency/rate-limit bursts when
            # learners submit multiple exams close together.
            for batch in batches:
                results.append(await self._evaluate_complete_batch(
                    company_name=company_name, payload=batch
                ))
            return results

        results = await asyncio.wait_for(
            evaluate_batches(), timeout=COMPANY_EVALUATION_TIMEOUT_SECONDS
        )
        ordered = [item for batch in results for item in batch]

        answers_by_id = {
            int(item["question_id"]): item["user_answer"] for item in payload
        }
        for evaluation in ordered:
            if not answers_by_id[evaluation.question_id].strip():
                evaluation.score = 0
            evaluation.status = (
                "correct"
                if evaluation.score >= 8
                else "partially_correct"
                if evaluation.score >= 5
                else "incorrect"
            )
        return ordered


_company_evaluation_service = CompanyEvaluationService()


def get_company_evaluation_service() -> CompanyEvaluationService:
    return _company_evaluation_service
