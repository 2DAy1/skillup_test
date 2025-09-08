from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import uvicorn
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis_engine import UserBehaviorAnalysisEngine
from src.models import InterestResponse
from config.settings import settings

app = FastAPI(
    title=settings.API_TITLE,
    description="API for analyzing user behavior based on Mixpanel data",
    version=settings.API_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analysis_engine = UserBehaviorAnalysisEngine()

@app.get("/")
async def root():
    return {
        "message": settings.API_TITLE,
        "version": settings.API_VERSION,
        "endpoints": {
            "interests": "/interests/{user_id}",
            "users": "/users",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "user-behavior-analysis"}

@app.get("/users")
async def get_all_users():
    try:
        users_summary = analysis_engine.get_all_users_summary(settings.CSV_FILE_PATH)
        return {
            "users": users_summary,
            "total_users": len(users_summary)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting users list: {str(e)}")

@app.get("/interests/{user_id}", response_model=InterestResponse)
async def get_user_interests(
    user_id: str = Path(..., description="Unique user identifier")
):
    try:
        if not os.path.exists(settings.CSV_FILE_PATH):
            raise HTTPException(
                status_code=404, 
                detail=f"Data file {settings.CSV_FILE_PATH} not found"
            )
        
        interests = analysis_engine.get_user_interests(user_id, settings.CSV_FILE_PATH)
        return interests
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User analysis error: {str(e)}")

@app.get("/interests/{user_id}/detailed")
async def get_detailed_user_interests(
    user_id: str = Path(..., description="Unique user identifier")
):
    try:
        if not os.path.exists(settings.CSV_FILE_PATH):
            raise HTTPException(
                status_code=404, 
                detail=f"Data file {settings.CSV_FILE_PATH} not found"
            )
        
        df = analysis_engine.load_user_data(settings.CSV_FILE_PATH)
        
        user_data = df[df['Distinct ID'] == user_id]
        if user_data.empty:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        
        user_row = user_data.iloc[0]
        total_events = int(user_row['Total Events of Tutorial viewed or Tutorial is saved or 4 others'])
        
        events = analysis_engine.generate_mock_events(user_id, total_events)
        user_profile = analysis_engine.analyze_user_interests(user_id, events)
        
        return {
            "user_id": user_id,
            "email": user_row['Email'],
            "name": user_row['Name'],
            "total_events": total_events,
            "all_interests": [
                {
                    "item": interest.tag_or_tool,
                    "score": interest.score,
                    "interactions": interest.interaction_count,
                    "last_interaction": interest.last_interaction
                }
                for interest in user_profile.interests
            ],
            "top_tags": user_profile.top_tags,
            "top_tools": user_profile.top_tools,
            "analysis_timestamp": user_profile.interests[0].last_interaction if user_profile.interests else None
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User analysis error: {str(e)}")

@app.get("/analytics/summary")
async def get_analytics_summary():
    try:
        if not os.path.exists(settings.CSV_FILE_PATH):
            raise HTTPException(
                status_code=404, 
                detail=f"Data file {settings.CSV_FILE_PATH} not found"
            )
        
        users_summary = analysis_engine.get_all_users_summary(settings.CSV_FILE_PATH)
        
        total_users = len(users_summary)
        total_events = sum(int(user['total_events']) for user in users_summary)
        avg_events = total_events / total_users if total_users > 0 else 0
        
        most_active_users = sorted(users_summary, key=lambda x: x['total_events'], reverse=True)[:5]
        
        return {
            "total_users": total_users,
            "total_events": total_events,
            "average_events_per_user": round(avg_events, 2),
            "most_active_users": most_active_users,
            "analysis_timestamp": "2024-01-01T00:00:00"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting analytics: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level="info"
    )
