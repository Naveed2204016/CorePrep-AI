import asyncio
import hashlib
import html
import os
import random
import re
import time
from dataclasses import dataclass
import httpx


REPOSITORY_URL = "https://github.com/TamimEhsan/interview-questions-bangladesh"
DEFAULT_RAW_BASE_URL = (
    "https://raw.githubusercontent.com/TamimEhsan/"
    "interview-questions-bangladesh/master/docs/companies"
)


@dataclass(frozen=True)
class CompanySource:
    name: str
    slug: str
    short_name: str
    paths: tuple[str, ...]


COMPANY_SOURCES = (
    CompanySource("Aastha IT", "aastha-it", "AI", ("aastha.md",)),
    CompanySource("AppifyLab", "appifylab", "AL", ("appifylab.md",)),
    CompanySource("Appscode", "appscode", "AC", ("appscode.md",)),
    CompanySource("bKash", "bkash", "BK", ("bkash.md",)),
    CompanySource("Bevy Commerce", "bevy-commerce", "BC", ("bevycommerce.md",)),
    CompanySource("Brain Station 23", "brain-station-23", "BS", ("bs23.md",)),
    CompanySource("Chaldal", "chaldal", "CH", ("chaldal.md",)),
    CompanySource("DSI", "dsi", "DS", ("dsi.md",)),
    CompanySource("Enosis Solutions", "enosis-solutions", "ES", ("enosis.md",)),
    CompanySource("Envobyte", "envobyte", "EN", ("envobyte.md",)),
    CompanySource("Exabyting", "exabyting", "EX", ("exabyting.md",)),
    CompanySource("Fringecore", "fringecore", "FC", ("fringecore.md",)),
    CompanySource("Inverse AI", "inverse-ai", "IA", ("inverseai.md",)),
    CompanySource("IQVIA", "iqvia", "IQ", ("iqvia.md",)),
    CompanySource("Kite Games Studio", "kite-games-studio", "KG", ("kite.md",)),
    CompanySource("Optimizely", "optimizely", "OP", ("optimizely.md",)),
    CompanySource("Orbitax", "orbitax", "OR", ("orbitax.md",)),
    CompanySource("Pathao", "pathao", "PA", ("pathao.md",)),
    CompanySource("Priyo", "priyo", "PR", ("priyo.md",)),
    CompanySource("Relisource", "relisource", "RL", ("relisource.md",)),
    CompanySource("REVE Systems", "reve-systems", "RE", ("revesystems.md",)),
    CompanySource("RoBenDevs", "robendevs", "RD", ("robendevs.md",)),
    CompanySource("Rokomari", "rokomari", "RO", ("rokomari.md",)),
    CompanySource("Shanghai BDCOM", "shanghai-bdcom", "BD", ("shanghaibdcom.md",)),
    CompanySource("ShellBeeHaken", "shellbeehaken", "SH", ("shellbeehaken.md",)),
    CompanySource("ShopUp", "shopup", "SU", ("shopup.md",)),
    CompanySource("Spectrum", "spectrum", "SP", ("spectrum.md",)),
    CompanySource("SRBD", "srbd", "SR", ("srbd.md",)),
    CompanySource("Synesis IT", "synesis-it", "SI", ("synesis.md",)),
    CompanySource(
        "Therap BD",
        "therap-bd",
        "TH",
        ("therap/swe.md", "therap/dbe.md", "therap/ml.md", "therap/sys.md"),
    ),
    CompanySource("WeDevs", "wedevs", "WD", ("wedevs.md",)),
    CompanySource("WellDev", "welldev", "WL", ("welldev.md",)),
    CompanySource("WSD", "wsd", "WS", ("wsd.md",)),
)
COMPANIES_BY_SLUG = {company.slug: company for company in COMPANY_SOURCES}

