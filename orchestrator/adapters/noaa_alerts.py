import requests, datetime as dt
from .util_cache import ttl_cache

@ttl_cache(ttl_seconds=60)
def fetch_alerts(lat=None, lon=None, radius_km=None, region=None, event=None):
    try:
        params = {"status": "actual"}
        if event: params["event"] = event
        r = requests.get("https://api.weather.gov/alerts", params=params, timeout=10)
        r.raise_for_status()
        data = r.json() or {}
        feats = data.get("features") or []
        alerts = []
        for f in feats:
            p = f.get("properties") or {}
            alerts.append({
                "id": f.get("id") or p.get("id"),
                "event": p.get("event"),
                "severity": p.get("severity"),
                "certainty": p.get("certainty"),
                "onset": p.get("onset"),
                "expires": p.get("expires"),
                "headline": p.get("headline"),
                "area": p.get("areaDesc"),
                "instruction": p.get("instruction"),
                "source": "NOAA/NWS"
            })
        return {"ok": True, "fetchedAt": dt.datetime.utcnow().isoformat() + "Z", "region": region, "alerts": alerts}
    except Exception as e:
        return {"ok": False, "code": "E_UPSTREAM", "message": f"NOAA error: {e}"}
