#!/usr/bin/env bash
# scripts/run_tests.sh
set -euo pipefail

ROOT_DIR="${1:-.}"
cd "$ROOT_DIR"

# Prefer Docker if docker-compose.yml exists
if [[ -f "docker-compose.yml" ]]; then
  echo "🐳 docker-compose.yml found. Running tests in container..."

  # Ensure .env exists (compose may try to load it)
  if [[ ! -f ".env" && -f ".env.example" ]]; then
    cp .env.example .env
    echo "📝 Created .env from .env.example"
  fi

  docker compose build
  docker compose run --rm app pytest -q
  echo "✅ Tests completed (Docker)."
  exit 0
fi

# Fallback to local pytest
echo "🧪 docker-compose.yml not found. Running tests locally..."

if [[ ! -d ".platform" ]]; then
  echo "⚠️  No virtualenv found at .platform"
  echo "    Create it with:"
  echo "      python3 -m venv .platform"
  echo "      source .platform/bin/activate"
  echo "      pip install -r requirements.txt"
  exit 1
fi

# shellcheck disable=SC1091
source .platform/bin/activate
pytest -q
echo "✅ Tests completed (local)."
