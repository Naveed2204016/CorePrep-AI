# CorePrep AI

### AI-Powered Learning, Assessment & Interview Preparation Platform

CorePrep AI is an AI-powered preparation platform designed to help students and job seekers improve their technical knowledge, prepare for examinations, and get ready for technical interviews.

The platform combines Artificial Intelligence with personalized learning approaches to provide a structured and interactive preparation experience.

Our goal is to make technical learning and career preparation more accessible, organized, and effective through AI-driven assistance.

### Project Overview

CorePrep AI brings multiple preparation tools together in one platform, helping users improve their technical skills, evaluate their knowledge, and prepare for professional opportunities.

The platform focuses on intelligent learning assistance, personalized preparation, and AI-powered evaluation.

**GitHub Repository:** https://github.com/Naveed2204016/CorePrep-AI

---

## Key Features

### 1. AI-Powered Assessments

- Generate subject-based practice assessments.
- Generate multiple-choice and short-answer questions.
- Submit answers and receive AI-powered evaluation.
- Get assessment scores and explanations.
- Identify weak areas that require further revision.

### 2. Personalized Learning Roadmaps

- Generate customized learning roadmaps based on selected subjects.
- Create roadmaps using uploaded job-description PDFs.
- Retrieve relevant learning materials using RAG.
- Modify and refine generated roadmaps.
- Save and manage learning roadmaps.
- Track topic completion and learning progress.

### 3. Company-Specific Interview Preparation

- Prepare for technical interviews at different companies.
- Generate company-focused interview questions.
- Take company-specific practice exams.
- Receive AI-powered answer evaluation.
- Get scores and feedback on submitted answers.

### 4. AI-Powered CV Review

- Upload CV/resume documents in PDF format.
- Extract and analyze CV content.
- Receive structured AI-generated feedback.
- Identify strengths and areas for improvement.
- Get actionable suggestions to improve your CV.

### 5. User Authentication & Profile

- Register and sign in to an account.
- Secure password-based authentication.
- Google OAuth authentication.
- Access protected application pages.
- Manage personal profile information.

---

## Technology Stack

CorePrep AI is developed using modern frontend, backend, database, and artificial intelligence technologies to provide an integrated software engineering interview preparation platform.

### 1. Frontend Technologies

| Technology     | Purpose                                    |
| -------------- | ------------------------------------------ |
| React 19       | Building interactive user interfaces       |
| TypeScript     | Type-safe frontend development             |
| Vite           | Frontend development server and build tool |
| React Router 7 | Managing application navigation and routes |
| Tailwind CSS 4 | Styling and responsive UI development      |
| Framer Motion  | Animations and UI transitions              |
| Lucide React   | Icons and visual elements                  |
| Axios          | Installed HTTP client dependency           |
| Oxlint         | Code linting and quality checks            |

### 2. Backend Technologies

| Technology    | Purpose                                       |
| ------------- | --------------------------------------------- |
| Python        | Backend programming language                  |
| FastAPI       | Building RESTful APIs                         |
| Uvicorn       | Running the FastAPI application               |
| SQLAlchemy    | Database ORM and query management             |
| MySQL         | Relational database management                |
| PyMySQL       | MySQL database connectivity                   |
| Pydantic      | Request validation and structured data models |
| HTTPX         | Asynchronous HTTP communication               |
| Python-dotenv | Environment variable management               |

### 3. Authentication and Security

- JWT-based authentication using Python-JOSE.
- Password hashing using Passlib and bcrypt.
- Google OAuth authentication using Authlib.
- Session management using Starlette SessionMiddleware.
- Protected backend endpoints using Bearer token authentication.

### 4. Artificial Intelligence

| Technology           | Purpose                                      |
| -------------------- | -------------------------------------------- |
| Google Gemini API    | Hosted LLM integration                       |
| Ollama               | Running language models locally              |
| Qwen 2.5 7B Instruct | Supported local language model               |
| Pydantic JSON Schema | Validating structured AI-generated responses |

The application supports switching between Gemini and Ollama through environment configuration.

### 5. Retrieval-Augmented Generation (RAG)

| Technology | Purpose                                          |
| ---------- | ------------------------------------------------ |
| BM25       | Lexical retrieval of relevant learning materials |
| Qdrant     | Optional persistent vector storage               |
| FastEmbed  | Generating text embeddings                       |
| Markdown   | Storing subject-specific learning materials      |

The default retrieval implementation uses BM25-based lexical search. An optional vector-based implementation uses Qdrant and FastEmbed.

### 6. Document Processing

- PyPDF for extracting text from uploaded PDF documents.
- PDF processing for job-description-based roadmap generation.
- PDF processing for AI-assisted CV reviews.

### 7. Development and Deployment Configuration

- Vercel configuration for frontend routing.
- Procfile for backend application startup.
- Environment-based configuration for database, authentication, and AI providers.

---

## System Architecture

CorePrep AI follows a client-server architecture in which the React frontend communicates with the FastAPI backend through RESTful APIs.

### 1. Architecture Overview

```text
                   COREPREP AI
                        |
                 React Frontend
                        |
                 REST API Requests
                        |
                  FastAPI Backend
                        |
              +---------+---------+
              |         |         |
          Authentication  Services  Database
              |         |         |
          JWT / OAuth   AI / RAG   MySQL
                        |
               +--------+--------+
               |                 |
           LLM Provider      RAG Service
               |                 |
          Gemini/Ollama     Markdown Corpus
                                 |
                      +----------+----------+
                      |                     |
                  BM25 Search          Vector Search
                                       (Optional)
                                           |
                                      Qdrant +
                                      FastEmbed
```

