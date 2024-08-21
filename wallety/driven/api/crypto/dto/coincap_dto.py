from typing import List

from pydantic import BaseModel, Field


class CoincapDTO(BaseModel):
    id: str
    rank: str
    symbol: str
    name: str
    price_usd: str = Field(..., alias='priceUsd')
    market_cap_usd: str = Field(..., alias='marketCapUsd')


