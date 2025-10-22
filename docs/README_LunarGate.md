# World Observatorium – Lunar Gate Pack (v1)
Generated: 2025-10-18T06:50:34.107681Z

This drop-in pack adds Phase-3 domains (Storms/NOAA, Magnetosphere, Radiation) and Biofield HIF engine,
plus fixtures, tests, and an updated OpenAPI master spec.

## Contents
- actions/: OpenAPI schemas for new domains and HIF
- orchestrator/adapters/: NOAA alerts, geomag Kp, radiation flux + TTL cache helper
- orchestrator/services/: HIF engine
- fixtures/: three golden snapshots
- tests/: HIF monotonicity pytest
- scripts/: smoke_phase3.sh
- specs/: merged master OpenAPI (v1.2.0)

## Quick run
- Ensure your FastAPI app wires these adapters and exposes /snapshot/global with the new fields.
- Run tests: `python -m pytest -q`
- Smoke: `scripts/smoke_phase3.sh`
