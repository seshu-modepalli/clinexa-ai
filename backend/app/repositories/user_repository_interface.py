from abc import ABC, abstractmethod

from app.models.user import User
from app.models.role import UserRole


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

    @abstractmethod
    def update_role(
        self,
        phone_number: str,
        role: UserRole
    ) -> None:
        pass
    @abstractmethod
    def find_by_id(
        self,
        user_id: str
    ) -> User | None:
        pass