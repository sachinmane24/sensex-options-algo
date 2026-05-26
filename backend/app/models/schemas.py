from pydantic import BaseModel
from typing import List, Optional


class Candle(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: float


class RunRequest(BaseModel):
    candles: List[Candle]
    spot_price: float
    expiry: str
    india_vix: Optional[float] = None
