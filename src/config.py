import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    
    # Try parsing the port, default to 587
    try:
        SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    except ValueError:
        SMTP_PORT = 587
        
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SENDER_NAME = os.getenv("SENDER_NAME", "Your Name")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # Treat DRY_RUN as True unless explicitly set to "false" (case-insensitive)
    DRY_RUN = os.getenv("DRY_RUN", "true").lower() != "false"

    @classmethod
    def validate(cls):
        """Validates configuration. If DRY_RUN is False, credentials must be provided."""
        if not cls.DRY_RUN:
            missing = []
            if not cls.SMTP_USER:
                missing.append("SMTP_USER")
            if not cls.SMTP_PASSWORD:
                missing.append("SMTP_PASSWORD")
            if missing:
                raise ValueError(
                    f"Configuration error: Missing required environment variables: {', '.join(missing)}. "
                    "Please set them in your .env file or keep DRY_RUN=true."
                )
