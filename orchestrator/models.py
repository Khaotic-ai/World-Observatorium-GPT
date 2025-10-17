from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class TimePayload(BaseModel):
    ok: bool = True
    nowUtc: str
    fetchedAt: str
    sources: List[str]

class WeatherPayload(BaseModel):
    ok: bool = True
    temperatureC: Optional[float] = None
    humidityPct: Optional[float] = None
    windSpeedMs: Optional[float] = None
    wmo: Optional[int] = None
    sources: List[str] = []
    # Optional, convenience label added by app layer:
    # wmo_text: Optional[str]

class QuakeEvent(BaseModel):
    id: Optional[str]
    time: Optional[str]
    magnitude: Optional[float]
    place: Optional[str]
    depthKm: Optional[float]
    coordinates: Optional[Dict[str, float]]

class QuakesPayload(BaseModel):
    ok: bool
    source: str
    count: int
    minMag: float
    events: List[QuakeEvent] = []

class SolarFlaresPayload(BaseModel):
    ok: bool
    source: str
    flares: List[Dict] = []
    window: Dict = {}

class LigoPayload(BaseModel):
    ok: bool
    source: str
    limit: int
    events: List[Dict] = []

class SnapshotPayload(BaseModel):
    ok: bool
    status: str = Field(..., description="complete | partial | error")
    fetchedAt: str
    missingDomains: List[str] = []
    time: Optional[TimePayload] = None
    weather: Optional[WeatherPayload] = None
    air: Optional[Dict] = None
    quakes: Optional[QuakesPayload] = None
    solar: Optional[SolarFlaresPayload] = None
    ligo: Optional[LigoPayload] = None

WMO_MAP = {
    0: "Clear", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Freezing drizzle", 57: "Freezing drizzle (dense)",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Freezing rain (slight)", 67: "Freezing rain (heavy)",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
}
