import os
from typing import List, Optional

import httpx
from wallety.application.ports.driven.crypto_repository_port import CryptoRepositoryPort
from wallety.domain.crypto import Crypto
from wallety.domain.historical_price import HistoricalPrice
from wallety.domain.market import Market
from wallety.driven.api.crypto.coincap_mapper import CoincapMapper
from wallety.driven.api.crypto.dto.coincap_data_list_dto import CoincapDataListDTO
from wallety.driven.api.crypto.dto.coincap_data_single_dto import CoincapDataSingleDTO
from wallety.driven.api.crypto.dto.historical_data_list_dto import HistoricalData
from wallety.driven.api.crypto.dto.market_data_list_dto import MarketDataResponse


class CryptoAPIRepository(CryptoRepositoryPort):

    def __init__(self, mapper: CoincapMapper):
        self.mapper = mapper

    async def get_list(self) -> List[Crypto]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://rest.coincap.io/v3/assets?apiKey={os.getenv('API_KEY')}")
            response.raise_for_status()

            data = CoincapDataListDTO(**response.json())
            return self.mapper.from_data_list_to_list_entities(data)

    async def get(self, id) -> Crypto:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://rest.coincap.io/v3/assets/{id}/?apiKey={os.getenv('API_KEY')}")
            response.raise_for_status()

            info = CoincapDataSingleDTO(**response.json())
            return self.mapper.from_data_single_to_entity(info)

    async def get_markets(self, id) -> List[Market]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://rest.coincap.io/v3/assets/{id}/markets/?apiKey={os.getenv('API_KEY')}")
            response.raise_for_status()

            info = MarketDataResponse(**response.json())
            return self.mapper.to_domains_market(info)

    async def get_historical_price(
            self,
            id: str,
            interval: str,
            start: Optional[int] = None,
            end: Optional[int] = None
    ) -> List[HistoricalPrice]:
        url = f"https://rest.coincap.io/v3/assets/{id}/history"
        params = {
            "interval": interval,
            "apiKey": os.getenv("API_KEY")
        }

        if start:
            params["start"] = start
        if end:
            params["end"] = end

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

            info = HistoricalData(**response.json())
            return self.mapper.to_domains_historical_price(info.data)
