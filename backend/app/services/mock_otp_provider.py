import secrets

from app.services.otp_provider import OTPProvider


class MockOTPProvider(OTPProvider):

    async def generate_otp(self) -> str:

        return f"{secrets.randbelow(1_000_000):06d}"