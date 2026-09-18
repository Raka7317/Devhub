from fastapi import Request
from fastapi.responses import JSONResponse


MAX_REQUEST_SIZE = 6 * 1024 * 1024  # 6 MB


async def request_size_middleware(request: Request, call_next):

    content_length = request.headers.get("content-length")

    if content_length:

        try:
            content_length = int(content_length)
        except ValueError:
            return JSONResponse(
                status_code=400,
                content={
                    "detail": "Invalid Content-Length header"
                }
            )

        if content_length > MAX_REQUEST_SIZE:
            return JSONResponse(
                status_code=413,
                content={
                    "detail": "Request too large. Maximum size is 6 MB."
                }
            )

    return await call_next(request)