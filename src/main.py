from typing import Any
from fastapi import FastAPI, Request
from pydantic import BaseModel


from src.auth.router import router as auth_router
from src.order.router import router as order_router

app = FastAPI(
    title="My App",
    description="Description of my app.",
    version="1.0",
    docs_url='/docs',
    openapi_url='/openapi.json', # This line solved my issue, in my case it was a lambda function
    redoc_url=None
)

app.include_router(auth_router)
app.include_router(order_router)


# site.mount_app(app)