from fastapi import FastAPI, Query
from typing import List, Set
import datetime

from orchestrator.adapters import open_meteo
# Note: usgs, nasa_donki, and ligo modules are expected to already exist in the repo.
try:
    from orchestrator.adapters import usgs, nasa_donki, ligo
except Exception:
    usgs = nasa_donki = ligo = None  # graceful degradation for local drop-in

from orchestrator.models import SnapshotPayload, WMO_MAP

app = FastAPI(title="World Observatorium API", version="0.2.1")

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
    }
