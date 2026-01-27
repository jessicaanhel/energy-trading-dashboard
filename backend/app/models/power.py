from dataclasses import dataclass
from datetime import datetime

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
    energy_type: str
    timezone: str
