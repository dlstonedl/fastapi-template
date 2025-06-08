from dotenv import load_dotenv
import os

load_dotenv()

TORTOISE_ORM = {
    "connections": {
        "default": os.getenv("DB_URL")
        # "engine": "tortoise.backends.asyncmy",
        # "credentials": {
        #     "host": "127.0.0.1",
        #     "port": 3306,
        #     "user": "root",
        #     "password": "123456",
        #     "database": "fastapi",
        #     "charset": "utf8mb4",
        #     # 连接池配置
        #     "minsize": 5,
        #     "maxsize": 10,
        #     "connect_timeout": 10,
        #     "init_command": "SET time_zone = '+08:00'",  # 可选初始化命令
        # }
    },
    "apps": {
        "models": {
            "models": os.getenv("DB_MODELS").split(","),
            "default_connection": "default"
        }
    }
}
