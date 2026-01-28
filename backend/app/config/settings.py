import os

ENV = os.getenv("ENV", "local")

CSV_DATA_DIR = os.getenv("CSV_DATA_DIR", "data")
DYNAMO_POWER_TABLE = os.getenv("POWER_TABLE_NAME", "PowerTable")