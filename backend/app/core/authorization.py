from typing import Callable

from fastapi import Depends, HTTPException, status
from pymongo.database import Database

from app.core.security import get_current_user
from app.database.dependencies import get_database
from app.models.role import UserRole
from app.repositories.user_repository import (
    MongoUserRepository
)


def require_roles(
    *allowed_roles: UserRole
) -> Callable:

    def role_checker(
        token_user: dict = Depends(get_current_user),
        database: Database = Depends(get_database)
    ) -> dict:

        user_repository = MongoUserRepository(
            database
        )

        user = user_repository.find_by_id(
            token_user["user_id"]
        )

        if user is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={
                    "WWW-Authenticate": "Bearer"
                }
            )

        if not user.is_active:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        if user.role not in allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return {
            "user_id": user.id,
            "phone_number": user.phone_number,
            "role": user.role.value
        }

    return role_checker