from dotenv import load_dotenv
import os

load_dotenv()

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": os.getenv("DB_HOST"),
                "port": int(os.getenv("DB_PORT")),
                "user": os.getenv("DB_USER"),
                "password": os.getenv("DB_PASSWORD"),
                "database": os.getenv("DB_NAME"),
                "charset": "utf8mb4",
                # 连接池配置
                "minsize": int(os.getenv("DB_MIN_SIZE")),
                "maxsize": int(os.getenv("DB_MAX_SIZE")),
                "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT")),
                "init_command": "SET time_zone = '+08:00'",
            }
        }
    },
    "apps": {
        "models": {
            "models": os.getenv("DB_MODELS").split(","),
            "default_connection": "default"
        }
    }
}
