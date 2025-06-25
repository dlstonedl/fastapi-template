import logging

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.application.schemas.base_response import BaseResponse

logger = logging.getLogger(__name__)

async def http_exception_handler(request: Request, exc: HTTPException) -> Response:
    logger.error(exc, exc_info=True)
    return JSONResponse(
        content=BaseResponse.error(str(exc.status_code), exc.detail).dict(),
    )
