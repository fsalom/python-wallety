from pydantic import BaseModel, Field


class CoincapDTO(BaseModel):
    id: str
    symbol: str
    name: str
    price_usd: float = Field(..., alias='priceUsd')
    market_cap_usd: float = Field(..., alias='marketCapUsd')


