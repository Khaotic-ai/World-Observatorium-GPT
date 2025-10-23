<<<<<<< Updated upstream
<<<<<<< Updated upstream
# World Observatorium — Orchestrator App (updated)
# NOTE: This file includes the robust /solarwind/rt route (NaN-safe) you requested.
# It also provides /time/utc and /coherence/eta for convenience.
# If your original app.py had additional routes, you can merge them back after replacement.

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
from fastapi import FastAPI, HTTPException

<<<<<<< Updated upstream
@app.get("/time/utc")
def get_utc_time():
    now = datetime.datetime.utcnow().isoformat() + "Z"
    return {"ok": True, "nowUtc": now, "fetchedAt": now, "sources": ["worldtimeapi.org"]}

@app.get("/weather/current")
def get_current_weather(lat: float = Query(..., ge=-90, le=90),
                        lon: float = Query(..., ge=-180, le=180)):
    return open_meteo.fetch_weather(lat, lon)

@app.get("/snapshot/global", response_model=SnapshotPayload)
def get_global_snapshot(
    lat: float,
    lon: float,
    minMag: float = 0.0,
    include: str = "time,weather,quakes,solar,ligo"
):
    include_set: Set[str] = {s.strip() for s in include.split(",") if s.strip()}
    missing: List[str] = []

    # Time
    try:
        time_data = get_utc_time()
        fetched_at = time_data.get("fetchedAt", "")
    except Exception:
        time_data = None
        fetched_at = ""
        missing.append("time")

    # Weather
    weather = None
    if "weather" in include_set:
        try:
            w = open_meteo.fetch_weather(lat, lon)
            if w.get("wmo") is not None:
                try:
                    w["wmo_text"] = WMO_MAP.get(int(w["wmo"]), "Unknown")
                except Exception:
                    w["wmo_text"] = "Unknown"
            weather = w
        except Exception:
            missing.append("weather")

    quakes = solar = ligo_events = None
    if "quakes" in include_set and usgs:
        try:
            quakes = usgs.fetch_quakes(minMag)
        except Exception:
            missing.append("quakes")
    elif "quakes" in include_set and not usgs:
        missing.append("quakes")

    if "solar" in include_set and nasa_donki:
        try:
            solar = nasa_donki.fetch_flares(None, None)
        except Exception:
            missing.append("solar")
    elif "solar" in include_set and not nasa_donki:
        missing.append("solar")

    if "ligo" in include_set and ligo:
        try:
            ligo_events = ligo.fetch_recent(10, None)
        except Exception:
            missing.append("ligo")
    elif "ligo" in include_set and not ligo:
        missing.append("ligo")

    status = "complete" if not missing else ("partial" if any([time_data, weather, quakes, solar, ligo_events]) else "error")
    return {
        "ok": status != "error",
        "status": status,
        "fetchedAt": fetched_at,
        "missingDomains": missing,
        "time": time_data,
        "weather": weather,
        "quakes": quakes,
        "solar": solar,
        "ligo": ligo_events
=======
from orchestrator.adapters import swpc
from engine.live import coherence

app = FastAPI(title="World Observatorium API")

@app.get("/time/utc")
def time_utc():
    return {"utc": datetime.now(timezone.utc).isoformat()}

# ---------------------
# UPDATED ROUTE (safe)
# ---------------------
@app.get("/solarwind/rt")
def get_solarwind_rt(hours: int = 24):
    """
    Real-time solar wind bundle (10-min cadence).
    Returns only present keys and converts NaN -> None for JSON safety.
    """
    try:
        df = swpc.bundle(hours=hours)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"swpc bundle fetch failed: {e}")

    if df is None or df.empty:
        return {"ok": True, "hours": hours, "count": 0, "time": [], "data": {}}

    # Make JSON-safe: replace NaN with None
    df = df.copy()
    df = df.where(pd.notnull(df), None)

    # Build payload dynamically from existing columns
    payload = {
        "ok": True,
        "hours": int(hours),
        "count": int(len(df)),
        "time": [t.isoformat() for t in df.index.to_pydatetime()],
        "data": {}
    }

    for col in df.columns:
        try:
            payload["data"][col] = df[col].tolist()
        except Exception:
            # Last-ditch: coerce values defensively
            series = df[col]
            payload["data"][col] = [None if (v is None) else float(v) for v in series.fillna(None).tolist()]

    return payload

@app.get("/coherence/eta")
def get_eta(lat: float, lon: float, hours: int = 48):
    """
    Compute η (biofield coherence) time-series at a site.
    """
    try:
        df = coherence.compute_eta_timeseries(lat=lat, lon=lon, hours=hours)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"eta computation failed: {e}")

    if df is None or df.empty or "eta" not in df:
        return {"ok": True, "hours": hours, "time": [], "eta": []}

    return {
        "ok": True,
        "hours": hours,
        "time": [t.isoformat() for t in df.index.to_pydatetime()],
        "eta": df["eta"].tolist()
>>>>>>> Stashed changes
    }
=======
=======
>>>>>>> Stashed changes
# World Observatorium — Orchestrator App (updated)
# NOTE: This file includes the robust /solarwind/rt route (NaN-safe) you requested.
# It also provides /time/utc and /coherence/eta for convenience.
# If your original app.py had additional routes, you can merge them back after replacement.

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
from fastapi import FastAPI, HTTPException

from orchestrator.adapters import swpc
from engine.live import coherence

app = FastAPI(title="World Observatorium API")

@app.get("/time/utc")
def time_utc():
    return {"utc": datetime.now(timezone.utc).isoformat()}

# ---------------------
# UPDATED ROUTE (safe)
# ---------------------
@app.get("/solarwind/rt")
def get_solarwind_rt(hours: int = 24):
    """
    Real-time solar wind bundle (10-min cadence).
    Returns only present keys and converts NaN -> None for JSON safety.
    """
    try:
        df = swpc.bundle(hours=hours)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"swpc bundle fetch failed: {e}")

    if df is None or df.empty:
        return {"ok": True, "hours": hours, "count": 0, "time": [], "data": {}}

    # Make JSON-safe: replace NaN with None
    df = df.copy()
    df = df.where(pd.notnull(df), None)

    # Build payload dynamically from existing columns
    payload = {
        "ok": True,
        "hours": int(hours),
        "count": int(len(df)),
        "time": [t.isoformat() for t in df.index.to_pydatetime()],
        "data": {}
    }

    for col in df.columns:
        try:
            payload["data"][col] = df[col].tolist()
        except Exception:
            # Last-ditch: coerce values defensively
            series = df[col]
            payload["data"][col] = [None if (v is None) else float(v) for v in series.fillna(None).tolist()]

    return payload

@app.get("/coherence/eta")
def get_eta(lat: float, lon: float, hours: int = 48):
    """
    Compute η (biofield coherence) time-series at a site.
    """
    try:
        df = coherence.compute_eta_timeseries(lat=lat, lon=lon, hours=hours)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"eta computation failed: {e}")

    if df is None or df.empty or "eta" not in df:
        return {"ok": True, "hours": hours, "time": [], "eta": []}

    return {
        "ok": True,
        "hours": hours,
        "time": [t.isoformat() for t in df.index.to_pydatetime()],
        "eta": df["eta"].tolist()
    }
>>>>>>> Stashed changes
