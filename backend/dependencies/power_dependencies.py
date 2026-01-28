from backend.app.config.settings import (
    ENV,
    CSV_DATA_DIR,
    DYNAMO_POWER_TABLE,
)
from backend.app.data_sources.csv_data_source import CsvDataSource
from backend.app.data_sources.dynamo_data_source import DynamoDataSource
from backend.app.services.power_service import PowerDataService


def get_power_service() -> PowerDataService:
    if ENV == "local":
        data_source = CsvDataSource(CSV_DATA_DIR)
    else:
        data_source = DynamoDataSource(DYNAMO_POWER_TABLE)

    return PowerDataService(data_source)