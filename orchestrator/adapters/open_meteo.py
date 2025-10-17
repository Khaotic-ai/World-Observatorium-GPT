import requests
from orchestrator.cache import ttl_cache

@ttl_cache(ttl_seconds=45)
def fetch_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "UTC"
    }
    r = requests.get(url, params=params, timeout=8)
    r.raise_for_status()
    data = r.json() or {}
    cur = (data.get("current") or {})
    return {
        "ok": True,
        "temperatureC": cur.get("temperature_2m"),
        "humidityPct": cur.get("relative_humidity_2m"),
        "windSpeedMs": cur.get("wind_speed_10m"),
        "wmo": cur.get("weather_code"),
        "sources": ["Open-Meteo"]
    }
