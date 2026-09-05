"""RAG-grounded DSA roadmap generation and revision."""

import asyncio
import json
import logging
import os
import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.core.llm_config import (
    LLMRateLimitError,
    LLMRequestError,
    LLMTransientError,
    get_llm,
)
from app.services.curriculum_registry import CURRICULA, TopicSpec, canonical_subject, subject_slug
from app.services.rag_service import get_rag_service

logger = logging.getLogger(__name__)

ROADMAP_GENERATION_MAX_RETRIES = max(
    1, int(os.getenv("ROADMAP_GENERATION_MAX_RETRIES", "3"))
)


class GeneratedTopic(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=3, max_length=160)
    days: int = Field(ge=1, le=70)
    description: str = Field(min_length=10, max_length=700)


class GeneratedPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=3, max_length=200)
    topics: list[GeneratedTopic] = Field(min_length=4, max_length=20)


PLAN_SCHEMA = GeneratedPlan.model_json_schema()


class GeneratedMixedTopic(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject: str
    title: str = Field(min_length=3, max_length=160)
    days: int = Field(ge=1, le=70)
    description: str = Field(min_length=10, max_length=700)


class GeneratedMixedPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=3, max_length=200)
    topics: list[GeneratedMixedTopic] = Field(min_length=1, max_length=30)


MIXED_PLAN_SCHEMA = GeneratedMixedPlan.model_json_schema()

JOB_SUBJECT_PATTERNS = {
    "Data Structures & Algorithms": (r"\bdsa\b", r"\bdata structures?(?:\s+(?:and|&))?\s+algorithms?\b"),
    "Object-Oriented Programming": (r"\boop\b", r"\bobject[ -]oriented programming\b"),
    "DBMS": (r"\bdbms\b", r"\bdatabase management systems?\b"),
    "Operating Systems": (r"\boperating systems?\b", r"\bos\b"),
    "Computer Networks": (r"\bcomputer networks?\b", r"\bnetworking fundamentals?\b", r"\bcn\b"),
    "System Design": (r"\bsystem design\b",),
    "Frontend Development": (r"\bfront[ -]?end(?: development)?\b",),
    "Backend Development": (r"\bback[ -]?end(?: development)?\b",),
    "Machine Learning": (r"\bmachine learning\b", r"\bml concepts?\b"),
    "DevOps": (r"\bdevops\b",),
    "Git & GitHub": (r"\bgithub\b", r"\bgit(?: version control)?\b"),
    "Software Testing & QA": (r"\bsoftware testing\b", r"\bquality assurance\b", r"\bqa testing\b"),
}

