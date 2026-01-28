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