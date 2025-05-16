
class Crypto:
    def __init__(self,
                 crypto_id: str,
                 symbol: str,
                 name: str,
                 price_usd: float,
                 market_cap_usd: float):
        self.id = crypto_id
        self.symbol = symbol
        self.name = name
        self.price_usd = price_usd
        self.market_cap_usd = market_cap_usd
