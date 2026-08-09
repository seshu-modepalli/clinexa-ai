from pymongo.database import Database

from app.database.connection import MongoDB


def get_database() -> Database:
    return MongoDB.get_database()