from fastapi import HTTPException, Depends, APIRouter
from datetime import datetime
from typing import List

from backend.app.models.domain import PowerSlot
from backend.app.models.api import PowerRequest
from backend.app.services.power_service import PowerDataService
from backend.app.services.aggregator import Aggregator
from backend.app.utils import format_production_data
from backend.dependencies.power_dependencies import get_power_service


router = APIRouter()
ALL_PARKS = "ALL"

def parse_iso_datetime(given_datetime: str) -> datetime:
    try:
        return datetime.fromisoformat(given_datetime)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

def aggregate_slots(power_slots: List[PowerSlot], volume_type: str):
    if volume_type == "average_per_hour":
        return Aggregator.average_mw_per_hour(power_slots)
    elif volume_type == "total_per_hour":
        return Aggregator.total_mw_by_energy_type(power_slots)
    else:
        raise HTTPException(status_code=400, detail="Invalid volume type")

def filter_slots_by_park(power_slots: List[PowerSlot],park_name: str) -> List[PowerSlot]:
    if park_name == ALL_PARKS:
        return power_slots

    return [
        slot
        for slot in power_slots
        if slot.park_name == park_name
    ]


@router.post("/power")
def get_power_data(request: PowerRequest, power_service: PowerDataService = Depends(get_power_service)):
    """Handle internal APi request from frontend. Return ready for visualization data"""
    start_datetime = parse_iso_datetime(request.start)
    end_datetime = parse_iso_datetime(request.end)
    if end_datetime < start_datetime:
        raise HTTPException(status_code=400, detail="Start date must be before end date")

    power_slots = power_service.get_slots(start_datetime, end_datetime)
    filtered_slots = filter_slots_by_park(power_slots, request.park)
    aggregated_data = aggregate_slots(filtered_slots, request.volume)

    return format_production_data(aggregated_data)