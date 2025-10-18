# World Observatorium — Open‑Meteo Integration

Import `actions/open_meteo.yaml` in the GPT editor (Configure → Actions → Add action → Import from file).

## Endpoint
- **getForecast(latitude, longitude, timezone?, current?)**

## Recommended call
```
timezone=UTC
current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code
```

## Test prompt
Call getForecast with latitude=-27.47, longitude=153.03, timezone=UTC,
current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code.