RESOURCE_CATALOG = {
    "complexity": (
        "Big-O Cheat Sheet", "https://www.bigocheatsheet.com/",
        "Abdul Bari: Asymptotic Notations", "https://www.youtube.com/watch?v=9TlHvipP5yA",
    ),
    "arrays": (
        "Array Data Structure Guide", "https://www.geeksforgeeks.org/array-data-structure-guide/",
        "mycodeschool: Introduction to Arrays", "https://www.youtube.com/watch?v=0r1SfRoLuzU",
    ),
    "strings": (
        "String Data Structure", "https://www.geeksforgeeks.org/string-data-structure/",
        "CS Dojo: Strings", "https://www.youtube.com/watch?v=Wdjr6uoZ0e0",
    ),
    "hashing": (
        "Hashing Data Structure", "https://www.geeksforgeeks.org/hashing-data-structure/",
        "CS Dojo: Hash Tables", "https://www.youtube.com/watch?v=shs0KM3wKv8",
    ),
    "two pointers": (
        "Two Pointers Technique", "https://www.geeksforgeeks.org/two-pointers-technique/",
        "NeetCode: Two Pointers", "https://www.youtube.com/watch?v=On03HWe2tZM",
    ),
    "sliding window": (
        "Sliding Window Technique", "https://www.geeksforgeeks.org/window-sliding-technique/",
        "NeetCode: Sliding Window", "https://www.youtube.com/watch?v=MK-NZ4hN7rs",
    ),
    "prefix sums": (
        "Prefix Sum Array", "https://www.geeksforgeeks.org/prefix-sum-array-implementation-applications-competitive-programming/",
        "Khan Academy: Prefix Sums", "https://www.youtube.com/watch?v=yuws7YK0Yng",
    ),
    "linked": (
        "Linked List Guide", "https://www.geeksforgeeks.org/linked-list-data-structure/",
        "William Fiset: Linked Lists", "https://www.youtube.com/watch?v=njTh_OwMljA",
    ),
    "stack": (
        "Stack Data Structure", "https://www.geeksforgeeks.org/stack-data-structure/",
        "William Fiset: Stack Introduction", "https://www.youtube.com/watch?v=L3ud3rXpIxA",
    ),
    "queues": (
        "Queue Data Structure", "https://www.geeksforgeeks.org/queue-data-structure/",
        "William Fiset: Queue Introduction", "https://www.youtube.com/watch?v=KxzhEQ-zpDc",
    ),
    "tree": (
        "Tree Data Structure Guide", "https://www.geeksforgeeks.org/tree-data-structure/",
        "William Fiset: Tree Algorithms", "https://www.youtube.com/watch?v=1-l_UOFi1Xw",
    ),
    "tries": (
        "Trie Data Structure", "https://www.geeksforgeeks.org/trie-insert-and-search/",
        "Tushar Roy: Trie", "https://www.youtube.com/watch?v=AXjmTQ8LEoI",
    ),
    "heap": (
        "Heap Data Structure", "https://www.geeksforgeeks.org/heap-data-structure/",
        "Abdul Bari: Heap", "https://www.youtube.com/watch?v=HqPJF2L5h9U",
    ),
    "graph": (
        "Graph Data Structure Guide", "https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/",
        "freeCodeCamp: Graph Algorithms", "https://www.youtube.com/watch?v=tWVWeAqZ0WU",
    ),
    "dynamic": (
        "Dynamic Programming Guide", "https://www.geeksforgeeks.org/dynamic-programming/",
        "freeCodeCamp: Dynamic Programming", "https://www.youtube.com/watch?v=oBt53YbR9Kk",
    ),
    "sorting": (
        "Sorting Algorithms", "https://www.geeksforgeeks.org/sorting-algorithms/",
        "Abdul Bari: Sorting Algorithms", "https://www.youtube.com/watch?v=pkkFqlG0Hds",
    ),
    "binary search": (
        "Binary Search", "https://www.geeksforgeeks.org/binary-search/",
        "Abdul Bari: Binary Search", "https://www.youtube.com/watch?v=C2apEw9pgtw",
    ),
    "recursion": (
        "Recursion", "https://www.geeksforgeeks.org/recursion/",
        "Abdul Bari: Recursion", "https://www.youtube.com/watch?v=kepBmgvWNDw",
    ),
    "backtracking": (
        "Backtracking Algorithms", "https://www.geeksforgeeks.org/backtracking-algorithms/",
        "William Fiset: Backtracking", "https://www.youtube.com/watch?v=DKCbsiDBN6c",
    ),
    "greedy": (
        "Greedy Algorithms", "https://www.geeksforgeeks.org/greedy-algorithms/",
        "Abdul Bari: Greedy Method", "https://www.youtube.com/watch?v=ARvQcqJ_-NY",
    ),
}

