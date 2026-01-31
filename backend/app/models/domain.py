from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class EnergyType(str, Enum):
    """Supported energy production types."""
    WIND = "Wind"
    SOLAR = "Solar"

@dataclass
class PowerSlot:
    """Single power production measurement."""
    park_name: str
    timestamp: datetime
    mw: float
    energy_type: EnergyType

@dataclass
class ParkInfo:
    """Metadata about a power park."""
    park_name: str
    energy_type: EnergyType
    timezone: str