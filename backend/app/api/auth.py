from fastapi import APIRouter, Depends, HTTPException,status
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
from app.core.authorization import require_roles
from app.models.role import UserRole

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
    "/verify-otp"
)
async def verify_otp(
    request: OTPVerifyRequest,
    auth_service: AuthService = Depends(get_auth_service)
):

    return await auth_service.verify_otp(
        request.phone_number,
        request.otp
    )

@router.get("/me")
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    database: Database = Depends(get_database)
):

    user_repository = MongoUserRepository(
        database
    )

    user = user_repository.find_by_id(
        current_user["user_id"]
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return {
        "user_id": user.id,
        "phone_number": user.phone_number,
        "role": user.role.value,
        "is_verified": user.is_verified,
        "is_active": user.is_active
    }

@router.get("/patient-test")
async def patient_test(
    current_user: dict = Depends(
        require_roles(UserRole.PATIENT)
    )
):
    return {
        "message": "Patient authorization successful",
        "user": current_user
    }

@router.get("/doctor-test")
async def doctor_test(
    current_user: dict = Depends(
        require_roles(UserRole.DOCTOR)
    )
):
    return {
        "message": "Doctor authorization successful",
        "user": current_user
    }

@router.get("/hospital-admin-test")
async def hospital_admin_test(
    current_user: dict = Depends(
        require_roles(UserRole.HOSPITAL_ADMIN)
    )
):
    return {
        "message": "Hospital admin authorization successful",
        "user": current_user
    }

@router.get("/system-admin-test")
async def system_admin_test(
    current_user: dict = Depends(
        require_roles(UserRole.SYSTEM_ADMIN)
    )
):
    return {
        "message": "System admin authorization successful",
        "user": current_user
    }
@router.post("/dev/set-role/{phone_number}/{role}")
async def set_dev_role(
    phone_number: str,
    role: UserRole,
    current_user: dict = Depends(
        require_roles(UserRole.SYSTEM_ADMIN)
    ),
    database: Database = Depends(get_database)
):
    user_repository = MongoUserRepository(database)

    user = user_repository.find_by_phone(
        phone_number
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user_repository.update_role(
        phone_number,
        role
    )

    return {
        "message": "Role updated successfully",
        "phone_number": phone_number,
        "role": role.value
    }