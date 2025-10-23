
from __future__ import annotations
import numpy as np, pandas as pd
from .features import lunar_phase_fraction, resample10
from orchestrator.adapters import swpc

# Weighting for η components (can be tuned)
WEIGHTS = {
    "kp":0.16,"proton":0.12,"bz":0.12,"vsw":0.07,"dst":0.07,
    "aqi":0.12,"temp":0.12,"humidity":0.08,"wind":0.08,"seismic":0.06
}

def _score_temp(t):    return np.clip(1 - (np.abs(t-25)/12), 0, 1)
def _score_aqi(a):     return np.clip(1 - (a/150.0), 0, 1)
def _score_kp(k):      return np.clip(1 - (k/8.0), 0, 1)
def _score_pfu(p):     return np.clip(1 - (p/10.0), 0, 1)
def _score_wind(w):    return np.clip(1 - (np.abs(w-9)/20.0), 0, 1)
def _score_hum(h):     return np.clip(1 - (np.abs(h-50)/35.0), 0, 1)
def _score_bz(bz):     return np.clip(1 - (np.clip(-bz,0,None)/20.0), 0, 1)   # southward Bz hurts
def _score_vsw(v):     return np.clip(1 - (np.clip(v-400,0,None)/600.0), 0, 1)
def _score_dst(dst):   return np.clip(1 - (np.clip(-dst,0,None)/300.0), 0, 1)

def compute_eta_timeseries(lat: float, lon: float, hours: int = 48) -> pd.DataFrame:
    """Compute η(t) from available live drivers (PR‑1 bundle + optional surface inputs)."""
    sw = swpc.bundle(hours=hours)
    df = sw.copy()

    # Component scores based on available columns
    comps = pd.DataFrame(index=df.index)
    if "kp" in df:                  comps["kp"] = _score_kp(df["kp"])
    if "proton_pfu" in df:          comps["proton"] = _score_pfu(df["proton_pfu"])
    if "bz_gsm" in df:              comps["bz"] = _score_bz(df["bz_gsm"])
    if "solar_wind_speed" in df:    comps["vsw"] = _score_vsw(df["solar_wind_speed"])
    if "dst" in df:                 comps["dst"] = _score_dst(df["dst"])

    # Hooks for surface metrics once wired in your repo (BOM/IQAir/QLD DES)
    rename_map = {
        "tempC":"temp_c","humidityPct":"humidity_pct","windSpeed":"wind_kmh",
        "aqiUS":"aqi_us","seismicLocal":"seismic_local"
    }
    for src,dst in rename_map.items():
        if src in df and dst not in df:
            df[dst] = df[src]

    if "temp_c" in df:              comps["temp"] = _score_temp(df["temp_c"])
    if "humidity_pct" in df:        comps["humidity"] = _score_hum(df["humidity_pct"])
    if "wind_kmh" in df:            comps["wind"] = _score_wind(df["wind_kmh"])
    if "aqi_us" in df:              comps["aqi"] = _score_aqi(df["aqi_us"])
    if "seismic_local" in df:       comps["seismic"] = np.clip(1 - (df["seismic_local"]*10.0), 0, 1)

    # Normalize weights to available components
    w = {k:v for k,v in WEIGHTS.items() if k in comps.columns}
    weight_vec = pd.Series(w)
    df["eta"] = (comps.fillna(0) * weight_vec).sum(axis=1) / weight_vec.sum()
    return df
