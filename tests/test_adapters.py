
import time
import requests

BASE = "http://localhost:8000"

def wait_for_api(timeout=25):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{BASE}/time/utc", timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            time.sleep(1)
    raise RuntimeError("API did not become ready in time")

def test_time_endpoint():
    wait_for_api()
    r = requests.get(f"{BASE}/time/utc", timeout=5)
    r.raise_for_status()
    j = r.json()
    assert "ok" in j and j["ok"] is True
    assert "nowUtc" in j

def test_weather_endpoint():
    wait_for_api()
    r = requests.get(f"{BASE}/weather/current", params={"lat": -27.47, "lon": 153.03}, timeout=10)
    r.raise_for_status()
    j = r.json()
    assert "ok" in j
    assert "temperatureC" in j

def test_quakes_endpoint():
    wait_for_api()
    r = requests.get(f"{BASE}/quakes/past-day", params={"minMag": 4.5}, timeout=15)
    r.raise_for_status()
    j = r.json()
    assert "ok" in j
    assert "events" in j

def test_solar_endpoint():
    wait_for_api()
    r = requests.get(f"{BASE}/solar/flares", timeout=20)
    r.raise_for_status()
    j = r.json()
    assert "ok" in j
    assert "flares" in j

def test_ligo_endpoint():
    wait_for_api()
    r = requests.get(f"{BASE}/ligo/recent", params={"limit": 3}, timeout=20)
    r.raise_for_status()
    j = r.json()
    assert "ok" in j
    assert "events" in j
