from typing import Annotated
from fastapi import Header
from .common.errors import NotFoundError
from .models.common.request_context import RequestContext
from uuid import UUID, uuid4
from .models.user.user_schema_model import UserModel
from datetime import datetime
from .configs.app_configs import AppConfigsInstance
from . import constants


async def get_request_context(
    x_access_token: Annotated[str | None, Header()] = None,
    x_request_id: Annotated[str | None, Header()] = None,
) -> RequestContext:
    if x_request_id is None:
        x_request_id = uuid4().__str__()

    if x_access_token != AppConfigsInstance.get_global_access_token:
        raise NotFoundError(message="access_token not found in headers")

    return RequestContext(
        request_id=x_request_id,
        user=constants.GLOBAL_USER,
        request_time=datetime.now(),
    )
