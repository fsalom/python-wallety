from abc import ABC, abstractmethod

from wallety.domain.entities.crypto import Crypto


class CryptoRepositoryPort(ABC):
    @abstractmethod
    def top100(self) -> [Crypto]:
        pass

    @abstractmethod
    def get(self, coin) -> Crypto:
        pass
