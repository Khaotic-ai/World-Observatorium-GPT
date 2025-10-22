import requests
from .util_cache import ttl_cache

@ttl_cache(ttl_seconds=180)
def fetch_kp(hours=24):
    try:
        r = requests.get("https://services.swpc.noaa.gov/json/planetary_k_index_1m.json", timeout=10)
        r.raise_for_status()
        series = r.json() or []
        kp_values = [float(s.get("kp_index", 0)) for s in series[-hours:]]
        if not kp_values:
            return {"ok": False, "code":"E_EMPTY", "message":"No Kp data"}
        kp = kp_values[-1]
        trend = "steady"
        if len(kp_values) >= 3:
            d = kp_values[-1] - kp_values[-3]
            trend = "rising" if d > 0.3 else "falling" if d < -0.3 else "steady"
        return {"ok": True, "kpIndex": kp, "kpTrend": trend, "dstIndex": None, "sources": ["NOAA/SWPC"]}
    except Exception as e:
        return {"ok": False, "code": "E_UPSTREAM", "message": f"Kp error: {e}"}
