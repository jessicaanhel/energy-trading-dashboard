import csv
import os
from datetime import datetime
from typing import List

from backend.app.data_sources.power_data_source import PowerDataSource
from backend.app.models.power import PowerSlot, ParkInfo, EnergyType


class CsvDataSource(PowerDataSource):
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.parks = self.load_parks()

    def load_parks(self) -> List[ParkInfo]:
        parks = []
        with open(os.path.join(self.data_dir, "park_info.csv")) as f:
            reader = csv.DictReader(f)
            for row in reader:
                parks.append(ParkInfo(
                    park_name=row["park_name"],
                    timezone=row["timezone"],
                    energy_type=EnergyType(row["energy_type"])
                ))
        return parks

    def load_slots(self, start: datetime, end: datetime) -> List[PowerSlot]:
        park_map = {p.park_name: p for p in self.parks}
        slots = []

        for file_name in os.listdir(self.data_dir):
            if not file_name.endswith(".csv") or file_name == "park_info.csv":
                continue
            park_name = file_name.replace(".csv", "")
            park = park_map[park_name]
            with open(os.path.join(self.data_dir, file_name)) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ts = datetime.fromisoformat(row["datetime"])
                    if start <= ts <= end:
                        slots.append(PowerSlot(
                            park_name=park_name,
                            timestamp=ts,
                            mw=float(row["MW"]),
                            energy_type=park.energy_type
                        ))
        return slots