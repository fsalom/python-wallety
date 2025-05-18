import pytest

from fastapi.testclient import TestClient

import wallety.main
from wallety.domain.entities.crypto import Crypto


@pytest.fixture(autouse=True)
def fake_service(monkeypatch):
    class FakeService:
        async def get_list(self):
            return [
                Crypto("1", "SYM1", "Name1", 1.0, 2.0),
                Crypto("2", "SYM2", "Name2", 3.0, 4.0),
            ]

        async def get(self, id):
            return Crypto(id, "SYM", f"Name{id}", 0.0, 0.0)

    monkeypatch.setattr(
        "wallety.driving.api.crypto.crypto_api_adapter.service", FakeService()
    )


client = TestClient(wallety.main.app)


def test_crypto_top100():
    response = client.get("/crypto/top100/")
    assert response.status_code == 200
    assert response.json() == [{"name": "Name1"}, {"name": "Name2"}]


def test_crypto_by_name():
    response = client.get("/crypto/1")
    assert response.status_code == 200
    assert response.json() == {"name": "Name1"}