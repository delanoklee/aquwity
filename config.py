import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""

    # API Configuration
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    # Screenshot Configuration
    SCREENSHOT_INTERVAL = int(os.getenv('SCREENSHOT_INTERVAL', 5))  # minutes

    # Database Configuration
    DB_PATH = os.getenv('DB_PATH', './data/acuity.db')

    # Screenshot storage
    SCREENSHOT_DIR = './data/screenshots'

    # Inactivity threshold (how similar screenshots need to be to count as inactive)
    INACTIVITY_THRESHOLD = 0.95  # 95% similarity = inactive

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not found. Please copy .env.example to .env and add your API key.")
        return True
