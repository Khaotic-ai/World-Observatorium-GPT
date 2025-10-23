
# World Observatorium — Phase 3.2 Drop‑In

## What this adds
- **PR‑1**: `/solarwind/rt` — live Kp, Bz/Bt, solar wind speed/density/temp, proton flux (10‑min cadence).
- **PR‑2**: `/coherence/eta` — computed η(t) coherence from space‑weather (+ hooks for BOM/AQI/seismic).

## How to integrate (quick)
1. Copy `engine/live/*` into your repo under `engine/live/`.
2. Copy `orchestrator/adapters/swpc.py` into `orchestrator/adapters/`.
3. Append the contents of `app.append.routes.py` to `orchestrator/app.py`.
4. Merge `specs/observatorium.additions.yaml` into your OpenAPI master.
5. (Optional) Add packages from `requirements.additions.txt`.
6. Run server and hit:
   - `GET /solarwind/rt?hours=48`
   - `GET /coherence/eta?lat=-25.95&lon=152.62&hours=48`
