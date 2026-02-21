from fastapi import FastAPI
from src.app.api.routes import router as api_router

app = FastAPI(
    title="AI-Driven Data Platform Migration Tool",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}