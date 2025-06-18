from os  import getenv
from dotenv import load_dotenv

# Load environment variables from .env file
try:
    load_dotenv()
except Exception as e:
    print(f"Error loading .env file: {e}")
# Configuration class to hold application settings

GOOGLE_CSE_ID = str(getenv("GOOGLE_CSE_ID"))
GOOGLE_API_KEY = str(getenv("GOOGLE_API_KEY"))
OPENWEATHER_API_KEY = str(getenv("OPENWEATHER_API_KEY"))

if not GOOGLE_CSE_ID or not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_CSE_ID and GOOGLE_API_KEY must be set in the environment variables.")
if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY must be set in the environment variables.")