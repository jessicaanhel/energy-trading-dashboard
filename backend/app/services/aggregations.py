from collections import defaultdict
from typing import List, Dict
from backend.app.models.power import PowerSlot, ParkInfo

def total_mw_per_hour(slots: List[PowerSlot]) -> Dict[str, float]:
    result = defaultdict(float)
    for slot in slots:
        hour = slot.timestamp.strftime('%Y-%m-%d %H:00')
        result[hour] += slot.mw
    return dict(result)

def average_mw_per_hour(slots: List[PowerSlot]) -> Dict[str, float]:
    sums = defaultdict(float)
    counts = defaultdict(int)
    for slot in slots:
        hour = slot.timestamp.strftime('%Y-%m-%d %H:00')
        sums[hour] += slot.mw
        counts[hour] += 1
    return {h: sums[h]/counts[h] for h in sums}

def total_mw_by_energy_type(slots: List[PowerSlot], parks: Dict[str, ParkInfo]) -> Dict[str, float]:
    result = defaultdict(float)
    for slot in slots:
        energy_type = parks[slot.park_name].energy_type
        result[energy_type] += slot.mw
    return dict(result)
