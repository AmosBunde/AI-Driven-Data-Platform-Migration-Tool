#!/usr/bin/env bash
# scripts/make_dirs.sh
set -euo pipefail

ROOT_DIR="${1:-.}"

# Create directory tree
mkdir -p "$ROOT_DIR"/src/app/api
mkdir -p "$ROOT_DIR"/src/app/ui
mkdir -p "$ROOT_DIR"/src/agents
mkdir -p "$ROOT_DIR"/src/parsing/dialects
mkdir -p "$ROOT_DIR"/src/conversion
mkdir -p "$ROOT_DIR"/src/validation
mkdir -p "$ROOT_DIR"/src/orchestration
mkdir -p "$ROOT_DIR"/src/vector
mkdir -p "$ROOT_DIR"/src/config

mkdir -p "$ROOT_DIR"/assets/legacy
mkdir -p "$ROOT_DIR"/assets/reports
mkdir -p "$ROOT_DIR"/scripts
mkdir -p "$ROOT_DIR"/tests

# Create __init__.py markers (so imports work immediately)
touch "$ROOT_DIR"/src/__init__.py
touch "$ROOT_DIR"/src/app/__init__.py
touch "$ROOT_DIR"/src/app/api/__init__.py
touch "$ROOT_DIR"/src/app/ui/__init__.py
touch "$ROOT_DIR"/src/agents/__init__.py
touch "$ROOT_DIR"/src/parsing/__init__.py
touch "$ROOT_DIR"/src/parsing/dialects/__init__.py
touch "$ROOT_DIR"/src/conversion/__init__.py
touch "$ROOT_DIR"/src/validation/__init__.py
touch "$ROOT_DIR"/src/orchestration/__init__.py
touch "$ROOT_DIR"/src/vector/__init__.py
touch "$ROOT_DIR"/src/config/__init__.py

echo "✅ Project directories created under: $ROOT_DIR"
echo ""
echo "Next steps:"
echo "  - Add your .env (.env.example is recommended)"
echo "  - Run tests: ./scripts/run_tests.sh"