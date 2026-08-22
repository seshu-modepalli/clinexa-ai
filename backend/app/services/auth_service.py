from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    hash_otp,
    verify_otp_hash
)
from app.models.otp import OTP
from app.repositories.otp_repository_interface import (
    OTPRepositoryInterface
)
from app.repositories.user_repository_interface import (
    UserRepositoryInterface
)
from app.services.otp_provider import OTPProvider
from app.config import settings


class AuthService:

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        otp_repository: OTPRepositoryInterface,
        otp_provider: OTPProvider
    ):
        self.user_repository = user_repository
        self.otp_repository = otp_repository
        self.otp_provider = otp_provider

    async def request_otp(
        self,
        phone_number: str
    ) -> None:

        otp = await self.otp_provider.generate_otp()

        otp_hash = hash_otp(otp)

        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(
                minutes=settings.OTP_EXPIRY_MINUTES
            )
        )

        # Remove previous OTPs for this phone number
        self.otp_repository.delete_by_phone(
            phone_number
        )

        otp_record = OTP(
            phone_number=phone_number,
            otp_hash=otp_hash,
            expires_at=expires_at,
            attempts=0
        )

        self.otp_repository.save(otp_record)

        # Development only
        print(
            f"[DEV OTP] "
            f"Phone: {phone_number} | "
            f"OTP: {otp} | "
            f"Expires: {expires_at}"
        )

    async def verify_otp(
    self,
    phone_number: str,
    otp: str
) -> dict:

        otp_record = (
            self.otp_repository.find_latest_by_phone(
                phone_number
            )
        )

        if otp_record is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="OTP not found or expired"
            )

        now = datetime.now(timezone.utc)

        expires_at = otp_record.expires_at

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(
        tzinfo=timezone.utc
        )

        if now >= expires_at:

            self.otp_repository.delete_by_phone(
                phone_number
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="OTP has expired"
            )

        if otp_record.attempts >= settings.OTP_MAX_ATTEMPTS:

            self.otp_repository.delete_by_phone(
                phone_number
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Maximum OTP attempts exceeded"
            )

        valid = verify_otp_hash(
            otp,
            otp_record.otp_hash
        )

        if not valid:

            otp_record.attempts += 1
            self.otp_repository.update_attempts(
            phone_number,
            otp_record.attempts
        )

            # Remove the OTP after max attempts
            if otp_record.attempts >= settings.OTP_MAX_ATTEMPTS:

                self.otp_repository.delete_by_phone(
                    phone_number
                )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid OTP"
            )

        # OTP is single-use
        self.otp_repository.delete_by_phone(
            phone_number
        )

        user = self.user_repository.find_by_phone(
    phone_number
)
        if user is None:

            return {
                "is_registered": False,
                "registration_required": True,
                "phone_number": phone_number
            }

        return {
            "is_registered": True,
            "registration_required": False,
            "access_token": create_access_token(
                user_id=user.id,
                role=user.role.value
            ),
            "token_type": "bearer"
        }