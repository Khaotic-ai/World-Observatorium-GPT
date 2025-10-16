import requests

def fetch_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"}
    r = requests.get(url, params=params, timeout=5)
    data = r.json()
    return {
        "ok": True,
        "temperatureC": data.get("current", {}).get("temperature_2m"),
        "humidityPct": data.get("current", {}).get("relative_humidity_2m"),
        "windSpeedMs": data.get("current", {}).get("wind_speed_10m"),
        "sources": ["Open-Meteo"]
    }
