# 🐛 CodeJarvis Troubleshooting Guide

## "Failed to fetch" Error Fix

The "Failed to fetch" error typically occurs when the frontend cannot connect to the backend API. Here's how to fix it:

### 1. ✅ Check if Backend is Running

First, make sure your backend server is running:

```bash
python run.py
```

You should see output like:
```
Starting CodeJarvis development server...
 * Environment: Development
 * Running on http://127.0.0.1:5000/
 * Debug mode: on
```

### 2. 🔍 Test Backend Connection

Run the debug script to check connectivity:

```bash
python debug_connection.py
```

### 3. 🌐 Start Frontend

In a separate terminal, start the frontend:

```bash
cd frontend/codej
npm start
```

### 4. 🚀 Use the Automated Startup Script

For convenience, use the automated startup script:

```bash
python start_servers.py
```

## Common Issues and Solutions

### Issue 1: "Connection refused" or "ECONNREFUSED"

**Problem**: Backend server is not running or running on wrong port.

**Solutions**:
1. Start backend: `python run.py`
2. Check if port 5000 is available: `netstat -ano | findstr :5000`
3. If port is occupied, change the port in `run.py`

### Issue 2: CORS Errors

**Problem**: Browser blocks requests due to CORS policy.

**Solutions**:
1. Backend CORS is already configured in `backend/__init__.py`
2. Clear browser cache and cookies
3. Try in incognito/private mode
4. Check browser console for specific CORS errors

### Issue 3: "Module not found" or Import Errors

**Problem**: Missing dependencies or incorrect Python path.

**Solutions**:
1. Install backend dependencies: `pip install -r backend/requirements.txt`
2. Install frontend dependencies: `cd frontend/codej && npm install`
3. Make sure you're in the project root directory

### Issue 4: Database Connection Issues

**Problem**: MongoDB connection errors.

**Solutions**:
1. MongoDB is optional for basic functionality
2. The app uses demo data when no database is available
3. To use MongoDB, ensure it's running on default port 27017

### Issue 5: API Returns Empty Data

**Problem**: No platform accounts connected.

**Solutions**:
1. Use demo endpoints: `http://localhost:5000/api/stats/demo`
2. Test with real users: `http://localhost:5000/api/stats/test/codeforces/tourist`
3. Connect your accounts in the frontend settings

## Testing Endpoints Manually

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Demo Stats (with real data)
```bash
curl http://localhost:5000/api/stats/demo
```

### Daily Activity
```bash
curl http://localhost:5000/api/stats/daily
```

### Problem History
```bash
curl "http://localhost:5000/api/stats/problems?limit=10"
```

### Advanced Analytics
```bash
curl http://localhost:5000/api/stats/analytics
```

## Debug Mode

### Enable Backend Debug Logging

The backend already has request logging enabled. You'll see requests in the console like:
```
Request: GET http://localhost:5000/api/stats
```

### Frontend Debug

Open browser Developer Tools (F12) and check:
1. **Console tab**: For JavaScript errors
2. **Network tab**: For failed API requests
3. **Application tab**: For storage issues

## Port Configuration

### Default Ports
- Backend: `http://localhost:5000`
- Frontend: `http://localhost:3000`

### Changing Ports

**Backend** (in `run.py` or `backend/app.py`):
```python
app.run(host="0.0.0.0", port=8000, debug=True)  # Change to port 8000
```

**Frontend** (create `.env` in `frontend/codej/`):
```
PORT=3001
```

## Environment Variables

Create a `.env` file in the project root for configuration:

```bash
FLASK_SECRET=your-secret-key
MONGODB_URI=mongodb://localhost:27017/contesthub
CLIENT_ORIGIN=http://localhost:3000
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
SENDGRID_API_KEY=your-sendgrid-api-key
```

## Advanced Debugging

### Check Network Traffic

1. Open Developer Tools → Network tab
2. Refresh the page
3. Look for failed requests (red status codes)
4. Click on failed requests to see details

### Check API Response Format

The API should return JSON with proper headers:
```
Content-Type: application/json
Access-Control-Allow-Origin: *
```

### Verify Frontend Configuration

Check if frontend is making requests to the correct URL in your React components.

## Getting Help

If you're still having issues:

1. Run `python debug_connection.py` and share the output
2. Check browser console errors
3. Verify both servers are running on correct ports
4. Try the demo endpoints to ensure backend is working

## Quick Fix Checklist

- [ ] Backend server running (`python run.py`)
- [ ] Frontend server running (`cd frontend/codej && npm start`)
- [ ] Both servers on correct ports (5000 and 3000)
- [ ] No firewall blocking connections
- [ ] Browser allows localhost connections
- [ ] All dependencies installed
- [ ] No other applications using the same ports

## Success Indicators

When everything is working correctly:

1. Backend shows: `* Running on http://127.0.0.1:5000/`
2. Frontend opens browser to: `http://localhost:3000`
3. API health check returns: `{"status": "ok"}`
4. Demo stats show real data (3000+ problems for tourist)
5. No CORS errors in browser console
