from app.models.role import UserRole
from app.models.user import User
from app.repositories.user_repository import MongoUserRepository
from app.database.dependencies import get_database


def create_dev_admin():

    database = get_database()

    repository = MongoUserRepository(database)

    phone_number = "9000000000"

    existing_user = repository.find_by_phone(
        phone_number
    )

    if existing_user:

        repository.update_role(
            phone_number,
            UserRole.SYSTEM_ADMIN
        )

        print("Development admin already exists.")

        return

    user = User(
        phone_number=phone_number,
        role=UserRole.SYSTEM_ADMIN,
        is_verified=True
    )

    repository.save(user)

    print(
        "Development SYSTEM_ADMIN created."
    )


if __name__ == "__main__":
    create_dev_admin()