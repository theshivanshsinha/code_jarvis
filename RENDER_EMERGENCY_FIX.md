# 🚨 EMERGENCY RENDER DEPLOYMENT FIX

If you're still getting "Continuing to scan for open port 5000", try these steps in order:

## 1. Update Start Command in Render Dashboard

Go to your Render service → Settings → Start Command and try these in order:

### Option A (Recommended):
```
python server.py
```

### Option B:
```
python simple_server.py
```

### Option C:
```
python app.py
```

### Option D:
```
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

## 2. Environment Variables Required

Make sure these are set in Render dashboard:

```
FLASK_SECRET=your-random-secret-key
CLIENT_ORIGIN=https://your-frontend.onrender.com
GOOGLE_REDIRECT_URI=https://your-backend.onrender.com/api/auth/google/callback
```

## 3. If Still Failing - Check Render Logs

Look for these messages in the logs:
- "Starting on port 5000" ✅
- "App imported successfully" ✅
- "Serving Flask app" ✅

If you see import errors, the issue is with Python dependencies.

## 4. Nuclear Option - Simple Health Check

If nothing works, create a file called `test.py`:

```python
#!/usr/bin/env python3
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "CodeJarvis Backend is running!"

@app.route('/api/health')
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
```

Then use start command: `python test.py`

## 5. Contact Support

If none of these work, the issue might be:
- Render platform issue
- Python version compatibility
- Memory/resource limits

## 6. Final Debug Command

Use this start command to see exactly what's happening:
```
python -c "import os; print('PORT:', os.environ.get('PORT')); exec(open('server.py').read())"
```