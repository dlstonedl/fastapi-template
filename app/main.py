from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from tortoise.contrib.fastapi import register_tortoise

from app.adapter.controller.rest_user_controller import rest_user_router
from app.infrastructure.common.httpx_client_singleton import HttpxClientSingleton
from app.infrastructure.common.tortoise_orm_config import TORTOISE_ORM
from app.adapter.controller.user_controller import user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    HttpxClientSingleton.get_client()
    yield
    await HttpxClientSingleton.close()
app = FastAPI(lifespan=lifespan)

register_tortoise(app,
                  config=TORTOISE_ORM,
                  generate_schemas=False,
                  add_exception_handlers=True)

app.include_router(user_router, prefix="/users", tags=["用户"])
app.include_router(rest_user_router, prefix="/rest-users", tags=["远程用户"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
