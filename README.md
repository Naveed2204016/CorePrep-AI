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
