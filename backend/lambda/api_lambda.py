import os
import json
from datetime import datetime
from typing import List

from backend.app.data_sources.sync_csv_to_dynamo import run_csv_sync
from backend.app.models.power import PowerSlot, PowerRequest
from backend.app.data_sources.dynamo_data_source import DynamoDataSource
from backend.app.services.power_service import PowerDataService
from backend.app.services.aggregator import Aggregator
from backend.app.api.power_api import format_production_data


def lambda_handler(event, context):
    """
    Lambda version of FastAPI /power endpoint.
    Expects event["body"] to contain JSON like:
    {
        "start": "2026-01-27T00:00:00",
        "end": "2026-01-27T23:00:00",
        "park": "ALL",
        "volume": "average_per_hour"
    }
    """
    try:
        run_csv_sync()
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

    try:
        start_dt = datetime.fromisoformat(req.start)
        end_dt = datetime.fromisoformat(req.end)
    except ValueError:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid date format"})}

    slots: List[PowerSlot] = service.get_slots(start_dt, end_dt)

    if req.park != "ALL":
        slots = [s for s in slots if s.park_name == req.park]

    if req.volume == "average_per_hour":
        aggregated = Aggregator.average_mw_per_hour(slots)
    elif req.volume == "total_per_hour":
        aggregated = Aggregator.total_mw_by_energy_type(slots)
    else:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid volume type"})}

    response = format_production_data(aggregated)

    return {"statusCode": 200, "body": json.dumps(response)}