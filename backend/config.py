import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

class Settings:
    # Fetch API key
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Default model (fast + free)
    MODEL: str = os.getenv("MODEL", "llama-3.1-8b-instant")

    # Default DB - sql lite
    DATABASE_URL = "sqlite:///./chat.db"


settings = Settings()


