from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, List


def local_to_utc(dt: datetime, time_zone_name: str) -> datetime:
    """Convert a datetime in a given local timezone to a UTC-aware datetime."""
    if dt.tzinfo is not None:
        raise ValueError("Expected naive datetime")

    try:
        return dt.replace(tzinfo=ZoneInfo(time_zone_name)).astimezone(ZoneInfo("UTC"))
    except Exception:
        raise ValueError(f"Invalid timezone: {time_zone_name}")


def format_with_local_offset(utc_dt: datetime, timezone_name: str) -> str:
    """
    Returns an ISO string with the correct local offset 2026-02-04T12:00:00+01:00
    """
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=ZoneInfo("UTC"))
    local_dt = utc_dt.astimezone(ZoneInfo(timezone_name))

    return local_dt.isoformat()

def format_production_data(aggregated: Dict[str, Dict[str, float]]) -> List[Dict]:
    """Prepare aggregated dict for frontend table/chart"""
    result = []
    for hour in sorted(aggregated):
        result.append({
            "hour": hour,
            "wind_mw": aggregated[hour].get("Wind", 0),
            "solar_mw": aggregated[hour].get("Solar", 0)
        })
    return result