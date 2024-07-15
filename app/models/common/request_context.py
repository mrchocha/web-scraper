from pydantic import BaseModel
from uuid import UUID, uuid4
from ..user.user_schema_model import UserModel
from datetime import datetime


class RequestContext(BaseModel):
    request_id: str = uuid4().__str__()
    user: UserModel
    request_time: datetime = datetime.now()
