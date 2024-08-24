from pydantic import BaseModel


class CryptoDTO(BaseModel):
    name: str
