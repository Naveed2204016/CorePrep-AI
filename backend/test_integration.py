"""
Quick Test Example - CorePrep Backend
Shows how to use the services independently for testing
"""

import asyncio
import json
from app.services.roadmap_service import get_roadmap_service
from app.services.assessment_service import get_assessment_service
from app.services.rag_service import get_rag_service


async def test_roadmap_generation():
    """Test roadmap generation"""
    print("="*60)
    print("TEST 1: Roadmap Generation")
    print("="*60)
    
    service = get_roadmap_service()
    
    # Generate roadmap
    roadmap = service.generate_roadmap(subject="dsa", timeline_weeks=8)
    
    print(f"Title: {roadmap.get('title')}")
    print(f"Topics: {len(roadmap.get('topics', []))}")
    print("\nTopics:")
    for topic in roadmap.get('topics', []):
        print(f"  - {topic['name']} ({topic['duration_weeks']} weeks)")
        print(f"    Description: {topic['description'][:60]}...")
    
    return roadmap


async def test_suggest_edit(roadmap):
    """Test suggest edit functionality"""
    print("\n" + "="*60)
    print("TEST 2: Suggest Edit")
    print("="*60)
    
    service = get_roadmap_service()
    
    suggestion = "Add 1 week to Linked Lists, increase difficulty"
    print(f"Suggestion: {suggestion}")
    
    updated = service.suggest_edit(roadmap, suggestion)
    
    print("\nUpdated Topics:")
    for topic in updated.get('topics', []):
        print(f"  - {topic['name']} ({topic['duration_weeks']} weeks)")


async def test_question_generation():
    """Test question generation"""
    print("\n" + "="*60)
    print("TEST 3: Assessment Question Generation")
    print("="*60)
    
    service = get_assessment_service()
    
    questions = service.generate_questions(
        topic="Linked Lists",
        subject="dsa",
        num_mcq=3,
        num_short=2
    )
    
    print(f"MCQ Questions: {len(questions.get('mcq', []))}")
    print(f"Short Answer: {len(questions.get('short', []))}")
    
    # Show first MCQ
    if questions.get('mcq'):
        mcq = questions['mcq'][0]
        print(f"\nSample MCQ:")
        print(f"  Q: {mcq['question']}")
        print(f"  Options: {list(mcq.get('options', {}).keys())}")
        print(f"  Answer: {mcq.get('correct')}")
    
    return questions


async def test_answer_evaluation():
    """Test answer evaluation"""
    print("\n" + "="*60)
    print("TEST 4: Answer Evaluation")
    print("="*60)
    
    service = get_assessment_service()
    
    # Test MCQ evaluation
    mcq_result = service.evaluate_answer(
        question="What is the time complexity of binary search?",
        question_type="mcq",
        user_answer="C",
        correct_answer="C",
        options={"A": "O(n)", "B": "O(n^2)", "C": "O(log n)", "D": "O(1)"},
        subject="dsa"
    )
    
    print("MCQ Evaluation:")
    print(f"  User Answer: C")
    print(f"  Correct: {mcq_result['is_correct']}")
    print(f"  Marks: {mcq_result['marks']}/1.0")
    print(f"  Explanation: {mcq_result['explanation'][:100]}...")
    
    # Test short answer evaluation
    short_result = service.evaluate_answer(
        question="Explain why linked lists are useful",
        question_type="short",
        user_answer="They allow efficient insertion and deletion at any position",
        correct_answer="Linked lists are useful because they allow O(1) insertion and deletion once position is found, unlike arrays which require O(n)",
        subject="dsa"
    )
    
    print("\nShort Answer Evaluation:")
    print(f"  User Answer: {short_result.get('explanation', '')[:60]}...")
    print(f"  Correct: {short_result.get('is_correct')}")
    print(f"  Marks: {short_result.get('marks')}/1.0")


async def test_rag_retrieval():
    """Test RAG context retrieval"""
    print("\n" + "="*60)
    print("TEST 5: RAG Context Retrieval")
    print("="*60)
    
    rag = get_rag_service()
    
    # First, try to index if not already done
    print("Indexing DSA content...")
    rag.index_subject("dsa")
    
    # Retrieve context
    context_docs = rag.retrieve_context("What is binary search?", subject="dsa")
    
    print(f"Found {len(context_docs)} relevant documents")
    if context_docs:
        print(f"\nTop result:")
        print(f"  Subject: {context_docs[0].metadata.get('subject')}")
        print(f"  Content: {context_docs[0].page_content[:150]}...")


async def main():
    """Run all tests"""
    print("\n🧪 CorePrep Backend - Integration Tests\n")
    
    try:
        # Test RAG first (needed for quality)
        await test_rag_retrieval()
        
        # Test roadmap generation
        roadmap = await test_roadmap_generation()
        
        # Test editing
        await test_suggest_edit(roadmap)
        
        # Test questions
        await test_question_generation()
        
        # Test evaluation
        await test_answer_evaluation()
        
        print("\n" + "="*60)
        print("✅ All tests completed successfully!")
        print("="*60)
        print("\n💡 Next: Connect frontend to API endpoints")
        print("   - POST /api/v1/roadmaps/generate")
        print("   - POST /api/v1/assessments/generate")
        print("   - POST /api/v1/assessments/submit")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
