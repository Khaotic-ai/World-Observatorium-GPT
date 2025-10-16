
import os
import requests
import datetime as dt
from typing import Any, Dict

DONKI_URL = "https://api.nasa.gov/DONKI/FLR"

def fetch_flares(start_date: str = None, end_date: str = None) -> Dict[str, Any]:
    try:
        api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
        if start_date is None or end_date is None:
            today = dt.datetime.utcnow().date().isoformat()
            start_date = start_date or today
            end_date = end_date or today
        params = {"startDate": start_date, "endDate": end_date, "api_key": api_key}
        r = requests.get(DONKI_URL, params=params, timeout=12)
        r.raise_for_status()
        arr = r.json() if r.text else []
        flares = []
        for item in arr or []:
            flares.append({
                "flrId": item.get("flrID"),
                "class": (item.get("classType") or "").strip() or None,
                "beginTime": item.get("beginTime"),
                "peakTime": item.get("peakTime"),
                "endTime": item.get("endTime"),
                "location": (item.get("sourceLocation") or "").strip() or None
            })
        return {"ok": True, "source": "nasa_donki:FLR", "flares": flares, "window": {"startDate": start_date, "endDate": end_date}}
    except Exception as e:
        return {"ok": False, "code": "E_UPSTREAM", "message": f"DONKI error: {e}"}
