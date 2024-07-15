import uuid
from pydantic import BaseModel, ConfigDict


class UpdateProductInputModel(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    id: str
    source_uniq_id: str | None = None
    name: str | None = None
    price: int | None = None
    image_url: str | None = None
