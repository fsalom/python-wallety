from wallety.domain.entities.crypto import Crypto
from wallety.driving.api.crypto.crypto_api_mapper import CryptoMapper
from wallety.driving.api.crypto.models.crypto_dto import CryptoDTO


def test_from_entity_to_model():
    crypto = Crypto("1", "SYM", "Name", 10.0, 20.0)
    dto = CryptoMapper.from_entity_to_model(crypto)
    assert isinstance(dto, CryptoDTO)
    assert dto.name == "Name"


def test_from_entities_to_models():
    items = [
        Crypto("1", "SYM", "Name1", 1.0, 2.0),
        Crypto("2", "SYM2", "Name2", 3.0, 4.0),
    ]
    result = CryptoMapper().from_entities_to_models(items)
    assert isinstance(result, list)
    assert all(isinstance(item, CryptoDTO) for item in result)
    assert [item.name for item in result] == ["Name1", "Name2"]