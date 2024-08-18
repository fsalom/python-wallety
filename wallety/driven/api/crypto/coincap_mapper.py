from wallety.domain.entities.crypto import Crypto
from wallety.driven.api.crypto.dto.crypto_dto import CryptoDTO, CryptoDataDTO


class CoincapMapper:
    def from_list_models_to_list_entities(self, crypto_data_dto: CryptoDataDTO) -> [Crypto]:
        cryptos = [self.from_model_to_entity(**item) for item in crypto_data_dto.data]
        return cryptos

    @staticmethod
    def from_model_to_entity(crypto_dto: CryptoDTO) -> Crypto:
        return Crypto(crypto_id=crypto_dto.crypto_id,
                      rank=crypto_dto.rank,
                      symbol=crypto_dto.symbol,
                      name=crypto_dto.name,
                      price_usd=float(crypto_dto.price_usd),
                      market_cap=crypto_dto.market_cap)