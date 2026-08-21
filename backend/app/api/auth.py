from fastapi import APIRouter, Depends
from pymongo.database import Database
from app.core.security import get_current_user
from app.database.dependencies import get_database
from app.repositories.user_repository import MongoUserRepository
from app.schemas.auth import (
    OTPRequest,
    OTPVerifyRequest,
    TokenResponse
)
from app.services.auth_service import AuthService
from app.services.otp_provider_factory import get_otp_provider
from app.repositories.otp_repository import MongoOTPRepository

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


def get_auth_service(
    database: Database = Depends(get_database)
) -> AuthService:

    user_repository = MongoUserRepository(database)

    otp_repository = MongoOTPRepository(database)

    otp_provider = get_otp_provider()

    return AuthService(
        user_repository=user_repository,
        otp_repository=otp_repository,
        otp_provider=otp_provider
    )

@router.post("/request-otp")
async def request_otp(
    request: OTPRequest,
    auth_service: AuthService = Depends(get_auth_service)
):

    await auth_service.request_otp(
        request.phone_number
    )

    return {
        "message": "OTP generated successfully"
    }


@router.post(
    "/verify-otp",
    response_model=TokenResponse
)
async def verify_otp(
    request: OTPVerifyRequest,
    auth_service: AuthService = Depends(get_auth_service)
):

    token = await auth_service.verify_otp(
        request.phone_number,
        request.otp
    )

    return TokenResponse(
        access_token=token
    )
@router.get("/me")
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    return current_user