from typing import Any
from fastapi import FastAPI, Request
from pydantic import BaseModel


from src.adminsite import site
from src.auth.router import router as auth_router
from src.order.router import router as order_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)


site.mount_app(app)