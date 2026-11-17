# Local Setup Guide

This guide summarizes the local setup documented for CorePrep AI. Check the root README and environment example files for the latest project-specific values.

## Prerequisites
- Python 3.10 or newer
- Node.js and npm
- MySQL Server
- Git
- Ollama only if you plan to use a local language model

## 1. Get the source

```bash
git clone https://github.com/Naveed2204016/CorePrep-AI.git
cd CorePrep-AI
```

## 2. Configure the backend

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `backend/.env` with your own database and AI-provider settings. Do not commit this file.

## 3. Configure MySQL

Create a local database:

```sql
CREATE DATABASE coreprep_ai
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Set `DATABASE_URL` in `backend/.env` using your own local MySQL username and password.

## 4. Configure the AI provider

For Gemini, set the provider and API key in the backend environment file. For Ollama, install and start Ollama, obtain the model documented by the project, and configure its local base URL and model name.

Never paste a real API key into a public repository.

## 5. Start the backend

From the backend directory:

```bash
uvicorn app.main:app --reload --port 8000
```

The README documents the API at `http://localhost:8000`, interactive API documentation at `/docs`, and health check at `/health`.

## 6. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
```

Create `frontend/.env` from `frontend/.env.example` and set the backend API base URL as needed. Then run:

```bash
npm run dev
```

The documented frontend development URL is `http://localhost:5173`.

## Troubleshooting
- Confirm MySQL is running and the database URL is correct.
- Confirm the selected AI provider is available and configured.
- Check backend and frontend terminals for error messages.
- Use the API documentation page to inspect available endpoints.
- Verify environment variable names against the current `.env.example` files.
