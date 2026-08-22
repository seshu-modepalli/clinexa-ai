from datetime import datetime, timedelta, timezone
import hashlib
import hmac

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)
from jose import JWTError, jwt

from app.config import settings


bearer_scheme = HTTPBearer()


def create_access_token(
    user_id: str,
    role: str
) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": user_id,
        "role": role,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


def decode_access_token(token: str) -> dict:

    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

    except JWTError:
        raise ValueError(
            "Invalid or expired token"
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    )
) -> dict:

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if not user_id:
            raise ValueError("Invalid token")

        return {
            "user_id": user_id
        }

    except ValueError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


def hash_otp(otp: str) -> str:

    return hmac.new(
        settings.JWT_SECRET_KEY.encode(),
        otp.encode(),
        hashlib.sha256
    ).hexdigest()


def verify_otp_hash(
    otp: str,
    otp_hash: str
) -> bool:

    expected_hash = hash_otp(otp)

    return hmac.compare_digest(
        expected_hash,
        otp_hash
    )