from fastapi import FastAPI

from app.db.database import Base, engine
from app.api.v1.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="CorePrep AI Backend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    auth_router
)


@app.get("/")
def home():

    return {
        "message":"CorePrep API running"
    }