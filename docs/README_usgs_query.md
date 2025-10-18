# World Observatorium — USGS Earthquakes (Query API)

Import `actions/usgs_query.yaml` in the GPT editor (Configure → Actions → Add action → Import from file).

## Endpoint
- **getEarthquakesQuery(format, starttime, endtime, minmagnitude?, limit?, orderby?)**

## Recommended call
```
format=geojson
starttime=<UTC now - 24h>
endtime=<UTC now>
minmagnitude=3
limit=50
orderby=time
```

## Test prompt
Call getEarthquakesQuery with format=geojson, starttime=<UTC today-24h>, endtime=<UTC now>,
minmagnitude=3, limit=50, orderby=time.
