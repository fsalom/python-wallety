class Tokens:
    def __init__(self,
                 access_token: str,
                 refresh_token: str,
                 expires_in: int,
                 token_type: str = 'Bearer',
                 scope: str = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.scope = scope
