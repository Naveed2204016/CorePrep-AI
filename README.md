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

---

## AI Integration & Retrieval-Augmented Generation

CorePrep AI integrates Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG) to provide personalized learning roadmaps, intelligent assessments, company-specific examination evaluation, and CV feedback.

### 1. Large Language Model Integration

The backend supports two LLM providers.

**Google Gemini**

- Uses Google's hosted language model API.
- Generates structured JSON responses.
- Supports roadmap generation, assessment generation, answer evaluation, and CV review.

**Ollama**

- Runs language models locally.
- Supports Qwen 2.5 7B Instruct.
- Provides an alternative to hosted AI services.

The LLM provider is selected using the `LLM_PROVIDER` environment variable.

The backend uses a common JSON-generating interface to communicate with either provider.

### 2. Retrieval-Augmented Generation (RAG)

RAG retrieves relevant information from subject-specific learning materials and provides that information to the LLM as additional context.

The retrieval process:

1. Load Markdown learning documents from `backend/data/`.
2. Divide documents into smaller chunks based on headings and chunk size.
3. Retrieve relevant chunks based on the user's query.
4. Provide the retrieved content to the LLM.
5. Generate context-aware roadmaps or assessment questions.

### 3. RAG Retrieval Methods

CorePrep AI implements two retrieval approaches.

**Lexical Retrieval (Default)**

- Uses BM25-based relevance scoring.
- Matches query terms against document content.
- Considers section headings during retrieval.
- Uses less memory and does not require an embedding model.

**Vector-Based Retrieval (Optional)**

- Uses FastEmbed to generate text embeddings.
- Uses Qdrant for persistent vector storage.
- Supports semantic similarity-based retrieval.
- Uses the `BAAI/bge-small-en-v1.5` embedding model.

The retrieval implementation can be selected using `RAG_BACKEND`.

### 4. AI-Powered Roadmap Generation

The roadmap generation service combines predefined curriculum information, retrieved learning materials, and LLM-generated content.

**Topic-Based Roadmap**

1. The user selects a computer science subject.
2. The user selects a preparation timeline.
3. The RAG service retrieves relevant learning materials.
4. The LLM generates a structured roadmap.
5. Pydantic validates the generated response.
6. The backend assigns topic schedules and learning resources.
7. The generated roadmap is saved as a draft.

The supported topic-based timelines are 4, 6, 8, and 10 weeks.

**Job-Description-Based Roadmap**

1. The user uploads a one-page job-description PDF.
2. PyPDF extracts the document text.
3. The system detects relevant computer science subjects using predefined keyword patterns.
4. The RAG service retrieves subject-specific information.
5. The LLM generates a mixed preparation roadmap.
6. The backend validates and stores the generated roadmap.

The uploaded PDF must be 5 MB or smaller.

Supported job-roadmap timelines are 6, 8, 10, and 12 weeks.

### 5. AI-Powered Assessment Generation and Evaluation

The assessment service generates questions based on the selected roadmap topic.

**Question Generation**

- Generates multiple-choice questions (MCQs).
- Generates short-answer questions.
- Uses retrieved learning materials as context.
- Validates the generated questions using structured schemas.
- Ensures each MCQ has four options and one correct answer.

**Answer Evaluation**

- Evaluates submitted answers.
- Checks MCQ correctness against the stored correct option.
- Uses semantic evaluation for short answers.
- Generates explanations and revision areas.
- Uses deterministic fallback evaluation when AI evaluation fails.

A score of 70% or above is considered a passing result.

### 6. Company-Specific Interview Preparation

The company preparation service provides interview practice for 33 configured companies.

The question bank is retrieved from the public repository:

https://github.com/TamimEhsan/interview-questions-bangladesh

The system creates a fixed 20-question practice examination using available company questions and supplemental questions.

The company evaluation service:

- Evaluates answers using an LLM.
- Assigns scores from 0 to 10.
- Classifies answers as correct, partially correct, or incorrect.
- Provides individual feedback.
- Generates suggested answers.
- Uses sequential batches, retry handling, and evaluation timeouts.

### 7. AI-Powered CV Review

The CV review service analyzes uploaded PDF resumes.

The process:

1. Validate the uploaded PDF.
2. Extract text using PyPDF.
3. Send the extracted content to the configured LLM.
4. Generate structured feedback.
5. Return the review results to the frontend.

The review evaluates:

- Clarity and readability.
- Experience and achievement impact.
- Technical skills and relevance.
- Projects and evidence of ability.
- Structure, completeness, and ATS suitability.

The service returns an overall score out of 100, strengths, improvement suggestions, missing sections, and relevant keywords.

### 8. Performance Analysis

The profile performance service analyzes submitted roadmap assessment answers.

It calculates:

- Total answered questions.
- Correct and incorrect answers.
- Overall accuracy.
- Subject-wise accuracy.
- Subject weakness scores.
- Weak subjects requiring further preparation.

This helps users identify areas that need improvement.

---

## API Documentation

CorePrep AI provides RESTful APIs through FastAPI. The endpoints are organized into versioned modules under `/api/v1`.

