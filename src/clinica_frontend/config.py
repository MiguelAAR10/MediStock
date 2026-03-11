import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


class Settings:
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000/api/v1")
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

    PAGE_TITLE = os.getenv("PAGE_TITLE", "Clinica Prime AI")
    PAGE_ICON = os.getenv("PAGE_ICON", ":hospital:")
    LAYOUT = os.getenv("LAYOUT", "wide")
