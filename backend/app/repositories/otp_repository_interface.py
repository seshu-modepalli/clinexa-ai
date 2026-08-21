from abc import ABC, abstractmethod

from app.models.otp import OTP


class OTPRepositoryInterface(ABC):

    @abstractmethod
    def save(self, otp: OTP) -> OTP:
        pass

    @abstractmethod
    def find_latest_by_phone(
        self,
        phone_number: str
    ) -> OTP | None:
        pass

    @abstractmethod
    def delete_by_phone(
        self,
        phone_number: str
    ) -> None:
        pass
    @abstractmethod
    def update_attempts(
        self,
        phone_number: str,
        attempts: int
    ) -> None:
        pass