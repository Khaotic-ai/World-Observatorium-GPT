
import os, json, requests, tomllib

CFG_PATH = os.path.join(os.path.dirname(__file__), "config.toml")
with open(CFG_PATH, "rb") as f:
    cfg = tomllib.load(f)

BASE = cfg.get("BASE", "").rstrip("/")
LAT  = cfg.get("LAT", -25.95)
LON  = cfg.get("LON", 153.06)

def get_json(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def snapshot():
    return get_json(f"{BASE}/snapshot/global?lat={LAT}&lon={LON}")

if __name__ == "__main__":
    data = snapshot()
    print(json.dumps(data, indent=2))
