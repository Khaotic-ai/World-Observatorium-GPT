#!/usr/bin/env bash
set -euo pipefail
export PYTHONUNBUFFERED=1
exec uvicorn orchestrator.app:app --host 0.0.0.0 --port 8000 --reload
