# AI-Driven Data Platform Migration Tool
**Legacy SQL → Snowflake-Style Warehouse (Schema + ETL + Query Conversion + Validation)**

## Overview
This project is an agentic migration tool that reads legacy SQL schemas, ETL scripts, and queries, then produces a target “Snowflake-style” warehouse implementation (DDL + transformed queries + dbt models). It validates correctness by executing test queries on sample data in a legacy environment and comparing results to a target environment, flagging mismatches and generating migration reports.

**Primary outputs**
- Converted warehouse schema (DDL)
- Rewritten SQL for the target warehouse
- Generated dbt models + tests
- Validation runs (row counts / checksums / sampled diffs / query output diffs)
- Migration reports (Markdown/HTML/JSON)

---

## Key Features
- **AI agents** to interpret legacy SQL + ETL scripts and convert them into a target warehouse design
- **SQL parsing + normalization** for deterministic transformations where possible
- **dbt generation**: models, sources, tests, and macros (as needed)
- **Validation harness** to compare legacy vs target results with configurable strategies
- **Vector search** (FAISS local or Pinecone cloud) for retrieval of mapping rules, docs, and prior conversions
- **Containerized runtime** with Docker for consistent local and cloud execution
- **Simple Web UI** to upload assets, run migrations, and review results

---

## Tech Stack
- **Python**
- **LangChain / AutoGen** (agents)
- **SQL parser** (recommended: `sqlglot`)
- **Postgres test DB** (legacy execution)
- **Airflow/dbt pipeline simulator** (or real invocations)
- **Vector store**: FAISS (local) or Pinecone (cloud)
- **Docker / Docker Compose**
- **Web UI**: FastAPI (recommended) + minimal frontend

---

## What It Does (End-to-End)
1. **Ingest** legacy SQL + ETL scripts (files or folders)
2. **Parse** SQL into AST, extract objects/features, build lineage graph
3. **Convert**
   - Generate target warehouse schema (DDL)
   - Rewrite queries for target dialect
   - Generate dbt models and tests
4. **Validate**
   - Run legacy queries on a test Postgres dataset
   - Run target queries on Snowflake (or target simulator)
   - Compare outputs; flag mismatches
5. **Report**
   - Conversion summary and confidence
   - Validation results and diffs
   - Actionable migration notes

---

## Suggested Repo Layout
If your repo differs, update this section to match your actual structure.

```
.
├─ README.md
├─ docker-compose.yml
├─ Dockerfile
├─ .env.example
├─ requirements.txt / pyproject.toml
├─ src/
│  ├─ app/
│  │  ├─ main.py                 # web UI + API entry
│  │  ├─ api/                    # endpoints
│  │  └─ ui/                     # minimal frontend
│  ├─ agents/
│  │  ├─ orchestrator.py
│  │  ├─ schema_agent.py
│  │  ├─ query_agent.py
│  │  ├─ etl_agent.py
│  │  └─ report_agent.py
│  ├─ parsing/
│  │  ├─ sql_parser.py
│  │  ├─ lineage.py
│  │  └─ dialects/
│  ├─ conversion/
│  │  ├─ mappings.py
│  │  ├─ ddl_generator.py
│  │  ├─ query_rewriter.py
│  │  └─ dbt_generator.py
│  ├─ validation/
│  │  ├─ runner.py
│  │  ├─ comparators.py
│  │  └─ fixtures.py
│  ├─ orchestration/
│  │  ├─ airflow_sim.py
│  │  └─ dbt_sim.py
│  ├─ vector/
│  │  ├─ store.py
│  │  └─ embedding.py
│  └─ config/
│     └─ settings.py
├─ assets/
│  ├─ legacy/                    # sample legacy assets
│  └─ reports/                   # generated outputs
└─ scripts/
   ├─ bootstrap_local.sh
   ├─ run_migration.py
   └─ seed_sample_data.py
```

---

## Architecture
### Inputs
- Legacy DDL (schemas/tables/views)
- Legacy queries (views, stored procedures, ad hoc SQL)
- ETL definitions (SQL scripts, orchestrator configs, Python jobs, etc.)
- Optional docs: naming conventions, data dictionary, mapping rules, historical examples

