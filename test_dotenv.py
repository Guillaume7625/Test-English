from dotenv import load_dotenv
import os

load_dotenv()
print("Dotenv loaded successfully.")
print("OPENAI_API_KEY:", os.getenv('OPENAI_API_KEY'))

