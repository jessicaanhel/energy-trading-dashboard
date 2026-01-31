import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from typing import Dict, List

from backend.app.data_sources.power_data_source import PowerDataSource
from backend.app.models.domain import PowerSlot, ParkInfo, EnergyType


class DynamoDataSource(PowerDataSource):
    def __init__(self, table_name: str):
        self.table = boto3.resource("dynamodb").Table(table_name)

    def load_parks(self) -> List[ParkInfo]:
        resp = self.table.scan(
            FilterExpression="item_type = :t",
            ExpressionAttributeValues={":t": "PARK"}
        )

        parks_list: List[ParkInfo] = [
            ParkInfo(
                park_name=i["park_name"],
                timezone=i["timezone"],
                energy_type=EnergyType(i["energy_type"])
            ) for i in resp.get("Items", [])
        ]

        return parks_list

    def load_slots(self, start: datetime, end: datetime) -> List[PowerSlot]:
        parks_list = self.load_parks()
        park_map: Dict[str, ParkInfo] = {p.park_name: p for p in parks_list}  # scalable lookup

        slots: List[PowerSlot] = []

        for park_name, park in park_map.items():
            last_evaluated_key = None
            while True:
                resp = self.table.query(
                    KeyConditionExpression=Key("pk").eq(f"PARK#{park_name}") &
                                           Key("sk").between(f"SLOT#{start.isoformat()}",
                                                              f"SLOT#{end.isoformat()}"),
                    ExclusiveStartKey=last_evaluated_key
                )

                for item in resp.get("Items", []):
                    slots.append(PowerSlot(
                        park_name=park_name,
                        timestamp=datetime.fromisoformat(item["timestamp_utc"]),
                        mw=float(item["mw"]),
                        energy_type=park.energy_type
                    ))

                last_evaluated_key = resp.get("LastEvaluatedKey")
                if not last_evaluated_key:
                    break

        return slots

    def save_park(self, park: ParkInfo):
        self.table.put_item(
            Item={
                "pk": f"PARK#{park.park_name}",
                "sk": "META",
                "item_type": "PARK",
                "park_name": park.park_name,
                "timezone": park.timezone,
                "energy_type": park.energy_type
            }
        )

    def save_slot(self, slot: PowerSlot):
        self.table.put_item(
            Item={
                "pk": f"PARK#{slot.park_name}",
                "sk": f"SLOT#{slot.timestamp.isoformat()}",
                "item_type": "SLOT",
                "park_name": slot.park_name,
                "timestamp_utc": slot.timestamp.isoformat(),
                "mw": slot.mw
            }
        )