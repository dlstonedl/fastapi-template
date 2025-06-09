from pydantic.v1 import BaseSettings

class RestUserConfig(BaseSettings):
    rest_user_base_url: str = ""

    class Config:
        env_file = ".env"
