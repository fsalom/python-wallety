
class Crypto:
    def __init__(self,
                 crypto_id: int,
                 rank: str,
                 symbol: str,
                 name: str,
                 price_usd: float,
                 market_cap: float):
        self.id = crypto_id
        self.rank = rank
        self.symbol = symbol
        self.name = name
        self.price_usd = price_usd
        self.market_cap = market_cap
