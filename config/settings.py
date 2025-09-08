import os
from typing import Dict, Any

class Settings:
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TITLE: str = "User Behavior Analysis API"
    API_VERSION: str = "1.0.0"
    
    CSV_FILE_PATH: str = "data/users.csv"
    
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
    
    @classmethod
    def get_database_url(cls) -> str:
        return os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    @classmethod
    def get_mixpanel_token(cls) -> str:
        return os.getenv("MIXPANEL_TOKEN", "")

settings = Settings()
