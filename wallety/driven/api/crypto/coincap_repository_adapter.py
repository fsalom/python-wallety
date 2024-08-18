
import httpx
from fastapi import HTTPException

from wallety.application.ports.driven.crypto_repository_port import CryptoRepositoryPort
from wallety.domain.entities.crypto import Crypto
from wallety.driven.api.crypto.coincap_mapper import CoincapMapper
from wallety.driven.api.crypto.dto.crypto_dto import CryptoDataDTO


class CryptoAPIRepository(CryptoRepositoryPort):

    def __init__(self, mapper: CoincapMapper):
        self.mapper = mapper

    async def top100(self) -> [Crypto]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.coincap.io/v2/assets")
                response.raise_for_status()
                json = response.json()
                crypto_data = CryptoDataDTO(**json)
                return self.mapper.from_list_models_to_list_entities(crypto_data)
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code,
                                detail=f"Error fetching data: {exc.response.text}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting data: {str(exc)}")

    async def get(self, coin) -> Crypto:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://api.coincap.io/v2/assets/{coin}")
                response.raise_for_status()
                json = response.json()
                crypto_dto = CryptoDataDTO(**json)
                return self.mapper.from_model_to_entity(crypto_dto)
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code,
                                detail=f"Error fetching data: {exc.response.text}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting data: {str(exc)}")
