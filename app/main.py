from fastapi import FastAPI, Request
from app.routes.v1.report_router import report_router
import time
# from app.db.migration import init_db
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.utils.config import get_settings


# set the logging basic config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


fastapiApp = FastAPI(
    docs_url="/api/docs",
    title = "Store Monitoring API",
    prefix="/api/v1"
);

settings = get_settings()

fastapiApp.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

@fastapiApp.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


fastapiApp.include_router(report_router, tags=["report"])


print("fast api application wow")
# async def create_db():
#   await init_db()


# @app.on_event("startup")
# async def startup_event():
#     logger.info("Starting up...")
#     await create_db()
#     logger.info("Startup completed")


