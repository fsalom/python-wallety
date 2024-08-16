from fastapi import FastAPI

from wallety.driving.api.user.user_api_adapter import router

app = FastAPI()
app.include_router(router)
