import json
import os

from backend.app.api.power import parse_iso_datetime
from backend.app.data_sources.dynamo_data_source import DynamoDataSource
from backend.app.models.api import PowerRequest
from backend.app.services.aggregator import Aggregator
from backend.app.services.power_service import PowerDataService
from backend.app.utils import format_production_data


def lambda_handler(event, context):
    body = json.loads(event["body"])
    req = PowerRequest(
        start=body["start"],
        end=body["end"],
        park=body.get("park", "ALL"),
        volume=body.get("volume", "average_per_hour")
    )

    table_name = os.environ["POWER_TABLE_NAME"]
    data_source = DynamoDataSource(table_name)
    service = PowerDataService(data_source)

    start_dt = parse_iso_datetime(req.start)
    end_dt = parse_iso_datetime(req.end)

    slots = service.get_slots(start_dt, end_dt)

    if req.park != "ALL":
        slots = [slot for slot in slots if s.park_name == req.park]

    if req.volume == "average_per_hour":
        aggregated = Aggregator.average_mw_per_hour(slots)
    elif req.volume == "total_per_hour":
        aggregated = Aggregator.total_mw_by_energy_type(slots)

    response = format_production_data(aggregated)

    return {"statusCode": 200, "body": json.dumps(response)}