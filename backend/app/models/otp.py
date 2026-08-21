from datetime import datetime


class OTP:

    def __init__(
        self,
        phone_number: str,
        otp_hash: str,
        expires_at: datetime,
        attempts: int = 0,
        otp_id: str | None = None,
    ):
        self.id = otp_id
        self.phone_number = phone_number
        self.otp_hash = otp_hash
        self.expires_at = expires_at
        self.attempts = attempts