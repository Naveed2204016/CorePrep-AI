"""RAG-grounded assessment generation and batched answer evaluation."""

import asyncio
import json
import logging
import os
import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.llm_config import get_llm
from app.services.curriculum_registry import canonical_subject, subject_slug
from app.services.rag_service import get_rag_service


class GeneratedMCQ(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=10, max_length=700)
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str = Field(min_length=1, max_length=500)
    revision_area: str = Field(min_length=2, max_length=160)

    @model_validator(mode="after")
    def correct_answer_is_an_option(self) -> "GeneratedMCQ":
        if self.correct_answer not in self.options:
            raise ValueError("correct_answer must exactly match one option")
        return self


class GeneratedShortQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=10, max_length=700)
    reference_answer: str = Field(min_length=10, max_length=1200)
    revision_area: str = Field(min_length=2, max_length=160)


class GeneratedAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mcq: list[GeneratedMCQ] = Field(max_length=10)
    short: list[GeneratedShortQuestion] = Field(max_length=10)


class EvaluatedAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question_id: int
    is_correct: bool
    marks: float = Field(ge=0, le=1)
    explanation: str = Field(min_length=10, max_length=700)
    revision_area: str = Field(min_length=2, max_length=160)


class EvaluationBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    answers: list[EvaluatedAnswer]


ASSESSMENT_SCHEMA = GeneratedAssessment.model_json_schema()
EVALUATION_SCHEMA = EvaluationBatch.model_json_schema()
EVALUATION_TIMEOUT_SECONDS = float(
    os.getenv("ASSESSMENT_EVALUATION_TIMEOUT_SECONDS", "170")
)
logger = logging.getLogger(__name__)


