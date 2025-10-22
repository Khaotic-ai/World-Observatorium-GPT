import json
from copy import deepcopy
from pathlib import Path
from orchestrator.services.hif_engine import compute as hif_compute

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"

def load(name):
    with open(FIXTURES / name, "r", encoding="utf-8") as f:
        return json.load(f)

def test_monotonic_kp_decreases_coherence():
    calm = load("calm_day.json")
    storm = load("geostorm_day.json")
    c = hif_compute(calm)
    s = hif_compute(storm)
    assert c["ok"] and s["ok"]
    assert calm["magnetosphere"]["kpIndex"] < storm["magnetosphere"]["kpIndex"]
    assert c["coherence_score"] > s["coherence_score"]

def test_monotonic_aqi_decreases_coherence():
    calm = load("calm_day.json")
    smoke = load("smoke_day.json")
    c = hif_compute(calm)
    m = hif_compute(smoke)
    assert c["ok"] and m["ok"]
    assert calm["air"]["aqiUS"] < smoke["air"]["aqiUS"]
    assert c["coherence_score"] > m["coherence_score"]

def test_alerts_increase_stress_and_lower_coherence():
    calm = load("calm_day.json")
    with_alerts = deepcopy(calm)
    with_alerts.setdefault("storms", {}).setdefault("alerts", []).extend([
        {"id": "A1", "event": "Severe Thunderstorm", "severity": "Severe"},
        {"id": "A2", "event": "Flood Watch", "severity": "Moderate"},
        {"id": "A3", "event": "High Wind", "severity": "Moderate"}
    ])
    base = hif_compute(calm)
    alerted = hif_compute(with_alerts)
    assert base["ok"] and alerted["ok"]
    assert alerted["stress_load"] > base["stress_load"]
    assert alerted["coherence_score"] < base["coherence_score"]

def test_outputs_are_bounded_0_1_and_numeric():
    calm = load("calm_day.json")
    out = hif_compute(calm)
    for key in ("coherence_score", "hif_local", "hif_cosmic", "stress_load"):
        assert isinstance(out[key], (int, float))
        assert 0.0 <= out[key] <= 1.0
