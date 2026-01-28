from backend.app.data_sources.csv_data_source import CsvDataSource
from backend.app.data_sources.dynamo_data_source import DynamoDataSource
from datetime import datetime, timedelta

def run_csv_sync():
    csv_source = CsvDataSource("data")
    dynamo = DynamoDataSource("power-table")

    now = datetime.utcnow()
    start = now - timedelta(hours=1)

    parks = csv_source.load_parks()
    slots = csv_source.load_slots(start, now)

    # Save parks
    for park in parks:
        dynamo.save_park(park)

    # Save slots
    for slot in slots:
        dynamo.save_slot(slot)

if __name__ == "__main__":
    run_csv_sync()
