from pydantic.v1 import BaseSettings

class RemoteUrlConfig(BaseSettings):
    REST_USER_BASE_URL: str = ""

    class Config:
        env_file = ".env"
