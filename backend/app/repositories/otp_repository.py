from pymongo.database import Database

from app.models.otp import OTP
from app.repositories.otp_repository_interface import (
    OTPRepositoryInterface
)


class MongoOTPRepository(OTPRepositoryInterface):

    COLLECTION_NAME = "otps"

    def __init__(self, database: Database):
        self.collection = database[self.COLLECTION_NAME]

    def save(self, otp: OTP) -> OTP:

        document = {
            "phone_number": otp.phone_number,
            "otp_hash": otp.otp_hash,
            "expires_at": otp.expires_at,
            "attempts": otp.attempts,
        }

        result = self.collection.insert_one(document)

        otp.id = str(result.inserted_id)

        return otp

    def find_latest_by_phone(
        self,
        phone_number: str
    ) -> OTP | None:

        document = self.collection.find_one(
            {
                "phone_number": phone_number
            },
            sort=[
                ("_id", -1)
            ]
        )

        if not document:
            return None

        return OTP(
            phone_number=document["phone_number"],
            otp_hash=document["otp_hash"],
            expires_at=document["expires_at"],
            attempts=document.get("attempts", 0),
            otp_id=str(document["_id"])
        )

    def delete_by_phone(
        self,
        phone_number: str
    ) -> None:

        self.collection.delete_many(
            {
                "phone_number": phone_number
            }
        )
    def update_attempts(
        self,
        phone_number: str,
        attempts: int
        ) -> None:

        self.collection.update_one(
        {
            "phone_number": phone_number
        },
        {
            "$set": {
                "attempts": attempts
            }
        }
    )