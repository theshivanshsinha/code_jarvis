@echo off
title CodeJarvis - Starting Both Servers
color 0A

echo.
echo ==========================================
echo    🚀 Starting CodeJarvis Application
echo ==========================================
echo.

REM Change to project directory
cd /d "C:\Users\shiva\OneDrive\Documents\projects\CodeJarvis"

echo 📂 Project Directory: %CD%
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ⚠️  Virtual environment not found. Creating...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r backend\requirements.txt
) else (
    echo ✅ Virtual environment found
    call .venv\Scripts\activate.bat
)

echo.
echo 🐍 Starting Backend Server (Flask)...
echo Backend will be available at: http://localhost:5000
echo.

REM Start backend in new window
start "CodeJarvis Backend" cmd /k "cd /d "%CD%" && call .venv\Scripts\activate.bat && python run.py"

REM Wait for backend to start
echo ⏳ Waiting for backend to initialize...
timeout /t 8 /nobreak > nul

REM Test if backend is running
powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:5000/api/health' -TimeoutSec 5; Write-Host '✅ Backend is running!' } catch { Write-Host '⚠️  Backend may still be starting...' }"

echo.
echo ⚛️  Starting Frontend Server (React)...
echo Frontend will be available at: http://localhost:3000
echo.

REM Start frontend in new window
start "CodeJarvis Frontend" cmd /k "cd /d "%CD%\frontend\codej" && npm start"

echo ⏳ Waiting for frontend to compile...
timeout /t 10 /nobreak > nul

echo.
echo ==========================================
echo    🎉 CodeJarvis is Starting!
echo ==========================================
echo.
echo 🌐 Application URLs:
echo    Backend API: http://localhost:5000
echo    Frontend UI: http://localhost:3000
echo.
echo 🔧 Useful Endpoints:
echo    Health Check: http://localhost:5000/api/health
echo    Email Config: http://localhost:5000/api/email/config
echo    Stats Demo:   http://localhost:5000/api/stats
echo.
echo 💡 Tips:
echo    - Keep both terminal windows open
echo    - Frontend may take 30-60 seconds to fully load
echo    - Check browser developer tools (F12) for any errors
echo.
echo Press any key to open the frontend in your browser...
pause > nul

echo 🚀 Opening CodeJarvis in your browser...
start http://localhost:3000

echo.
echo ✅ CodeJarvis is now running!
echo.
echo Press any key to exit this launcher...
pause > nul
