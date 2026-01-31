from datetime import datetime, timedelta
from typing import List
import pytest

from backend.app.models.domain import ParkInfo, PowerSlot
from backend.app.data_sources.power_data_source import PowerDataSource
from backend.app.services.aggregator import Aggregator
from backend.app.services.power_service import PowerDataService


class FakeDataSource(PowerDataSource):
    def load_parks(self) -> List[ParkInfo]:
        return [
            ParkInfo("Netterden", "Solar", "Amsterdam"),
            ParkInfo("Stadskanaal", "Wind", "NewYork"),
        ]

    def load_slots(self, start: datetime, end: datetime) -> List[PowerSlot]:
        return [
            PowerSlot("Netterden", start, 10.0, "Solar"),
            PowerSlot("Netterden", start + timedelta(minutes=15), 10.0, "Solar"),
            PowerSlot("Stadskanaal", start, 20.0, "Wind"),
            PowerSlot("Netterden", end, 15.0, "Solar"),
        ]

print(Aggregator.average_mw_per_hour(FakeDataSource().load_slots(start=datetime.now(), end=datetime.now())))

class EmptyPowerDataSource(PowerDataSource):
    def load_parks(self): return {}
    def load_slots(self, start, end): return []


@pytest.fixture
def power_service() -> PowerDataService:
    """Provide a PowerDataService using the mock data source."""
    return PowerDataService(FakeDataSource())