class AssessmentService:
    def __init__(self) -> None:
        self.rag = get_rag_service()

    def _context(self, subject: str, topic: str) -> str:
        subject = canonical_subject(subject)
        chunks = self.rag.retrieve(
            f"{topic}: definitions, mechanisms, trade-offs, examples, and interview misconceptions",
            subject_slug(subject),
            limit=5,
        )
        if not chunks:
            raise RuntimeError(f"No RAG context found for {subject}: {topic}")
        return "\n\n".join(
            f"SOURCE: {chunk.source} — {chunk.heading}\n{chunk.text}"
            for chunk in chunks
        )

    async def generate_questions(
        self, *, topic: str, subject: str, num_mcq: int, num_short: int
    ) -> GeneratedAssessment:
        context = self._context(subject, topic)
        prompt = f"""Create an assessment for the focused topic `{topic}` in `{subject}`.

RAG CORPUS:
{context}

Requirements:
- Return exactly {num_mcq} MCQs and exactly {num_short} short-answer questions.
- Use only facts supported by the RAG corpus above.
- Write every question as a standalone technical question. Never use phrases such as
  "according to the corpus", "according to the curriculum", "based on the context",
  "from the passage", "from the material above", or otherwise reveal that retrieval was used.
- Test conceptual understanding, mechanisms, trade-offs, and application—not trivia.
- Keep every question strictly within `{topic}`; do not test other roadmap cards.
- Make questions distinct and range from foundational to interview-level intermediate difficulty.
- Every MCQ must have exactly four plausible, non-overlapping options and one unambiguous answer.
- `correct_answer` must copy the full correct option text exactly.
- Short questions need a concise reference answer containing the concepts required for full credit.
- `revision_area` must be a short subtopic from the corpus, not the whole question.
- Do not mention the corpus or reveal answers inside question text."""
        data = await get_llm().generate_json(
            system_prompt=(
                "You are a rigorous technical interviewer and assessment author. "
                "Return accurate, fair, schema-conformant questions grounded only in supplied material."
            ),
            user_prompt=prompt,
            schema_name="rag_assessment",
            schema=ASSESSMENT_SCHEMA,
            temperature=0.25,
        )
        assessment = GeneratedAssessment.model_validate(
            self._prepare_assessment_data(data, num_mcq, num_short)
        )
        if len(assessment.mcq) != num_mcq or len(assessment.short) != num_short:
            raise ValueError(
                f"LLM returned {len(assessment.mcq)} MCQ and {len(assessment.short)} short; "
                f"expected {num_mcq} and {num_short}"
            )
        return assessment

    @staticmethod
    def _prepare_assessment_data(
        data: dict[str, Any], num_mcq: int, num_short: int
    ) -> dict[str, Any]:
        """Repair common model drift without changing question content."""
        prepared = dict(data)
        raw_mcq = prepared.get("mcq", [])
        raw_short = prepared.get("short", [])
        mcq_items: list[Any] = []
        if isinstance(raw_mcq, list):
            for raw in raw_mcq[:num_mcq]:
                if not isinstance(raw, dict):
                    mcq_items.append(raw)
                    continue
                item = dict(raw)
                if "correct_answer" not in item and "correct" in item:
                    item["correct_answer"] = str(item["correct"])
                options = item.get("options")
                if isinstance(options, dict):
                    ordered_keys = [key for key in ("A", "B", "C", "D") if key in options]
                    item["options"] = [str(options[key]) for key in ordered_keys]
                    correct = str(item.get("correct_answer", item.get("correct", ""))).strip().upper()
                    if correct in options:
                        item["correct_answer"] = str(options[correct])
                elif isinstance(options, list):
                    correct = str(item.get("correct_answer", item.get("correct", ""))).strip()
                    if correct.upper() in {"A", "B", "C", "D"}:
                        index = ord(correct.upper()) - ord("A")
                        if index < len(options):
                            item["correct_answer"] = str(options[index])
                item.pop("correct", None)
                item["question"] = AssessmentService._clean_question_text(
                    str(item.get("question", ""))
                )
                mcq_items.append(item)
        prepared["mcq"] = mcq_items
        if isinstance(raw_short, list):
            short_items = []
            for raw in raw_short[:num_short]:
                if isinstance(raw, dict):
                    item = dict(raw)
                    item["question"] = AssessmentService._clean_question_text(
                        str(item.get("question", ""))
                    )
                    short_items.append(item)
                else:
                    short_items.append(raw)
            prepared["short"] = short_items
        else:
            prepared["short"] = raw_short
        return prepared

    @staticmethod
    def _clean_question_text(question: str) -> str:
        """Remove retrieval/curriculum framing while retaining question content."""
        cleaned = re.sub(
            r"^\s*(?:according to|based on|from)\s+(?:(?:the\s+)?(?:provided\s+|given\s+)?"
            r"(?:rag\s+)?(?:corpus|curriculum|context|passage|material|information)|these(?:\s+materials?)?)"
            r"(?:\s+above)?\s*[,;:]?\s*",
            "",
            question,
            flags=re.IGNORECASE,
        )
        if cleaned and cleaned[0].islower():
            cleaned = cleaned[0].upper() + cleaned[1:]
        return cleaned

    async def evaluate_answers(
        self,
        *,
        topic: str,
        subject: str,
        questions: list[dict[str, Any]],
    ) -> tuple[list[EvaluatedAnswer], str]:
        try:
            context = self._context(subject, topic)
        except Exception as exc:
            logger.warning(
                "Assessment evaluation RAG retrieval failed; using deterministic fallback: %s",
                exc,
            )
            return self._fallback_evaluation(topic, questions), "fallback"
        prompt = f"""Evaluate all answers for the `{topic}` assessment in one batch.

RAG CORPUS:
{context}

QUESTIONS AND RESPONSES:
{json.dumps(questions, ensure_ascii=False)}

Evaluation rules:
- Return one evaluation for every question_id, in the supplied order.
- For MCQs, the server determines correctness by comparing the selected option with
  correct_answer. Explain the correct concept without changing that determination.
- For short answers, compare meaning against reference_answer and the corpus.
- Treat a short answer as correct when its semantic meaning covers at least 50% of the
  essential reference concepts, even when wording and examples differ.
- Give marks from 0.5 to 1 for answers meeting that threshold. Use marks below 0.5 and
  is_correct=false only when fewer than half of the essential concepts are covered.
- A blank, completely irrelevant, or contradictory answer receives 0 and is incorrect.
- Set is_correct=true exactly when marks >= 0.5.
- Give a concise 1-3 sentence explanation grounded in the corpus for every answer.
- Explain the correct concept even when the user's answer is blank or wrong.
- revision_area must name the most relevant corpus subtopic; use `{topic}` only when no narrower label applies.
- Explanations must be standalone: never mention the corpus, curriculum, context,
  reference material, grading prompt, or that an LLM performed the evaluation.
- Do not praise or shame the learner."""

        async def request_evaluation() -> EvaluationBatch:
            data = await get_llm().generate_json(
                system_prompt=(
                    "You are a fair technical examiner. Grade consistently and explain results "
                    "using only the supplied reference answers and RAG corpus."
                ),
                user_prompt=prompt,
                schema_name="rag_assessment_evaluation",
                schema=EVALUATION_SCHEMA,
                temperature=0.1,
            )
            return EvaluationBatch.model_validate(data)

        try:
            batch = await asyncio.wait_for(
                request_evaluation(), timeout=EVALUATION_TIMEOUT_SECONDS
            )
            by_id = {item.question_id: item for item in batch.answers}
            if set(by_id) != {int(question["question_id"]) for question in questions}:
                raise ValueError("Evaluation did not return every submitted question")
            ordered = [by_id[int(question["question_id"])] for question in questions]
            for evaluation, question in zip(ordered, questions):
                if question.get("question_type") == "mcq":
                    selected = AssessmentService._normalize_answer(
                        str(question.get("user_answer", ""))
                    )
                    correct = AssessmentService._normalize_answer(
                        str(question.get("correct_answer", ""))
                    )
                    evaluation.is_correct = bool(selected) and selected == correct
                    evaluation.marks = 1.0 if evaluation.is_correct else 0.0
                    prefix = (
                        "Your selected option matches the correct answer. "
                        if evaluation.is_correct
                        else "Your selected option does not match the correct answer. "
                    )
                    evaluation.explanation = prefix + evaluation.explanation
                else:
                    evaluation.is_correct = evaluation.marks >= 0.5
            return ordered, "groq-rag"
        except Exception as exc:
            logger.warning("Assessment evaluation used deterministic fallback: %s", exc)
            return self._fallback_evaluation(topic, questions), "fallback"

    @staticmethod
    def _normalize_answer(value: str) -> str:
        return " ".join(value.casefold().split())

    @staticmethod
    def _fallback_evaluation(
        topic: str, questions: list[dict[str, Any]]
    ) -> list[EvaluatedAnswer]:
        evaluations: list[EvaluatedAnswer] = []
        for question in questions:
            user = str(question.get("user_answer", "")).strip()
            reference = str(question.get("correct_answer", "")).strip()
            if question.get("question_type") == "mcq":
                marks = 1.0 if user == reference else 0.0
            else:
                reference_words = {word.lower().strip(".,:;()") for word in reference.split() if len(word) > 3}
                user_words = {word.lower().strip(".,:;()") for word in user.split() if len(word) > 3}
                overlap = len(reference_words & user_words) / max(1, len(reference_words))
                marks = round(overlap, 2) if user else 0.0
            evaluations.append(EvaluatedAnswer(
                question_id=int(question["question_id"]),
                is_correct=marks >= 0.5,
                marks=marks,
                explanation=(
                    f"The reference concept is: {reference}" if reference
                    else f"Review the core mechanisms and trade-offs of {topic}."
                ),
                revision_area=topic,
            ))
        return evaluations


def get_assessment_service() -> AssessmentService:
    return AssessmentService()
