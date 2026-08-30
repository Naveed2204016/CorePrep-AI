"""Build or refresh the persistent DSA vector index."""

from app.services.rag_service import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    VECTOR_DB_PATH,
    RAGService,
)


if __name__ == "__main__":
    service = RAGService()
    try:
        info = service.client.get_collection(COLLECTION_NAME)
        print(f"Collection: {COLLECTION_NAME}")
        print(f"Embedding model: {EMBEDDING_MODEL}")
        print(f"Storage: {VECTOR_DB_PATH}")
        print(f"Indexed vectors: {info.points_count}")
    finally:
        service.close()
