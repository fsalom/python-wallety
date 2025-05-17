from pydantic import BaseModel
from typing import List


class WalletDTO(BaseModel):
    id: int
    user_id: int
    cryptos: List[str]