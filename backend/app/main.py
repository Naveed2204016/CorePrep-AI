import os

from fastapi import FastAPI

from app.db.database import Base, engine
from app.api.v1.auth import router as auth_router
from app.api.v1.roadmaps import router as roadmaps_router
from app.api.v1.assessments import router as assessments_router
from app.api.v1.cv_reviews import router as cv_reviews_router
from app.api.v1.company_prep import router as company_prep_router
from app.api.v1.profile import router as profile_router
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.models import roadmap, company_prep


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="CorePrep AI Backend"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "coreprep-dev-only-change-me")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv(
        "CORS_ORIGINS", "http://localhost:5173"
    ).split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(roadmaps_router)
app.include_router(assessments_router)
app.include_router(cv_reviews_router)
app.include_router(company_prep_router)
app.include_router(profile_router)

@app.get("/")
def home():

    return {
        "message":"CorePrep API running"
    }


@app.get("/health")
def health():
    return {"status": "ok"}
