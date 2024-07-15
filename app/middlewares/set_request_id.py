from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
from starlette.datastructures import MutableHeaders


class SetRequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        x_request_id = request.headers.get("X-Request-Id")
        if x_request_id is None:
            new_header = MutableHeaders(request._headers)
            new_header["X-Request-Id"] = uuid.uuid4().__str__()
            request._headers = new_header
            request.scope.update(headers=request.headers.raw)

        response = await call_next(request)
        return response
