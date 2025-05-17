from typing import List

from wallety.application.ports.driven.wallet_repository_port import WalletRepositoryPort
from wallety.application.ports.driving.wallet_service_port import WalletServicePort
from wallety.domain.entities.wallet import Wallet


class WalletServices(WalletServicePort):
    def __init__(self, wallet_repository: WalletRepositoryPort):
        self.wallet_repository = wallet_repository

    async def create(self, wallet: Wallet) -> Wallet:
        return self.wallet_repository.create(wallet)

    async def list_wallets(self, user_id: int) -> List[Wallet]:
        return self.wallet_repository.list_wallets(user_id)