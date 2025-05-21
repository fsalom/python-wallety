from typing import List, Optional


class Wallet:
    def __init__(self, wallet_id: Optional[int], user_id: int, cryptos: Optional[List[str]] = None):
        """
        Domain entity representing a cryptocurrency wallet for a specific user.
        :param wallet_id: Unique wallet identifier (None for new wallets).
        :param user_id: Identifier of the owner user.
        :param cryptos: List of cryptocurrency IDs in the wallet.
        """
        self.id = wallet_id
        self.user_id = user_id
        self.cryptos = cryptos or []