#!/usr/bin/env bash
set -euo pipefail
BASE=${BASE:-http://localhost:8000}
LAT=${LAT:--25.95}
LON=${LON:-153.06}
echo "[snapshot]"; curl -fsS "$BASE/snapshot/global?lat=$LAT&lon=$LON" | jq '.ok,.biofield.coherence_score' || true
