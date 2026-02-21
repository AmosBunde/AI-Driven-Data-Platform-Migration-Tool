import os
from pathlib import Path
from src.parsing.sql_parser import parse_assets
from src.conversion.query_rewriter import rewrite_queries
from src.conversion.ddl_generator import generate_ddl
from src.conversion.dbt_generator import generate_dbt_project
from src.validation.runner import run_validation
from src.agents.report_agent import build_report

def run_migration(input_path: str, output_path: str, legacy_dialect: str, target_dialect: str) -> dict:
    out = Path(output_path)
    out.mkdir(parents=True, exist_ok=True)

    parsed = parse_assets(input_path=input_path, legacy_dialect=legacy_dialect, output_dir=str(out / "lineage"))
    ddl_paths = generate_ddl(parsed, output_dir=str(out / "converted/ddl"), target_dialect=target_dialect)
    query_paths = rewrite_queries(parsed, output_dir=str(out / "converted/queries"), target_dialect=target_dialect)
    dbt_path = generate_dbt_project(parsed, output_dir=str(out / "converted/dbt_project"), target_dialect=target_dialect)

    validation = run_validation(parsed, output_dir=str(out / "validation"))
    report_path = build_report(parsed, validation, output_dir=str(out))

    return {
        "input_path": input_path,
        "output_path": output_path,
        "legacy_dialect": legacy_dialect,
        "target_dialect": target_dialect,
        "artifacts": {
            "ddl": ddl_paths,
            "queries": query_paths,
            "dbt_project": dbt_path,
            "report": report_path,
        },
        "validation_summary": validation.get("summary", {}),
    }