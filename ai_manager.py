from google import genai
from google.genai import types
import config
import logging
from itertools import cycle

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verify API keys
if not config.GEMINI_API_KEYS:
    raise ValueError("No Gemini API keys provided in config!")

# Create a cyclic iterator for round-robin key selection
key_iterator = cycle(config.GEMINI_API_KEYS)

def get_next_key():
    return next(key_iterator)

# System instruction to make the bot pro-level assistant
SYS_INSTRUCT = (
    "You are a highly advanced AI Assistant on Telegram. You provide clear, accurate, and professional answers. "
    "If user asks for code, provide full working code blocks. "
    "Be helpful, concise, and polite. You understand and speak Hinglish and Hindi well if requested."
)

class AIManager:
    def __init__(self):
        pass

    async def generate_response(self, text, history=[]):
        keys_tried = 0
        max_retries = len(config.GEMINI_API_KEYS)

        while keys_tried < max_retries:
            current_key = get_next_key()
            logger.info(f"Trying Gemini response with key ending in ...{current_key[-4:]}")
            try:
                client = genai.Client(api_key=current_key)

                # Format history for new SDK
                # New SDK uses Content objects with role and parts
                formatted_history = []
                for msg in history:
                    role = msg.get('role', 'user')
                    if role == 'bot':
                        role = 'model'
                    parts = msg.get('parts', [])
                    if parts:
                        formatted_history.append(
                            types.Content(role=role, parts=[types.Part(text=p) if isinstance(p, str) else types.Part(text=str(p)) for p in parts])
                        )

                # Add current user message
                formatted_history.append(
                    types.Content(role='user', parts=[types.Part(text=text)])
                )

                response = client.models.generate_content(
                    model='gemini-2.5-flash-preview-04-17',
                    contents=formatted_history,
                    config=types.GenerateContentConfig(
                        system_instruction=SYS_INSTRUCT,
                        temperature=0.7,
                        top_p=0.95,
                        top_k=40,
                        max_output_tokens=8192,
                    )
                )
                return response.text

            except Exception as e:
                logger.error(f"Error with key ...{current_key[-4:]}: {e}")
                keys_tried += 1

        # If all keys failed
        logger.error("All Gemini API keys failed!")
        return "Sorry, I am currently experiencing high load. Please try again later. 😞"

ai = AIManager()
