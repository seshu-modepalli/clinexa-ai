from pydantic import BaseModel, Field


class OTPRequest(BaseModel):
    phone_number: str = Field(
        ...,
        min_length=10,
        max_length=15
    )


class OTPVerifyRequest(BaseModel):
    phone_number: str = Field(
        ...,
        min_length=10,
        max_length=15
    )

    otp: str = Field(
        ...,
        min_length=6,
        max_length=6
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    phone_number: str
    role: str
    is_verified: bool
    is_active: bool