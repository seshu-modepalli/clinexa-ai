from datetime import datetime

from pymongo.database import Database
from app.models.role import UserRole
from app.models.user import User
from app.repositories.user_repository_interface import (
    UserRepositoryInterface
)


class MongoUserRepository(UserRepositoryInterface):

    COLLECTION_NAME = "users"

    def __init__(self, database: Database):
        self.collection = database[self.COLLECTION_NAME]

    def find_by_phone(
        self,
        phone_number: str
    ) -> User | None:

        document = self.collection.find_one(
            {
                "phone_number": phone_number
            }
        )

        if not document:
            return None

        return User(
            phone_number=document["phone_number"],
            role=UserRole(document["role"]),
            user_id=str(document["_id"]),
            is_verified=document.get("is_verified", False),
            is_active=document.get("is_active", True),
            created_at=document.get("created_at")
        )

    def save(self, user: User) -> User:

        document = {
            "phone_number": user.phone_number,
            "role": user.role.value,
            "is_verified": user.is_verified,
            "is_active": user.is_active,
            "created_at": user.created_at
        }

        result = self.collection.insert_one(document)

        user.id = str(result.inserted_id)

        return user