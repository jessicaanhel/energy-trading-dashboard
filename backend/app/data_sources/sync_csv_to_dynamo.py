from backend.app.data_sources.csv_data_source import CsvDataSource
from backend.app.data_sources.dynamo_data_source import DynamoDataSource
from datetime import datetime, timedelta

def sync_csv_to_dynamo():
    csv_source = CsvDataSource("data")
    dynamo = DynamoDataSource("power-slots")

    now = datetime.utcnow()
    start = now - timedelta(hours=1)

    parks = csv_source.load_parks()
    slots = csv_source.load_slots(start, now)

    for park in parks:
        dynamo.save_park(park)

    for slot in slots:
        dynamo.save_slot(slot)

if __name__ == "__main__":
    sync_csv_to_dynamo()