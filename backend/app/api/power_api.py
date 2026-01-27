from datetime import datetime
from typing import List, Dict

from backend.app.models.power import PowerSlot
from backend.app.services.power_service import PowerDataService
from backend.app.services.aggregator import Aggregator


def get_production_data(service: PowerDataService, start: datetime, end: datetime, volume: str) -> List[Dict]:
    """
    Return production data in a readable format for table or chart:
    [
        {"hour": "2026-01-27 14:00", "wind_mw": 50, "solar_mw": 20},
        ...
    ]
    """
    slots = service.get_slots(start, end)

    if volume == "average_per_hour":
        aggregated = Aggregator.average_mw_per_hour(slots)
    elif volume == "total_per_hour":
        aggregated = Aggregator.total_mw_by_energy_type(slots)
    else:
        raise ValueError(f"Invalid volume: {volume}")

    result: List[Dict] = []
    for hour in sorted(aggregated):
        wind_mw = aggregated[hour].get("Wind", 0)
        solar_mw = aggregated[hour].get("Solar", 0)
        result.append({
            "hour": hour,
            "wind_mw": wind_mw,
            "solar_mw": solar_mw
        })

    return result
