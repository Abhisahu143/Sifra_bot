import google.generativeai as genai
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
SYS_INSTRUCT = '''
You are a highly advanced AI Assistant on Telegram. You provide clear, accurate, and professional answers.
You can format your answers using Markdown (bold, italic, code blocks).
If user asks for code, provide full working code blocks.
Be helpful, concise, and polite. Your native tongue is English, but you understand and speak Hinglish and Hindi well if requested.
'''

generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
}

class AIManager:
    def __init__(self):
        pass

    async def generate_response(self, text, history=[]):
        keys_tried = 0
        max_retries = len(config.GEMINI_API_KEYS)
        last_error = None
        
        while keys_tried < max_retries:
            current_key = get_next_key()
            logger.info(f"Trying Gemini response with key ending in ...{current_key[-4:]}")
            try:
                genai.configure(api_key=current_key)
                
                # Format history for Gemini API:
                # Gemini format: [{'role': 'user', 'parts': ['hello']}, {'role': 'model', 'parts': ['hi']}]
                formatted_history = []
                for msg in history:
                    # Map standard roles to gemini roles
                    role = msg.get('role', 'user')
                    if role == 'bot':
                        role = 'model'
                    elif role == 'user':
                        role = 'user'
                        
                    formatted_history.append({
                        "role": role,
                        "parts": msg.get('parts', [])
                    })

                model = genai.GenerativeModel(
                    model_name='gemini-2.5-flash',
                    system_instruction=SYS_INSTRUCT,
                    generation_config=generation_config
                )
                
                chat = model.start_chat(history=formatted_history)
                response = chat.send_message(text)
                return response.text
                
            except Exception as e:
                logger.error(f"Error with key ...{current_key[-4:]}: {e}")
                last_error = e
                keys_tried += 1
                
        # If all keys failed
        logger.error("All Gemini API keys failed!")
        return "Sorry, I am currently experiencing high load or an issue with my brain (API keys limit). Please try again later. 😞"

ai = AIManager()
