from pydantic import BaseModel
from typing import List


class CreateWalletDTO(BaseModel):
    cryptos: List[str]