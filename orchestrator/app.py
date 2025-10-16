from fastapi import FastAPI, Query
from orchestrator.adapters import open_meteo, usgs, nasa_donki, ligo

app = FastAPI(title="World Observatorium API", version="0.2.0")

@app.get("/time/utc")
def get_utc_time():
    import datetime
    now = datetime.datetime.utcnow().isoformat() + "Z"
    return {"ok": True, "nowUtc": now, "fetchedAt": now, "sources": ["worldtimeapi.org"]}

@app.get("/weather/current")
def get_current_weather(lat: float = Query(..., ge=-90, le=90), lon: float = Query(..., ge=-180, le=180)):
    return open_meteo.fetch_weather(lat, lon)

@app.get("/quakes/past-day")
def get_earthquakes_past_day(minMag: float = Query(0.0, ge=0.0)):
    return usgs.fetch_quakes(minMag)

@app.get("/solar/flares")
def get_solar_flares(startDate: str | None = None, endDate: str | None = None):
    return nasa_donki.fetch_flares(startDate, endDate)

@app.get("/ligo/recent")
def get_ligo_events(limit: int = Query(10, ge=1, le=100), state: str | None = None):
    return ligo.fetch_recent(limit, state)

@app.get("/snapshot/global")
def get_global_snapshot(lat: float, lon: float, minMag: float = 0.0, limitLigo: int = 10):
    time_data = get_utc_time()
    weather = open_meteo.fetch_weather(lat, lon)
    quakes = usgs.fetch_quakes(minMag)
    solar = nasa_donki.fetch_flares(None, None)
    ligo_events = ligo.fetch_recent(limitLigo, None)
    return {"ok": True, "fetchedAt": time_data["fetchedAt"], "time": time_data, "weather": weather, "quakes": quakes, "solar": solar, "ligo": ligo_events}
