from wallety.domain.entities.crypto import Crypto
from wallety.driven.api.crypto.dto.coincap_data_list_dto import CoincapDataListDTO
from wallety.driven.api.crypto.dto.coincap_data_single_dto import CoincapDataSingleDTO
from wallety.driven.api.crypto.dto.coincap_dto import CoincapDTO


class CoincapMapper:
    def from_data_list_to_list_entities(self, crypto_data_dto: CoincapDataListDTO) -> [Crypto]:
        cryptos = [self.from_model_to_entity(item) for item in crypto_data_dto.data]
        return cryptos

    def from_data_single_to_entity(self, crypto_data_dto: CoincapDataSingleDTO) -> [Crypto]:
        return self.from_model_to_entity(crypto_data_dto.data)

    @staticmethod
    def from_model_to_entity(crypto_dto: CoincapDTO) -> Crypto:
        return Crypto(crypto_id=crypto_dto.id,
                      rank=crypto_dto.rank,
                      symbol=crypto_dto.symbol,
                      name=crypto_dto.name,
                      price_usd=crypto_dto.price_usd,
                      market_cap=crypto_dto.market_cap_usd
                      )
