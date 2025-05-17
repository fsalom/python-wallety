from typing import List

from pydantic import BaseModel

from wallety.driven.api.crypto.dto.historical_price_data_dto import HistoricalPriceData


class HistoricalData(BaseModel):
    data: List[HistoricalPriceData]
    timestamp: int
