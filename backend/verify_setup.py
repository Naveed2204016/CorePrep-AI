#!/usr/bin/env python3
"""
Verification script to check if everything is properly set up
Run this before running the backend to catch issues early
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"📍 Python: {version.major}.{version.minor}.{version.micro}", end=" ")
    if version.major >= 3 and version.minor >= 9:
        print("✅")
        return True
    else:
        print("❌ (Need 3.9+)")
        return False


def check_required_packages():
    """Check if required packages are installed"""
    required = [
        'fastapi',
        'sqlalchemy',
        'langchain',
        'chromadb',
        'sentence_transformers',
        'pydantic',
        'python_jose'
    ]
    
    print("\n📦 Checking packages:")
    all_ok = True
    for pkg in required:
        try:
            __import__(pkg)
            print(f"  {pkg:<25} ✅")
        except ImportError:
            print(f"  {pkg:<25} ❌")
            all_ok = False
    
    if not all_ok:
        print("\n  Run: pip install -r requirements.txt")
    return all_ok


def check_env_file():
    """Check if .env file exists and has required settings"""
    print("\n🔧 Checking configuration:")
    
    if not os.path.exists('.env'):
        print("  .env file ❌ (Not found)")
        print("  → Copy .env.example to .env and update settings")
        return False
    
    print("  .env file ✅")
    
    # Read .env and check required keys
    required_keys = [
        'DATABASE_URL',
        'LLM_PROVIDER',
        'SECRET_KEY'
    ]
    
    with open('.env', 'r') as f:
        env_content = f.read()
    
    all_ok = True
    for key in required_keys:
        if key in env_content and not env_content.split(f'{key}=')[1].startswith('your_'):
            print(f"  {key:<25} ✅")
        else:
            print(f"  {key:<25} ⚠️  (Set in .env)")
            all_ok = False
    
    return all_ok


def check_directory_structure():
    """Check if required directories exist"""
    print("\n📁 Checking directories:")
    
    required_dirs = [
        'app',
        'app/api/v1',
        'app/services',
        'app/models',
        'app/core',
        'data/dsa',
        'data/dbms',
        'data/cn',
        'data/os'
    ]
    
    all_ok = True
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"  {dir_path:<30} ✅")
        else:
            print(f"  {dir_path:<30} ❌")
            all_ok = False
    
    return all_ok


def check_required_files():
    """Check if critical files exist"""
    print("\n📄 Checking critical files:")
    
    required_files = [
        'app/main.py',
        'app/api/v1/roadmaps.py',
        'app/api/v1/assessments.py',
        'app/services/roadmap_service.py',
        'app/services/assessment_service.py',
        'app/services/rag_service.py',
        'data/dsa/arrays.md',
        'data/dsa/linkedlist.md',
        'data/dsa/trees.md'
    ]
    
    all_ok = True
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"  {file_path:<40} ✅")
        else:
            print(f"  {file_path:<40} ❌")
            all_ok = False
    
    return all_ok


def check_database_connection():
    """Check if database can be connected"""
    print("\n🗄️  Checking database connection:")
    
    try:
        from app.db.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("  Database connection ✅")
            return True
    
    except Exception as e:
        print(f"  Database connection ❌")
        print(f"  Error: {str(e)[:60]}")
        print("  → Check DATABASE_URL in .env")
        print("  → Ensure MySQL server is running")
        return False


def check_llm_setup():
    """Check LLM configuration"""
    print("\n🧠 Checking LLM setup:")
    
    try:
        from app.core.llm_config import LLM_PROVIDER, get_llm
        
        print(f"  LLM Provider: {LLM_PROVIDER}")
        
        if LLM_PROVIDER == 'ollama':
            print("  → Make sure Ollama is running: ollama serve")
            print("  → And model is pulled: ollama pull mistral")
        elif LLM_PROVIDER == 'openai':
            print("  → Ensure OPENAI_API_KEY is set in .env")
        
        # Try to get LLM instance
        try:
            llm = get_llm()
            print(f"  LLM instance ✅")
            return True
        except Exception as e:
            print(f"  LLM instance ❌")
            print(f"  Error: {str(e)[:60]}")
            return False
    
    except Exception as e:
        print(f"  Configuration ❌: {e}")
        return False


def check_rag_setup():
    """Check RAG service"""
    print("\n🔍 Checking RAG setup:")
    
    try:
        from app.services.rag_service import get_rag_service
        
        rag = get_rag_service()
        print("  RAG service ✅")
        
        # Check if content files exist
        content_count = 0
        for root, dirs, files in os.walk('data'):
            for file in files:
                if file.endswith('.md'):
                    content_count += 1
        
        print(f"  Content files found: {content_count}")
        
        if content_count == 0:
            print("  ⚠️  Add markdown files to data/ for RAG to work properly")
            return True  # Not critical, just reduces quality
        
        return True
    
    except Exception as e:
        print(f"  RAG setup ❌: {e}")
        return False


def check_models_imported():
    """Check if all models can be imported"""
    print("\n📊 Checking database models:")
    
    try:
        from app.models import (
            User, Roadmap, RoadmapTopic, TopicResource,
            Assessment, AssessmentQuestion,
            UserAssessmentAttempt, UserAnswer
        )
        print("  All models imported ✅")
        return True
    
    except Exception as e:
        print(f"  Model import ❌: {e}")
        return False


def print_status_summary(all_results):
    """Print summary of all checks"""
    print("\n" + "="*60)
    
    passed = sum(1 for r in all_results.values() if r)
    total = len(all_results)
    
    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print("="*60)
        print("\n🚀 Ready to start backend!")
        print("\nNext steps:")
        print("1. Run: python setup.py")
        print("2. Start LLM: ollama serve (in new terminal)")
        print("3. Run: uvicorn app.main:app --reload")
        return True
    else:
        print(f"⚠️  SOME CHECKS FAILED ({passed}/{total})")
        print("="*60)
        print("\nFailed checks:")
        for check_name, result in all_results.items():
            if not result:
                print(f"  ❌ {check_name}")
        
        print("\nPlease fix issues above before starting backend.")
        return False


def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("🔍 CorePrep Backend - Setup Verification")
    print("="*60)
    
    results = {
        "Python Version": check_python_version(),
        "Required Packages": check_required_packages(),
        "Configuration": check_env_file(),
        "Directory Structure": check_directory_structure(),
        "Critical Files": check_required_files(),
        "Database Models": check_models_imported(),
        "RAG Setup": check_rag_setup(),
    }
    
    # Database and LLM are important but not critical for structure
    db_ok = check_database_connection()
    llm_ok = check_llm_setup()
    
    if not db_ok:
        print("  ⚠️  Database not ready (setup.py will help)")
    if not llm_ok:
        print("  ⚠️  LLM not ready (start it before testing)")
    
    success = print_status_summary(results)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
