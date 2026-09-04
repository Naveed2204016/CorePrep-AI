from pathlib import Path

from app.services.rag_service import LexicalRAGService


def test_lexical_retrieval_prefers_matching_heading(tmp_path: Path):
    subject = tmp_path / "dsa"
    subject.mkdir()
    (subject / "curriculum.md").write_text(
        "# Arrays\nIndexing and contiguous storage.\n"
        "# Graph Traversal\nBreadth-first search uses a queue; depth-first search uses a stack.",
        encoding="utf-8",
    )
    service = LexicalRAGService(tmp_path)

    results = service.retrieve("graph traversal breadth first search", "dsa", limit=1)

    assert len(results) == 1
    assert results[0].heading == "Graph Traversal"


def test_lexical_retrieval_stays_within_subject(tmp_path: Path):
    for slug in ("dsa", "dbms"):
        subject = tmp_path / slug
        subject.mkdir()
        (subject / "curriculum.md").write_text(
            "# Indexes\nIndexes improve lookup performance.", encoding="utf-8"
        )
    service = LexicalRAGService(tmp_path)

    results = service.retrieve("indexes", "dbms")

    assert results
    assert all(chunk.source.startswith("dbms/") for chunk in results)
