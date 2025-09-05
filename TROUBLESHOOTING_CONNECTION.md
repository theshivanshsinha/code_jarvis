# 🔧 Connection Issues Troubleshooting

## ❌ "Failed to fetch" Error Fix

This error means the React frontend can't connect to the Flask backend. Here's how to fix it:

### 🚀 **Quick Solution**

1. **Use the new startup script:**
   ```
   Double-click: start_both_servers.bat
   ```
   This starts both servers automatically with proper timing.

2. **Or start manually in this exact order:**
   
   **Terminal 1 (Backend):**
   ```bash
   cd C:\Users\shiva\OneDrive\Documents\projects\CodeJarvis
   call .venv\Scripts\activate.bat
   python run.py
   ```
   Wait until you see: `Running on http://127.0.0.1:5000`

   **Terminal 2 (Frontend):**
   ```bash
   cd C:\Users\shiva\OneDrive\Documents\projects\CodeJarvis\frontend\codej
   npm start
   ```

### 🔍 **Check Backend is Running**

Open: http://localhost:5000/api/health

**Should return:**
```json
{"status": "ok", "message": "CodeJarvis API is running!"}
```

**If it doesn't work:**
- Backend server is not running
- Start backend first, then frontend

### 🌐 **Test Connection**

In browser developer tools (F12) > Console, test:
```javascript
fetch('http://localhost:5000/api/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

### 🔧 **Common Issues & Fixes**

#### 1. **Backend Not Started**
```
Error: Failed to fetch
```
**Fix:** Start backend server first:
```bash
python run.py
```

#### 2. **Port Already in Use**
```
Error: Port 5000 is already in use
```
**Fix:** Kill existing process:
```bash
# Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

#### 3. **CORS Issues**
```
Error: Access-Control-Allow-Origin
```
**Fix:** Backend already configured for CORS, but restart both servers:
- Stop both servers
- Start backend first
- Wait 5 seconds
- Start frontend

#### 4. **Wrong URLs**
The frontend tries to connect to:
- `http://localhost:5000` ✅ Correct
- `http://127.0.0.1:5000` ✅ Also works

Make sure backend shows:
```
* Running on http://127.0.0.1:5000/
* Running on all addresses (0.0.0.0)
```

#### 5. **Virtual Environment Issues**
```
Error: No module named 'flask'
```
**Fix:** Activate virtual environment:
```bash
call .venv\Scripts\activate.bat
pip install -r backend\requirements.txt
```

### 🧪 **Testing Steps**

1. **Backend Health Check:**
   ```
   http://localhost:5000/api/health
   ```

2. **Backend API Test:**
   ```
   http://localhost:5000/api/stats
   ```

3. **Email Config Test:**
   ```
   http://localhost:5000/api/email/config
   ```

4. **Frontend Connection Test:**
   - Open browser dev tools (F12)
   - Check Network tab
   - Refresh frontend page
   - Look for failed requests to localhost:5000

### 📝 **Startup Order (Important!)**

**✅ Correct Order:**
1. Start Backend (python run.py)
2. Wait for "Running on http://127.0.0.1:5000"
3. Start Frontend (npm start)
4. Wait for "webpack compiled successfully"

**❌ Wrong Order:**
1. Starting frontend first
2. Starting both simultaneously
3. Not waiting for backend to fully start

### 🔄 **Reset Everything**

If still having issues:

1. **Kill all processes:**
   ```bash
   taskkill /f /im python.exe
   taskkill /f /im node.exe
   ```

2. **Clear browser cache:**
   - Ctrl+Shift+R (hard refresh)
   - Or clear browser data

3. **Restart in correct order:**
   - Backend first
   - Wait 5 seconds
   - Frontend second

### 📞 **Still Need Help?**

If none of these work:

1. **Check Windows Firewall:** Make sure ports 3000 and 5000 are allowed
2. **Check Antivirus:** Temporarily disable to test
3. **Try different ports:** Modify the configuration if needed
4. **Check logs:** Look at both terminal outputs for error messages

### 🎯 **Success Indicators**

**Backend Working:**
- Terminal shows: `Running on http://127.0.0.1:5000`
- Browser shows: `http://localhost:5000/api/health` returns JSON

**Frontend Working:**
- Terminal shows: `webpack compiled successfully`
- Browser shows: `http://localhost:3000` loads the app
- No "Failed to fetch" errors in dev tools

**Both Connected:**
- Frontend loads data from backend
- No network errors in browser dev tools
- Contest data appears on homepage
