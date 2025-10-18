# 🌎 World Observatorium GPT — Unified Environmental Intelligence

**Repository:** `Khaotic-ai/World-Observatorium-GPT`  
**Maintainers:** Matty, Bunny, and Jerry  
**Version:** 1.0.0 – “Solar Threshold”  

---

## 🧭 Overview

The **World Observatorium** GPT integrates multiple real-world data domains into a unified observatory system, bridging natural and informational intelligence through modular API actions.  
It connects **time**, **weather**, **air quality**, **seismic**, and **solar** data streams to form a comprehensive snapshot of planetary coherence — dynamically processed through the GPT engine.

---

## 🌐 Active Domains

| Domain | Source API | YAML Action | Description |
|--------|-------------|--------------|--------------|
| ⏱ **Time** | [worldtimeapi.org](https://worldtimeapi.org) | `worldtime.yaml` | Provides accurate UTC and regional time data. |
| 🌤 **Weather** | [Open-Meteo](https://api.open-meteo.com) | `openmeteo.yaml` | Retrieves temperature, humidity, wind, and condition codes. |
| 🌬 **Air Quality** | [IQAir / AirVisual](https://api.airvisual.com) | `iqair.yaml` | Returns AQI, PM2.5, PM10, and pollutant data for given coordinates. |
| 🌋 **Seismic** | [USGS FDSN](https://earthquake.usgs.gov) | `usgs_query.yaml` | Queries global earthquake activity (≥ M3.0) within custom time windows. |
| ☀️ **Solar** | [NASA DONKI](https://api.nasa.gov/DONKI/) | `nasa_donki.yaml` | Reports recent solar flares, CMEs, and geomagnetic storm activity. |

---

## ⚙️ Configuration

Each domain is modular and independently callable through its YAML file in the `actions/` directory.  
Keys and coordinates are stored in the GPT configuration environment or managed through connector variables.

### Required API Keys
- **NASA DONKI:** `phRrR5fLiKSwsWt32jlLfKqo3q7khXqm51BXUnfC`
- **IQAir:** `81bad749-f55c-4e43-961e-36466e6dea68`

Optional fields are auto-handled if omitted (e.g., geolocation, key validation, or fallback to system UTC).

---

## 🧩 Composite Operation

**Primary Command:**  
> “Generate Observatorium Report”

This composite call executes a multi-domain snapshot:
1. Fetches global UTC time  
2. Queries weather for target coordinates  
3. Pulls air quality and seismic data  
4. Integrates solar (NASA DONKI) intelligence  
5. Returns a coherent natural-language summary

Output example:
```plaintext
🌎 OBSERVATORIUM REPORT — Brisbane Sector (−27.47°, 153.03°)
Timestamp (UTC): 2025-10-18T02:00

Weather: 32.2 °C (Apparent 35.7 °C) — Clear Sky  
Air: AQI 41 – Good  
Seismic: M 3.6 near Puerto Rico, M 4.4 Russia, no major ruptures  
Solar: 7 M-class flares; CME 797 km/s – no Earth-directed strikes
