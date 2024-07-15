from app.models.common.db_configs import DBTypeEnum
from app.common.errors import NotFoundError

from app.configs.app_configs import AppConfigsInstance
from app.repository.product.local_product_repository import __LocalProductRepository
from app.repository.product.product_repository_interface import IProductRepository


def __ProductRepositoryFactory() -> IProductRepository:
    db_type = AppConfigsInstance.get_db_type
    match db_type:
        case DBTypeEnum.LOCAL:
            return __LocalProductRepository()
        case _:
            raise NotFoundError(
                f"Product repository service not found for db type type '{db_type}'",
            )


ProductRepositoryInstance = __ProductRepositoryFactory()
