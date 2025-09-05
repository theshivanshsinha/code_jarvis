# CodeJarvis Backend

A Flask-based backend for the CodeJarvis competitive programming platform.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Environment Variables** (Optional)
   Create a `.env` file in the project root:
   ```
   FLASK_SECRET=your-secret-key
   MONGODB_URI=mongodb://localhost:27017/contesthub
   CLIENT_ORIGIN=http://localhost:3000
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   SENDGRID_API_KEY=your-sendgrid-api-key
   ```

## Running the Application

### Method 1: Using the main run script (Recommended)
```bash
python run.py
```

### Method 2: Running the backend app directly
```bash
python backend/app.py
```

### Method 3: Using Flask's built-in command
```bash
set FLASK_APP=backend.app
flask run
```

All methods will start the application on http://127.0.0.1:5000/

### Available Endpoints

#### Core Endpoints
- `GET /` - Welcome page
- `GET /api/health` - Health check
- `GET /api/auth/*` - Authentication endpoints
- `GET /api/contests` - Contest listings
- `POST /api/accounts` - Account management
- `POST /api/reminders` - Reminder creation

#### Statistics Endpoints
- `GET /api/stats` - User statistics overview
- `GET /api/stats/<platform>` - Platform-specific detailed stats
- `GET /api/stats/demo` - Demo with real data from famous users
- `GET /api/stats/test/<platform>/<username>` - Test platform APIs

#### Problem Analytics (NEW!)
- `GET /api/stats/daily` - Enhanced daily activity with real data
- `GET /api/stats/problems` - Comprehensive problem history with filtering
- `GET /api/stats/analytics` - Advanced problem solving analytics

### Testing the Setup

You can test if everything is working by visiting:
- http://127.0.0.1:5000/ - Should show "CodeJarvis Backend is running!"
- http://127.0.0.1:5000/api/health - Should return `{"status": "ok"}`

## API Details

### Stats Endpoints

#### GET /api/stats
Returns comprehensive overview and per-platform statistics:
```json
{
  "overview": {
    "totalContests": 45,
    "maxRating": {"platform": "codeforces", "value": 1654},
    "problemsSolved": {"total": 287, "easy": 120, "medium": 145, "hard": 22},
    "platformProblems": {...},
    "activeStreak": 5
  },
  "perPlatform": {
    "leetcode": {"totalSolved": 150, "rating": 0, "connected": true, ...},
    "codeforces": {"totalSolved": 87, "rating": 1654, "connected": true, ...}
  }
}
```

#### GET /api/stats/{platform}
Returns detailed stats for a specific platform (used for hover/detailed views):
```json
{
  "platform": "leetcode",
  "username": "user123",
  "connected": true,
  "totalSolved": 150,
  "easy": 80, "medium": 60, "hard": 10,
  "rating": 1543,
  "strengths": ["Problem Solver", "Foundation Strong"],
  "badges": [{"name": "Century", "description": "Solved 100+ problems"}],
  "recentActivity": "Last active: 2 days ago"
}
```

## 🧩 Problem Analytics (NEW!)

### Enhanced Daily Activity
```bash
GET /api/stats/daily?platform=codeforces&days=30
```
Returns comprehensive daily activity with real submission data:
```json
{
  "days": [{"date": "2024-01-15", "count": 5, "weekday": "Monday"}],
  "totalActivity": 150,
  "activeDays": 45,
  "platform": "codeforces",
  "dateRange": {"start": "2023-12-16", "end": "2024-01-15"}
}
```

### Problem History with Filtering
```bash
GET /api/stats/problems?difficulty=hard&platform=codeforces&verdict=AC&limit=50
```
Returns detailed problem history with advanced filtering:
```json
{
  "problems": [
    {
      "platform": "codeforces",
      "problemId": "1800A",
      "title": "Is It a Cat?",
      "difficulty": "easy",
      "rating": 800,
      "verdict": "OK",
      "language": "C++17",
      "url": "https://codeforces.com/problemset/problem/1800/A",
      "tags": ["implementation", "strings"],
      "date": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 156,
  "showing": 50,
  "statistics": {
    "successRate": 87.5,
    "platformDistribution": {"codeforces": 100, "leetcode": 56},
    "difficultyDistribution": {"easy": 45, "medium": 78, "hard": 33}
  }
}
```

### Advanced Analytics
```bash
GET /api/stats/analytics?days=90&platform=all
```
Returns comprehensive problem solving analytics:
```json
{
  "analytics": {
    "timeAnalysis": {
      "dailyAverage": 2.3,
      "mostActiveDay": ["2024-01-15", 8],
      "totalActiveDays": 67
    },
    "performance": {
      "byDifficulty": {
        "easy": {"attempts": 120, "success": 110, "successRate": 91.7},
        "medium": {"attempts": 80, "success": 65, "successRate": 81.3},
        "hard": {"attempts": 30, "success": 18, "successRate": 60.0}
      }
    },
    "streaks": {
      "current": 5,
      "maximum": 12,
      "activeDays": 67
    },
    "patterns": {
      "hourDistribution": {"14": 15, "15": 23, "16": 18},
      "difficultyProgression": [...],
      "successTrend": [...]
    }
  }
}
```

### Filtering Options
- **platform**: `all`, `codeforces`, `leetcode`, `atcoder`
- **difficulty**: `all`, `easy`, `medium`, `hard`
- **verdict**: `all`, `AC`, `WA`, `TLE`, etc.
- **days**: Number of days to look back (default: 90)
- **limit**: Maximum results (default: 100)
- **sort**: `date`, `difficulty`, `platform`
- **order**: `desc`, `asc`
- **tags**: Comma-separated list of problem tags

## Notes

- WSGI has been removed for simplified development setup
- MongoDB is optional for basic functionality (some features use mock data)
- The application uses relative imports and should be run from the project root
