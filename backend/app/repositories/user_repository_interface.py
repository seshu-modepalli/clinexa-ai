from abc import ABC, abstractmethod

from app.models.user import User


class UserRepositoryInterface(ABC):

    @abstractmethod
    def find_by_phone(
        self,
        phone_number: str
    ) -> User | None:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass