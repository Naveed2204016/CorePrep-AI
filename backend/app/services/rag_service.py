"""Retrieve subject-specific corpus chunks with lexical or vector search."""

import hashlib
import json
import math
import os
import re
import uuid
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
# Default to the low-memory backend so constrained deployments cannot
# accidentally initialize the embedding runtime. Opt in to vector mode.
RAG_BACKEND = os.getenv("RAG_BACKEND", "lexical").strip().lower()
VECTOR_DB_PATH = Path(os.getenv("VECTOR_DB_PATH", "./data/vector_db")).resolve()
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "dsa_corpus")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "1200"))
CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "180"))


@dataclass(frozen=True)
class CorpusChunk:
    id: str
    text: str
    source: str
    heading: str


def _load_chunks(data_root: Path) -> list[CorpusChunk]:
    chunks: list[CorpusChunk] = []
    for path in sorted(data_root.glob("*/*.md")):
        content = path.read_text(encoding="utf-8")
        sections = re.split(r"(?=^#{1,3}\s+)", content, flags=re.MULTILINE)
        document_title = path.stem.replace("_", " ").title()
        for section_number, section in enumerate(filter(str.strip, sections)):
            lines = section.strip().splitlines()
            heading = lines[0].lstrip("# ").strip() if lines else document_title
            prefix = f"Document: {document_title}\nSection: {heading}\n"
            body = "\n".join(lines[1:]).strip() or heading
            start = 0
            chunk_number = 0
            while start < len(body):
                end = min(start + CHUNK_SIZE, len(body))
                if end < len(body):
                    boundary = body.rfind(" ", start + CHUNK_SIZE // 2, end)
                    if boundary > start:
                        end = boundary
                text = prefix + body[start:end].strip()
                point_id = str(uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"coreprep:{path.name}:{section_number}:{chunk_number}:{text}",
                ))
                source = path.relative_to(data_root).as_posix()
                chunks.append(CorpusChunk(point_id, text, source, heading))
                if end >= len(body):
                    break
                start = max(start + 1, end - CHUNK_OVERLAP)
                chunk_number += 1
    return chunks


class BaseRAGService:
    def retrieve(self, query: str, subject_slug: str, limit: int = 8) -> list[CorpusChunk]:
        raise NotImplementedError

    def roadmap_context(self, subject: str, subject_slug: str, focus: str = "") -> str:
        query = (
            f"Design a progressive {subject} interview roadmap "
            "using focused single-topic cards with topic-specific learning resources. "
            + focus
        )
        return "\n\n".join(
            f"SOURCE: {chunk.source} — {chunk.heading}\n{chunk.text}"
            for chunk in self.retrieve(query, subject_slug, limit=10)
        )

    def close(self) -> None:
        """Release resources, if this retrieval backend owns any."""


class LexicalRAGService(BaseRAGService):
    """Small-memory BM25 retrieval for constrained hosting environments."""

    def __init__(self, data_root: Path = DATA_ROOT) -> None:
        self.chunks = _load_chunks(data_root)
        if not self.chunks:
            raise RuntimeError(f"No roadmap corpus documents found in {data_root}")

    @staticmethod
    def _tokens(value: str) -> list[str]:
        return re.findall(r"[a-z0-9]+", value.casefold())

    def retrieve(self, query: str, subject_slug: str, limit: int = 8) -> list[CorpusChunk]:
        candidates = [
            chunk for chunk in self.chunks
            if chunk.source.split("/", 1)[0] == subject_slug
        ]
        if not candidates:
            return []

        query_terms = set(self._tokens(query))
        documents = [self._tokens(f"{chunk.heading} {chunk.text}") for chunk in candidates]
        document_frequency = Counter(term for terms in documents for term in set(terms))
        average_length = sum(map(len, documents)) / len(documents)
        scores: list[tuple[float, int, CorpusChunk]] = []
        for position, (chunk, terms) in enumerate(zip(candidates, documents)):
            frequencies = Counter(terms)
            score = 0.0
            for term in query_terms:
                frequency = frequencies[term]
                if not frequency:
                    continue
                inverse_frequency = math.log(
                    1 + (len(documents) - document_frequency[term] + 0.5)
                    / (document_frequency[term] + 0.5)
                )
                denominator = frequency + 1.5 * (
                    0.25 + 0.75 * len(terms) / max(1, average_length)
                )
                score += inverse_frequency * frequency * 2.5 / denominator
            score += 1.5 * len(query_terms & set(self._tokens(chunk.heading)))
            if "assessment" in chunk.source:
                score += 0.15
            scores.append((score, -position, chunk))

        scores.sort(key=lambda item: (item[0], item[1]), reverse=True)
        return [item[2] for item in scores[:limit]]


