from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    run_mode: str = os.getenv("RUN_MODE", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4.1-mini")

    vector_backend: str = os.getenv("VECTOR_BACKEND", "faiss")

    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db: str = os.getenv("POSTGRES_DB", "legacy")
    postgres_user: str = os.getenv("POSTGRES_USER", "legacy")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "legacy")

    target_warehouse: str = os.getenv("TARGET_WAREHOUSE", "simulator")

settings = Settings()