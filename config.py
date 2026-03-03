import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# Get Gemini API keys correctly, handling spaces
keys_str = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_KEYS = [k.strip() for k in keys_str.split(",") if k.strip()]

MONGO_URL = os.getenv("MONGO_URL")

DB_NAME = "telegram_ai_bot"
COLLECTION_USERS = "users"
COLLECTION_CHATS = "chats"
