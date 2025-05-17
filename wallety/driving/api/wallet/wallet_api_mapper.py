from wallety.domain.entities.wallet import Wallet
from wallety.driving.api.wallet.models.wallet_dto import WalletDTO


class WalletMapper:
    @staticmethod
    def from_entity_to_model(wallet: Wallet) -> WalletDTO:
        return WalletDTO(id=wallet.id, user_id=wallet.user_id, cryptos=wallet.cryptos)