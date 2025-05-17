from fastapi import FastAPI

from wallety.driving.api.crypto.crypto_api_adapter import router as crypto_router
from wallety.driving.api.wallet.wallet_api_adapter import router as wallet_router

app = FastAPI()
app.include_router(crypto_router)
app.include_router(wallet_router)
app.include_router(wallet_router)