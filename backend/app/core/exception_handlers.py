from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ClinexaException
from app.core.logging_core import logger


async def clinexa_exception_handler(
    request: Request,
    exc: ClinexaException
):
    logger.error(
        "Application error | method=%s | path=%s | error_code=%s | message=%s",
        request.method,
        request.url.path,
        exc.error_code,
        exc.message
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.error_code,
            "message": exc.message
        }
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unhandled exception | method=%s | path=%s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred"
        }
    )