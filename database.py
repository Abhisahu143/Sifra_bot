from motor.motor_asyncio import AsyncIOMotorClient
import datetime
import config

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(config.MONGO_URL)
        self.db = self.client[config.DB_NAME]
        self.users = self.db[config.COLLECTION_USERS]
        self.chats = self.db[config.COLLECTION_CHATS]

    async def add_user(self, user_id, username, first_name):
        user = await self.users.find_one({"_id": user_id})
        if not user:
            await self.users.insert_one({
                "_id": user_id,
                "username": username,
                "first_name": first_name,
                "joined_date": datetime.datetime.utcnow(),
                "messages_count": 0,
                "banned": False
            })

    async def inc_message_count(self, user_id):
        await self.users.update_one(
            {"_id": user_id},
            {"$inc": {"messages_count": 1}}
        )

    async def get_user(self, user_id):
        return await self.users.find_one({"_id": user_id})

    async def get_all_users_count(self):
        return await self.users.count_documents({})

    async def get_all_users(self):
        return await self.users.find({}).to_list(length=None)

    async def ban_user(self, user_id):
        return await self.users.update_one({"_id": user_id}, {"$set": {"banned": True}})

    async def unban_user(self, user_id):
        return await self.users.update_one({"_id": user_id}, {"$set": {"banned": False}})

    # Chat history for context
    async def add_message(self, user_id, role, text):
        message = {
            "role": role,
            "parts": [{"text": text}],
            "timestamp": datetime.datetime.utcnow()
        }
        await self.chats.update_one(
            {"_id": user_id},
            {"$push": {"history": {"$each": [message], "$slice": -20}}}, # Keep last 20 messages for context
            upsert=True
        )

    async def get_history(self, user_id):
        chat = await self.chats.find_one({"_id": user_id})
        if chat and "history" in chat:
            # Format required by Gemini
            # Remove timestamp for gemini
            formatted_history = []
            for msg in chat["history"]:
                formatted_history.append({
                    "role": msg["role"],
                    "parts": [msg["parts"][0]["text"]] # gemini expects string parts or dicts
                })
            return formatted_history
        return []

    async def clear_history(self, user_id):
        await self.chats.update_one({"_id": user_id}, {"$set": {"history": []}})

db = Database()
