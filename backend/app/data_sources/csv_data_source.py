import csv
from datetime import datetime
from backend.app.models.power import PowerSlot, ParkInfo

def load_parks_ifo(path):
    metadata = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            metadata[row['park_name']] = ParkInfo(
                park_name=row['park_name'],
                energy_type=row['energy_type'],
                timezone=row['timezone']
            )
    return metadata

def load_slots(path, park_name):
    slots = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = datetime.fromisoformat(row['timestamp'])
            mw = float(row['mw'])
            slots.append(PowerSlot(park_name=park_name, timestamp=ts, mw=mw))
    return slots
