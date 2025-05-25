from typing import List, Optional

from wallety.application.ports.driven.crypto_repository_port import CryptoRepositoryPort
from wallety.application.ports.driving.crypto_service_port import CryptoServicePort
from wallety.domain.crypto import Crypto
from wallety.domain.historical_price import HistoricalPrice
from wallety.domain.market import Market


class CryptoServices(CryptoServicePort):
    def __init__(self, crypto_repository: CryptoRepositoryPort):
        self.crypto_repository = crypto_repository

    async def get_list(self) -> List[Crypto]:
        return await self.crypto_repository.get_list()

    async def get(self, id) -> Crypto:
        return await self.crypto_repository.get(id)

    async def get_markets(self, id) -> List[Market]:
        return await self.crypto_repository.get_markets(id)

    async def get_historical_price(
        self,
        id: str,
        interval: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
    ) -> List[HistoricalPrice]:
        return await self.crypto_repository.get_historical_price(id, interval, start, end)
