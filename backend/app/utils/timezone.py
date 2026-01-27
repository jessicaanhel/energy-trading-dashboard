from datetime import datetime
from zoneinfo import ZoneInfo


def local_to_utc(dt: datetime, tz_name: str) -> datetime:
    if dt.tzinfo is not None:
        raise ValueError("Expected naive datetime")

    try:
        return dt.replace(tzinfo=ZoneInfo(tz_name)).astimezone(ZoneInfo("UTC"))
    except Exception:
        raise ValueError(f"Invalid timezone: {tz_name}")
