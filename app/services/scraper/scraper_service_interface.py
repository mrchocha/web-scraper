from abc import ABC, abstractmethod

from app.models.common import request_context
from app.models.scraper.scraper_configs_input import ScraperConfigsInput


class IScraperService(ABC):
    @abstractmethod
    async def scrap(
        context: request_context.RequestContext, input: ScraperConfigsInput
    ):
        pass
