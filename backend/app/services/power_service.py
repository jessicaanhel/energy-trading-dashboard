from datetime import datetime
from backend.app.data_sources.power_data_source import PowerDataSource
from backend.app.models.domain import PowerSlot


class PowerDataService:
    def __init__(self, data_source: PowerDataSource):
        self.data_source = data_source
        self.parks = data_source.load_parks()

    def get_slots(self, start: datetime, end: datetime) -> list[PowerSlot]:
        return self.data_source.load_slots(start, end)