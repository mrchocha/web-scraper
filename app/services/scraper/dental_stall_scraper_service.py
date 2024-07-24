import asyncio
from typing import List

from app.models.notification.notification_schema_model import SendNotificationInput
from app.models.products.create_product_input_model import CreateProductInputModel
from app.models.products.product_schema_model import ProductModel
from app.common.errors import InternalServerError
from app.models.common import request_context
from app.models.products.update_product_input_model import UpdateProductInputModel
from app.repository.product.product_cache_service import ProductCacheServiceInstance
from app.repository.product.product_repository_factory import (
    ProductRepositoryInstance,
)
from app.services.notification.notification_service_factory import (
    NotificationServiceInstance,
)
from app.services.scraper.models import (
    ParsedProductModel,
    ProcessedProductMetadataModel,
)
from .scraper_service_interface import IScraperService
from app.models.scraper.scraper_configs_input import ScraperConfigsInput
import aiohttp, aiohttp_retry
from aiohttp_retry import ExponentialRetry
from bs4 import BeautifulSoup


class __DentalStallScraperService(IScraperService):
    __DENTAL_STALL_BASE_URL: str = "https://dentalstall.com"
    __EXP_RETRY_CONFIGS: ExponentialRetry = ExponentialRetry(
        attempts=5,
        statuses=[429, 500, 502, 503, 504],
        factor=1,
    )

    def build_url(
        self,
        page_no: int,
    ) -> str:
        base_url = self.__DENTAL_STALL_BASE_URL

        return f"{base_url}/shop/page/{page_no}/"

    def parse_product_data(self, content: bytes) -> List[ParsedProductModel]:
        soup = BeautifulSoup(content, "html5lib")
        content_div = soup.find("div", {"class": "mf-shop-content"})

        product_divs = content_div.find_all("div", {"class": "product-inner"})

        products = []

        for product_div in product_divs:
            thumbnail_div = product_div.find(
                "img", {"class": "attachment-woocommerce_thumbnail"}
            )
            price_div = product_div.find("bdi")
            product_name = thumbnail_div["title"]
            product_image = thumbnail_div["data-lazy-src"]
            product_price = float(price_div.text[1:])

            product_page_link = product_div.find("a")["href"]
            source_uniq_id = product_page_link.replace(
                f"{ self.__DENTAL_STALL_BASE_URL}/product/", ""
            ).replace("/", "")

            products.append(
                CreateProductInputModel(
                    source_uniq_id=source_uniq_id,
                    name=product_name,
                    price=product_price,
                    image_url=product_image,
                )
            )
        return products

    async def fetch_page_data(self, url: str) -> bytes:
        try:
            async with aiohttp.ClientSession() as client_session:
                retry_client = aiohttp_retry.RetryClient(
                    client_session, retry_options=self.__EXP_RETRY_CONFIGS
                )
                async with retry_client.get(url) as web_page_response:
                    if web_page_response.status != 200:
                        raise InternalServerError(
                            message="Error while fetching page.",
                            payload={
                                "url": url,
                                "status_code": web_page_response.status_code,
                                "data": web_page_response.__str__(),
                            },
                        )
                    text = await web_page_response.read()
                    return text.decode("utf-8")
        except Exception as ex:
            raise ex

    async def __upsert_data_in_db(
        self, context: request_context.RequestContext, products: List[ProductModel]
    ) -> ProcessedProductMetadataModel:
        products_repo = ProductRepositoryInstance

        create_count = 0
        updated_count = 0

        for product in products:
            fetched_product = await ProductCacheServiceInstance.get_by_source_id(
                context=context, source_id=product.source_uniq_id
            )

            if fetched_product is None:
                create_count += 1
                created_product = await products_repo.create_product(
                    context=context,
                    create_product_input=CreateProductInputModel(
                        **product.model_dump()
                    ),
                )
                await ProductCacheServiceInstance.put(
                    context == context,
                    key=product.source_uniq_id,
                    product=created_product,
                )
                continue

            update_required = False
            update_product_input = UpdateProductInputModel(id=fetched_product.id)

            if product.price != fetched_product.price:
                update_required = True
                update_product_input.price = product.price

            if product.image_url != fetched_product.image_url:
                update_required = True
                update_product_input.image_url = product.image_url

            if product.name != fetched_product.name:
                update_required = True
                update_product_input.image_url = product.name

            if update_required:
                updated_count += 1
                updated_product = await products_repo.update_product_by_id(
                    context=context, update_product_input=update_product_input
                )
                await ProductCacheServiceInstance.put(
                    context=context, key=product.source_uniq_id, product=updated_product
                )

        return ProcessedProductMetadataModel(
            created_count=create_count,
            updated_count=updated_count,
            fetched_count=len(products),
        )

    async def __scrap_and_update_data_in_db(
        self, context: request_context.RequestContext, url: str
    ) -> dict:
        print(
            f"DentalStallScraperService.__scrap_and_update_data_in_db: started scraping page with url {url}"
        )
        page_data = await self.fetch_page_data(url=url)
        products = self.parse_product_data(page_data)
        scrap_meta = await self.__upsert_data_in_db(context=context, products=products)

        print(
            f"DentalStallScraperService.__scrap_and_update_data_in_db: completed scraping page with url {url}"
        )
        return scrap_meta

    async def scrap(
        self, context: request_context.RequestContext, input: ScraperConfigsInput
    ):
        # await asyncio.sleep(10)
        start_page = input.after
        end_page = start_page + input.size

        print(
            f"DentalStallScraperService.scrap: scraping data from total {end_page-start_page} pages, starting from {start_page}"
        )

        tasks = []
        for page_no in range(start_page, end_page):
            url = self.build_url(page_no)
            tasks.append(self.__scrap_and_update_data_in_db(context, url))

        processed_model_metadata_list = await asyncio.gather(*tasks)

        created_count = 0
        updated_count = 0
        fetched_count = 0

        for processed_model_metadata in processed_model_metadata_list:
            fetched_count += processed_model_metadata.fetched_count
            updated_count += processed_model_metadata.updated_count
            created_count += processed_model_metadata.created_count

        overall_processed_model_metadata = ProcessedProductMetadataModel(
            created_count=created_count,
            updated_count=updated_count,
            fetched_count=fetched_count,
        )

        # send notification to user
        await NotificationServiceInstance.send(
            context,
            SendNotificationInput(
                receiver_id=context.user.id,
                message="Successfully Scraped data!",
                payload=overall_processed_model_metadata.model_dump(),
            ),
        )

        print(
            f"DentalStallScraperService.scrap: successfully scraped all the pages with metadata {overall_processed_model_metadata}"
        )


DentalStallScraperServiceInstance = __DentalStallScraperService()
