from typing import List

from fastapi import APIRouter

from wallety.application.services.wallet_services import WalletServices
from wallety.driven.db.wallet.wallet_db_adapter import DBWalletAdapter
from wallety.driving.api.wallet.wallet_api_mapper import WalletMapper
from wallety.driving.api.wallet.models.create_wallet_dto import CreateWalletDTO
from wallety.driving.api.wallet.models.wallet_dto import WalletDTO
from wallety.domain.wallet import Wallet

router = APIRouter()
_db_adapter = DBWalletAdapter()
_service = WalletServices(wallet_repository=_db_adapter)


@router.post("/users/{user_id}/wallets", response_model=WalletDTO)
async def create_wallet(user_id: int, payload: CreateWalletDTO):
    """
    Create a new cryptocurrency wallet for a given user.
    """
    wallet = Wallet(wallet_id=None, user_id=user_id, cryptos=payload.cryptos)
    created = await _service.create(wallet)
    return WalletMapper.from_entity_to_model(created)


@router.get("/users/{user_id}/wallets", response_model=List[WalletDTO])
async def list_wallets(user_id: int):
    """
    List all cryptocurrency wallets for a given user.
    """
    wallets = await _service.list_wallets(user_id)
    return [WalletMapper.from_entity_to_model(w) for w in wallets]