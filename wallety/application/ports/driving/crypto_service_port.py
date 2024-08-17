from abc import ABC, abstractmethod

from wallety.domain.entities.crypto import Crypto


class CryptoServicePort(ABC):
    @abstractmethod
    def top100(self):
        pass

    @abstractmethod
    def get(self, crypto) -> [Crypto]:
        pass
