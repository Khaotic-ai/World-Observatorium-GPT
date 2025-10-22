#!/usr/bin/env python3
"""
World Observatorium — Global Snapshot Collector
© 2025 Khaotic-ai | CC BY-NC-SA 4.0
"""
import requests, datetime, json

LAT, LON = -25.95, 153.06
AIR_KEY = "81bad749-f55c-4e43-961e-36466e6dea68"
NASA_KEY = "phRrR5fLiKSwsWt32jlLfKqo3q7khXqm51BXUnfC"

def get_json(url):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"ok": False, "message": str(e)}

def snapshot():
    now = datetime.datetime.utcnow().isoformat() + "Z"
    one_day_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).isoformat()
    three_days_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=3)).date()

    return {
        "time": get_json("https://worldtimeapi.org/api/timezone/Etc/UTC"),
        "weather": get_json(f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code&timezone=UTC"),
        "air": get_json(f"https://api.airvisual.com/v2/nearest_city?lat={LAT}&lon={LON}&key={AIR_KEY}"),
        "quakes": get_json(f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={one_day_ago}&minmagnitude=3"),
        "solar": get_json(f"https://api.nasa.gov/DONKI/FLR?startDate={three_days_ago}&endDate={datetime.date.today()}&api_key={NASA_KEY}"),
        "timestamp": now
    }

if __name__ == "__main__":
    print(json.dumps(snapshot(), indent=2))
