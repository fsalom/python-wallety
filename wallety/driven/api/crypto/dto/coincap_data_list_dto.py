from typing import List
from pydantic import BaseModel
from wallety.driven.api.crypto.dto.coincap_dto import CoincapDTO


class CoincapDataListDTO(BaseModel):
    data: List[CoincapDTO]

