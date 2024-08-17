from wallety.application.ports.driven.crypto_repository_port import CryptoRepositoryPort
from wallety.application.ports.driving.crypto_service_port import CryptoServicePort
from wallety.domain.entities.crypto import Crypto


class CryptoServices(CryptoServicePort):
    def __init__(self, crypto_repository_port: CryptoRepositoryPort):
        self.crypto_repository_port = crypto_repository_port

    def top100(self):
        return self.crypto_repository_port.top100()

    def get(self, crypto) -> [Crypto]:
        return self.crypto_repository_port.get(crypto)
