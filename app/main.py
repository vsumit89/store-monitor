from fastapi import FastAPI, Request
from app.routes.v1.report_router import report_router
import time
# from app.db.migration import init_db
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.utils.config import get_settings


# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a logger instance for this module
logger = logging.getLogger(__name__)

# Create the FastAPI instance
fastapiApp = FastAPI(
    docs_url="/api/docs",
    title = "Store Monitoring API",
    prefix="/api/v1"
);

# Get application settings
settings = get_settings()

# CORS middleware to handle Cross-Origin Resource Sharing
fastapiApp.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Middleware to calculate and add X-Process-Time header to responses
@fastapiApp.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


fastapiApp.include_router(report_router, tags=["report"])


