from typing import Dict, List


def format_production_data(aggregated: Dict[str, Dict[str, float]]) -> List[Dict]:
    """Prepare aggregated dict for frontend table/chart"""
    result = []
    for hour in sorted(aggregated):
        result.append({
            "hour": hour,
            "wind_mw": aggregated[hour].get("Wind", 0),
            "solar_mw": aggregated[hour].get("Solar", 0)
        })
    return result