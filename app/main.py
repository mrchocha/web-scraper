from fastapi import FastAPI
from .routers import scraper_routers
from .middlewares.check_access_token import CheckAccessTokenMiddleware
from .middlewares.set_request_id import SetRequestIdMiddleware
from .middlewares.error_handler import ErrorHandlerMiddleware
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


app = FastAPI()

app.add_middleware(CheckAccessTokenMiddleware)
app.add_middleware(SetRequestIdMiddleware)
app.add_middleware(ErrorHandlerMiddleware)


app.include_router(scraper_routers.router)


@app.get("/")
async def hello():
    return {"message": "hello from Rahul!"}
