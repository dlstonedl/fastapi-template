from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from app.adapter.exception.exception_handler import http_exception_handler
from app.domain.exception.exception import BusinessException
from app.infrastructure.common.logging_config import setup_logging

# 加载.env环境变量，只需要在这里调用一次
load_dotenv('.env')
load_dotenv('.env.local', override=True)

import uvicorn
from tortoise.contrib.fastapi import register_tortoise

from app.adapter.controller import rest_user_controller, user_controller
from app.adapter.middleware.auth_middleware import auth_middleware
from app.infrastructure.common.httpx_client_singleton import HttpxClientSingleton
from app.infrastructure.common.tortoise_orm_config import TORTOISE_ORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # 在应用启动时获取httpx客户端
        HttpxClientSingleton.get_client()
        yield
    finally:
        # 在应用关闭时关闭httpx客户端
        await HttpxClientSingleton.close()

setup_logging()
app = FastAPI(lifespan=lifespan)

register_tortoise(app,
                  config=TORTOISE_ORM,
                  generate_schemas=False,
                  add_exception_handlers=True)

# 路由
app.include_router(user_controller.router)
app.include_router(rest_user_controller.router)

# 中间件
app.middleware("http")(auth_middleware)

# 异常处理
app.exception_handler(BusinessException)(http_exception_handler)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
