import logging

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.adapter.middleware.user_context import current_user, UserContext

logger = logging.getLogger(__name__)

async def auth_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    # 示例：从 Header 中提取 token
    token = request.headers.get("Authorization")
    if not token:
        return await call_next(request)

    # 简化：假设 token 是 user_id:username 的格式
    token_context = None
    try:
        parts = token.replace("Bearer ", "").split(":")
        token_context = current_user.set(UserContext(id=int(parts[0]), username=parts[1]))
        logger.info(current_user.get())
        # 执行下一个中间件或请求处理
        return await call_next(request)
    except Exception:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})
    finally:
        # 清理上下文变量
        if token_context:
            current_user.reset(token_context)
        logger.info(current_user.get())

