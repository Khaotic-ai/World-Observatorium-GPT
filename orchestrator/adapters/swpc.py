<<<<<<< Updated upstream

from __future__ import annotations

import pandas as pd
import requests


UTC = "UTC"


def _as_utc_index(df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    """
    Ensure index is tz-aware UTC DatetimeIndex.
    """
    t = pd.to_datetime(df[time_col], utc=True, errors="coerce")
    out = df.copy()
    out = out.set_index(t).drop(columns=[time_col])
    out.index = out.index.tz_convert(UTC)  # no-op but explicit
    out = out.sort_index()
    return out


def _window_hours(df: pd.DataFrame, hours: int) -> pd.DataFrame:
    """
    Return the trailing {hours} hours using a mask (avoid deprecated .last()).
    """
    if df.empty:
        return df
    end = df.index.max()
    start = end - pd.Timedelta(hours=hours)
    return df.loc[(df.index >= start) & (df.index <= end)]


def _resample10(df: pd.DataFrame) -> pd.DataFrame:
    """
    Uniform 10-min cadence with short interpolation.
    """
    if df.empty:
        return df
    # Use time-aware resampling; result stays tz-aware
    return (
        df.sort_index()
          .resample("10min")
          .mean()
          .interpolate(limit=3)
    )


# -----------------------------
# Fetchers (all UTC tz-aware)
# -----------------------------

def fetch_kp_1m(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    js = requests.get(url, timeout=20).json()
    df = pd.DataFrame(js)

    # time column can be named "time_tag" or first column; parse with utc=True
    if "time_tag" in df.columns:
        df["time"] = df["time_tag"]
    else:
        df["time"] = df.iloc[:, 0]

    # kp can be "kp_index" or "estimated_kp"
    if "kp_index" in df.columns:
        df["kp"] = pd.to_numeric(df["kp_index"], errors="coerce")
    elif "estimated_kp" in df.columns:
        df["kp"] = pd.to_numeric(df["estimated_kp"], errors="coerce")
    else:
        df["kp"] = pd.NA

    df = df[["time", "kp"]].dropna(subset=["time", "kp"])
    df = _as_utc_index(df, "time")
    return _resample10(_window_hours(df, hours))


def fetch_dscovr_plasma(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"
    js = requests.get(url, timeout=20).json()
    cols = js[0]
    df = pd.DataFrame(js[1:], columns=cols)

    # Normalize column names we use
    # time_tag, density, speed, temperature (strings -> numeric)
    df["time"] = df["time_tag"]
    for c in ("density", "speed", "temperature"):
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df[["time", "density", "speed", "temperature"]].dropna(subset=["time"])
    df = _as_utc_index(df, "time")
    df = df.rename(columns={"speed": "solar_wind_speed"})
    return _resample10(_window_hours(df, hours))


def fetch_dscovr_mag(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/products/solar-wind/mag-6-hour.json"
    js = requests.get(url, timeout=20).json()
    cols = js[0]
    df = pd.DataFrame(js[1:], columns=cols)

    df["time"] = df["time_tag"]
    for c in ("bx_gsm", "by_gsm", "bz_gsm", "bt"):
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df[["time", "bx_gsm", "by_gsm", "bz_gsm", "bt"]].dropna(subset=["time"])
    df = _as_utc_index(df, "time")
    return _resample10(_window_hours(df, hours))


def fetch_goes_protons(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-plot-1-day.json"
    js = requests.get(url, timeout=20).json()

    # Filter the >=10 MeV series and build a DataFrame
    rows = []
    for r in js:
        if r.get("energy") == ">=10 MeV":
            rows.append({"time": r.get("time_tag"), "proton_pfu": r.get("flux")})

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df["proton_pfu"] = pd.to_numeric(df["proton_pfu"], errors="coerce")
    df = df.dropna(subset=["time"])
    df = _as_utc_index(df, "time")
    return _resample10(_window_hours(df, hours))


def bundle(hours: int = 48) -> pd.DataFrame:
    """
    Join all feeds on a **tz-aware UTC** index; columns:
    kp, bx_gsm, by_gsm, bz_gsm, bt, solar_wind_speed, density, temperature, proton_pfu
    """
    kp = fetch_kp_1m(hours)
    mag = fetch_dscovr_mag(hours)
    plasma = fetch_dscovr_plasma(hours)
    pfu = fetch_goes_protons(hours)

    # All indexes are tz-aware UTC now → safe concat
    out = pd.concat([kp, mag, plasma, pfu], axis=1).sort_index()
    return out

=======

from __future__ import annotations

import pandas as pd
import requests


UTC = "UTC"


def _as_utc_index(df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    """
    Ensure index is tz-aware UTC DatetimeIndex.
    """
    t = pd.to_datetime(df[time_col], utc=True, errors="coerce")
    out = df.copy()
    out = out.set_index(t).drop(columns=[time_col])
    out.index = out.index.tz_convert(UTC)  # no-op but explicit
    out = out.sort_index()
    return out


def _window_hours(df: pd.DataFrame, hours: int) -> pd.DataFrame:
    """
    Return the trailing {hours} hours using a mask (avoid deprecated .last()).
    """
    if df.empty:
        return df
    end = df.index.max()
    start = end - pd.Timedelta(hours=hours)
    return df.loc[(df.index >= start) & (df.index <= end)]


def _resample10(df: pd.DataFrame) -> pd.DataFrame:
    """
    Uniform 10-min cadence with short interpolation.
    """
    if df.empty:
        return df
    # Use time-aware resampling; result stays tz-aware
    return (
        df.sort_index()
          .resample("10min")
          .mean()
          .interpolate(limit=3)
    )


# -----------------------------
# Fetchers (all UTC tz-aware)
# -----------------------------

def fetch_kp_1m(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    js = requests.get(url, timeout=20).json()
    df = pd.DataFrame(js)

    # time column can be named "time_tag" or first column; parse with utc=True
    if "time_tag" in df.columns:
        df["time"] = df["time_tag"]
    else:
        df["time"] = df.iloc[:, 0]

    # kp can be "kp_index" or "estimated_kp"
    if "kp_index" in df.columns:
        df["kp"] = pd.to_numeric(df["kp_index"], errors="coerce")
    elif "estimated_kp" in df.columns:
        df["kp"] = pd.to_numeric(df["estimated_kp"], errors="coerce")
    else:
        df["kp"] = pd.NA

    df = df[["time", "kp"]].dropna(subset=["time", "kp"])
    df = _as_utc_index(df, "time")
    return _resample10(_window_hours(df, hours))


def fetch_dscovr_plasma(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"
    js = requests.get(url, timeout=20).json()
    cols = js[0]
    df = pd.DataFrame(js[1:], columns=cols)

    # Normalize column names we use
    # time_tag, density, speed, temperature (strings -> numeric)
    df["time"] = df["time_tag"]
    for c in ("density", "speed", "temperature"):
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df[["time", "density", "speed", "temperature"]].dropna(subset=["time"])
    df = _as_utc_index(df, "time")
    df = df.rename(columns={"speed": "solar_wind_speed"})
    return _resample10(_window_hours(df, hours))


def fetch_dscovr_mag(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/products/solar-wind/mag-6-hour.json"
    js = requests.get(url, timeout=20).json()
    cols = js[0]
    df = pd.DataFrame(js[1:], columns=cols)

    df["time"] = df["time_tag"]
    for c in ("bx_gsm", "by_gsm", "bz_gsm", "bt"):
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df[["time", "bx_gsm", "by_gsm", "bz_gsm", "bt"]].dropna(subset=["time"])
    df = _as_utc_index(df, "time")
    return _resample10(_window_hours(df, hours))


def fetch_goes_protons(hours: int = 48) -> pd.DataFrame:
    url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-plot-1-day.json"
    js = requests.get(url, timeout=20).json()

    # Filter the >=10 MeV series and build a DataFrame
    rows = []
    for r in js:
        if r.get("energy") == ">=10 MeV":
            rows.append({"time": r.get("time_tag"), "proton_pfu": r.get("flux")})

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df["proton_pfu"] = pd.to_numeric(df["proton_pfu"], errors="coerce")
    df = df.dropna(subset=["time"])
    df = _as_utc_index(df, "time")
    return _resample10(_window_hours(df, hours))


def bundle(hours: int = 48) -> pd.DataFrame:
    """
    Join all feeds on a **tz-aware UTC** index; columns:
    kp, bx_gsm, by_gsm, bz_gsm, bt, solar_wind_speed, density, temperature, proton_pfu
    """
    kp = fetch_kp_1m(hours)
    mag = fetch_dscovr_mag(hours)
    plasma = fetch_dscovr_plasma(hours)
    pfu = fetch_goes_protons(hours)

    # All indexes are tz-aware UTC now → safe concat
    out = pd.concat([kp, mag, plasma, pfu], axis=1).sort_index()
    return out

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
