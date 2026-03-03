import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def test_db():
    print("Connecting to DB...")
    client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    try:
        info = await client.server_info()
        print("Connected successfully!", info.get("version"))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(test_db())
