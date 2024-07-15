from pydantic import BaseModel
from .product_schema_model import ProductModel


class CreateProductInputModel(BaseModel):
    source_uniq_id: str
    name: str
    price: int
    image_url: str
