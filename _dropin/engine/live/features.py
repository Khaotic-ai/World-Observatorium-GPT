
from __future__ import annotations
import pandas as pd
from datetime import datetime, timezone

def resample10(df: pd.DataFrame) -> pd.DataFrame:
    """Uniform 10‑min cadence with light interpolation."""
    return (df.sort_index()
              .resample("10min").mean()
              .interpolate(limit=3))

def lunar_phase_fraction(dt_utc: datetime) -> float:
    """0=new, 0.5=full, 1=next new (simple approximation)."""
    base = datetime(2000,1,6,18,14, tzinfo=timezone.utc)
    synodic = 29.53058867
    days = (dt_utc - base).total_seconds()/86400.0
    return (days % synodic)/synodic
