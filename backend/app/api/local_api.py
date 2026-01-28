from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import List
from backend.app.models.power import PowerSlot, PowerRequest
from backend.app.data_sources.csv_data_source import CsvDataSource
from backend.app.services.power_service import PowerDataService
from backend.app.services.aggregator import Aggregator
from backend.app.api.power_api import format_production_data
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="PTC Power API (Local CSV)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"
data_source = CsvDataSource(DATA_DIR)
service = PowerDataService(data_source)


@app.post("/power")
def get_power_data(req: PowerRequest):
    try:
        start = datetime.fromisoformat(req.start)
        end = datetime.fromisoformat(req.end)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    slots: List[PowerSlot] = service.get_slots(start, end)

    if req.park != "ALL":
        slots = [s for s in slots if s.park_name == req.park]

    if req.volume == "average_per_hour":
        aggregated = Aggregator.average_mw_per_hour(slots)
    elif req.volume == "total_per_hour":
        aggregated = Aggregator.total_mw_by_energy_type(slots)
    else:
        raise HTTPException(status_code=400, detail="Invalid volume type")

    return format_production_data(aggregated)
