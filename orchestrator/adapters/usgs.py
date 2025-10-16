
import requests
from typing import Any, Dict

USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

def fetch_quakes(minMag: float = 0.0) -> Dict[str, Any]:
    try:
        resp = requests.get(USGS_URL, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        events = []
        for f in data.get("features", []):
            props = f.get("properties", {}) or {}
            geom = f.get("geometry", {}) or {}
            coords = (geom.get("coordinates") or [None, None, None])
            mag = props.get("mag")
            if mag is None or (isinstance(minMag, (int, float)) and mag < float(minMag)):
                continue
            events.append({
                "id": f.get("id"),
                "time": datetime_from_ms(props.get("time")),
                "magnitude": mag,
                "place": props.get("place"),
                "depthKm": coords[2] if len(coords) > 2 else None,
                "coordinates": {"lat": coords[1], "lon": coords[0]} if len(coords) >= 2 else None
            })
        return {
            "ok": True,
            "source": "usgs:v1.0",
            "count": len(events),
            "minMag": float(minMag) if minMag is not None else 0.0,
            "events": events
        }
    except Exception as e:
        return {"ok": False, "code": "E_UPSTREAM", "message": f"USGS error: {e}"}

def datetime_from_ms(ms):
    try:
        if ms is None: return None
        import datetime
        return datetime.datetime.utcfromtimestamp(ms/1000.0).isoformat() + "Z"
    except Exception:
        return None
