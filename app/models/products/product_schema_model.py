from ..common.base_entity_model import BaseEntityModel
from pydantic import BaseModel


class ProductModel(BaseEntityModel):
    source_uniq_id: str
    name: str
    price: int
    image_url: str
