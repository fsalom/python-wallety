from wallety.domain.entities.wallet import Wallet
from wallety.driven.db.wallet.models.wallet_db import WalletDB


class WalletDBMapper:
    @staticmethod
    def from_entity_to_model(wallet: Wallet) -> WalletDB:
        return WalletDB(id=wallet.id, user_id=wallet.user_id, cryptos=wallet.cryptos)

    @staticmethod
    def from_model_to_entity(wallet_db: WalletDB) -> Wallet:
        return Wallet(wallet_id=wallet_db.id, user_id=wallet_db.user_id, cryptos=wallet_db.cryptos)