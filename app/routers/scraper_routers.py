from fastapi import APIRouter, Body, Depends
from typing import Annotated

from fastapi.responses import JSONResponse

from app.services.scraper.scraper_service_factory import ScraperServiceFactory
from app.models.scraper.scraper_configs_input import ScraperConfigsInput
from app.models.common.request_context import RequestContext
from app.dependencies import get_request_context
from fastapi import BackgroundTasks


router = APIRouter(prefix="/scrap_data")


@router.post("/")
async def scrap_data(
    context: Annotated[RequestContext, Depends(get_request_context)],
    input: ScraperConfigsInput,
    background_tasks: BackgroundTasks,
):
    try:
        print("scrap_data: got request to scrap data")

        # run task in background
        scraper_function = ScraperServiceFactory(scrap_from=input.scrap_from).scrap
        background_tasks.add_task(scraper_function, context, input)
        response_message = {
            "success": True,
            "message": f"""scraping job scheduled successfully with requestId '{context.request_id}'. Notification will be received on '{context.user.email}' on job completion""",
            "trace_id": context.request_id,
        }

        print("scrap_data: Added background task to scrap data")
        return JSONResponse(content=response_message)
    except Exception as exc:
        raise exc