CURRICULUM = [
    ("Time & Space Complexity", "complexity", "Analyze Big-O time and auxiliary-space costs, including best, average, worst, and amortized cases."),
    ("Arrays", "arrays", "Implement traversal, insertion, deletion, in-place updates, and common subarray patterns."),
    ("Strings", "strings", "Practise character counting, palindrome checks, substring operations, and immutable-string trade-offs."),
    ("Hashing", "hashing", "Use hash maps and sets for counting, lookup, deduplication, and index tracking."),
    ("Two Pointers", "two pointers", "Apply converging, same-direction, and fast-slow pointers while maintaining clear invariants."),
    ("Sliding Window", "sliding window", "Solve fixed and variable window problems using incremental state and frequency maps."),
    ("Prefix Sums", "prefix sums", "Build prefix and difference arrays for range queries and subarray-sum transformations."),
    ("Linked Lists", "linked", "Implement traversal, reversal, insertion, deletion, merging, and fast-slow pointer techniques."),
    ("Stacks", "stack", "Implement stacks and apply them to parsing, monotonic-stack, and next-greater-element problems."),
    ("Queues & Deques", "queues", "Implement queues and deques and use them in buffering, BFS, and monotonic-window problems."),
    ("Sorting", "sorting", "Compare elementary and efficient sorts by complexity, stability, and in-place behavior."),
    ("Binary Search", "binary search", "Master exact lookup, boundaries, rotated arrays, and binary search on a monotonic answer."),
    ("Recursion", "recursion", "Define base cases, trace call stacks, form recurrences, and reason about recursive complexity."),
    ("Backtracking", "backtracking", "Generate subsets, permutations, and constraint solutions using choose-explore-unchoose."),
    ("Trees & BSTs", "tree", "Practise traversals, depth and path problems, BST invariants, insertion, search, and deletion."),
    ("Heaps", "heap", "Use priority queues for top-k, streaming, scheduling, and merge problems."),
    ("Tries", "tries", "Implement prefix insertion and search, then apply tries to autocomplete and word lookup."),
    ("Graphs", "graph", "Cover representations, BFS, DFS, topological ordering, union-find, shortest paths, and MSTs."),
    ("Greedy Algorithms", "greedy", "Recognize greedy-choice structure and justify interval, scheduling, and selection decisions."),
    ("Dynamic Programming", "dynamic", "Build memoized and tabulated solutions from states, transitions, and base cases."),
]

CURRICULA["Data Structures & Algorithms"] = [
    TopicSpec(title, description, RESOURCE_CATALOG[key][1], 1)
    for title, key, description in CURRICULUM
]