### 1. Authentication APIs

| Method | Endpoint                       | Description                            |
| ------ | ------------------------------ | -------------------------------------- |
| POST   | `/api/v1/auth/signup`          | Register a new user                    |
| POST   | `/api/v1/auth/login`           | Authenticate a user and generate a JWT |
| GET    | `/api/v1/auth/google`          | Start Google OAuth authentication      |
| GET    | `/api/v1/auth/google/callback` | Handle Google OAuth callback           |

### 2. Roadmap APIs

| Method | Endpoint                                     | Description                                   |
| ------ | -------------------------------------------- | --------------------------------------------- |
| POST   | `/api/v1/roadmaps/generate`                  | Generate a topic-based roadmap                |
| POST   | `/api/v1/roadmaps/generate-from-job`         | Generate a roadmap from a job-description PDF |
| GET    | `/api/v1/roadmaps`                           | Retrieve the user's confirmed roadmaps        |
| GET    | `/api/v1/roadmaps/{roadmap_id}`              | Retrieve a specific roadmap                   |
| DELETE | `/api/v1/roadmaps/{roadmap_id}`              | Delete a roadmap                              |
| POST   | `/api/v1/roadmaps/{roadmap_id}/suggest-edit` | Suggest changes to a draft roadmap            |
| POST   | `/api/v1/roadmaps/{roadmap_id}/confirm`      | Confirm and activate a roadmap                |

### 3. Assessment APIs

| Method | Endpoint                                     | Description                                |
| ------ | -------------------------------------------- | ------------------------------------------ |
| POST   | `/api/v1/assessments/generate`               | Generate an assessment for a roadmap topic |
| POST   | `/api/v1/assessments/{assessment_id}/submit` | Submit answers and receive evaluation      |

### 4. Company Preparation APIs

| Method | Endpoint                                              | Description                             |
| ------ | ----------------------------------------------------- | --------------------------------------- |
| GET    | `/api/v1/company-prep/companies`                      | Retrieve available companies            |
| GET    | `/api/v1/company-prep/companies/{company_slug}`       | Retrieve company information            |
| POST   | `/api/v1/company-prep/companies/{company_slug}/exams` | Generate a company-specific examination |
| POST   | `/api/v1/company-prep/exams/{exam_id}/submit`         | Submit and evaluate examination answers |

### 5. CV Review APIs

| Method | Endpoint                     | Description                           |
| ------ | ---------------------------- | ------------------------------------- |
| POST   | `/api/v1/cv-reviews/analyze` | Upload and analyze a CV in PDF format |

### 6. Profile APIs

| Method | Endpoint                      | Description                                              |
| ------ | ----------------------------- | -------------------------------------------------------- |
| GET    | `/api/v1/profile/performance` | Retrieve overall and subject-wise assessment performance |

### 7. General Backend Endpoints

| Method | Endpoint  | Description                                      |
| ------ | --------- | ------------------------------------------------ |
| GET    | `/`       | Check whether the backend application is running |
| GET    | `/health` | Check backend health status                      |

### Interactive API Documentation

FastAPI automatically provides interactive API documentation.

After starting the backend, visit:

http://localhost:8000/docs

Most application endpoints require JWT Bearer authentication.

---

## Development Commands

### Frontend Commands

Run these commands inside the `frontend` directory.

| Command           | Description                          |
| ----------------- | ------------------------------------ |
| `npm install`     | Install frontend dependencies        |
| `npm run dev`     | Start the development server         |
| `npm run build`   | Type-check and build the application |
| `npm run lint`    | Run Oxlint                           |
| `npm run preview` | Preview the production build         |

### Backend Commands

Run these commands inside the `backend` directory.

| Command                                     | Description                          |
| ------------------------------------------- | ------------------------------------ |
| `pip install -r requirements.txt`           | Install backend dependencies         |
| `uvicorn app.main:app --reload --port 8000` | Start the FastAPI development server |

---

## Deployment Configuration

CorePrep AI contains separate deployment configuration for its frontend and backend.

### Frontend Deployment

The frontend contains a `vercel.json` configuration file.

It uses URL rewrites to direct application routes to `index.html`, supporting client-side React Router navigation.

### Backend Deployment

The backend contains a `Procfile` with the following startup command:

```text
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

This allows the backend to start using the deployment platform's assigned port.

### Environment Configuration

The application uses environment variables to configure:

- Database connectivity.
- JWT authentication.
- Google OAuth credentials.
- Gemini or Ollama LLM providers.
- RAG retrieval settings.
- Frontend and backend URLs.
- CORS configuration.

Never upload private API keys, database passwords, or secret environment files to GitHub.

---

## Future Improvements

Potential areas for further development include:

- Expanding the learning knowledge base.
- Adding more company-specific interview question banks.
- Supporting additional assessment formats.
- Improving personalized learning recommendations.
- Enhancing performance analytics.
- Adding automated deployment and testing workflows.

---

## Repository

**GitHub:** https://github.com/Naveed2204016/CorePrep-AI
