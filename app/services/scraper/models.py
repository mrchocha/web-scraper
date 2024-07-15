from pydantic import BaseModel


class ParsedProductModel(BaseModel):
    source_uniq_id: str
    name: str
    price: int
    image_url: str


class ProcessedProductMetadataModel(BaseModel):
    created_count: int = 0
    updated_count: int = 0
    fetched_count: int = 0