class VectorRAGService(BaseRAGService):
    """Persistent local Qdrant with FastEmbed client-side embeddings."""

    def __init__(self, data_root: Path = DATA_ROOT) -> None:
        # Lazy imports keep ML runtimes out of the 512 MB lexical deployment.
        from fastembed import TextEmbedding
        from qdrant_client import QdrantClient

        self.data_root = data_root
        VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
        self.client = QdrantClient(path=str(VECTOR_DB_PATH))
        self.embedding = TextEmbedding(model_name=EMBEDDING_MODEL)
        self._ensure_index()

    def _corpus_fingerprint(self) -> str:
        digest = hashlib.sha256()
        digest.update(f"{EMBEDDING_MODEL}:{CHUNK_SIZE}:{CHUNK_OVERLAP}".encode())
        for path in sorted(self.data_root.glob("*/*.md")):
            digest.update(str(path.relative_to(self.data_root)).encode())
            digest.update(path.read_bytes())
        return digest.hexdigest()

    def _ensure_index(self) -> None:
        from qdrant_client.models import Distance, PointStruct, VectorParams

        manifest_path = VECTOR_DB_PATH / "corpus_manifest.json"
        fingerprint = self._corpus_fingerprint()
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            manifest = {}
        if (
            manifest.get("fingerprint") == fingerprint
            and self.client.collection_exists(COLLECTION_NAME)
        ):
            return
        if self.client.collection_exists(COLLECTION_NAME):
            self.client.delete_collection(COLLECTION_NAME)
        chunks = _load_chunks(self.data_root)
        if not chunks:
            raise RuntimeError(f"No roadmap corpus documents found in {self.data_root}")
        vectors = list(self.embedding.embed([chunk.text for chunk in chunks]))
        self.client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=len(vectors[0]), distance=Distance.COSINE),
        )
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=chunk.id,
                    vector=vector.tolist(),
                    payload={
                        "text": chunk.text,
                        "source": chunk.source,
                        "heading": chunk.heading,
                        "subject": chunk.source.split("/", 1)[0],
                    },
                )
                for chunk, vector in zip(chunks, vectors)
            ],
            wait=True,
        )
        manifest_path.write_text(
            json.dumps({"fingerprint": fingerprint, "chunks": len(chunks)}, indent=2),
            encoding="utf-8",
        )

    def retrieve(self, query: str, subject_slug: str, limit: int = 8) -> list[CorpusChunk]:
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        self._ensure_index()
        query_vector = next(self.embedding.query_embed(query)).tolist()
        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            query_filter=Filter(
                must=[FieldCondition(key="subject", match=MatchValue(value=subject_slug))]
            ),
            limit=limit,
            with_payload=True,
        ).points
        return [
            CorpusChunk(
                id=str(result.id),
                text=str((result.payload or {}).get("text", "")),
                source=str((result.payload or {}).get("source", "unknown")),
                heading=str((result.payload or {}).get("heading", "")),
            )
            for result in results
        ]

    def close(self) -> None:
        self.client.close()


@lru_cache(maxsize=1)
def get_rag_service() -> BaseRAGService:
    if RAG_BACKEND == "lexical":
        return LexicalRAGService()
    if RAG_BACKEND == "vector":
        return VectorRAGService()
    raise ValueError("RAG_BACKEND must be 'lexical' or 'vector'")
