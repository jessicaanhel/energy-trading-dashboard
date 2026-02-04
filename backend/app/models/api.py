from pydantic import BaseModel


class PowerRequest(BaseModel):
    """API request payload for power data."""
    start: str
    end: str
    volume: str
    park: str