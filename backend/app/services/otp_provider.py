from abc import ABC, abstractmethod


class OTPProvider(ABC):

    @abstractmethod
    async def generate_otp(self) -> str:
        pass