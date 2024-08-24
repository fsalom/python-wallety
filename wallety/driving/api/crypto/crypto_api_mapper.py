from wallety.domain.entities.crypto import Crypto
from wallety.driving.api.crypto.models.crypto_dto import CryptoDTO


class CryptoMapper:
    def from_entities_to_models(self, cryptos: [Crypto]) -> [CryptoDTO]:
        cryptos = [self.from_entity_to_model(**item) for item in cryptos]
        return cryptos

    @staticmethod
    def from_entity_to_model(crypto: Crypto) -> CryptoDTO:
        return CryptoDTO(name=crypto.name)
