# Pro-Level AI Assistant Telegram Bot

A highly advanced, AI-powered Telegram assistant bot built using Python and the `aiogram` framework. This bot uses Google's Gemini 2.5 Flash API for intelligent text responses and Pollinations AI for free, on-demand image generation.

## Features

- **Conversational AI**: Powered by Google's Gemini API for smart, context-aware chatting.
- **Image Generation**: Simply type `/image <prompt>` to generate custom images for free using Pollinations AI.
- **Memory Context**: The bot remembers the last 20 messages of conversation using MongoDB for fluid interactions.
- **User Management**: Admins can view statistics and manage users (ban/unban capabilities in code).
- **Pro Performance**: Fully asynchronous architecture using `aiohttp` and Motor (Async MongoDB driver).

## Local Setup

### Prerequisites
- Python 3.9+
- MongoDB database (local or Atlas)
- Google Gemini API Key
- Telegram Bot Token from [@BotFather](https://t.me/botfather)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Abhisahu143/Sifra_bot.git
   cd Sifra_bot
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Environment:**
   Create a `.env` file in the root directory (like the provided `.env` but with your own keys):
   ```ini
   # Multiple Gemini Keys can be provided separated by comma for round-robin usage
   GEMINI_API_KEY=your_gemini_key_1,your_gemini_key_2
   
   # MongoDB Connection String
   MONGO_URL=mongodb+srv://<user>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
   
   # Telegram Bot Token
   BOT_TOKEN=your_telegram_bot_token
   
   # Admin Telegram User ID (Get your ID from @userinfobot)
   ADMIN_ID=your_telegram_id
   ```

4. **Run the Bot:**
   ```bash
   python bot.py
   ```

## Deploying on Render.com

This bot is designed to run perfectly as a "Background Worker" on Render.

1. Create a GitHub repository and push all files (excluding `.env`, which is in `.gitignore`).
2. Go to Render.com and create a new **Background Worker**.
3. Connect your GitHub repository.
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `python bot.py`
6. Go to the **Environment** tab in your Render service settings and add all the variables from your `.env` file (`GEMINI_API_KEY`, `MONGO_URL`, `BOT_TOKEN`, `ADMIN_ID`).
7. Click **Save and Deploy**. Your bot should be online in a few minutes!

## Commands List

- `/start` - Start the bot and get a welcome message.
- `/image <prompt>` - Generate an AI image (e.g., `/image a futuristic city`).
- `/clear` - Wipes your conversation memory to start fresh.
- `/stats` - (Admins only) View total number of users.

---
*Created with Python, Aiogram, and Gemini API.*
