from abc import ABC, abstractmethod
from typing import List, Optional

from wallety.domain.entities.crypto import Crypto
from wallety.domain.entities.historical_price import HistoricalPrice
from wallety.domain.entities.market import Market


class CryptoRepositoryPort(ABC):
    @abstractmethod
    def get_list(self) -> [Crypto]:
        pass

    @abstractmethod
    def get(self, coin) -> Crypto:
        pass

    @abstractmethod
    def get_markets(self, id) -> List[Market]:
        pass

    @abstractmethod
    def get_historical_price(
            self,
            id: str,
            interval: str,
            start: Optional[int] = None,
            end: Optional[int] = None
    ) -> List[HistoricalPrice]:
        pass