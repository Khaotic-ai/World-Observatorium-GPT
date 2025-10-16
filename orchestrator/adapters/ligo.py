
import requests
from typing import Any, Dict

GRACEDB_URL = "https://gracedb.ligo.org/apiweb/superevents/"

def fetch_recent(limit: int = 10, state: str = None) -> Dict[str, Any]:
    try:
        params = {"format": "json", "limit": int(limit)}
        if state:
            params["state"] = state
        r = requests.get(GRACEDB_URL, params=params, timeout=12)
        r.raise_for_status()
        data = r.json() or {}
        events = []
        for e in (data.get("superevents") or []):
            events.append({
                "eventId": e.get("superevent_id"),
                "created": e.get("created"),
                "far": e.get("far"),
                "labels": e.get("labels") or [],
                "url": e.get("links", {}).get("self")
            })
        return {"ok": True, "source": "ligo:gracedb", "limit": int(limit), "events": events}
    except Exception as e:
        return {"ok": False, "code": "E_UPSTREAM", "message": f"LIGO error: {e}"}
