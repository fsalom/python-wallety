from pydantic import BaseModel, Field


class MarketData(BaseModel):
    exchange_id: str = Field(alias="exchangeId")
    base_id: str = Field(alias="baseId")
    quote_id: str = Field(alias="quoteId")
    base_symbol: str = Field(alias="baseSymbol")
    quote_symbol: str = Field(alias="quoteSymbol")
    volume_usd_24hr: float = Field(alias="volumeUsd24Hr")
    price_usd: float = Field(alias="priceUsd")
    volume_percent: float = Field(alias="volumePercent")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        from_attributes = True
