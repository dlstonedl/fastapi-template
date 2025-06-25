from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.application.schemas.base_response import BaseResponse

async def http_exception_handler(request: Request, exc: HTTPException) -> Response:
    print(exc)
    return JSONResponse(
        content=BaseResponse.error(str(exc.status_code), exc.detail).dict(),
    )