SUPPLEMENTAL_QUESTIONS = (
    "Explain the four pillars of object-oriented programming with examples.",
    "What is the difference between an abstract class and an interface?",
    "How does a hash table work, and how are collisions handled?",
    "Compare an array and a linked list, including their common time complexities.",
    "What is the difference between a stack and a queue? Give practical examples.",
    "Explain breadth-first search and depth-first search and when you would use each.",
    "What is dynamic programming, and how do you recognize a problem that can use it?",
    "Explain the difference between a process and a thread.",
    "What is a race condition, and how can it be prevented?",
    "What is deadlock? Describe the conditions required for deadlock to occur.",
    "Explain database normalization and the purpose of the first three normal forms.",
    "What is a database index, and what are its advantages and disadvantages?",
    "Compare SQL and NoSQL databases and describe when you might choose each.",
    "What are database transactions and the ACID properties?",
    "What is the difference between an INNER JOIN and a LEFT JOIN?",
    "Explain HTTP request methods and which of them should be idempotent.",
    "What is the difference between authentication and authorization?",
    "How does DNS translate a domain name into an IP address?",
    "Compare TCP and UDP and give an appropriate use case for each.",
    "What is a REST API, and what makes an API RESTful?",
    "How would you design pagination for an API that contains millions of records?",
    "What is caching, and what cache invalidation problems should developers consider?",
    "Explain horizontal scaling and vertical scaling.",
    "How would you identify and improve a slow API endpoint?",
    "What is dependency injection, and why is it useful?",
    "Explain synchronous and asynchronous programming with examples.",
    "What is the purpose of unit, integration, and end-to-end testing?",
    "What happens from the moment a user enters a URL until the page is displayed?",
    "Describe how you would review a pull request for correctness and maintainability.",
    "Tell me about a difficult technical problem you solved and how you approached it.",
)

# The upstream collection occasionally contains notes rather than standalone
# questions. Keep explicit, reviewable corrections here instead of changing or
# guessing at the community repository content.
QUESTION_REWRITES: dict[str, dict[str, str]] = {
    "aastha-it": {
        "design a basic social media system.": (
            "Design a basic social-media system where users can create profiles, "
            "follow other users, publish posts, like and comment on posts, and view "
            "a paginated home feed. Describe the API, database schema, feed-generation "
            "approach, authentication, and how the design would scale."
        ),
        "solve leetcode easy to medium-level coding problems.": (
            "Given an array of integers and a target value, return the indices of two "
            "distinct elements whose sum equals the target. Describe an O(n) solution, "
            "handle the case where no pair exists, and analyze time and space complexity."
        ),
    },
    "appscode": {
        "given a array of numbers. you have to perform a number of queries. each queries ask for the average of numbers from a range.": (
            "Given an array of N numbers and Q queries, where each query provides "
            "two indices L and R, return the average of all values from index L "
            "through R inclusive. Design an efficient solution for a large number "
            "of queries, explain your preprocessing approach, and analyze its time "
            "and space complexity."
        ),
        "a dynamic programming problem.(similar to 0/1 knapsack)": (
            "You are given N items. The i-th item has weight w[i] and value v[i], "
            "and a bag can carry at most W total weight. Each item may be selected "
            "at most once. Find the maximum total value that can be placed in the "
            "bag. Explain the dynamic-programming state and transitions, and give "
            "the time and space complexity of your solution."
        ),
        "how does trie works. implementation of trie.": (
            "Explain how a trie stores and searches strings. Then design a trie "
            "supporting insert(word), search(word), and startsWith(prefix), and "
            "analyze the time and space complexity of each operation."
        ),
        "what is hashing? how does it work? what is hash collision?": (
            "Explain how hashing and hash tables work. What causes a hash collision, "
            "and how can collisions be handled using separate chaining and open addressing?"
        ),
        "design an api for a music streaming platform like spotify": (
            "Design a REST API for a music-streaming platform where users can search "
            "for songs, play a track, create and update playlists, follow artists, "
            "and view listening history. Define the main resources, endpoints, request "
            "and response structures, authentication approach, pagination, and error handling."
        ),
        "design the schema and write queries like fetching the top 10 songs of the previous month.": (
            "Design a relational database schema for a music-streaming platform that "
            "stores users, artists, albums, songs, playlists, and play events. Then "
            "write an SQL query that returns the ten most-played songs during the "
            "previous calendar month, including each song's title, artist, and play count."
        ),
        "write a regex validator for email.": (
            "Write a regular expression for validating common email-address formats. "
            "Explain what the expression accepts, what it rejects, and why production "
            "systems should still verify an address by sending a confirmation email."
        ),
        "what is the difference between div and span": (
            "Explain the difference between the HTML div and span elements, including "
            "their default display behavior, semantic meaning, and appropriate use cases."
        ),
    },
    "enosis-solutions": {
        "system design question: file management software. @@senior@@": (
            "Design a file-management system where users can upload, download, rename, "
            "move, share, version, and delete files and folders. Explain the APIs, metadata "
            "schema, object storage, permissions, versioning, concurrent updates, and how "
            "the system would scale for large files and many users."
        ),
    },
    "optimizely": {
        "build a tshirt distribution system": (
            "Design a T-shirt distribution system that tracks sizes and inventory, accepts "
            "employee size preferences, assigns one available shirt per employee, and reports "
            "unfulfilled requests. Describe the data model, allocation rules, APIs, and how "
            "concurrent requests should be handled."
        ),
        "task management software reviewer assignment": (
            "Design a reviewer-assignment feature for task-management software. A task may "
            "require multiple reviewers, reviewers have workload limits, and the same person "
            "cannot be both author and reviewer. Define the data model, assignment algorithm, "
            "APIs, validation rules, and handling of concurrent assignments."
        ),
        "design a backend for a simplified version of internet banking": (
            "Design the backend for an internet-banking system that supports account balances, "
            "transaction history, transfers between accounts, and utility-bill payments. "
            "Explain the APIs, database model, authentication, transaction consistency, "
            "idempotency, audit logging, and failure recovery."
        ),
    },
    "shellbeehaken": {
        "a sql query was given to perform with a subquery and a join operation.": (
            "Given Employee(id, name, department_id, salary) and Department(id, name), "
            "write an SQL query using a JOIN and a subquery to return employees whose salary "
            "is greater than the average salary of their own department, together with the "
            "department name."
        ),
        "draw a class diagram of a course management system": (
            "Design a class diagram for a course-management system where instructors create "
            "courses and lessons, students enroll in courses, submit assignments, and receive "
            "grades. Show the main classes, attributes, operations, relationships, and cardinalities."
        ),
    },
    "therap-bd": {
        "solve the problem using object oriented programming": (
            "Using object-oriented programming, design a library system where members can "
            "search for books, borrow and return available copies, and view active loans. "
            "Define the main classes and relationships, then implement the borrow operation "
            "with suitable validation and error handling."
        ),
        "design an erd of online restaurant management system": (
            "Design an ER diagram for an online restaurant-management system supporting "
            "customers, restaurants, menu items, orders, order items, payments, and deliveries. "
            "Identify primary and foreign keys, relationships, and cardinalities."
        ),
    },
    "welldev": {
        "a basic gre-like math question.": (
            "A product's price is increased by 20% and then discounted by 20%. If its original "
            "price was 1,000, calculate the final price and percentage change from the original."
        ),
        "basic recursive implementation problem": (
            "Implement a recursive function that returns the factorial of a non-negative integer "
            "n. Define the base case, handle invalid negative input, and analyze the time and "
            "space complexity."
        ),
        "printing cumulative sum": (
            "Given an array of N integers, produce an array where the value at index i is the "
            "sum of all input values from index 0 through i. Implement the solution and analyze "
            "its time and space complexity."
        ),
        "details on two pointers": (
            "Explain the two-pointer technique and when it is applicable. Then use it to determine "
            "whether a sorted array contains two distinct values whose sum equals a target, and "
            "analyze the solution's complexity."
        ),
    },
}

