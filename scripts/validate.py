#!/usr/bin/env python3
"""
Observatorium CI Validator
- Structural validation of OpenAPI action YAMLs in /actions
- Live health checks for each provider (small, bounded calls)
- Summarized pass/fail with non-zero exit on failure
"""

from __future__ import annotations
import os, sys, json, time, datetime as dt
from pathlib import Path

import yaml
import requests

ACTIONS_DIR = Path("actions")
TIMEOUT = 20
NOW_UTC = dt.datetime.utcnow()
TODAY = NOW_UTC.date()
THREE_DAYS_AGO = (NOW_UTC - dt.timedelta(days=3)).date()

NASA_API_KEY = os.getenv("NASA_API_KEY")
IQAIR_KEY = os.getenv("IQAIR_KEY")

required_files = {
    "worldtime.yaml": "WorldTime",
    "openmeteo.yaml": "Open-Meteo",
    "iqair.yaml": "IQAir",
    "usgs_query.yaml": "USGS Query",
    "nasa_donki.yaml": "NASA DONKI",
}

def load_yaml(p: Path) -> dict:
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def require(cond: bool, msg: str):
    if not cond:
        raise AssertionError(msg)

def check_openapi_structure(spec: dict, name: str):
    require("openapi" in spec, f"{name}: missing 'openapi'")
    require("paths" in spec and isinstance(spec["paths"], dict), f"{name}: missing 'paths'")
    # minimal sanity: each method should have an operationId
    for path, ops in spec["paths"].items():
        require(isinstance(ops, dict), f"{name}: path {path} not a dict")
        for method, op in ops.items():
            require(isinstance(op, dict), f"{name}: op {path} {method} not a dict")
            require("operationId" in op, f"{name}: {path} {method} missing operationId")

def get(url: str, **params):
    r = requests.get(url, params=params, timeout=TIMEOUT)
    return r.status_code, r

def test_worldtime():
    url = "https://worldtimeapi.org/api/timezone/Etc/UTC"
    code, r = get(url)
    ok = (code == 200) and ("utc_datetime" in r.text or "datetime" in r.text)
    return ok, ("WorldTime", code, url)

def test_open_meteo():
    url = "https://api.open-meteo.com/v1/forecast"
    params = dict(
        latitude=-27.47, longitude=153.03,
        timezone="UTC",
        current="temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code",
    )
    code, r = get(url, **params)
    ok = (code == 200) and ("current" in r.text)
    return ok, ("Open-Meteo", code, url, params)

def test_iqair():
    if not IQAIR_KEY:
        # Treat as soft-pass if key not provided; CI should set secret to truly test.
        return True, ("IQAir (skipped - no key)", 0, "")
    url = "https://api.airvisual.com/v2/nearest_city"
    params = dict(lat=-27.47, lon=153.03, key=IQAIR_KEY)
    code, r = get(url, **params)
    ok = (code == 200) and ("status" in r.text or "data" in r.text)
    return ok, ("IQAir", code, url, {"lat": params["lat"], "lon": params["lon"], "key": "***"})

def test_usgs_query():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    starttime = (NOW_UTC - dt.timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    endtime = NOW_UTC.strftime("%Y-%m-%dT%H:%M:%SZ")
    params = dict(format="geojson", starttime=starttime, endtime=endtime, minmagnitude=3, limit=10, orderby="time")
    code, r = get(url, **params)
    ok = (code == 200) and ("features" in r.text)
    return ok, ("USGS Query", code, url, params)

def test_nasa_donki():
    if not NASA_API_KEY:
        return True, ("NASA DONKI (skipped - no key)", 0, "")
    base = "https://api.nasa.gov/DONKI"
    # try GST (usually light)
    url = f"{base}/GST"
    params = dict(startDate=str(THREE_DAYS_AGO), endDate=str(TODAY), api_key=NASA_API_KEY)
    code, r = get(url, **params)
    ok = (code == 200) and (r.headers.get("content-type","").startswith("application/json"))
    return ok, ("NASA DONKI GST", code, url, {"startDate": params["startDate"], "endDate": params["endDate"], "api_key": "***"})

def main():
    print("🔧 Observatorium CI Validator\n")

    # 1) Structural checks
    print("1) 🔍 OpenAPI structure checks:")
    for fname, label in required_files.items():
        path = ACTIONS_DIR / fname
        if not path.exists():
            print(f"   ❌ {label}: missing file actions/{fname}")
            return sys.exit(2)
        spec = load_yaml(path)
        try:
            check_openapi_structure(spec, label)
            print(f"   ✓ {label}: structure OK")
        except AssertionError as e:
            print(f"   ❌ {e}")
            return sys.exit(2)

    # 2) Live endpoint checks
    print("\n2) 🌐 Live endpoint checks:")
    tests = [test_worldtime, test_open_meteo, test_iqair, test_usgs_query, test_nasa_donki]
    failures = []
    for t in tests:
        try:
            ok, meta = t()
            label = meta[0]
            code = meta[1]
            if ok:
                mark = "✓"
            else:
                mark = "❌"
                failures.append(label)
            # Do not print secrets
            meta_redacted = json.dumps(meta[2:], ensure_ascii=False, default=str)
            print(f"   {mark} {label}: HTTP {code} {meta_redacted}")
        except Exception as ex:
            failures.append(t.__name__)
            print(f"   ❌ {t.__name__}: {ex}")

    print("\n3) 📋 Summary:")
    if failures:
        print(f"   ❌ Failed checks: {', '.join(failures)}")
        sys.exit(1)
    else:
        print("   ✅ All checks passed")
        sys.exit(0)

if __name__ == "__main__":
    main()
