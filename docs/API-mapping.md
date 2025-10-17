# API Mapping (GPT ↔ Orchestrator ↔ Provider)

| Domain   | GPT Action (OpenAPI)         | Orchestrator Route                 | Upstream Provider              | Notes |
|---------|-------------------------------|------------------------------------|--------------------------------|------|
| Time    | `getUtcTime` (worldtime.yaml) | `/time/utc`                        | worldtimeapi.org               | Canonical UTC anchor |
| Weather | `getForecast` (openmeteo.yaml)| `/weather/current?lat&lon`         | Open-Meteo `/forecast`         | Return metric units |
| Air     | `getAirQualityNearest`        | `/air/nearest?lat&lon` (todo)      | IQAir `/nearest_city`          | Requires API key |
| Seismic | `getEarthquakesPastDay`       | `/quakes/past-day?minMag`          | USGS all_day.geojson           | Filter in adapter |
| Solar   | (composite; no GPT action yet)| `/solar/flares?startDate&endDate`  | NASA DONKI `/FLR`              | DEMO_KEY ok |
| GW      | (composite; no GPT action yet)| `/ligo/recent?limit&state`         | LIGO GraceDB `/superevents/`   | JSON list |

**Canonical field names** returned by orchestrator:- `time.nowUtc` (ISO 8601 Z), `fetchedAt`- `weather.temperatureC`, `humidityPct`, `windSpeedMs`, `wmo`- `air.aqiUS`, `pm25`, `city`, `ts`- `quakes.events[]: {id, time, magnitude, place, depthKm, coordinates:{lat,lon}}`
