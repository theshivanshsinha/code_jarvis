@echo off
title CodeJarvis Application Launcher
echo.
echo ======================================
echo 🚀 CodeJarvis Application Launcher
echo ======================================
echo.

REM Change to project directory
cd /d "C:\Users\shiva\OneDrive\Documents\projects\CodeJarvis"

REM Check if PowerShell script exists
if exist "start_codejarvis.ps1" (
    echo Starting with PowerShell script...
    powershell -ExecutionPolicy Bypass -File "start_codejarvis.ps1"
) else (
    echo PowerShell script not found. Starting manually...
    echo.
    echo Starting Backend Server...
    start "CodeJarvis Backend" cmd /k "call .venv\Scripts\activate && python run.py"
    
    timeout /t 5 /nobreak > nul
    
    echo Starting Frontend Server...
    start "CodeJarvis Frontend" cmd /k "cd frontend\codej && npm start"
    
    echo.
    echo ======================================
    echo 🎉 CodeJarvis is starting!
    echo ======================================
    echo Backend: http://localhost:5000
    echo Frontend: http://localhost:3000
    echo.
    echo Press any key to open the application...
    pause > nul
    start http://localhost:3000
)

pause
