from fastapi import FastAPI
import uvicorn
from tortoise.contrib.fastapi import register_tortoise

from app.web.controller.rest_user_controller import rest_user_router
from app.infrastructure.core.db_config import TORTOISE_ORM
from app.web.controller.user_controller import user_router

app = FastAPI()

register_tortoise(app,
                  config=TORTOISE_ORM,
                  generate_schemas=False,
                  add_exception_handlers=True)

app.include_router(user_router, prefix="/users", tags=["用户"])
app.include_router(rest_user_router, prefix="/rest-users", tags=["远程用户"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
