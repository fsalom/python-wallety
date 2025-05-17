from pydantic import BaseModel
from typing import List


class WalletDB(BaseModel):
    id: int
    user_id: int
    cryptos: List[str]