from fastapi import Request
from ..common.errors import NotFoundError
from starlette.middleware.base import BaseHTTPMiddleware


class CheckAccessTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        access_token = request.headers.get("X-Access-Token")
        if access_token is None:
            return NotFoundError(
                message="Access Token not found in headers"
            ).to_json_response()

        response = await call_next(request)
        return response
