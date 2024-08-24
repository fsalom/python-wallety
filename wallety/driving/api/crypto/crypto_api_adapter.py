from typing import List
from fastapi import APIRouter

from wallety.application.services.crypto_services import CryptoServices
from wallety.driven.api.crypto.coincap_mapper import CoincapMapper
from wallety.driven.api.crypto.coincap_repository_adapter import CryptoAPIRepository
from wallety.driving.api.crypto.crypto_api_mapper import CryptoMapper
from wallety.driving.api.crypto.models.crypto_dto import CryptoDTO

router = APIRouter()
crypto_api_repository_adapter = CryptoAPIRepository(mapper=CoincapMapper())
mapper = CryptoMapper()
service = CryptoServices(crypto_repository_port=crypto_api_repository_adapter)


@router.get("/crypto/top100/", response_model=List[CryptoDTO])
async def crypto_top100():
    cryptos = await service.top100()
    cryptos_dto = [CryptoMapper.from_entity_to_model(crypto) for crypto in cryptos]
    return cryptos_dto


@router.get("/crypto/{name}", response_model=CryptoDTO)
async def crypto(name: str):
    crypto = await service.get(name)
    return CryptoMapper.from_entity_to_model(crypto)
