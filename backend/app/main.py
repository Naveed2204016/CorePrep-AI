from fastapi import FastAPI

app = FastAPI(
    title="CorePrep AI API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "CorePrep AI API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }