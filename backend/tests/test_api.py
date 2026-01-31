from datetime import datetime, timedelta
from fastapi import HTTPException

from backend.app.api.power import parse_iso_datetime
from backend.app.models.power import PowerSlot
from backend.app.services.aggregator import Aggregator
from backend.app.services.power_service import PowerDataService
from backend.tests.test_service_fake import power_service


def test_get_slots(power_service: PowerDataService):
    start = datetime.now()
    end = start + timedelta(hours=1)
    slots = power_service.get_slots(start, end)
    assert len(slots) == 4
    assert all(isinstance(slot, PowerSlot) for slot in slots)

def test_dateformat():
    request_start_time = "2020-01-16T00:00:00"
    assert parse_iso_datetime(request_start_time) == datetime(2020, 1, 16, 0, 0)

def test_wrong_dateformat():
    try:
        parse_iso_datetime("2025/78/12:00:00")
    except HTTPException:
        pass
    else:
        raise AssertionError("ValueError and HTTP exeption was not raised")

def test_average_aggregate_slots(power_service):
    start = datetime.now()
    end = start + timedelta(hours=1)
    slots = power_service.get_slots(start, end)
    start_hour = start.strftime('%Y-%m-%d %H:00')
    end_time = end.strftime('%Y-%m-%d %H:00')
    average = Aggregator.average_mw_per_hour(slots)
    assert average ==  {start_hour: {'Solar': 10, 'Wind': 20}, end_time: { 'Solar': 15}}

def test_total_mw_by_e_type(power_service):
    start = datetime.now()
    end = start + timedelta(hours=1)
    slots = power_service.get_slots(start, end)
    start_hour = start.strftime('%Y-%m-%d %H:00')
    end_time = end.strftime('%Y-%m-%d %H:00')
    total = Aggregator.total_mw_by_energy_type(slots)
    assert total == {start_hour: {'Solar': 20, 'Wind': 20}, end_time: {'Solar': 15}}


def test_filter_by_park(power_service: PowerDataService):
    start = datetime.now()
    end = start + timedelta(hours=1)
    slots = power_service.get_slots(start, end)
    filtered = [slot for slot in slots if slot.park_name == "Netterden"]
    assert all(slot.park_name == "Netterden" for slot in filtered)