### 2. How the System Works

1. Users interact with the application through the React frontend.
2. The frontend sends HTTP requests to the FastAPI backend.
3. FastAPI handles authentication, request validation, and application logic.
4. SQLAlchemy communicates with MySQL to store and retrieve user and application data.
5. AI services communicate with Gemini or Ollama to generate and evaluate learning content.
6. The RAG service retrieves relevant information from subject-specific Markdown documents.
7. Retrieved information is provided to the LLM when generating context-aware roadmaps and assessments.
8. The backend validates and stores generated results and returns responses to the frontend.

### 3. Backend Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── roadmaps.py
│   │       ├── assessments.py
│   │       ├── company_prep.py
│   │       ├── cv_reviews.py
│   │       └── profile.py
│   │
│   ├── core/
│   │   ├── google_auth.py
│   │   ├── llm_config.py
│   │   └── security.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── roadmap.py
│   │   └── company_prep.py
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── roadmap_service.py
│   │   ├── assessment_service.py
│   │   ├── company_prep_service.py
│   │   ├── company_evaluation_service.py
│   │   ├── cv_review_service.py
│   │   └── curriculum_registry.py
│   │
│   └── main.py
│
├── data/
├── migrations/
├── scripts/
├── tests/
├── requirements.txt
├── .env.example
└── Procfile
```

### 4. Frontend Project Structure

```text
frontend/
│
├── public/
│
├── src/
│   ├── assets/
│   │
│   ├── components/
│   │   ├── auth/
│   │   ├── layout/
│   │   └── ui/
│   │
│   ├── features/
│   │   └── company-prep/
│   │       └── data/
│   │
│   ├── pages/
│   │
│   ├── services/
│   │
│   ├── types/
│   │
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
│
├── package.json
├── .env.example
├── vite.config.ts
└── vercel.json
```

### 5. Main Architectural Components

**Frontend:** Handles user interaction, authentication screens, roadmap creation, assessments, company preparation, CV review, and profile interfaces.

**API Layer:** FastAPI provides endpoints for authentication, roadmap management, assessments, company preparation, CV analysis, and profile performance.

**Database Layer:** SQLAlchemy manages relational data stored in MySQL, including users, roadmaps, topics, resources, assessments, and examination results.

**AI Layer:** The LLM configuration provides a common interface for generating structured responses using Gemini or Ollama.

**RAG Layer:** Retrieves relevant learning materials from the Markdown knowledge base using lexical or optional vector-based retrieval.

**Service Layer:** Contains the main business logic for roadmap generation, assessment generation and evaluation, company examination, and CV review.

---

## Getting Started

Follow these instructions to install and run CorePrep AI locally.

### 1. Prerequisites

Install the following software:

- Python 3.10+
- Node.js and npm
- MySQL Server
- Git

For local LLM execution, install [Ollama](https://ollama.com/).

Alternatively, you can use the Google Gemini API.

### 2. Clone the Repository

```bash
git clone https://github.com/Naveed2204016/CorePrep-AI.git

cd CorePrep-AI
```

### 3. Backend Setup

Navigate to the backend directory:

```powershell
cd backend
```

Create a virtual environment:

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip

pip install -r requirements.txt
```

Create the environment file:

```powershell
Copy-Item .env.example .env
```

### 4. Database Configuration

Start your MySQL server and create the database:

```sql
CREATE DATABASE coreprep_ai
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Configure the database connection in `backend/.env`:

```env
DATABASE_URL=mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost:3306/coreprep_ai

SECRET_KEY=your_long_random_secret_key
```

Replace the database credentials with your actual MySQL credentials.

The backend initializes its SQLAlchemy database tables when the application starts.

### 5. Configure the AI Provider

CorePrep AI supports Google Gemini and Ollama.

**Option A: Google Gemini**

```env
LLM_PROVIDER=gemini

GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

**Option B: Ollama**

Download the supported model:

```bash
ollama pull qwen2.5:7b-instruct
```

Configure:

```env
LLM_PROVIDER=ollama

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b-instruct
```

### 6. Configure RAG

The default RAG implementation uses BM25-based lexical retrieval.

For optional vector-based retrieval, configure:

```env
RAG_BACKEND=vector

VECTOR_DB_PATH=./data/vector_db
QDRANT_COLLECTION=dsa_corpus
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

RAG_CHUNK_SIZE=1200
RAG_CHUNK_OVERLAP=180
```

Qdrant uses local persistent storage, while FastEmbed generates the document embeddings.

### 7. Configure Frontend

Open another terminal and navigate to the frontend directory:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Create the environment file:

```powershell
Copy-Item .env.example .env
```

Configure `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_USE_MOCK_AUTH=false
```

### 8. Run the Backend

From the backend directory:

```powershell
uvicorn app.main:app --reload --port 8000
```

Backend URLs:

- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 9. Run the Frontend

From the frontend directory:

```powershell
npm run dev
```

Frontend URL:

http://localhost:5173

### 10. Start Using CorePrep AI

1. Open the frontend application.
2. Create an account and sign in.
3. Select a preparation feature.
4. Generate a roadmap or start a company-specific examination.
5. Complete assessments and review your performance.

**Note:** The backend and frontend must run in separate terminals. MySQL and your selected AI provider must also be available.
