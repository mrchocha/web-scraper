from abc import ABC, abstractmethod

from app.models.common import request_context
from app.models.products.create_product_input_model import CreateProductInputModel
from app.models.products.product_schema_model import ProductModel
from app.models.products.update_product_input_model import UpdateProductInputModel


class IProductRepository(ABC):
    @abstractmethod
    async def create_product(
        self,
        context: request_context.RequestContext,
        product: CreateProductInputModel,
    ) -> ProductModel:
        pass

    @abstractmethod
    async def get_product_by_id(
        self,
        context: request_context.RequestContext,
        product_id: str,
    ) -> ProductModel | None:
        pass

    @abstractmethod
    async def get_product_by_source_id(
        self,
        context: request_context.RequestContext,
        source_id: str,
    ) -> ProductModel | None:
        pass

    @abstractmethod
    async def update_product_by_id(
        self,
        context: request_context.RequestContext,
        product: UpdateProductInputModel,
    ) -> ProductModel:
        pass
