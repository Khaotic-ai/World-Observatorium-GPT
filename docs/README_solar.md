# World Observatorium — Solar Domain Integration (NASA DONKI)

Import `actions/nasa_donki.yaml` in the GPT editor (Configure → Actions → Add action → Import from file).

## Endpoints
- **getSolarFlares(startDate, endDate, api_key)**
- **getCoronalMassEjections(startDate, endDate, mostAccurateOnly?, api_key)**
- **getGeomagneticStorms(startDate, endDate, api_key)**

## Conversation Starters
- Check solar activity in the last 48 hours.
- Show solar flares and geomagnetic storms this week.

## Test Prompts
Call getSolarFlares with startDate=<UTC today-3d>, endDate=<UTC today>, api_key=<YOUR_NASA_KEY>.
Call getCoronalMassEjections with startDate=<UTC today-3d>, endDate=<UTC today>, mostAccurateOnly=true, api_key=<YOUR_NASA_KEY>.
Call getGeomagneticStorms with startDate=<UTC today-7d>, endDate=<UTC today>, api_key=<YOUR_NASA_KEY>.

Then combine into a Solar Activity section: counts by class (X/M/C), max CME speed, highest Kp.
