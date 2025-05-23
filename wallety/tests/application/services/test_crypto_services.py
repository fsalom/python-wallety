import pytest

from wallety.application.services.crypto_services import CryptoServices
from wallety.domain.crypto import Crypto
from wallety.domain.market import Market
from wallety.domain.historical_price import HistoricalPrice


class DummyRepo:
    async def get_list(self):
        return [Crypto("1", "SYM", "Name", 10.0, 20.0)]

    async def get(self, id):
        return Crypto(id, "SYM", f"Name{id}", 1.0, 2.0)

    async def get_markets(self, id):
        return [
            Market(
                exchange_id="E",
                base_id="B",
                quote_id="Q",
                base_symbol="BS",
                quote_symbol="QS",
                volume_usd_24hr=1.0,
                price_usd=2.0,
                volume_percent=3.0,
            )
        ]

    async def get_historical_price(self, id, interval, start=None, end=None):
        return [HistoricalPrice(price_usd=1.0, date="2020-01-01")]


@pytest.mark.asyncio
async def test_get_list():
    repo = DummyRepo()
    service = CryptoServices(repo)
    result = await service.get_list()
    assert isinstance(result, list)
    assert all(isinstance(item, Crypto) for item in result)
    assert result[0].id == "1"
    assert result[0].name == "Name"


@pytest.mark.asyncio
async def test_get():
    repo = DummyRepo()
    service = CryptoServices(repo)
    result = await service.get("2")
    assert isinstance(result, Crypto)
    assert result.id == "2"
    assert result.name == "Name2"


@pytest.mark.asyncio
async def test_get_markets():
    repo = DummyRepo()
    service = CryptoServices(repo)
    result = await service.get_markets("1")
    assert isinstance(result, list)
    assert all(isinstance(item, Market) for item in result)
    assert result[0].exchange_id == "E"


@pytest.mark.asyncio
async def test_get_historical_price():
    repo = DummyRepo()
    service = CryptoServices(repo)
    result = await service.get_historical_price("1", "d1", start=0, end=1)
    assert isinstance(result, list)
    assert all(isinstance(item, HistoricalPrice) for item in result)
    assert result[0].date == "2020-01-01"


@pytest.mark.asyncio
async def test_get_coins_alias():
    repo = DummyRepo()
    service = CryptoServices(repo)
    result_alias = await service.get_coins()
    result_direct = await service.get_list()
    assert len(result_alias) == len(result_direct)
    assert [c.id for c in result_alias] == [c.id for c in result_direct]


@pytest.mark.asyncio
async def test_get_coin_with_id_alias():
    repo = DummyRepo()
    service = CryptoServices(repo)
    result_alias = await service.get_coin_with_id("3")
    result_direct = await service.get("3")
    assert isinstance(result_alias, type(result_direct))
    assert result_alias.id == result_direct.id


@pytest.mark.asyncio
async def test_get_markets_for_coin_with_id_alias():
    repo = DummyRepo()
    service = CryptoServices(repo)
    result_alias = await service.get_markets_for_coin_with_id("4")
    result_direct = await service.get_markets("4")
    assert len(result_alias) == len(result_direct)
    assert [m.exchange_id for m in result_alias] == [m.exchange_id for m in result_direct]


@pytest.mark.asyncio
async def test_get_historical_price_for_coin_with_id_alias():
    repo = DummyRepo()
    service = CryptoServices(repo)
    result_alias = await service.get_historical_price_for_coin_with_id(
        "5", "d1", start=0, end=1
    )
    result_direct = await service.get_historical_price("5", "d1", start=0, end=1)
    assert len(result_alias) == len(result_direct)
    assert [h.date for h in result_alias] == [h.date for h in result_direct]