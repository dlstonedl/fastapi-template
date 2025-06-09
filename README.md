### FastAPI
默认接口文档：http://127.0.0.1:8000/docs

### ASGI服务器：uvicorn
```
uvicorn main:app --reload
生产环境：gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### poetry：虚拟环境、模块管理、依赖管理
```
pip3 install poetry
pip3 show poetry
MAC为了防止冲突：brew install poetry
poetry -v

poetry init
poetry config --list
poetry config virtualenvs.in-project true
poetry env use python3
poetry add fastapi
poetry remove fastapi
poetry show --tree
poetry lock
pyproject.toml -> poetry.lock -> 虚拟环境

brew install poetry，缺少poetry-core
curl -sSL https://install.python-poetry.org | python3 -
配置PATH路径

下载新项目
poetry install
```

### 迁移工具：aerich
```
配置文件：aerich.ini，可直接配置在pyproject.toml中
依赖：poetry add tomlkit --dev
-- 初始化
poetry run aerich init -t app.core.db_config.TORTOISE_ORM
poetry run aerich init-db
-- SQL变更
poetry run aerich migrate --name "add_user_model"
poetry run aerich upgrade
```

### 代办事项
- 权限校验（类似ThreadLocal）
- 统一异常处理
- 数据库时区
- 缓存使用
- 多数据源
- DockerFile
- 补充测试



