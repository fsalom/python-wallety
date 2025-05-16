from abc import ABC, abstractmethod
from typing import List, Optional

from wallety.domain.entities.crypto import Crypto
from wallety.domain.entities.historical_price import HistoricalPrice
from wallety.domain.entities.market import Market


class CryptoServicePort(ABC):
    @abstractmethod
    def get_coins(self) -> List[Crypto]:
        pass

    @abstractmethod
    def get_coin_with_id(self, id) -> Crypto:
        pass

    @abstractmethod
    def get_markets_for_coin_with_id(self, id) -> List[Market]:
        pass

    @abstractmethod
    def get_historical_price_for_coin_with_id(
            self,
            id: str,
            interval: str,
            start: Optional[int] = None,
            end: Optional[int] = None
    ) -> List[HistoricalPrice]:
        pass
