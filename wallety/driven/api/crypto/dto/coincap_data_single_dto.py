from pydantic import BaseModel
from wallety.driven.api.crypto.dto.coincap_dto import CoincapDTO


class CoincapDataSingleDTO(BaseModel):
    data: CoincapDTO
