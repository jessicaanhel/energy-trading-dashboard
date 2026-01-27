from collections import defaultdict
from typing import List, Dict
from backend.app.models.power import PowerSlot


class Aggregator:
    @staticmethod
    def average_mw_per_hour(slots: List[PowerSlot]) -> Dict[str, Dict[str, float]]:
        """Average MW per hour per energy type"""
        sums = defaultdict(lambda: defaultdict(float))
        counts = defaultdict(lambda: defaultdict(int))

        for slot in slots:
            hour = slot.timestamp.strftime('%Y-%m-%d %H:00')
            sums[hour][slot.energy_type] += slot.mw
            counts[hour][slot.energy_type] += 1

        averages = {}
        for hour, energy_dict in sums.items():
            averages[hour] = {}
            for e_type, total_mw in energy_dict.items():
                averages[hour][e_type] = total_mw / counts[hour][e_type]

        return averages

    @staticmethod
    def total_mw_by_energy_type(slots: List[PowerSlot]) -> Dict[str, Dict[str, float]]:
        """Total MW per hour per energy type"""
        totals = defaultdict(lambda: defaultdict(float))

        for slot in slots:
            hour = slot.timestamp.strftime('%Y-%m-%d %H:00')
            energy_type = slot.energy_type
            totals[hour][energy_type] += slot.mw

        result: Dict[str, Dict[str, float]] = {}
        for hour in totals:
            result[hour] = {}
            for energy_type in totals[hour]:
                result[hour][energy_type] = totals[hour][energy_type]

        return result
