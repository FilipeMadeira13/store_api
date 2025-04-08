from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from store.core.config import settings


class MongoClient:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(settings.DATABASE_URL)

    def get(self) -> AsyncIOMotorClient:
        return self.client


db_client = MongoClient()
