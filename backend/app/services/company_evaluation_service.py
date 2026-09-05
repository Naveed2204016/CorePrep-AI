import asyncio
import json
import logging
import os
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
)

from app.core.llm_config import (
    LLMRateLimitError,
    LLMRequestError,
    LLMTransientError,
    get_llm,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Raw structure returned by the LLM
# ---------------------------------------------------------

class CompanyAnswerEvaluationPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: int
    score: float = Field(ge=0, le=10)
    feedback: str
    suggested_answer: str


class CompanyEvaluationBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answers: list[CompanyAnswerEvaluationPayload]


# ---------------------------------------------------------
# Final structure used by the rest of the application
# ---------------------------------------------------------

class CompanyAnswerEvaluation(BaseModel):
    question_id: int

    score: float = Field(
        ge=0,
        le=10,
    )

    status: Literal[
        "correct",
        "partially_correct",
        "incorrect",
    ]

    feedback: str
    suggested_answer: str


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

COMPANY_EVALUATION_SCHEMA = (
    CompanyEvaluationBatch.model_json_schema()
)

COMPANY_EVALUATION_TIMEOUT_SECONDS = float(
    os.getenv(
        "COMPANY_EVALUATION_TIMEOUT_SECONDS",
        "240",
    )
)

COMPANY_EVALUATION_BATCH_SIZE = max(
    1,
    int(
        os.getenv(
            "COMPANY_EVALUATION_BATCH_SIZE",
            "5",
        )
    ),
)

COMPANY_EVALUATION_MAX_RETRIES = max(
    1,
    int(
        os.getenv(
            "COMPANY_EVALUATION_MAX_RETRIES",
            "3",
        )
    ),
)

COMPANY_EVALUATION_REFERENCE_MAX_CHARS = max(
    200,
    int(
        os.getenv(
            "COMPANY_EVALUATION_REFERENCE_MAX_CHARS",
            "1500",
        )
    ),
)

COMPANY_EVALUATION_USER_MAX_CHARS = max(
    200,
    int(
        os.getenv(
            "COMPANY_EVALUATION_USER_MAX_CHARS",
            "2500",
        )
    ),
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def _clip(
    value: str,
    limit: int,
) -> str:

    if len(value) <= limit:
        return value

    return value[:limit]


def _status_for_score(
    score: float,
) -> Literal[
    "correct",
    "partially_correct",
    "incorrect",
]:

    if score >= 8:
        return "correct"

    if score >= 5:
        return "partially_correct"

    return "incorrect"


# ---------------------------------------------------------
# Service
# ---------------------------------------------------------

class CompanyEvaluationService:

    async def _evaluate_batch(
        self,
        *,
        company_name: str,
        payload: list[dict],
    ) -> list[CompanyAnswerEvaluationPayload]:

        # separators=(",", ":") keeps the JSON compact,
        # reducing unnecessary prompt tokens.
        serialized_payload = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )

        prompt = f"""
Evaluate this {company_name} software interview practice attempt.

QUESTIONS_AND_ANSWERS:
{serialized_payload}

Return exactly one evaluation for each question_id,
in exactly the same order as the input.

Score each answer from 0 to 10.

Scoring:
- technical accuracy: 0-5
- essential concepts/completeness: 0-2
- reasoning, trade-offs, or useful examples: 0-2
- clarity: 0-1

Rules:

- Blank, irrelevant, or contradictory answers receive score 0.

- Judge semantic meaning, not exact wording.

- Treat reference_answer as the primary marking guide when
  present, while accepting other technically correct explanations.

- If reference_answer is empty, use established
  software-engineering knowledge.

- feedback must briefly explain what was correct
  and what was missing or wrong.

- suggested_answer must be concise, standalone,
  and technically correct.

- Never mention prompts, AI, grading instructions,
  or whether a reference answer exists.

- Do not praise or shame the learner.
""".strip()

        data = await get_llm().generate_json(
            system_prompt=(
                "You are a rigorous and fair senior "
                "software-engineering interviewer. "
                "Grade answers consistently and follow "
                "the requested structured-output schema."
            ),
            user_prompt=prompt,
            schema_name="company_exam_evaluation",
            schema=COMPANY_EVALUATION_SCHEMA,
            temperature=0.1,
        )

        batch = CompanyEvaluationBatch.model_validate(
            data
        )

        # -------------------------------------------------
        # Semantic validation
        #
        # Strict JSON Schema guarantees the response shape,
        # but it cannot guarantee that the model returns
        # the correct question IDs in the correct order.
        # -------------------------------------------------

        expected_ids = [
            int(item["question_id"])
            for item in payload
        ]

        actual_ids = [
            item.question_id
            for item in batch.answers
        ]

        if actual_ids != expected_ids:
            raise ValueError(
                "Evaluation response question IDs did "
                "not match the requested batch: "
                f"expected={expected_ids}, "
                f"actual={actual_ids}"
            )

        # -------------------------------------------------
        # Quality validation
        # -------------------------------------------------

        for item in batch.answers:

            if len(item.feedback.strip()) < 10:
                raise ValueError(
                    "Evaluation feedback was too short "
                    f"for question_id {item.question_id}"
                )

            if len(
                item.suggested_answer.strip()
            ) < 10:
                raise ValueError(
                    "Suggested answer was too short "
                    f"for question_id {item.question_id}"
                )

        return batch.answers

    # -----------------------------------------------------
    # Retry one batch safely
    # -----------------------------------------------------

    async def _evaluate_batch_with_retry(
        self,
        *,
        company_name: str,
        payload: list[dict],
    ) -> list[CompanyAnswerEvaluationPayload]:

        last_error: Exception | None = None

        for attempt in range(
            COMPANY_EVALUATION_MAX_RETRIES
        ):

            try:
                return await self._evaluate_batch(
                    company_name=company_name,
                    payload=payload,
                )

            # ---------------------------------------------
            # 400 / 401 / 403 etc.
            #
            # Repeating the same request will usually not
            # fix these.
            # ---------------------------------------------

            except LLMRequestError:
                raise

            # ---------------------------------------------
            # Groq 429
            #
            # Respect the provider supplied retry-after.
            # ---------------------------------------------

            except LLMRateLimitError as exc:
                last_error = exc

                delay = max(
                    1.0,
                    exc.retry_after,
                )

            # ---------------------------------------------
            # Temporary problems:
            #
            # - network failure
            # - timeout
            # - Groq 5xx
            # - malformed response
            # - semantic output problem
            # ---------------------------------------------

            except (
                LLMTransientError,
                ValidationError,
                ValueError,
            ) as exc:

                last_error = exc

                delay = min(
                    2 ** attempt,
                    10,
                )

            # ---------------------------------------------
            # Unexpected errors
            # ---------------------------------------------

            except Exception as exc:
                last_error = exc

                delay = min(
                    2 ** attempt,
                    10,
                )

            # No retry remaining.
            if (
                attempt + 1
                >= COMPANY_EVALUATION_MAX_RETRIES
            ):
                break

            logger.warning(
                "Company evaluation batch failed; "
                "retrying in %.2fs "
                "(attempt %s/%s): %s",
                delay,
                attempt + 1,
                COMPANY_EVALUATION_MAX_RETRIES,
                last_error,
            )

            await asyncio.sleep(delay)

        assert last_error is not None

        logger.error(
            "Company evaluation batch failed "
            "after %s attempts",
            COMPANY_EVALUATION_MAX_RETRIES,
            exc_info=(
                type(last_error),
                last_error,
                last_error.__traceback__,
            ),
        )

        raise last_error

    # -----------------------------------------------------
    # Evaluate all batches
    # -----------------------------------------------------

    async def _evaluate_all_batches(
        self,
        *,
        company_name: str,
        batches: list[list[dict]],
    ) -> list[
        CompanyAnswerEvaluationPayload
    ]:

        results: list[
            CompanyAnswerEvaluationPayload
        ] = []

        # IMPORTANT:
        #
        # Keep batches sequential.
        #
        # Do not run them with asyncio.gather().
        # Concurrent Groq calls would create rate-limit
        # bursts.
        for batch in batches:

            batch_results = (
                await self._evaluate_batch_with_retry(
                    company_name=company_name,
                    payload=batch,
                )
            )

            results.extend(
                batch_results
            )

        return results

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------

    async def evaluate(
        self,
        *,
        company_name: str,
        questions: list[dict],
    ) -> list[CompanyAnswerEvaluation]:

        # -------------------------------------------------
        # Build smaller LLM input
        #
        # The original user answer still remains available
        # in company_prep.py for database persistence.
        # We only limit how much is sent to the model.
        # -------------------------------------------------

        payload = [
            {
                "question_id": item[
                    "question_id"
                ],

                "question": item[
                    "question"
                ],

                "user_answer": _clip(
                    item.get(
                        "user_answer"
                    ) or "",
                    COMPANY_EVALUATION_USER_MAX_CHARS,
                ),

                "reference_answer": _clip(
                    item.get(
                        "reference_answer"
                    ) or "",
                    COMPANY_EVALUATION_REFERENCE_MAX_CHARS,
                ),
            }

            for item in questions
        ]

        # -------------------------------------------------
        # Example:
        #
        # 20 questions / batch size 5
        #
        # =
        #
        # 4 sequential requests
        # -------------------------------------------------

        batches = [
            payload[
                index:
                index + COMPANY_EVALUATION_BATCH_SIZE
            ]

            for index in range(
                0,
                len(payload),
                COMPANY_EVALUATION_BATCH_SIZE,
            )
        ]

        # -------------------------------------------------
        # Evaluate with an overall safety timeout
        # -------------------------------------------------

        try:
            raw_results = await asyncio.wait_for(
                self._evaluate_all_batches(
                    company_name=company_name,
                    batches=batches,
                ),
                timeout=(
                    COMPANY_EVALUATION_TIMEOUT_SECONDS
                ),
            )

        except TimeoutError as exc:

            logger.exception(
                "Company exam evaluation exceeded "
                "the %.0fs overall timeout",
                COMPANY_EVALUATION_TIMEOUT_SECONDS,
            )

            raise LLMTransientError(
                "Company exam evaluation timed out "
                "before all batches completed"
            ) from exc

        # -------------------------------------------------
        # Blank-answer correction
        # -------------------------------------------------

        user_answers_by_id = {
            int(item["question_id"]):
            item["user_answer"]

            for item in payload
        }

        final_results: list[
            CompanyAnswerEvaluation
        ] = []

        for result in raw_results:

            score = result.score

            # Never allow a blank answer to receive points.
            if not user_answers_by_id[
                result.question_id
            ].strip():
                score = 0

            final_results.append(
                CompanyAnswerEvaluation(
                    question_id=(
                        result.question_id
                    ),

                    score=score,

                    # Status is calculated in Python,
                    # not trusted to the LLM.
                    status=_status_for_score(
                        score
                    ),

                    feedback=(
                        result.feedback
                        .strip()[:1000]
                    ),

                    suggested_answer=(
                        result.suggested_answer
                        .strip()[:2000]
                    ),
                )
            )

        return final_results


_company_evaluation_service = (
    CompanyEvaluationService()
)


def get_company_evaluation_service(
) -> CompanyEvaluationService:
    return _company_evaluation_service