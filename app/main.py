from fastapi import FastAPI
import uvicorn
from tortoise.contrib.fastapi import register_tortoise

from app.api.users import user_router
from app.core.db_config import TORTOISE_ORM

app = FastAPI()

register_tortoise(app,
                  config=TORTOISE_ORM,
                  generate_schemas=False,
                  add_exception_handlers=True)

app.include_router(user_router, prefix="/users", tags=["用户"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
