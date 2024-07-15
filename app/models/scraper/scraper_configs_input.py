from pydantic import BaseModel
from enum import Enum


class ScrapFrom(Enum):
    DENTAL_STALL = "dentalstall"


class ScraperConfigsInput(BaseModel):
    scrap_from: ScrapFrom = ScrapFrom.DENTAL_STALL
    after: int = 1
    size: int = 1
