from fastapi import FastAPI
from app.config.settings import get_settings
from app.core.logging_core import logger


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="AI Powered Healthcare Assistant",
    version=settings.APP_VERSION
)

@app.on_event("startup")
async def startup_event():
    logger.info("Clinexa AI application started")
    # Add any startup tasks here, e.g., database connections, etc.

@app.get("/")
def root():
    logger.info("Root endpoint called.")
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running"
    }


@app.get("/health")
def health():
    logger.info("Health check endpoint called.")
    return {
        "status": "UP",
        "debug": settings.DEBUG,
    }