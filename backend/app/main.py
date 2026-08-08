from fastapi import FastAPI
from app.config.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="AI Powered Healthcare Assistant",
    version=settings.APP_VERSION
)


@app.get("/")
def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running"
    }


@app.get("/health")
def health():
    return {
        "status": "UP",
        "debug": settings.DEBUG,
    }