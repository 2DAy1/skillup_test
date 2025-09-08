from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class EventType(str, Enum):
    VIEWED = "tutorial_viewed"
    SAVED = "tutorial_saved"
    COMPLETED = "tutorial_completed"
    STARTED = "tutorial_started"
    LIKED = "tutorial_liked"

class UserEvent(BaseModel):
    user_id: str
    tutorial_id: str
    event_type: EventType
    timestamp: datetime
    tags: List[str] = []
    tools: List[str] = []

class Tutorial(BaseModel):
    id: str
    title: str
    tags: List[str]
    tools: List[str]
    difficulty_level: Optional[str] = None
    category: Optional[str] = None

class UserInterest(BaseModel):
    tag_or_tool: str
    score: float
    interaction_count: int
    last_interaction: datetime

class UserProfile(BaseModel):
    user_id: str
    email: str
    name: str
    total_events: int
    interests: List[UserInterest]
    top_tags: List[str]
    top_tools: List[str]

class InterestResponse(BaseModel):
    user_id: str
    top_tags: List[Dict[str, float]]
    top_tools: List[Dict[str, float]]
    total_interactions: int
    analysis_timestamp: datetime
