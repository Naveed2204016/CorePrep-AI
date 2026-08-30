#!/usr/bin/env python3
"""
Setup script for CorePrep AI Backend
Initializes database, RAG indices, and seeds sample data
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.database import Base, engine, SessionLocal
from app.models import (
    Roadmap, RoadmapTopic, TopicResource, 
    Assessment, AssessmentQuestion, 
    UserAssessmentAttempt, UserAnswer, User
)
from app.services.rag_service import get_rag_service


def init_database():
    """Initialize database tables"""
    print("📦 Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")


def setup_rag():
    """Setup and index RAG documents"""
    print("🧠 Setting up RAG indices...")
    rag_service = get_rag_service()
    
    subjects = ["dsa", "dbms", "cn", "os"]
    
    for subject in subjects:
        print(f"  Indexing {subject.upper()}...", end=" ")
        if rag_service.index_subject(subject):
            print("✅")
        else:
            print("⚠️  (No content found)")


def seed_sample_data():
    """Seed sample resources for topics"""
    print("🌱 Seeding sample data...")
    db = SessionLocal()
    
    # Sample DSA roadmap (for testing)
    # In production, user creates via API
    
    sample_resources = {
        "Arrays": [
            {
                "type": "blog",
                "title": "Array Data Structure - GeeksforGeeks",
                "url": "https://www.geeksforgeeks.org/array-data-structure/",
                "description": "Comprehensive guide to arrays"
            },
            {
                "type": "video",
                "title": "Arrays Explained - YouTube",
                "url": "https://www.youtube.com/watch?v=ZoG7DwwjWh0",
                "description": "Visual explanation of array concepts"
            }
        ],
        "Linked Lists": [
            {
                "type": "blog",
                "title": "Linked List - GeeksforGeeks",
                "url": "https://www.geeksforgeeks.org/data-structures/linked-list/",
                "description": "Complete linked list tutorial"
            },
            {
                "type": "video",
                "title": "Linked Lists Explained - YouTube",
                "url": "https://www.youtube.com/watch?v=DyG9S3B1QX8",
                "description": "Step-by-step linked list explanation"
            }
        ]
    }
    
    print("✅ Sample data ready (use API to create roadmaps)")
    db.close()


def print_startup_guide():
    """Print startup instructions"""
    print("\n" + "="*60)
    print("✨ CorePrep AI Backend Setup Complete!")
    print("="*60)
    print("""
📋 NEXT STEPS:

1. Install dependencies:
   pip install -r requirements.txt

2. Setup LLM (choose one):
   
   Option A - Ollama (Recommended for dev):
   - Download from https://ollama.ai
   - Run: ollama pull mistral
   - Start: ollama serve (runs on http://localhost:11434)
   
   Option B - OpenAI:
   - Set OPENAI_API_KEY in .env
   - Set LLM_PROVIDER=openai

3. Update .env with your settings:
   - DATABASE_URL (MySQL)
   - LLM configuration
   - VECTOR_DB_PATH

4. Run migrations (if using Alembic):
   alembic upgrade head

5. Start the backend:
   cd backend
   uvicorn app.main:app --reload

6. API will be available at:
   http://localhost:8000
   
   Docs: http://localhost:8000/docs

📚 API ENDPOINTS:

Roadmaps:
- POST   /api/v1/roadmaps/generate          - Create roadmap
- POST   /api/v1/roadmaps/suggest-edit      - Modify roadmap
- GET    /api/v1/roadmaps/{id}              - Get roadmap
- POST   /api/v1/roadmaps/{id}/confirm      - Activate roadmap
- GET    /api/v1/roadmaps                   - List user roadmaps

Assessments:
- POST   /api/v1/assessments/generate       - Create exam
- POST   /api/v1/assessments/submit         - Submit exam
- GET    /api/v1/assessments/attempt/{id}   - Get results

🔒 Authentication:
All endpoints require Bearer token (from auth API)

⚡ OPTIMIZATION TIPS:

1. LLM Speed:
   - Use Ollama locally (fastest, no network latency)
   - Cache roadmap generation
   - Use mistral model (fast & good quality)

2. RAG Quality:
   - Add more detailed .md files in data/
   - Use sentence-transformers for embeddings
   - Keep context chunks under 1000 chars

3. Database:
   - Index frequently queried columns
   - Cache assessment results
   - Use connection pooling

📞 TROUBLESHOOTING:

- LLM slow? Switch to OpenAI or use smaller model
- RAG no results? Check data/*.md files exist
- DB connection? Verify DATABASE_URL in .env
- Auth failing? Ensure token format: "Bearer <token>"

""")
    print("="*60)


def main():
    """Main setup flow"""
    print("\n🚀 CorePrep AI Backend Initialization\n")
    
    try:
        init_database()
        setup_rag()
        seed_sample_data()
        print_startup_guide()
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
