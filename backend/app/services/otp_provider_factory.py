from app.config import settings
from app.services.mock_otp_provider import MockOTPProvider
from app.services.otp_provider import OTPProvider


def get_otp_provider() -> OTPProvider:

    provider = settings.OTP_PROVIDER.lower()

    if provider == "mock":
        return MockOTPProvider()

    raise ValueError(
        f"Unsupported OTP provider: {provider}"
    )