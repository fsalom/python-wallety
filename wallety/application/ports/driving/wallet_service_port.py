from abc import ABC, abstractmethod
from typing import List

from wallety.domain.wallet import Wallet


class WalletServicePort(ABC):
    @abstractmethod
    def create(self, wallet: Wallet) -> Wallet:
        """Create a new wallet."""
        pass

    @abstractmethod
    def list_wallets(self, user_id: int) -> List[Wallet]:
        """List wallets for a specific user."""
        pass