### Processing Stages
- **Ingestion** → file classification + chunking + metadata
- **Parsing** → AST normalization + feature detection
- **Lineage** → build dependency and transformation graph
- **Conversion** → target DDL + SQL rewrite + dbt generation
- **Validation** → execute + compare + diff
- **Reporting** → structured JSON + human-readable report

---

## Requirements

### Local (recommended)
- Docker + Docker Compose
- Optional (non-Docker dev): Python 3.10+, Postgres 14+

### Cloud (recommended)
- Container runtime (Cloud Run / ECS Fargate / Azure Container Apps)
- Object storage for artifacts (S3/GCS/Azure Blob)
- Pinecone (optional) for vector store
- Snowflake (optional) for real target validation

---

## Configuration

All configuration should be environment-driven to keep local and cloud symmetric.

### `.env` (example)
Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

Minimum for local runs (FAISS + Postgres):
- `RUN_MODE=local`
- `APP_PORT=8080`
- `LOG_LEVEL=INFO`

LLM (examples):
- `LLM_PROVIDER=openai|azure_openai|...`
- `LLM_API_KEY=...`
- `LLM_MODEL=...`

Vector:
- `VECTOR_BACKEND=faiss|pinecone`
- Pinecone (if used):
  - `PINECONE_API_KEY=...`
  - `PINECONE_INDEX=...`

Legacy DB (Postgres):
- `POSTGRES_HOST=postgres`
- `POSTGRES_PORT=5432`
- `POSTGRES_DB=legacy`
- `POSTGRES_USER=legacy`
- `POSTGRES_PASSWORD=legacy`

Target (Snowflake, optional):
- `TARGET_WAREHOUSE=snowflake|simulator`
- `SNOWFLAKE_ACCOUNT=...`
- `SNOWFLAKE_USER=...`
- `SNOWFLAKE_PASSWORD=...` *(or use keypair auth)*
- `SNOWFLAKE_ROLE=...`
- `SNOWFLAKE_WAREHOUSE=...`
- `SNOWFLAKE_DATABASE=...`
- `SNOWFLAKE_SCHEMA=...`

Validation:
- `VALIDATION_MODE=fast|full`
- `COMPARE_STRATEGY=hash|rowdiff|aggregate`
- `ROW_SAMPLE_SIZE=1000`
- `FLOAT_TOLERANCE=0.0001`
- `TIMEZONE_DEFAULT=UTC`

---

## Quickstart (Local via Docker)

### 1) Start services
```bash
docker compose up --build
```

### 2) Seed sample data (optional)
```bash
docker compose exec app python scripts/seed_sample_data.py
```

### 3) Run a migration (CLI)
```bash
docker compose exec app python scripts/run_migration.py \
  --input assets/legacy \
  --output assets/reports/run_001
```

### 4) Run via Web UI (if provided)
Open:
- `http://localhost:8080`

---

## Running Without Docker (Local Dev)

### 1) Create and activate a virtualenv
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Start Postgres (via Docker, simplest)
```bash
docker run --name legacy-postgres \
  -e POSTGRES_PASSWORD=legacy \
  -e POSTGRES_USER=legacy \
  -e POSTGRES_DB=legacy \
  -p 5432:5432 \
  -d postgres:15
```

### 3) Export env vars and start the app
```bash
export $(cat .env | xargs)
python -m src.app.main
```

---

## Implementation Notes (How to Build It Properly)

### SQL Parsing and Normalization
**Goal:** turn legacy SQL into a normalized representation so conversions are repeatable.

Minimum responsibilities:
- Parse DDL + DML into AST
- Detect dialect-specific features
- Extract tables/columns/joins/filters/functions
- Emit:
  - normalized AST
  - dependency graph (views/procs → tables)
  - feature flags (e.g., QUALIFY needed, date function rewrites, etc.)

**Recommended approach**
- Use `sqlglot` to parse multiple dialects and transpile where possible
- For hard edge cases, fall back to agent-based rewriting with constrained prompts

### Deterministic Mapping Rules First
Keep mappings centralized (e.g., `src/conversion/mappings.py`):
- Data type mappings
- Function mappings
- Syntax rewrites
- Identifier casing and naming conventions

