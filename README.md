# User Behavior Analysis API

A sophisticated system for analyzing user behavior based on Mixpanel data. The system identifies the most relevant content categories (tags and tools) for specific users based on their interaction patterns with microlearning tutorials.

## 🚀 Features

- **Personalized Analysis**: Determines user interests based on behavior patterns
- **Weighted Scoring**: Different action types have different weights (view, save, complete)
- **Time Decay**: Recent interactions have greater influence on analysis
- **FastAPI**: Modern web framework with automatic documentation
- **Detailed Analytics**: Complete statistics on users and their activity

## 📁 Project Structure

```
SkillsUpTest/
├── src/                    # Source code
│   ├── __init__.py
│   ├── main.py            # FastAPI application
│   ├── models.py          # Pydantic data models
│   └── analysis_engine.py # Core analysis logic
├── config/                # Configuration
│   ├── __init__.py
│   └── settings.py        # Application settings
├── data/                  # Data files
│   └── users.csv         # User data
├── tests/                 # Test files
│   └── test_api.py       # API tests
├── docs/                  # Documentation
├── requirements.txt       # Dependencies
├── .gitignore            # Git ignore rules
├── demo.py               # Demo script
└── README.md             # This file
```

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd SkillsUpTest
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Demo
```bash
python demo.py
```

### 5. Start API Server
```bash
python -m src.main
```

Server will be available at: `http://localhost:8000`

## 📊 Analysis Algorithm

### Event Weights
- **Tutorial Viewed**: 1.0
- **Tutorial Started**: 1.5
- **Tutorial Saved**: 2.5
- **Tutorial Completed**: 3.0
- **Tutorial Liked**: 2.0

### Time Decay
Recent interactions have greater influence using exponential decay:
```
decay_factor = exp(-0.1 * days_ago)
final_score = event_weight * decay_factor
```

### Ranking
- Minimum 2 interactions required for inclusion
- Maximum 10 items in top lists
- Sorted by relevance score

## 🔌 API Endpoints

### Core Endpoints

#### `GET /`
Root endpoint with API information

#### `GET /health`
Health check endpoint

#### `GET /users`
Get list of all users

#### `GET /interests/{user_id}`
**Main endpoint** - Get user interests

**Parameters:**
- `user_id` (string) - Unique user identifier

**Response:**
```json
{
  "user_id": "e15b0045-0001-4555-af6a-78a5530feca4",
  "top_tags": [
    {"python": 15.2},
    {"javascript": 12.8},
    {"react": 10.5}
  ],
  "top_tools": [
    {"vscode": 8.3},
    {"git": 6.7},
    {"docker": 5.2}
  ],
  "total_interactions": 66,
  "analysis_timestamp": "2024-01-01T12:00:00"
}
```

#### `GET /interests/{user_id}/detailed`
Detailed information about all user interests

#### `GET /analytics/summary`
Overall statistics for all users

## 🧪 Testing

### Run API Tests
```bash
python tests/test_api.py
```

### Manual Testing
```bash
# Get user interests
curl http://localhost:8000/interests/e15b0045-0001-4555-af6a-78a5530feca4

# Get all users
curl http://localhost:8000/users

# Get analytics
curl http://localhost:8000/analytics/summary
```

## 📚 API Documentation

After starting the server, automatic documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## ⚙️ Configuration

Edit `config/settings.py` to customize:

```python
class Settings:
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CSV_FILE_PATH: str = "data/users.csv"
    
    EVENT_WEIGHTS: Dict[str, float] = {
        "tutorial_viewed": 1.0,
        "tutorial_saved": 2.5,
        "tutorial_completed": 3.0
    }
    
    TIME_DECAY_FACTOR: float = 0.1
    MIN_INTERACTIONS: int = 2
    MAX_TOP_ITEMS: int = 10
```

## 🔧 Development

### Project Structure
- `src/` - Main application code
- `config/` - Configuration files
- `tests/` - Test files
- `data/` - Data files

### Adding New Features
1. Add models to `src/models.py`
2. Extend analysis logic in `src/analysis_engine.py`
3. Add endpoints to `src/main.py`
4. Update tests in `tests/`

## 🚀 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "-m", "src.main"]
```

### Environment Variables
```bash
export CSV_FILE_PATH="/path/to/your/data.csv"
export API_HOST="0.0.0.0"
export API_PORT="8000"
```

## 📈 Extending the System

### Real Mixpanel Integration
Replace `generate_mock_events()` with actual Mixpanel API calls:

```python
def load_events_from_mixpanel(self, user_id: str) -> List[UserEvent]:
    # Real Mixpanel API integration
    pass
```

### Database Integration
Add database support for caching results:

```python
# Using SQLAlchemy or other ORM
```

### Machine Learning
Enhance recommendations with ML algorithms:

```python
# Using scikit-learn for clustering
```

## 📄 License

MIT License

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For questions and support, create an issue in the repository or contact the development team.