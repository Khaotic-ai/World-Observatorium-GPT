<<<<<<< Updated upstream
<<<<<<< Updated upstream

from __future__ import annotations
import pandas as pd, requests
from dateutil import parser as dparser

def _resample10(df: pd.DataFrame) -> pd.DataFrame:
    return (df.sort_index()
              .resample("10min").mean()
              .interpolate(limit=3))

def fetch_kp_1m(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    js = requests.get(url, timeout=20).json()
    df = pd.DataFrame(js)
    # prefer explicit columns but keep fallbacks
    if "time_tag" in df: df["time"] = pd.to_datetime(df["time_tag"]) 
    else:                  df["time"] = pd.to_datetime(df.iloc[:,0])
    if "kp_index" in df: df["kp"]   = pd.to_numeric(df["kp_index"], errors="coerce")
    elif "estimated_kp" in df: df["kp"] = pd.to_numeric(df["estimated_kp"], errors="coerce")
    else: df["kp"] = pd.NA
    df = df[["time","kp"]].dropna().set_index("time").sort_index()
    return _resample10(df.last(f"{hours}h"))

def fetch_dscovr_plasma(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"
    js = requests.get(url, timeout=20).json()
    cols = js[0]; df = pd.DataFrame(js[1:], columns=cols)
    df["time"] = pd.to_datetime(df["time_tag"])
    for c in ("density","speed","temperature"): df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.set_index("time")[ ["density","speed","temperature"] ].dropna().sort_index()
    df = df.rename(columns={"speed":"solar_wind_speed"})
    return _resample10(df.last(f"{hours}h"))

def fetch_dscovr_mag(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/products/solar-wind/mag-6-hour.json"
    js = requests.get(url, timeout=20).json()
    cols = js[0]; df = pd.DataFrame(js[1:], columns=cols)
    df["time"] = pd.to_datetime(df["time_tag"])
    for c in ("bx_gsm","by_gsm","bz_gsm","bt"): df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.set_index("time")[ ["bx_gsm","by_gsm","bz_gsm","bt"] ].dropna().sort_index()
    return _resample10(df.last(f"{hours}h"))

def fetch_goes_protons(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-plot-1-day.json"
    js = requests.get(url, timeout=20).json()
    rows = []
    for r in js:
        if r.get("energy") == ">=10 MeV":
            rows.append((dparser.parse(r["time_tag"]), float(r["flux"])))
    df = pd.DataFrame(rows, columns=["time","proton_pfu"]).set_index("time").sort_index()
    return _resample10(df.last(f"{hours}h"))

def bundle(hours: int = 48) -> pd.DataFrame:
    kp = fetch_kp_1m(hours)
    mag = fetch_dscovr_mag(hours)
    plasma = fetch_dscovr_plasma(hours)
    pfu = fetch_goes_protons(hours)
    return pd.concat([kp, mag, plasma, pfu], axis=1).sort_index()
=======
=======
>>>>>>> Stashed changes

from __future__ import annotations
import pandas as pd, requests
from dateutil import parser as dparser

def _resample10(df: pd.DataFrame) -> pd.DataFrame:
    return (df.sort_index()
              .resample("10min").mean()
              .interpolate(limit=3))

def fetch_kp_1m(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    js = requests.get(url, timeout=20).json()
    df = pd.DataFrame(js)
    # prefer explicit columns but keep fallbacks
    if "time_tag" in df: df["time"] = pd.to_datetime(df["time_tag"]) 
    else:                  df["time"] = pd.to_datetime(df.iloc[:,0])
    if "kp_index" in df: df["kp"]   = pd.to_numeric(df["kp_index"], errors="coerce")
    elif "estimated_kp" in df: df["kp"] = pd.to_numeric(df["estimated_kp"], errors="coerce")
    else: df["kp"] = pd.NA
    df = df[["time","kp"]].dropna().set_index("time").sort_index()
    return _resample10(df.last(f"{hours}h"))

def fetch_dscovr_plasma(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"
    js = requests.get(url, timeout=20).json()
    cols = js[0]; df = pd.DataFrame(js[1:], columns=cols)
    df["time"] = pd.to_datetime(df["time_tag"])
    for c in ("density","speed","temperature"): df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.set_index("time")[ ["density","speed","temperature"] ].dropna().sort_index()
    df = df.rename(columns={"speed":"solar_wind_speed"})
    return _resample10(df.last(f"{hours}h"))

def fetch_dscovr_mag(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/products/solar-wind/mag-6-hour.json"
    js = requests.get(url, timeout=20).json()
    cols = js[0]; df = pd.DataFrame(js[1:], columns=cols)
    df["time"] = pd.to_datetime(df["time_tag"])
    for c in ("bx_gsm","by_gsm","bz_gsm","bt"): df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.set_index("time")[ ["bx_gsm","by_gsm","bz_gsm","bt"] ].dropna().sort_index()
    return _resample10(df.last(f"{hours}h"))

def fetch_goes_protons(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-plot-1-day.json"
    js = requests.get(url, timeout=20).json()
    rows = []
    for r in js:
        if r.get("energy") == ">=10 MeV":
            rows.append((dparser.parse(r["time_tag"]), float(r["flux"])))
    df = pd.DataFrame(rows, columns=["time","proton_pfu"]).set_index("time").sort_index()
    return _resample10(df.last(f"{hours}h"))

def bundle(hours: int = 48) -> pd.DataFrame:
    kp = fetch_kp_1m(hours)
    mag = fetch_dscovr_mag(hours)
    plasma = fetch_dscovr_plasma(hours)
    pfu = fetch_goes_protons(hours)
    return pd.concat([kp, mag, plasma, pfu], axis=1).sort_index()
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
