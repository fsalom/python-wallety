from wallety.domain.crypto import Crypto
from wallety.driving.api.crypto.models.crypto_dto import CryptoDTO


class CryptoMapper:
    def from_entities_to_models(self, cryptos: [Crypto]) -> [CryptoDTO]:
        return [self.from_entity_to_model(crypto) for crypto in cryptos]

    @staticmethod
    def from_entity_to_model(crypto: Crypto) -> CryptoDTO:
        return CryptoDTO(name=crypto.name)