CONTEXT_DEPENDENT_PATTERNS = (
    "following code", "code above", "given a code", "given code", "some code",
    "code segment", "following code snippet", "following code?", "following code:",
    "graph in figure", "figures of graph", "given some figures", "given a list of",
    "option in a given list", "statements about", "this below operation", "above ticket",
    "follow up question", "problem repository", "questions may be asked", "questions might be asked",
    "questions from the previous rounds", "many questions from my cv", "write the output of",
    "what will be the output", "time complexity of the code", "time complexity of the following",
    "presentations on a ticket", "bfs, dfs, mergesort", "deletion and insertion of circular",
)


class CompanyQuestionSourceError(RuntimeError):
    pass


def _plain_markdown(value: str, *, preserve_code: bool = False) -> str:
    if preserve_code:
        value = re.sub(r"^```[^\n]*\n?|^```\s*$", "", value, flags=re.MULTILINE)
    else:
        value = re.sub(r"```.*?```", "", value, flags=re.DOTALL)
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"!\[([^]]*)]\([^)]*\)", r"\1", value)
    value = re.sub(r"\[([^]]+)]\([^)]*\)", r"\1", value)
    value = re.sub(r"</?[^>]+>", "", value)
    value = re.sub(r"^[ \t]*[-*+]\s+", "- ", value, flags=re.MULTILINE)
    value = re.sub(r"\*\*|__|(?<!\*)\*(?!\*)|(?<!_)_(?!_)", "", value)
    value = html.unescape(value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n\s*\n+", "\n", value)
    return value.strip()


def parse_company_questions(markdown: str, source_path: str) -> list[dict[str, str]]:
    questions: list[dict[str, str]] = []
    headings = list(re.finditer(r"^#{2,3}\s+(.+?)\s*$", markdown, re.MULTILINE))

    for index, match in enumerate(re.finditer(r"<article\b[^>]*>(.*?)</article>", markdown, re.DOTALL | re.IGNORECASE)):
        body = match.group(1)
        details = re.search(r"<details\b[^>]*>(.*?)</details>", body, re.DOTALL | re.IGNORECASE)
        question_body = re.sub(
            r"<details\b[^>]*>.*?</details>", "", body, flags=re.DOTALL | re.IGNORECASE
        )
        question = _plain_markdown(question_body)
        if not question:
            continue

        preceding = [heading.group(1) for heading in headings if heading.start() < match.start()]
        section = _plain_markdown(preceding[-1]) if preceding else "Interview Questions"
        digest = hashlib.sha256(
            f"{source_path}:{index}:{question}".encode("utf-8")
        ).hexdigest()[:16]
        item = {
            "id": digest,
            "question": question,
            "section": section,
            "sourcePath": source_path,
        }
        if details:
            answer = re.sub(r"<summary\b[^>]*>.*?</summary>", "", details.group(1), flags=re.DOTALL | re.IGNORECASE)
            item["answer"] = _plain_markdown(answer, preserve_code=True)
        questions.append(item)
    return questions


def improve_incomplete_questions(
    slug: str, questions: list[dict[str, str]]
) -> list[dict[str, str]]:
    rewrites = QUESTION_REWRITES.get(slug, {})
    improved = []
    for item in questions:
        updated = dict(item)
        normalized = " ".join(item["question"].casefold().split())
        if normalized in rewrites:
            updated["question"] = rewrites[normalized]
        improved.append(updated)
    return improved


def is_context_dependent_question(question: str) -> bool:
    normalized = " ".join(question.casefold().split())
    return any(pattern in normalized for pattern in CONTEXT_DEPENDENT_PATTERNS)


class CompanyPrepService:
    def __init__(self) -> None:
        self.raw_base_url = os.getenv(
            "COMPANY_QUESTIONS_RAW_BASE_URL", DEFAULT_RAW_BASE_URL
        ).rstrip("/")
        self.timeout = float(os.getenv("COMPANY_QUESTIONS_TIMEOUT_SECONDS", "15"))
        self.cache_ttl = int(os.getenv("COMPANY_QUESTIONS_CACHE_TTL_SECONDS", "3600"))
        self._cache: dict[str, tuple[float, list[dict[str, str]]]] = {}
        self._locks: dict[str, asyncio.Lock] = {}

    @staticmethod
    def companies() -> list[dict[str, object]]:
        return [
            {
                "name": company.name,
                "slug": company.slug,
                "shortName": company.short_name,
                "sourceUrl": f"{REPOSITORY_URL}/tree/master/docs/companies/{company.paths[0]}",
            }
            for company in COMPANY_SOURCES
        ]

    async def questions(self, slug: str) -> list[dict[str, str]]:
        company = COMPANIES_BY_SLUG.get(slug)
        if company is None:
            raise KeyError(slug)
        cached = self._cache.get(slug)
        now = time.monotonic()
        if cached and now - cached[0] < self.cache_ttl:
            return list(cached[1])

        lock = self._locks.setdefault(slug, asyncio.Lock())
        async with lock:
            cached = self._cache.get(slug)
            now = time.monotonic()
            if cached and now - cached[0] < self.cache_ttl:
                return list(cached[1])
            try:
                async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                    responses = await asyncio.gather(
                        *(client.get(f"{self.raw_base_url}/{path}") for path in company.paths)
                    )
                documents = []
                for path, response in zip(company.paths, responses):
                    response.raise_for_status()
                    documents.extend(parse_company_questions(response.text, path))
            except (httpx.HTTPError, httpx.TimeoutException) as exc:
                raise CompanyQuestionSourceError(
                    f"Could not load questions for {company.name}"
                ) from exc
            documents = improve_incomplete_questions(slug, documents)
            documents = [
                item for item in documents
                if not is_context_dependent_question(item["question"])
            ]
            self._cache[slug] = (time.monotonic(), documents)
            return list(documents)

    async def create_exam(self, slug: str) -> list[dict[str, str]]:
        questions = await self.questions(slug)
        selected = list(questions[:20])
        existing = {item["question"].strip().casefold() for item in selected}
        for index, question_text in enumerate(SUPPLEMENTAL_QUESTIONS):
            if len(selected) >= 20:
                break
            if question_text.casefold() in existing:
                continue
            selected.append({
                "id": hashlib.sha256(
                    f"supplemental:{index}:{question_text}".encode("utf-8")
                ).hexdigest()[:16],
                "question": question_text,
                "section": "Interview Questions",
                "sourcePath": "supplemental",
            })
            existing.add(question_text.casefold())
        random.SystemRandom().shuffle(selected)
        # The API persists this internal snapshot and explicitly exposes only IDs
        # and question text. Reference answers never leave the backend pre-submit.
        return selected


_company_prep_service = CompanyPrepService()


def get_company_prep_service() -> CompanyPrepService:
    return _company_prep_service
