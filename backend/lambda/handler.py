import os
from backend.app.api.power_api import get_production_data
from backend.app.data_sources.dynamo_data_source import DynamoDataSource
from backend.app.services.power_service import PowerDataService


def lambda_handler(event, context):
    start = event["start"]
    end = event["end"]
    volume = event.get("volume", "average_per_hour")

    table_name = os.environ["POWER_TABLE_NAME"]

    data_source = DynamoDataSource(table_name)
    service = PowerDataService(data_source)

    response = get_production_data(
        service=service,
        start=start,
        end=end,
        volume=volume
    )

    return {
        "statusCode": 200,
        "body": response
    }