<<<<<<< Updated upstream

# --- Append to orchestrator/app.py ---
from orchestrator.adapters import swpc
from engine.live import coherence

@app.get("/solarwind/rt")
def get_solarwind_rt(hours: int = 48):
    df = swpc.bundle(hours=hours)
    return {
        "ok": True,
        "hours": hours,
        "count": len(df),
        "time": [t.isoformat() for t in df.index.to_pydatetime()],
        "kp": df["kp"].tolist() if "kp" in df else [],
        "bz_gsm": df["bz_gsm"].tolist() if "bz_gsm" in df else [],
        "bt": df["bt"].tolist() if "bt" in df else [],
        "solar_wind_speed": df["solar_wind_speed"].tolist() if "solar_wind_speed" in df else [],
        "density": df["density"].tolist() if "density" in df else [],
        "temperature": df["temperature"].tolist() if "temperature" in df else [],
        "proton_pfu": df["proton_pfu"].tolist() if "proton_pfu" in df else []
    }

@app.get("/coherence/eta")
def get_eta(lat: float, lon: float, hours: int = 48):
    df = coherence.compute_eta_timeseries(lat=lat, lon=lon, hours=hours)
    return {
        "ok": True,
        "hours": hours,
        "time": [t.isoformat() for t in df.index.to_pydatetime()],
        "eta": df["eta"].tolist()
    }
=======

# --- Append to orchestrator/app.py ---
from orchestrator.adapters import swpc
from engine.live import coherence

@app.get("/solarwind/rt")
def get_solarwind_rt(hours: int = 48):
    df = swpc.bundle(hours=hours)
    return {
        "ok": True,
        "hours": hours,
        "count": len(df),
        "time": [t.isoformat() for t in df.index.to_pydatetime()],
        "kp": df["kp"].tolist() if "kp" in df else [],
        "bz_gsm": df["bz_gsm"].tolist() if "bz_gsm" in df else [],
        "bt": df["bt"].tolist() if "bt" in df else [],
        "solar_wind_speed": df["solar_wind_speed"].tolist() if "solar_wind_speed" in df else [],
        "density": df["density"].tolist() if "density" in df else [],
        "temperature": df["temperature"].tolist() if "temperature" in df else [],
        "proton_pfu": df["proton_pfu"].tolist() if "proton_pfu" in df else []
    }

@app.get("/coherence/eta")
def get_eta(lat: float, lon: float, hours: int = 48):
    df = coherence.compute_eta_timeseries(lat=lat, lon=lon, hours=hours)
    return {
        "ok": True,
        "hours": hours,
        "time": [t.isoformat() for t in df.index.to_pydatetime()],
        "eta": df["eta"].tolist()
    }
>>>>>>> Stashed changes
