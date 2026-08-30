# Run the topic-roadmap feature locally

The implemented RAG stack is entirely local and does not require a paid API:

- LLM: Qwen 2.5 7B Instruct, served by Ollama.
- Vector database: persistent embedded Qdrant.
- Embeddings: `BAAI/bge-small-en-v1.5`, executed by FastEmbed/ONNX.
- Application database: MySQL.

Python 3.10–3.14 and Node.js are required. The first vector-index run downloads the embedding model, and the Ollama pull downloads approximately 4.7 GB.

## 1. Install and prepare Ollama

Install Ollama from <https://ollama.com/download>, then open a terminal:

```powershell
ollama pull qwen2.5:7b-instruct
ollama run qwen2.5:7b-instruct
```

After it answers once, enter `/bye`. Ollama continues running in the background. Confirm it from another terminal:

```powershell
ollama list
curl.exe http://localhost:11434/api/tags
```

## 2. Configure and start MySQL

Create the database if it does not already exist:

```sql
CREATE DATABASE coreprep_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

If the roadmap tables already exist from the earlier prototype, run [`backend/migrations/001_topic_roadmap_days.sql`](../backend/migrations/001_topic_roadmap_days.sql) once. Do not run it against a fresh database.

## 3. Set up the FastAPI backend

From the repository root in PowerShell:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `backend/.env`:

```dotenv
DATABASE_URL=mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost:3306/coreprep_ai
SECRET_KEY=replace-this-with-a-long-random-value
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b-instruct
VECTOR_DB_PATH=./data/vector_db
QDRANT_COLLECTION=dsa_corpus
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
CORS_ORIGINS=http://localhost:5173
BACKEND_PUBLIC_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

Build and test the semantic index. The first command downloads the embedding model:

```powershell
python -m scripts.index_dsa
uvicorn app.main:app --reload --port 8000
```

Keep this terminal open. Check <http://localhost:8000/health> and <http://localhost:8000/docs>.

## 4. Set up the React frontend

Open a second PowerShell terminal at the repository root:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

The frontend `.env` must contain:

```dotenv
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_USE_MOCK_AUTH=false
```

Open <http://localhost:5173>, create an account, sign in, choose **Create Roadmap**, select **Data Structures & Algorithms**, choose 4/6/8/10 weeks, and generate the roadmap. You can suggest an edit, confirm the result, and then reopen the confirmed roadmap from the profile page.

## 5. What happens during generation

1. Markdown files under `backend/data/dsa` are divided by headings.
2. Large sections are split into overlapping chunks.
3. FastEmbed converts chunks into 384-dimensional semantic vectors.
4. Embedded Qdrant persists them under `backend/data/vector_db`.
5. The user request retrieves the ten most semantically relevant chunks.
6. Qwen receives those chunks and returns a schema-constrained roadmap.
7. FastAPI validates and normalizes the response before saving it in MySQL.

Changing a corpus file, embedding model, or chunk setting automatically causes a clean re-index on the next backend start or generation request.

## Deployment warning

Vercel can still host the frontend. A local Ollama URL cannot be reached from Railway. For Railway deployment, Ollama must run as a separate reachable service with enough memory and persistent model storage, and `OLLAMA_BASE_URL` must point to it. The Qwen 2.5 7B Ollama artifact is about 4.7 GB, so verify that the selected hosting plan has sufficient RAM and storage. Embedded Qdrant also needs a Railway persistent volume mounted at the directory configured by `VECTOR_DB_PATH`; otherwise its index is lost on redeployment.
