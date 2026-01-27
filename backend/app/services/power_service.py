from datetime import datetime
from typing import Dict
from backend.app.data_sources.power_data_source import PowerDataSource
from aggregator import Aggregator

class PowerDataService:
    def __init__(self, data_source: PowerDataSource):
        self.data_source = data_source
        self.parks = data_source.load_parks()

    def get_aggregations(self, start: datetime, end: datetime) -> Dict:
        slots = self.data_source.load_slots(start, end)
        return {
            "average_per_hour": Aggregator.average_mw_per_hour(slots),
            "total_per_hour": Aggregator.total_mw_per_hour(slots),
            "total_by_energy_type": Aggregator.total_mw_by_energy_type(slots, self.parks)
        }