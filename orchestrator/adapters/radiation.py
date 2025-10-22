import requests
from .util_cache import ttl_cache

@ttl_cache(ttl_seconds=300)
def fetch_flux(hours=24):
    try:
        r = requests.get("https://services.swpc.noaa.gov/json/goes/eps/avg_proton_flux_1m.json", timeout=10)
        r.raise_for_status()
        data = r.json() or []
        p10 = max([float(x.get("flux", 0)) for x in data[-hours:]] or [0.0])
        return {"ok": True, "radiationFlux": {"p10": p10}, "sources": ["NOAA/GOES"]}
    except Exception as e:
        return {"ok": False, "code":"E_UPSTREAM", "message": f"Radiation error: {e}"}
