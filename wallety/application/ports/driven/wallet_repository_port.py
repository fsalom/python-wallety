from abc import ABC, abstractmethod

from wallety.domain.entities.wallet import Wallet


class WalletRepositoryPort(ABC):
    @abstractmethod
    def create(self, wallet: Wallet) -> Wallet:
        """Persist a new wallet."""
        pass

    @abstractmethod
    def list_wallets(self, user_id: int) -> [Wallet]:
        """Retrieve all wallets for a given user."""
        pass