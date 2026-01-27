import boto3
from datetime import datetime
from typing import List

from backend.app.data_sources.power_data_source import PowerDataSource
from backend.app.models.power import PowerSlot, ParkInfo, EnergyType

class DynamoDataSource(PowerDataSource):
    def __init__(self, table_name: str):
        self.table = boto3.resource("dynamodb").Table(table_name)

    def load_parks(self) -> List[ParkInfo]:
        resp = self.table.scan(
            FilterExpression="item_type = :t",
            ExpressionAttributeValues={":t": "PARK"}
        )
        return [
            ParkInfo(
                name=i["park_name"],
                timezone=i["timezone"],
                energy_type=EnergyType(i["energy_type"])
            )
            for i in resp["Items"]
        ]

    def load_slots(self, start: datetime, end: datetime) -> List[PowerSlot]:
        resp = self.table.scan(
            FilterExpression="item_type = :t AND #ts BETWEEN :s AND :e",
            ExpressionAttributeNames={"#ts": "timestamp_utc"},
            ExpressionAttributeValues={
                ":t": "SLOT",
                ":s": start.isoformat(),
                ":e": end.isoformat(),
            },
        )

        return [
            PowerSlot(
                park_name=i["park_name"],
                timestamp_utc=datetime.fromisoformat(i["timestamp_utc"]),
                mw=float(i["mw"]),
            )
            for i in resp["Items"]
        ]
