from typing import List

from wallety.application.ports.driven.wallet_repository_port import WalletRepositoryPort
from wallety.domain.entities.wallet import Wallet


class DBWalletAdapter(WalletRepositoryPort):
    def __init__(self):
        self.wallets: List[Wallet] = []

    def create(self, wallet: Wallet) -> Wallet:
        # Assign a simple incremental ID
        new_id = len(self.wallets) + 1
        wallet.id = new_id
        self.wallets.append(wallet)
        return wallet

    def list_wallets(self, user_id: int) -> List[Wallet]:
        return [w for w in self.wallets if w.user_id == user_id]