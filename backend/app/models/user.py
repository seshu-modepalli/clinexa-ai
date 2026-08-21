from datetime import datetime, timezone

from app.models.role import UserRole


class User:

    def __init__(
        self,
        phone_number: str,
        role: UserRole = UserRole.PATIENT,
        user_id: str | None = None,
        is_verified: bool = False,
        is_active: bool = True,
        created_at: datetime | None = None,
    ):
        self.id = user_id
        self.phone_number = phone_number
        self.role = role
        self.is_verified = is_verified
        self.is_active = is_active
        self.created_at = created_at or datetime.now(timezone.utc)