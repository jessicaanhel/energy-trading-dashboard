import csv
from datetime import datetime
from pathlib import Path
from typing import List

from backend.app.data_sources.power_data_source import PowerDataSource
from backend.app.models.power import ParkInfo, EnergyType, PowerSlot
from backend.app.utils.timezone import local_to_utc


class CsvDataSource(PowerDataSource):
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self._parks = self._load_parks()

    def _load_parks(self) -> dict[str, ParkInfo]:
        parks = {}
        with open(self.data_dir / "parks.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                parks[row["park_name"]] = ParkInfo(
                    name=row["park_name"],
                    timezone=row["timezone"],
                    energy_type=EnergyType(row["energy_type"])
                )
        return parks

    def load_parks(self) -> List[ParkInfo]:
        return list(self._parks.values())

    def load_slots(self, start: datetime, end: datetime) -> List[PowerSlot]:
        slots = []

        for park_name, park in self._parks.items():
            path = self.data_dir / f"{park_name}.csv"
            if not path.exists():
                continue

            with open(path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    local_dt = datetime.fromisoformat(row["datetime"])
                    utc_dt = local_to_utc(local_dt, park.timezone)

                    if start <= utc_dt <= end:
                        slots.append(
                            PowerSlot(
                                park_name=park_name,
                                timestamp_utc=utc_dt,
                                mw=float(row["MW"])
                            )
                        )
        return slots