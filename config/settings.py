import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class Settings:
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TITLE: str = "User Behavior Analysis API"
    API_VERSION: str = "1.0.0"
    
    CSV_FILE_PATH: str = os.getenv("CSV_FILE_PATH", "data/users.csv")
    
    EVENT_WEIGHTS: Dict[str, float] = {
        "tutorial_viewed": 1.0,
        "tutorial_started": 1.5,
        "tutorial_saved": 2.5,
        "tutorial_completed": 3.0,
        "tutorial_liked": 2.0
    }
    
    TIME_DECAY_FACTOR: float = 0.1
    MIN_INTERACTIONS: int = 2
    MAX_TOP_ITEMS: int = 10
    
    CORS_ORIGINS: list = ["*"]
    
    # Mixpanel integration
    USE_MIXPANEL: bool = os.getenv("USE_MIXPANEL", "false").lower() in {"1", "true", "yes"}
    MIXPANEL_API_SECRET: str = os.getenv("MIXPANEL_API_SECRET", "")
    MIXPANEL_PROJECT_ID: str = os.getenv("MIXPANEL_PROJECT_ID", "")
    MIXPANEL_DEFAULT_EVENTS: list = [
        "Tutorial Viewed",
        "Tutorial Saved",
        "Tutorial Completed",
        "Tutorial Started",
        "Tutorial Liked",
    ]
    MIXPANEL_DEFAULT_WINDOW_DAYS: int = int(os.getenv("MIXPANEL_WINDOW_DAYS", "30"))

    @classmethod
    def get_database_url(cls) -> str:
        return os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    @classmethod
    def get_mixpanel_token(cls) -> str:
        return os.getenv("MIXPANEL_TOKEN", "")

settings = Settings()
