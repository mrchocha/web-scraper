from app.models.scraper.scraper_configs_input import ScrapFrom
from app.common.errors import NotFoundError
from app.services.scraper.scraper_service_interface import IScraperService
from .dental_stall_scraper_service import DentalStallScraperServiceInstance


def ScraperServiceFactory(scrap_from: ScrapFrom) -> IScraperService:
    match scrap_from:
        case ScrapFrom.DENTAL_STALL:
            return DentalStallScraperServiceInstance
        case _:
            raise NotFoundError(
                "Scraping service not found for url type '{scrap_from}'",
            )
