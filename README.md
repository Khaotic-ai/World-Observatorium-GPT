# 🌍 World Observatorium GPT

A planetary observatory backend for GPT Actions — integrating real-time data from weather, seismic, solar, and astrophysical sources into a unified API layer.

## Core Concepts
- Modular OpenAPI 3.1 specs for each data domain.
- Unified `/snapshot/global` endpoint for composite queries.
- Schema validation, caching, and normalization handled server-side.

## Architecture
GPT → Observatorium API (FastAPI) → Providers (Open-Meteo, USGS, NASA DONKI, LIGO)

## Quick Start
```bash
pip install -r requirements.txt
python orchestrator/app.py
```
