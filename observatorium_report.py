
import os, json, datetime
from datetime import timezone as TZ
import requests, tomllib

CFG_PATH = os.path.join(os.path.dirname(__file__), "config.toml")
with open(CFG_PATH, "rb") as f:
    cfg = tomllib.load(f)

BASE = cfg.get("BASE", "").rstrip("/")
LAT  = cfg.get("LAT", -25.95)
LON  = cfg.get("LON", 153.06)

def get_json(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def snapshot():
    url = f"{BASE}/snapshot/global?lat={LAT}&lon={LON}"
    data = get_json(url)
    now = datetime.datetime.now(TZ.utc).isoformat()
    if isinstance(data, dict):
        data.setdefault("fetchedAt", now)
    return data

def generate_report(data: dict) -> str:
    time_obj = data.get("time") or {}
    weather  = data.get("weather") or {}
    air      = data.get("air") or {}
    quakes   = data.get("quakes") or {}
    solar    = data.get("solar") or {}
    storms   = data.get("storms") or {}
    magneto  = data.get("magnetosphere") or {}
    rad      = data.get("radiation") or {}
    bio      = data.get("biofield") or {}

    temp = weather.get("temperatureC")
    hum  = weather.get("humidityPct")
    wind = weather.get("windSpeedMs")
    wmo  = weather.get("wmo")

    aqi  = air.get("aqiUS")
    pm25 = air.get("pm25")

    events = quakes.get("events") or []
    quake_count = len(events)
    last_place = last_mag = None
    if events:
        last_place = events[0].get("place")
        last_mag   = events[0].get("magnitude")

    flares = solar.get("flares") or []
    flare_count = len(flares)
    last_class = flares[0].get("class") if flares else None
    last_peak  = flares[0].get("peakTime") if flares else None

    storm_count = len(storms.get("alerts") or [])
    kp = magneto.get("kpIndex")
    kp_trend = magneto.get("kpTrend")
    p10 = (rad.get("radiationFlux") or {}).get("p10")
    coh = bio.get("coherence_score")

    location = "Cooloola Cove, QLD"
    timestamp = data.get("fetchedAt") or time_obj.get("nowUtc")

    report = f"""
🌎 OBSERVATORIUM REPORT — {location}
Timestamp (UTC): {timestamp}
Domains: Time | Weather | Air | Seismic | Solar | Storms | Magnetosphere | Radiation | Biofield

🌤 Weather: {temp} °C, {hum} %, {wind} m/s — WMO {wmo}
🌬 Air: AQI {aqi}, PM₂.₅ {pm25} µg/m³
🌋 Seismic: {quake_count} events ≥M3.0; latest {last_place} M{last_mag}
☀️ Solar: {flare_count} flares; last {last_class} at {last_peak}
🌪 Storms: {storm_count} alerts
🧲/🛰 Kp {kp} ({kp_trend}); p10 {p10}
💠 Biofield: coherence {coh}
✅ Status: {data.get("status","partial")}
© 2025 Khaotic-ai | World Observatorium Project
""".strip()
    return report

def main():
    data = snapshot()
    print(generate_report(data))
    with open("snapshot_last.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()
