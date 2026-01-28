from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel


class EnergyType(str):
    WIND = "Wind"
    SOLAR = "Solar"

@dataclass
class PowerSlot:
    park_name: str
    timestamp: datetime
    mw: float
    energy_type: EnergyType

@dataclass
class ParkInfo:
    park_name: str
    energy_type: EnergyType
    timezone: str


class PowerRequest(BaseModel):
    start: str
    end: str
    volume: str
    park: str = "ALL"

