import json
import logging
import os
from zoneinfo import ZoneInfo

from backend.app.api.power import parse_iso_datetime
from backend.app.api.sync_csv_to_dynamo import get_park_time_zone
from backend.app.data_sources.dynamo_data_source import DynamoDataSource
from backend.app.models.api import PowerRequest
from backend.app.services.aggregator import Aggregator
from backend.app.services.power_service import PowerDataService
from backend.app.utils import format_production_data


def lambda_handler(event, context):
    """
    Lambda version of FastAPI /power endpoint.
    Expects event["body"] to contain JSON like:
    {
        "start": "2026-01-27T00:00:00",
        "end": "2026-01-27T23:00:00",
        "park": "ALL" | "Bemmel" | "Netterden" | "Stadskanaal" | "Windskanaal" | "Zwartenbergseweg",
        "volume": "average_per_hour"
    }
    """
    try:
        body = json.loads(event["body"])
        req = PowerRequest(
            start=body["start"],
            end=body["end"],
            park=body.get("park", "ALL"),
            volume=body.get("volume", "average_per_hour")
        )
    except (KeyError, json.JSONDecodeError):
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid request"})}

    table_name = os.environ["POWER_TABLE_NAME"]
    data_source = DynamoDataSource(table_name)
    service = PowerDataService(data_source)

    start_dt = parse_iso_datetime(req.start)
    end_dt = parse_iso_datetime(req.end)

    slots = service.get_slots(start_dt, end_dt)

    parks = data_source.load_parks()
    timezones = {park.park_name: park.timezone for park in parks}

    if req.park != "ALL":
        slots = [slot for slot in slots if slot.park_name == req.park]

    if req.volume == "average_per_hour":
        aggregated = Aggregator.average_mw_per_hour(slots)
    elif req.volume == "total_per_hour":
        aggregated = Aggregator.total_mw_by_energy_type(slots)

    for slot in aggregated:
        local_timezone = get_park_time_zone(slot, timezones)
        slot.timestamp = slot.timestamp.astimezone(ZoneInfo(local_timezone)).isoformat()

    response = format_production_data(aggregated)

    return {"statusCode": 200, "body": json.dumps(response)}