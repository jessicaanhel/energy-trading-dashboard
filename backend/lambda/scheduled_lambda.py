import os
import json
from backend.app.data_sources.dynamo_data_source import DynamoDataSource
from backend.app.services.power_service import PowerDataService
from backend.app.services.aggregator import Aggregator
from backend.app.api.power_api import format_production_data

def lambda_handler(event, context):
    table_name = os.environ["POWER_TABLE_NAME"]
    agg_table = os.environ["AGG_TABLE_NAME"]

    body = json.loads(event["body"])
    start = body["start"]
    end = body["end"]

    data_source = DynamoDataSource(table_name)
    service = PowerDataService(data_source)

    slots = service.get_slots(start, end)

    avg_agg = Aggregator.average_mw_per_hour(slots)
    total_agg = Aggregator.total_mw_by_energy_type(slots)

    avg_formatted = format_production_data(avg_agg)
    total_formatted = format_production_data(total_agg)

    data_source.write_aggregated_data(agg_table, {"average": avg_formatted, "total": total_formatted})

    return {"statusCode": 200, "body": json.dumps("Aggregation complete")}