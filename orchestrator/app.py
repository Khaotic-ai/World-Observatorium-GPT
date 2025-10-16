from fastapi import FastAPI, Query
from orchestrator.adapters import open_meteo, usgs, nasa_donki, ligo

app = FastAPI(title="World Observatorium API", version="0.1.0")

@app.get("/time/utc")
def get_utc_time():
    import datetime
    now = datetime.datetime.utcnow().isoformat() + "Z"
    return {"ok": True, "nowUtc": now, "fetchedAt": now, "sources": ["worldtimeapi.org"]}

@app.get("/weather/current")
def get_current_weather(lat: float = Query(...), lon: float = Query(...)):
    return open_meteo.fetch_weather(lat, lon)

@app.get("/snapshot/global")
def get_global_snapshot(lat: float, lon: float):
    data = {
        "time": get_utc_time(),
        "weather": open_meteo.fetch_weather(lat, lon)
    }
    return {"ok": True, "fetchedAt": data["time"]["fetchedAt"], **data}
