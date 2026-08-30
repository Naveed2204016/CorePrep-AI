"""Chunk, embed, persist, and semantically retrieve subject-specific corpora."""

import hashlib
import json
import os
import re
import uuid
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, FieldCondition, Filter, MatchValue, PointStruct, VectorParams

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
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


class RAGService:
    """Persistent local Qdrant with FastEmbed client-side embeddings."""

    def __init__(self, data_root: Path = DATA_ROOT) -> None:
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
        chunks = self._load_chunks()
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

    def _load_chunks(self) -> list[CorpusChunk]:
        chunks: list[CorpusChunk] = []
        for path in sorted(self.data_root.glob("*/*.md")):
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
                    source = path.relative_to(self.data_root).as_posix()
                    chunks.append(CorpusChunk(point_id, text, source, heading))
                    if end >= len(body):
                        break
                    start = max(start + 1, end - CHUNK_OVERLAP)
                    chunk_number += 1
        return chunks

    def retrieve(self, query: str, subject_slug: str, limit: int = 8) -> list[CorpusChunk]:
        # Corpus files can be expanded while the API is running. Refresh the
        # persistent index when their fingerprint changes before retrieval.
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
        """Release the embedded Qdrant database lock deterministically."""
        self.client.close()


@lru_cache(maxsize=1)
def get_rag_service() -> RAGService:
    return RAGService()
