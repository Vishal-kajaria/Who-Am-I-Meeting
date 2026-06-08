from dotenv import load_dotenv
from supabase import create_client
import os

# Load variables from .env file
load_dotenv()

REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY",
    "SERPER_API_KEY",
    "SUPABASE_URL",
    "SUPABASE_KEY",
]

missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing:
    raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

# Get API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)