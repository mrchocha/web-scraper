from app.models.common import request_context
from app.models.products.create_product_input_model import CreateProductInputModel
from app.models.products.product_schema_model import ProductModel
from app.models.products.update_product_input_model import UpdateProductInputModel
from app.repository.product.product_repository_interface import IProductRepository

from pysondb import db
from datetime import datetime
import asyncio

DB = db.getDb("local-data.json")


class __LocalProductRepository(IProductRepository):
    async def __get_cache_key_for_get_product_by_id(
        self,
        context: request_context.RequestContext,
        product_id: str,
    ):
        await asyncio.sleep(1)
        return product_id

    async def __get_cache_key_for_get_product_by_source_id(
        self,
        context: request_context.RequestContext,
        source_id: str,
    ):
        await asyncio.sleep(1)
        return source_id

    async def create_product(
        self,
        context: request_context.RequestContext,
        create_product_input: CreateProductInputModel,
    ) -> ProductModel:
        product_model = ProductModel(**create_product_input.model_dump())
        product_id = DB.add(product_model.model_dump())
        product_model.id = product_id

        return product_model

    async def get_product_by_id(
        self,
        context: request_context.RequestContext,
        product_id: str,
    ) -> ProductModel | None:
        product_dicts = DB.getById(int(product_id))

        if len(product_dicts) == 0:
            return None

        response = ProductModel(**product_dicts[0])
        return

    async def get_product_by_source_id(
        self,
        context: request_context.RequestContext,
        source_id: str,
    ) -> ProductModel | None:
        product_dicts = DB.getBy({"source_uniq_id": source_id})

        if len(product_dicts) == 0:
            return None

        return ProductModel(**product_dicts[0])

    async def update_product_by_id(
        self,
        context: request_context.RequestContext,
        update_product_input: UpdateProductInputModel,
    ) -> ProductModel:
        update_query = update_product_input.model_dump()
        update_query["updated_at"] = datetime.now()
        DB.updateById(update_product_input.id, update_query)

        return self.get_product_by_id(
            context=context, product_id=update_product_input.id
        )
