import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import math
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import UserEvent, EventType, UserInterest, UserProfile, InterestResponse
from config.settings import settings

class UserBehaviorAnalysisEngine:
    def __init__(self):
        self.event_weights = settings.EVENT_WEIGHTS
        self.time_decay_factor = settings.TIME_DECAY_FACTOR
        self.min_interactions = settings.MIN_INTERACTIONS
        self.max_top_items = settings.MAX_TOP_ITEMS

    def load_user_data(self, csv_file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(csv_file_path)
            return df
        except Exception as e:
            raise Exception(f"Error loading data: {e}")

    def generate_mock_events(self, user_id: str, total_events: int) -> List[UserEvent]:
        events = []
        
        available_tags = [
            "python", "javascript", "react", "vue", "nodejs", "sql", "mongodb",
            "docker", "kubernetes", "aws", "git", "api", "frontend", "backend",
            "mobile", "ios", "android", "design", "ui", "ux", "analytics",
            "machine-learning", "data-science", "blockchain", "security"
        ]
        
        available_tools = [
            "vscode", "pycharm", "figma", "photoshop", "illustrator", "sketch",
            "postman", "insomnia", "docker", "kubernetes", "aws-cli", "git",
            "npm", "yarn", "pip", "conda", "jupyter", "notebook", "slack",
            "trello", "asana", "notion", "confluence", "github", "gitlab"
        ]
        
        event_types = [EventType.VIEWED, EventType.SAVED, EventType.COMPLETED, EventType.STARTED]
        
        for i in range(total_events):
            event_type = event_types[i % len(event_types)]
            
            num_tags = min(3, len(available_tags))
            num_tools = min(2, len(available_tools))
            
            selected_tags = available_tags[i % len(available_tags):i % len(available_tags) + num_tags]
            selected_tools = available_tools[i % len(available_tools):i % len(available_tools) + num_tools]
            
            days_ago = int((total_events - i) % 30)
            timestamp = datetime.now() - timedelta(days=days_ago)
            
            event = UserEvent(
                user_id=user_id,
                tutorial_id=f"tutorial_{i % 50}",
                event_type=event_type,
                timestamp=timestamp,
                tags=selected_tags,
                tools=selected_tools
            )
            events.append(event)
        
        return events

    def calculate_time_decay(self, event_time: datetime) -> float:
        days_ago = int((datetime.now() - event_time).days)
        return math.exp(-self.time_decay_factor * days_ago)

    def analyze_user_interests(self, user_id: str, events: List[UserEvent]) -> UserProfile:
        tag_scores = defaultdict(float)
        tool_scores = defaultdict(float)
        tag_interactions = defaultdict(int)
        tool_interactions = defaultdict(int)
        last_interactions = {}
        
        for event in events:
            event_weight = self.event_weights.get(event.event_type, 1.0)
            time_decay = self.calculate_time_decay(event.timestamp)
            final_weight = event_weight * time_decay
            
            for tag in event.tags:
                tag_scores[tag] += final_weight
                tag_interactions[tag] += 1
                last_interactions[f"tag_{tag}"] = event.timestamp
            
            for tool in event.tools:
                tool_scores[tool] += final_weight
                tool_interactions[tool] += 1
                last_interactions[f"tool_{tool}"] = event.timestamp
        
        interests = []
        
        for tag, score in tag_scores.items():
            if tag_interactions[tag] >= self.min_interactions:
                interests.append(UserInterest(
                    tag_or_tool=tag,
                    score=score,
                    interaction_count=tag_interactions[tag],
                    last_interaction=last_interactions.get(f"tag_{tag}", datetime.now())
                ))
        
        for tool, score in tool_scores.items():
            if tool_interactions[tool] >= self.min_interactions:
                interests.append(UserInterest(
                    tag_or_tool=tool,
                    score=score,
                    interaction_count=tool_interactions[tool],
                    last_interaction=last_interactions.get(f"tool_{tool}", datetime.now())
                ))
        
        interests.sort(key=lambda x: x.score, reverse=True)
        
        top_tags = [interest.tag_or_tool for interest in interests 
                   if interest.tag_or_tool in [tag for tag, _ in tag_scores.items()]][:self.max_top_items]
        
        top_tools = [interest.tag_or_tool for interest in interests 
                    if interest.tag_or_tool in [tool for tool, _ in tool_scores.items()]][:self.max_top_items]
        
        return UserProfile(
            user_id=user_id,
            email="",
            name="",
            total_events=len(events),
            interests=interests,
            top_tags=top_tags,
            top_tools=top_tools
        )

    def get_user_interests(self, user_id: str, csv_file_path: str) -> InterestResponse:
        df = self.load_user_data(csv_file_path)
        
        user_data = df[df['Distinct ID'] == user_id]
        if user_data.empty:
            raise ValueError(f"User with ID {user_id} not found")
        
        user_row = user_data.iloc[0]
        total_events = int(user_row['Total Events of Tutorial viewed or Tutorial is saved or 4 others'])
        
        events = self.generate_mock_events(user_id, total_events)
        user_profile = self.analyze_user_interests(user_id, events)
        
        top_tags = [
            {interest.tag_or_tool: interest.score} 
            for interest in user_profile.interests 
            if interest.tag_or_tool in user_profile.top_tags
        ][:self.max_top_items]
        
        top_tools = [
            {interest.tag_or_tool: interest.score} 
            for interest in user_profile.interests 
            if interest.tag_or_tool in user_profile.top_tools
        ][:self.max_top_items]
        
        return InterestResponse(
            user_id=user_id,
            top_tags=top_tags,
            top_tools=top_tools,
            total_interactions=user_profile.total_events,
            analysis_timestamp=datetime.now()
        )

    def get_all_users_summary(self, csv_file_path: str) -> List[Dict]:
        df = self.load_user_data(csv_file_path)
        
        summary = []
        for _, row in df.iterrows():
            summary.append({
                "user_id": row['Distinct ID'],
                "email": row['Email'],
                "name": row['Name'],
                "total_events": int(row['Total Events of Tutorial viewed or Tutorial is saved or 4 others'])
            })
        
        return summary
