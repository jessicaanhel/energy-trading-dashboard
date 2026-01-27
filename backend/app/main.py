from datetime import datetime
from backend.app.data_sources.csv_data_source import CsvDataSource
from backend.app.services.power_service import PowerDataService

def main():
    data_source = CsvDataSource()

    service = PowerDataService(data_source)

    result = service.get_aggregations(
        start=datetime(2020, 1, 1),
        end=datetime(2020, 12, 31)
    )

    print(result)

if __name__ == "__main__":
    main()
