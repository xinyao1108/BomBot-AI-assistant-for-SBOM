from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from beanie import init_beanie

class Database:
    __client: AsyncIOMotorClient | None = None
    __db: AsyncIOMotorDatabase | None = None
    
    @staticmethod
    async def connect(mongoConnStr: str, mongoDB: str) -> None:
        Database.__client = AsyncIOMotorClient(
            mongoConnStr,
            tls=True,
            tlsAllowInvalidCertificates=True
        )

        Database.__db = Database.client()[mongoDB]
        await init_beanie(database=Database.db(), document_models=[
            "app.model.context.SoftwareContext"
        ])

    @staticmethod
    def close() -> None:
        if Database.__client == None:
            raise ConnectionError("Cannot close database client. Database client is not connected")
        
        Database.__client.close()

    @staticmethod
    def client() -> AsyncIOMotorClient:
        if Database.__client == None:
            raise ConnectionError("Database client is None, database client is not connected")
        
        return Database.__client
    
    @staticmethod
    def db() -> AsyncIOMotorDatabase:
        if Database.__db == None:
            raise ConnectionError("Database is None, database is not connected")
        
        return Database.__db    