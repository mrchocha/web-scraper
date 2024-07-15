from typing import Annotated
from pydantic import (
    BaseModel,
    ConfigDict,
    PlainSerializer,
)
import uuid
from datetime import datetime

CustomDateTime = Annotated[
    datetime,
    PlainSerializer(lambda x: x.isoformat(), return_type=str),
]


class BaseEntityModel(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    id: str = ""
    created_at: str | None = datetime.now().isoformat()
    updated_at: str | None = datetime.now().isoformat()
