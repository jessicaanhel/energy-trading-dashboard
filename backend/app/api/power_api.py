from datetime import datetime

from backend.app.services.power_service import PowerDataService


def get_hourly_average(service: PowerDataService, start: datetime, end: datetime):
    agg = service.get_aggregations(start, end)["average_per_hour"]

    return [
        {
            "hour": h,
            "wind_mw": v.get("Wind", 0),
            "solar_mw": v.get("Solar", 0),
        }
        for h, v in sorted(agg.items())
    ]
