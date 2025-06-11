from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRoute
from tortoise.contrib.fastapi import register_tortoise

from app.adapter.controller import rest_user_controller, user_controller
from app.adapter.middleware.auth_middleware import auth_middleware
from app.infrastructure.common.httpx_client_singleton import HttpxClientSingleton
from app.infrastructure.common.tortoise_orm_config import TORTOISE_ORM

@asynccontextmanager
async def lifespan(app: FastAPI):
    HttpxClientSingleton.get_client()
    yield
    await HttpxClientSingleton.close()

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"
app = FastAPI(lifespan=lifespan, generate_unique_id_function=custom_generate_unique_id)

register_tortoise(app,
                  config=TORTOISE_ORM,
                  generate_schemas=False,
                  add_exception_handlers=True)

# 路由
app.include_router(user_controller.router)
app.include_router(rest_user_controller.router)

# 中间件
app.middleware("http")(auth_middleware)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
