from typing import Dict

from app.models.common import request_context
from app.models.products.product_schema_model import ProductModel
from app.repository.product.product_repository_factory import ProductRepositoryInstance


class __ProductCacheService:
    __cache: Dict[str, ProductModel]

    def __init__(self) -> None:
        self.__cache = {}

    async def get_by_id(
        self,
        context: request_context.RequestContext,
        id: str,
    ) -> ProductModel | None:
        if id in self.__cache:
            return self.__cache[id]

        product = await ProductRepositoryInstance.get_product_by_id(
            context=context, product_id=id
        )

        return product

    async def get_by_source_id(
        self,
        context: request_context.RequestContext,
        source_id: str,
    ) -> ProductModel | None:
        if source_id in self.__cache:
            return self.__cache[source_id]

        product = await ProductRepositoryInstance.get_product_by_source_id(
            context=context, source_id=source_id
        )

        if product is not None:
            await self.put(context=context, key=product.source_uniq_id, product=product)

        return product

    async def put(
        self,
        context: request_context.RequestContext,
        key: str,
        product: ProductModel,
    ):
        self.__cache[key] = product
        return None


ProductCacheServiceInstance = __ProductCacheService()
