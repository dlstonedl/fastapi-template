import logging

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.application.schemas.base_response import BaseResponse
from app.domain.exception.base_exception import BusinessException

logger = logging.getLogger(__name__)

async def http_exception_handler(request: Request, exc: BusinessException) -> Response:
    logger.error(exc, exc_info=True)
    return JSONResponse(
        content=BaseResponse.error(exc.get_error_code(), exc.get_error_message()).dict(),
    )
