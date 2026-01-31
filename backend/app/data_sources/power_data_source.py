from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List
from backend.app.models.domain import ParkInfo, PowerSlot

class PowerDataSource(ABC):

    @abstractmethod
    def load_parks(self) -> Dict[str, ParkInfo]:
        """Load park metadata from given data source"""
        pass

    @abstractmethod
    def load_slots(self, start: datetime, end: datetime) -> List[PowerSlot]:
        """Load each single power production wrapped in List from given data source"""
        pass
