from fastapi.responses import JSONResponse
from fastapi import status


class AppError(Exception):
    # Constructor or Initializer
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        payload: dict | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.payload = payload

    # __str__ is to print() the value
    def __str__(self):
        return repr(
            {
                "message": self.message,
                "statue": self.status_code,
                "payload": self.payload,
            }
        )

    def to_json_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.status_code,
            content={"message": self.message, "payload": self.payload},
        )


class NotFoundError(AppError):
    "Raised when value is not found"

    def __init__(
        self,
        message: str,
        payload: dict | None = None,
    ):
        super().__init__(message, status.HTTP_404_NOT_FOUND, payload)


class InvalidInputError(AppError):
    "Raised when input is invalid"

    def __init__(
        self,
        message: str,
        payload: dict | None = None,
    ):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, payload)


class InternalServerError(AppError):
    "Raised when internal server error"

    def __init__(
        self,
        message: str,
        payload: dict | None = None,
    ):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, payload)
