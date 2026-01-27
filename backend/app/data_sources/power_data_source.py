from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List
from backend.app.models.power import ParkInfo, PowerSlot

class PowerDataSource(ABC):

    @abstractmethod
    def load_parks(self) -> Dict[str, ParkInfo]:
        pass

    @abstractmethod
    def load_slots(self, start: datetime, end: datetime) -> List[PowerSlot]:
        pass
