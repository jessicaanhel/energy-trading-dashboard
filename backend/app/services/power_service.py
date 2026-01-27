from typing import List
from datetime import datetime
from backend.app.models.power import PowerSlot
from backend.app.data_sources.csv_data_source import load_power_csv, load_parks_metadata
from timezone import local_to_utc
from aggregations import average_mw_per_hour, total_mw_by_energy_type

class PowerDataService:
    def __init__(self, metadata_path: str):
        self.metadata = load_parks_metadata(metadata_path)
        self.records: List[PowerSlot] = []

    def load_all_records(self):
        self.records.clear()
        for park_name, meta in self.metadata.items():
            csv_records = load_power_csv(f"{park_name}.csv", park_name)
            for r in csv_records:
                r.timestamp = local_to_utc(r.timestamp, meta['timezone'])
            self.records.extend(csv_records)

    def get_records(self, start: datetime, end: datetime) -> List[PowerSlot]:
        return [r for r in self.records if start <= r.timestamp <= end]

    def get_aggregations(self, start: datetime, end: datetime):
        filtered = self.get_records(start, end)
        return {
            "average_per_hour": average_mw_per_hour(filtered),
            "total_by_energy_type": total_mw_by_energy_type(filtered, self.metadata)
        }
