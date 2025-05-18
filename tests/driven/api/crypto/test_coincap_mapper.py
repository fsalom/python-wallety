import pytest

from wallety.driven.api.crypto.coincap_mapper import CoincapMapper
from wallety.driven.api.crypto.dto.coincap_dto import CoincapDTO
from wallety.domain.entities.crypto import Crypto


@pytest.fixture()
def mapper():
    return CoincapMapper()


def test_from_model_to_entity():
    dto = CoincapDTO(id="1", symbol="SYM", name="Name", priceUsd=1.0, marketCapUsd=2.0)
    entity = CoincapMapper.from_model_to_entity(dto)
    assert isinstance(entity, Crypto)
    assert entity.id == "1"
    assert entity.symbol == "SYM"
    assert entity.name == "Name"
    assert entity.price_usd == 1.0
    assert entity.market_cap_usd == 2.0


def test_from_data_list_to_list_entities(mapper):
    data = [
        CoincapDTO(id="1", symbol="SYM", name="Name", priceUsd=1.0, marketCapUsd=2.0),
        CoincapDTO(id="2", symbol="SYM2", name="Name2", priceUsd=3.0, marketCapUsd=4.0),
    ]
    class ListDto:
        def __init__(self, data):
            self.data = data

    list_dto = ListDto(data)
    result = mapper.from_data_list_to_list_entities(list_dto)
    assert len(result) == 2
    assert all(isinstance(item, Crypto) for item in result)
    assert result[1].name == "Name2"


def test_from_data_single_to_entity(mapper):
    dto = CoincapDTO(id="1", symbol="SYM", name="Name", priceUsd=1.0, marketCapUsd=2.0)
    class SingleDto:
        def __init__(self, data):
            self.data = data

    single_dto = SingleDto(dto)
    result = mapper.from_data_single_to_entity(single_dto)
    assert isinstance(result, Crypto)
    assert result.id == "1"


def test_to_domains_market(mapper):
    from wallety.driven.api.crypto.dto.market_data_list_dto import MarketDataResponse
    from wallety.driven.api.crypto.dto.market_info_dto import MarketData
    from wallety.domain.entities.market import Market

    info = MarketData(
        exchangeId="E",
        baseId="B",
        quoteId="Q",
        baseSymbol="BS",
        quoteSymbol="QS",
        volumeUsd24Hr=1.0,
        priceUsd=2.0,
        volumePercent=3.0,
    )
    list_response = MarketDataResponse(data=[info], timestamp=123)
    result = mapper.to_domains_market(list_response)
    assert len(result) == 1
    assert isinstance(result[0], Market)
    assert result[0].exchange_id == "E"


def test_to_domains_historical_price(mapper):
    from wallety.driven.api.crypto.dto.historical_price_data_dto import HistoricalPriceData
    from wallety.domain.entities.historical_price import HistoricalPrice

    data = HistoricalPriceData(priceUsd=1.0, date="2020-01-01")
    result = mapper.to_domains_historical_price([data])
    assert isinstance(result[0], HistoricalPrice)
    assert result[0].price_usd == 1.0