Use agents primarily for:
- ambiguous transformations
- missing context inference
- complex ETL refactors spanning multiple statements/files

### Agent Orchestration (LangChain/AutoGen)
A practical staged pipeline:

1. **IngestAgent**
   - classify files (ddl/query/etl/doc)
   - chunk and index in vector store
2. **SchemaAgent**
   - create target DDL
   - emit constraints + clustering suggestions (where relevant)
3. **QueryAgent**
   - rewrite queries in target dialect
   - produce test queries where useful
4. **DbtAgent**
   - generate dbt project structure and models
5. **ValidationAgent**
   - execute legacy vs target queries
   - compare results and produce diffs
6. **ReportAgent**
   - compile final human-readable report + JSON summary

**Strong recommendation:**  
Every stage should output a structured JSON artifact plus its generated files on disk. This makes debugging and cloud execution far easier.

---

## Validation Strategy (Credibility Layer)

### Comparison modes
- **Schema checks**
  - columns present
  - data type compatibility within expected mapping
- **Data checks**
  - row counts
  - null counts by column
  - checksums/hashes for stable columns
  - aggregates by key (min/max/sum/count)
- **Query output checks**
  - canonicalize ordering
  - normalize floats using tolerance
  - sample-based comparisons for very large outputs

### Typical outputs
- `validation/results.json`
- `validation/diffs/*`
- `report.md`

---

## Output Artifacts (Expected)
A migration run should produce an output folder like:

```
assets/reports/run_001/
├─ converted/
│  ├─ ddl/
│  ├─ queries/
│  └─ dbt_project/
├─ validation/
│  ├─ results.json
│  └─ diffs/
├─ lineage/
│  └─ graph.json
└─ report.md
```

---

## Deployment (Cloud)

### Option A: Containerized API (recommended)
Deploy the Docker image to:
- AWS ECS/Fargate
- GCP Cloud Run
- Azure Container Apps

Use managed services for:
- secrets management (Secrets Manager / Secret Manager / Key Vault)
- object storage for artifacts (S3/GCS/Blob)
- Pinecone (optional) for vector retrieval
- Snowflake (optional) for target validation

**Cloud best practices**
- Store run artifacts in object storage (not ephemeral disk)
- Use IAM/workload identity for storage access
- Keep LLM keys and Snowflake credentials in a secret manager
- Avoid logging raw customer data and query outputs

### Option B: Batch Worker
For heavy migrations:
- API accepts job → stores inputs in object storage → enqueues message
- Worker pulls job → runs conversion + validation → stores outputs
- API serves status + downloads

---

## CI/CD (Baseline)

### Suggested checks
- Linting (ruff/flake8)
- Unit tests:
  - mappings
  - parser normalization
  - comparators
- Integration test:
  - docker compose up
  - run a small migration input
  - assert required artifacts exist and validation schema passes

### Typical pipeline
1. lint
2. unit tests
3. build image
4. integration tests (compose)
5. push image
6. deploy

---

## Troubleshooting

### Migrations fail immediately
- Verify `LLM_API_KEY` and `LLM_MODEL`
- Confirm container has outbound network access
- Check logs for provider auth errors

### SQL parsing errors
- Ensure correct legacy dialect configuration (e.g., `LEGACY_DIALECT=tsql|oracle|postgres`)
- Add dialect-specific rewrite rules before agent rewriting
- Persist parse failures as artifacts for review

### Validation mismatches
- Enforce stable ordering for comparisons
- Normalize timestamps/timezones
- Apply float tolerance for numeric diffs
- For huge result sets, use aggregate comparisons + sampling

### Pinecone issues
- Ensure index exists and API key is correct
- Ensure region/environment config is correct
- For local runs, switch to `VECTOR_BACKEND=faiss`

---

## Security Notes
- Do not log secrets or raw data
- Use least-privilege DB roles
- Prefer read-only access for validation
- Keep production isolated from validation environments

---

## Roadmap Ideas
- Conversion confidence score per object/query
- Auto-generated reconciliation SQL for failed diffs
- Better sampling strategies for very large tables
- Multi-target support (BigQuery/Redshift) using adapter interfaces
- Cost-aware Snowflake validation execution planner

---

## License
Add your license here.
