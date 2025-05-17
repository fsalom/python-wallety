from pydantic import BaseModel, Field


class HistoricalPriceData(BaseModel):
    price_usd: float = Field(alias="priceUsd")
    date: str
