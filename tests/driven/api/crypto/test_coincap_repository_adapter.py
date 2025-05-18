import os
import pytest
import httpx

from wallety.driven.api.crypto.coincap_repository_adapter import CryptoAPIRepository
from wallety.driven.api.crypto.coincap_mapper import CoincapMapper
from wallety.domain.entities.crypto import Crypto
from wallety.domain.entities.market import Market
from wallety.domain.entities.historical_price import HistoricalPrice


class DummyResponse:
    def __init__(self, json_data):
        self._json_data = json_data

    def raise_for_status(self):
        pass

    def json(self):
        return self._json_data


class DummyClient:
    def __init__(self, responses):
        self._responses = responses
        self._calls = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def get(self, *args, **kwargs):
        response = self._responses[self._calls]
        self._calls += 1
        return response


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("API_KEY", "testkey")


@pytest.fixture
def dummy_mapper():
    return CoincapMapper()


@pytest.mark.asyncio
async def test_get_list(monkeypatch, dummy_mapper):
    data = {
        "data": [
            {"id": "1", "symbol": "SYM1", "name": "Name1", "priceUsd": 1.0, "marketCapUsd": 2.0},
            {"id": "2", "symbol": "SYM2", "name": "Name2", "priceUsd": 3.0, "marketCapUsd": 4.0},
        ]
    }
    responses = [DummyResponse(data)]
    monkeypatch.setattr(httpx, "AsyncClient", lambda: DummyClient(responses))
    repo = CryptoAPIRepository(mapper=dummy_mapper)
    result = await repo.get_list()
    assert isinstance(result, list)
    assert all(isinstance(item, Crypto) for item in result)
    assert result[0].id == "1"
    assert result[1].name == "Name2"


@pytest.mark.asyncio
async def test_get(monkeypatch, dummy_mapper):
    data = {"data": {"id": "1", "symbol": "SYM", "name": "Name", "priceUsd": 5.0, "marketCapUsd": 6.0}}
    responses = [DummyResponse(data)]
    monkeypatch.setattr(httpx, "AsyncClient", lambda: DummyClient(responses))
    repo = CryptoAPIRepository(mapper=dummy_mapper)
    result = await repo.get("1")
    assert isinstance(result, Crypto)
    assert result.price_usd == 5.0


@pytest.mark.asyncio
async def test_get_markets(monkeypatch, dummy_mapper):
    data = {
        "data": [
            {"exchangeId": "E", "baseId": "B", "quoteId": "Q", "baseSymbol": "BS", "quoteSymbol": "QS", "volumeUsd24Hr": 10.0, "priceUsd": 20.0, "volumePercent": 30.0}
        ],
        "timestamp": 123
    }
    responses = [DummyResponse(data)]
    monkeypatch.setattr(httpx, "AsyncClient", lambda: DummyClient(responses))
    repo = CryptoAPIRepository(mapper=dummy_mapper)
    result = await repo.get_markets("1")
    assert isinstance(result, list)
    assert all(isinstance(item, Market) for item in result)
    assert result[0].price_usd == 20.0


@pytest.mark.asyncio
async def test_get_historical_price(monkeypatch, dummy_mapper):
    data = {
        "data": [{"priceUsd": 100.0, "date": "2020-01-01"}],
        "timestamp": 456
    }
    responses = [DummyResponse(data)]
    monkeypatch.setattr(httpx, "AsyncClient", lambda: DummyClient(responses))
    repo = CryptoAPIRepository(mapper=dummy_mapper)
    result = await repo.get_historical_price("1", "d1", start=0, end=1)
    assert isinstance(result, list)
    assert all(isinstance(item, HistoricalPrice) for item in result)
    assert result[0].date == "2020-01-01"