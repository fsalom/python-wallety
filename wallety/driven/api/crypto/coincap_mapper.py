from typing import List

from wallety.domain.crypto import Crypto
from wallety.domain.historical_price import HistoricalPrice
from wallety.domain.market import Market
from wallety.driven.api.crypto.dto.coincap_data_list_dto import CoincapDataListDTO
from wallety.driven.api.crypto.dto.coincap_data_single_dto import CoincapDataSingleDTO
from wallety.driven.api.crypto.dto.coincap_dto import CoincapDTO
from wallety.driven.api.crypto.dto.historical_price_data_dto import HistoricalPriceData
from wallety.driven.api.crypto.dto.market_data_list_dto import MarketDataResponse


class CoincapMapper:
    def from_data_list_to_list_entities(self, crypto_data_dto: CoincapDataListDTO) -> [Crypto]:
        cryptos = [self.from_model_to_entity(item) for item in crypto_data_dto.data]
        return cryptos

    def from_data_single_to_entity(self, crypto_data_dto: CoincapDataSingleDTO) -> [Crypto]:
        return self.from_model_to_entity(crypto_data_dto.data)

    @staticmethod
    def from_model_to_entity(crypto_dto: CoincapDTO) -> Crypto:
        return Crypto(crypto_id=crypto_dto.id,
                      symbol=crypto_dto.symbol,
                      name=crypto_dto.name,
                      price_usd=crypto_dto.price_usd,
                      market_cap_usd=crypto_dto.market_cap_usd)

    @staticmethod
    def to_domains_market(data: MarketDataResponse) -> List[Market]:
        return [
            Market(
                exchange_id=market.exchange_id,
                base_id=market.base_id,
                quote_id=market.quote_id,
                base_symbol=market.base_symbol,
                quote_symbol=market.quote_symbol,
                volume_usd_24hr=market.volume_usd_24hr,
                price_usd=market.price_usd,
                volume_percent=market.volume_percent
            )
            for market in data.data
        ]

    @staticmethod
    def to_domains_historical_price(prices: List[HistoricalPriceData]) -> List[HistoricalPrice]:
        return [
            HistoricalPrice(
                price_usd=price.price_usd,
                date=price.date
            )
            for price in prices
        ]
