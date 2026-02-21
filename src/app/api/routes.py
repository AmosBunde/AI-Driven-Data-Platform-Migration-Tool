from fastapi import APIRouter
from pydantic import BaseModel
from src.agents.orchestrator import run_migration

router = APIRouter()

class MigrationRequest(BaseModel):
    input_path: str = "assets/legacy"
    output_path: str = "assets/reports/run_001"
    legacy_dialect: str = "postgres"
    target_dialect: str = "snowflake"

@router.post("/migrate")
def migrate(req: MigrationRequest):
    result = run_migration(
        input_path=req.input_path,
        output_path=req.output_path,
        legacy_dialect=req.legacy_dialect,
        target_dialect=req.target_dialect,
    )
    return result