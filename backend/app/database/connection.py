from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from app.config.settings import get_settings
from app.core.logging_core import logger
from app.database.indexes import create_indexes


settings = get_settings()


class MongoDB:
    """
    Manages the MongoDB connection for Clinexa AI.
    """

    client: MongoClient | None = None
    database = None

    @classmethod
    def connect(cls):
        if cls.client is not None:
            return

        try:
            logger.info("Connecting to MongoDB")

            cls.client = MongoClient(
                settings.MONGODB_URL,
                serverSelectionTimeoutMS=5000
            )

            # Force connection test
            cls.client.admin.command("ping")

            cls.database = cls.client[
                settings.DATABASE_NAME
            ]
            create_indexes(cls.database)
            logger.info(
                "MongoDB connected successfully | database=%s",
                settings.DATABASE_NAME
            )

        except ConnectionFailure as exc:
            logger.error(
                "MongoDB connection failed | error=%s",
                str(exc)
            )

            cls.client = None
            cls.database = None

            raise

    @classmethod
    def disconnect(cls):
        if cls.client is not None:
            logger.info("Closing MongoDB connection")

            cls.client.close()

            cls.client = None
            cls.database = None

            logger.info("MongoDB connection closed")

    @classmethod
    def get_database(cls):
        if cls.database is None:
            raise RuntimeError(
                "MongoDB is not connected"
            )

        return cls.database