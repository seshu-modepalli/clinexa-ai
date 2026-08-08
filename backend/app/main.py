from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import get_settings
from app.core.exception_handlers import (
    clinexa_exception_handler,
    generic_exception_handler
)
from app.core.exceptions import ResourceNotFoundException
from app.core.logging_core import logger
from app.database.connection import MongoDB


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    logger.info("Starting Clinexa AI application")

    # Startup
    MongoDB.connect()

    logger.info("Clinexa AI application started successfully")

    yield

    # Shutdown
    logger.info("Shutting down Clinexa AI application")

    MongoDB.disconnect()

    logger.info("Clinexa AI application stopped")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI Powered Healthcare Assistant",
    version=settings.APP_VERSION,
    lifespan=lifespan
)


app.add_exception_handler(
    ResourceNotFoundException,
    clinexa_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)


@app.get("/")
def root():

    logger.info("Root endpoint requested")

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running"
    }


@app.get("/health")
def health():

    logger.info("Health check requested")

    mongo_status = "UP"

    try:
        MongoDB.get_database().command("ping")
    except Exception:
        mongo_status = "DOWN"

    return {
        "status": "UP",
        "debug": settings.DEBUG,
        "database": mongo_status
    }