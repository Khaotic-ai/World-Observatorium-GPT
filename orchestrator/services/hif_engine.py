
def compute(snapshot: dict) -> dict:
    try:
        w = (snapshot.get("weather") or {})
        a = (snapshot.get("air") or {})
        m = (snapshot.get("magnetosphere") or {})
        t = (snapshot.get("storms") or {})
        temp = float(w.get("temperatureC") or 22.0)
        rh   = float(w.get("humidityPct") or 50.0)
        aqi  = float(a.get("aqiUS") or 0.0)
        kp   = float(m.get("kpIndex") or 0.0)
        alerts = len((t.get("alerts") or []))
        comfort = max(0.0, 1.0 - abs((temp - 22.0)/15.0) - abs((rh - 50.0)/50.0))
        aqi_norm = 1.0 / (1.0 + (aqi/50.0))
        kp_norm  = 1.0 / (1.0 + (kp/3.0))
        stress = min(1.0, (kp/9.0) + (aqi/300.0) + (alerts*0.1))
        coherence = max(0.0, min(1.0, 0.4*comfort + 0.3*aqi_norm + 0.3*kp_norm - 0.2*stress))
        return {
            "ok": True,
            "coherence_score": round(coherence, 3),
            "hif_local": round(0.5*comfort + 0.5*aqi_norm, 3),
            "hif_cosmic": round(0.7*kp_norm + 0.3*(1.0-stress), 3),
            "stress_load": round(stress, 3),
            "notes": []
        }
    except Exception as e:
        return {"ok": False, "coherence_score": 0.0, "notes": [f"HIF error: {e}"]}
