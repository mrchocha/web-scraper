from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.common.errors import AppError


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except AppError as app_exc:
            return JSONResponse(
                status_code=app_exc.status_code,
                content={
                    "success": False,
                    "trace_id": request.headers.get("X-Request-Id"),
                    "error_message": f"Request failed with message: {app_exc.message}",
                    "payload": app_exc.payload,
                },
            )
        except Exception as exc:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "trace_id": request.headers.get("X-Request-Id"),
                    "error_message": exc.__str__(),
                },
            )
