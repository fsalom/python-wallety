from typing import List

from pydantic import BaseModel

from wallety.driven.api.crypto.dto.market_info_dto import MarketData


class MarketDataResponse(BaseModel):
    data: List[MarketData]
    timestamp: int