class RoadmapGenerationService:
    def __init__(self) -> None:
        self.rag = get_rag_service()

    async def _generate_json_with_retry(self, **kwargs: Any) -> dict[str, Any]:
        """Retry temporary provider failures before using a curated fallback."""
        last_error: Exception | None = None
        for attempt in range(ROADMAP_GENERATION_MAX_RETRIES):
            try:
                return await get_llm().generate_json(**kwargs)
            except LLMRequestError:
                raise
            except LLMRateLimitError as exc:
                last_error = exc
                delay = max(2.0, exc.retry_after + 1.0)
            except LLMTransientError as exc:
                last_error = exc
                delay = min(2 ** attempt, 10)

            if attempt + 1 >= ROADMAP_GENERATION_MAX_RETRIES:
                break
            logger.warning(
                "Roadmap AI request failed; retrying in %.2fs "
                "(attempt %s/%s): %s",
                delay,
                attempt + 1,
                ROADMAP_GENERATION_MAX_RETRIES,
                last_error,
            )
            await asyncio.sleep(delay)

        assert last_error is not None
        raise last_error

    async def generate_roadmap(self, subject: str, timeline_weeks: int) -> dict[str, Any]:
        subject = self._validate_request(subject, timeline_weeks)
        curriculum = CURRICULA[subject]
        total_days = timeline_weeks * 7
        required_topics = ", ".join(topic.title for topic in curriculum)
        prompt = f"""Create a {timeline_weeks}-week ({total_days}-day) {subject} interview roadmap.
Use only concepts supported by the corpus below. Produce exactly these {len(curriculum)} focused topics,
with these exact titles and in this order: {required_topics}.
The sum of every `days` value MUST equal {total_days}. Order prerequisites before advanced topics.
Descriptions must name the concepts and practice patterns to cover. Do not include URLs.

CURATED CORPUS:
{self.rag.roadmap_context(subject, subject_slug(subject))}"""
        try:
            data = await self._generate_json_with_retry(
                system_prompt=(
                    "You are a rigorous computer-science curriculum designer. Return a practical, "
                    "progressive plan grounded exclusively in the supplied corpus."
                ),
                user_prompt=prompt,
                schema_name="subject_roadmap",
                schema=PLAN_SCHEMA,
            )
            plan = GeneratedPlan.model_validate(
                self._prepare_plan_data(data, curriculum)
            )
            self._align_focused_topics(plan, curriculum)
            generation_source = "gemini-rag"
        except (ValidationError, ValueError, KeyError, OSError) as exc:
            logger.warning("Roadmap generation fell back to curated plan: %s", exc)
            plan = self._fallback_plan(subject, timeline_weeks)
            generation_source = "fallback"
        except Exception as exc:  # network/API errors should not make the product unusable
            logger.warning("LLM request failed; using curated plan: %s", exc)
            plan = self._fallback_plan(subject, timeline_weeks)
            generation_source = "fallback"
        result = self._format_plan(plan, total_days, curriculum)
        result["generation_source"] = generation_source
        return result

    @staticmethod
    def detect_job_subjects(text: str) -> list[str]:
        """Return canonical subjects mentioned explicitly in a job description."""
        normalized = " ".join(text.casefold().split())
        return [
            subject
            for subject, patterns in JOB_SUBJECT_PATTERNS.items()
            if any(re.search(pattern, normalized, re.IGNORECASE) for pattern in patterns)
        ]

    async def generate_job_roadmap(
        self, subjects: list[str], timeline_weeks: int
    ) -> dict[str, Any]:
        if timeline_weeks not in {6, 8, 10, 12}:
            raise ValueError("Job roadmap timeline must be 6, 8, 10, or 12 weeks")
        if not subjects:
            raise ValueError("No CS fundamentals were found in job description")

        canonical_subjects = list(dict.fromkeys(canonical_subject(item) for item in subjects))
        allowed = {
            subject: [topic.title for topic in CURRICULA[subject]]
            for subject in canonical_subjects
        }
        corpus = "\n\n".join(
            f"## {subject}\n{self.rag.roadmap_context(subject, subject_slug(subject))}"
            for subject in canonical_subjects
        )
        total_days = timeline_weeks * 7
        prompt = f"""Create a mixed {timeline_weeks}-week ({total_days}-day) interview roadmap for
these job-description subjects: {', '.join(canonical_subjects)}.
Select only the most important focused topics from each detected subject, using only the exact
topic titles in this allow-list: {json.dumps(allowed)}.
Include at least one topic from every detected subject, never duplicate a topic, and return at
most 30 topic cards total. The sum of `days` must equal {total_days}. Put prerequisites first.
Each topic object must include its exact canonical `subject` and `title`. Do not include URLs.

CURATED RAG CORPUS:
{corpus}"""
        try:
            data = await self._generate_json_with_retry(
                system_prompt=(
                    "You are a rigorous CS interview curriculum designer. Select the highest-value "
                    "topics across multiple detected subjects and obey the allow-list exactly."
                ),
                user_prompt=prompt,
                schema_name="job_description_roadmap",
                schema=MIXED_PLAN_SCHEMA,
            )
            plan = GeneratedMixedPlan.model_validate(data)
            self._validate_mixed_plan(plan, allowed)
            generation_source = "gemini-rag"
        except Exception as exc:
            logger.warning("Mixed roadmap generation fell back to curated plan: %s", exc)
            plan = self._fallback_mixed_plan(canonical_subjects, timeline_weeks)
            generation_source = "fallback"

        topics = [topic.model_dump() for topic in plan.topics]
        self._normalize_days(topics, total_days)
        current_day = 1
        formatted = []
        for topic in topics:
            end_day = current_day + topic["days"] - 1
            curriculum = CURRICULA[topic["subject"]]
            formatted.append({
                "subject": topic["subject"],
                "title": topic["title"],
                "start_day": current_day,
                "end_day": end_day,
                "description": topic["description"],
                "resources": self._resources_for(topic["title"], curriculum),
            })
            current_day = end_day + 1
        return {
            "title": plan.title,
            "topics": formatted,
            "generation_source": generation_source,
            "subjects": canonical_subjects,
        }

    @staticmethod
    def _validate_mixed_plan(plan: GeneratedMixedPlan, allowed: dict[str, list[str]]) -> None:
        seen: set[tuple[str, str]] = set()
        covered: set[str] = set()
        for topic in plan.topics:
            if topic.subject not in allowed or topic.title not in allowed[topic.subject]:
                raise ValueError(f"Unsupported mixed roadmap topic: {topic.subject} / {topic.title}")
            key = (topic.subject, topic.title)
            if key in seen:
                raise ValueError(f"Duplicate mixed roadmap topic: {topic.title}")
            seen.add(key)
            covered.add(topic.subject)
        if covered != set(allowed):
            raise ValueError("The mixed roadmap did not cover every detected subject")

    @staticmethod
    def _fallback_mixed_plan(subjects: list[str], weeks: int) -> GeneratedMixedPlan:
        # Round-robin keeps all detected subjects represented while respecting the hard cap.
        selected: list[GeneratedMixedTopic] = []
        indexes = {subject: 0 for subject in subjects}
        while len(selected) < 30:
            added = False
            for subject in subjects:
                curriculum = CURRICULA[subject]
                index = indexes[subject]
                if index < len(curriculum) and len(selected) < 30:
                    item = curriculum[index]
                    selected.append(GeneratedMixedTopic(
                        subject=subject, title=item.title, days=item.weight,
                        description=item.description,
                    ))
                    indexes[subject] += 1
                    added = True
            if not added:
                break
        return GeneratedMixedPlan(
            title=f"Job-Focused CS Fundamentals Roadmap - {weeks} Weeks",
            topics=selected,
        )

    async def suggest_edit(
        self, roadmap: dict[str, Any], suggestion: str, timeline_weeks: int, subject: str
    ) -> dict[str, Any]:
        if not suggestion.strip():
            raise ValueError("Suggestion cannot be empty")
        subject = canonical_subject(subject)
        curriculum = CURRICULA[subject]
        total_days = timeline_weeks * 7
        prompt = f"""Revise the {subject} roadmap in response to the user's request.
Keep the total exactly {total_days} days, with contiguous coverage and no more than 20 topics.
Every card must cover one focused curriculum topic; never create mixed-practice or review cards.
Do not combine unrelated topics, add concepts outside {subject}, or include URLs. Preserve prerequisite order.

CURRENT ROADMAP:
{json.dumps(roadmap, indent=2)}

USER REQUEST:
{suggestion}

CORPUS EXCERPTS:
{self.rag.roadmap_context(subject, subject_slug(subject), suggestion)}"""
        try:
            data = await self._generate_json_with_retry(
                system_prompt="You revise structured interview curricula while preserving constraints.",
                user_prompt=prompt,
                schema_name="revised_subject_roadmap",
                schema=PLAN_SCHEMA,
            )
            plan = GeneratedPlan.model_validate(
                self._prepare_plan_data(data, curriculum)
            )
            self._align_focused_topics(plan, curriculum)
            result = self._format_plan(plan, total_days, curriculum)
            result["generation_source"] = "gemini-rag"
            return result
        except Exception as exc:
            logger.warning("Roadmap revision failed: %s", exc)
            raise RuntimeError("The AI could not revise the roadmap. Please try again.") from exc

    @staticmethod
    def _validate_request(subject: str, weeks: int) -> str:
        canonical = canonical_subject(subject)
        if weeks not in {4, 6, 8, 10}:
            raise ValueError("Timeline must be 4, 6, 8, or 10 weeks")
        return canonical

    def _format_plan(
        self, plan: GeneratedPlan, total_days: int, curriculum: list[TopicSpec]
    ) -> dict[str, Any]:
        topics = [topic.model_dump() for topic in plan.topics]
        self._normalize_days(topics, total_days)
        current_day = 1
        formatted = []
        for topic in topics:
            end_day = current_day + topic["days"] - 1
            formatted.append({
                "title": topic["title"],
                "start_day": current_day,
                "end_day": end_day,
                "description": topic["description"],
                "resources": self._resources_for(topic["title"], curriculum),
            })
            current_day = end_day + 1
        return {"title": plan.title, "topics": formatted}

    @staticmethod
    def _normalize_days(topics: list[dict[str, Any]], total_days: int) -> None:
        raw_total = sum(topic["days"] for topic in topics)
        scaled = [max(1, round(topic["days"] * total_days / raw_total)) for topic in topics]
        difference = total_days - sum(scaled)
        cursor = 0
        while difference:
            index = cursor % len(scaled)
            if difference > 0:
                scaled[index] += 1
                difference -= 1
            elif scaled[index] > 1:
                scaled[index] -= 1
                difference += 1
            cursor += 1
        for topic, days in zip(topics, scaled):
            topic["days"] = days

    @staticmethod
    def _resources_for(title: str, curriculum: list[TopicSpec]) -> list[dict[str, str]]:
        spec = next((item for item in curriculum if item.title == title), None)
        if spec and title not in {item[0] for item in CURRICULUM}:
            return spec.resources()
        lowered = title.lower()
        key = next(
            (resource_key for topic_title, resource_key, _ in CURRICULUM if topic_title.lower() == lowered),
            None,
        ) or next((item for item in RESOURCE_CATALOG if item in lowered), "complexity")
        blog_title, blog_url, video_title, video_url = RESOURCE_CATALOG[key]
        return [
            {"title": blog_title, "url": blog_url, "type": "Blog"},
            {"title": video_title, "url": video_url, "type": "YouTube"},
        ]

    @staticmethod
    def _fallback_plan(subject: str, weeks: int) -> GeneratedPlan:
        units = CURRICULA[subject]
        return GeneratedPlan(
            title=f"{subject} Interview Preparation — {weeks} Weeks",
            topics=[
                GeneratedTopic(title=item.title, days=item.weight, description=item.description)
                for item in units
            ],
        )

    @staticmethod
    def _prepare_plan_data(
        data: dict[str, Any], curriculum: list[TopicSpec]
    ) -> dict[str, Any]:
        """Repair common model formatting drift before strict validation."""
        prepared = dict(data)
        raw_topics = prepared.get("topics")
        if not isinstance(raw_topics, list):
            return prepared

        topics: list[Any] = []
        for raw_topic in raw_topics[:len(curriculum)]:
            if not isinstance(raw_topic, dict):
                topics.append(raw_topic)
                continue
            topic = dict(raw_topic)
            days = topic.get("days")
            try:
                if float(days) < 1:
                    topic["days"] = 1
            except (TypeError, ValueError):
                pass
            topics.append(topic)
        prepared["topics"] = topics
        return prepared

    @staticmethod
    def _align_focused_topics(plan: GeneratedPlan, curriculum: list[TopicSpec]) -> None:
        """Keep AI-authored durations/descriptions while enforcing canonical card titles.

        Models occasionally paraphrase a requested title despite preserving its position
        and content. Rejecting that otherwise useful plan caused unnecessary fallbacks.
        """
        if len(plan.topics) != len(curriculum):
            raise ValueError(
                f"The generated roadmap returned {len(plan.topics)} topics; "
                f"expected {len(curriculum)}"
            )
        for generated, required in zip(plan.topics, curriculum):
            generated.title = required.title


def get_roadmap_service() -> RoadmapGenerationService:
    return RoadmapGenerationService()
