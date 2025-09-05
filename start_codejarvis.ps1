# CodeJarvis Startup Script for Windows
# This script starts both the backend and frontend servers

Write-Host "🚀 Starting CodeJarvis Application..." -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Blue

# Function to check if a port is in use
function Test-Port {
    param([int]$Port)
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue 2>$null
    return $connection
}

# Function to kill process on port
function Stop-ProcessOnPort {
    param([int]$Port)
    $processes = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
    if ($processes) {
        foreach ($processId in $processes) {
            try {
                Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
                Write-Host "✅ Stopped process $processId on port $Port" -ForegroundColor Yellow
            } catch {
                Write-Host "⚠️  Could not stop process $processId" -ForegroundColor Red
            }
        }
    }
}

# Check if running in correct directory
$projectRoot = "C:\Users\shiva\OneDrive\Documents\projects\CodeJarvis"
if (-not (Test-Path $projectRoot)) {
    Write-Host "❌ Project directory not found: $projectRoot" -ForegroundColor Red
    Write-Host "Please update the script with the correct path to your CodeJarvis project" -ForegroundColor Yellow
    exit 1
}

Set-Location $projectRoot
Write-Host "📂 Working directory: $projectRoot" -ForegroundColor Cyan

# Check for required dependencies
Write-Host "🔍 Checking dependencies..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js 16+" -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found. Creating from example..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Created .env file from example. Please configure your settings." -ForegroundColor Green
    } else {
        Write-Host "❌ No .env.example found. Please create a .env file manually." -ForegroundColor Red
    }
}

# Install backend dependencies if needed
if (-not (Test-Path ".venv\Scripts\activate.ps1")) {
    Write-Host "🔧 Setting up Python virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    & ".venv\Scripts\activate.ps1"
    pip install -r backend/requirements.txt
} else {
    Write-Host "✅ Python virtual environment found" -ForegroundColor Green
    & ".venv\Scripts\activate.ps1"
}

# Install frontend dependencies if needed
$frontendDir = "frontend\codej"
if (-not (Test-Path "$frontendDir\node_modules")) {
    Write-Host "🔧 Installing frontend dependencies..." -ForegroundColor Yellow
    Set-Location $frontendDir
    npm install
    Set-Location $projectRoot
} else {
    Write-Host "✅ Frontend dependencies found" -ForegroundColor Green
}

# Clean up any existing processes
Write-Host "🧹 Cleaning up existing processes..." -ForegroundColor Yellow
Stop-ProcessOnPort 5000  # Backend
Stop-ProcessOnPort 3000  # Frontend
Stop-ProcessOnPort 3001  # Frontend alternate

Start-Sleep 2

# Start backend server
Write-Host "🐍 Starting Backend Server (Python Flask)..." -ForegroundColor Magenta
$backendJob = Start-Job -ScriptBlock {
    param($projectPath)
    Set-Location $projectPath
    & ".venv\Scripts\activate.ps1"
    python run.py
} -ArgumentList $projectRoot

Start-Sleep 3

# Check if backend started successfully
if (Test-Port 5000) {
    Write-Host "✅ Backend server started on http://localhost:5000" -ForegroundColor Green
} else {
    Write-Host "❌ Backend server failed to start" -ForegroundColor Red
    Write-Host "Check the job output:" -ForegroundColor Yellow
    Receive-Job $backendJob
}

# Start frontend server
Write-Host "⚛️  Starting Frontend Server (React)..." -ForegroundColor Cyan
$frontendJob = Start-Job -ScriptBlock {
    param($projectPath)
    Set-Location "$projectPath\frontend\codej"
    npm start
} -ArgumentList $projectRoot

Start-Sleep 5

# Check if frontend started successfully
$frontendPort = if (Test-Port 3000) { 3000 } elseif (Test-Port 3001) { 3001 } else { $null }

if ($frontendPort) {
    Write-Host "✅ Frontend server started on http://localhost:$frontendPort" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend server failed to start" -ForegroundColor Red
    Write-Host "Check the job output:" -ForegroundColor Yellow
    Receive-Job $frontendJob
}

# Display status and URLs
Write-Host "`n🎉 CodeJarvis Application Status:" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Blue
Write-Host "Backend API: http://localhost:5000" -ForegroundColor White
Write-Host "Frontend UI: http://localhost:$frontendPort" -ForegroundColor White
Write-Host "`n📧 Email Configuration:" -ForegroundColor Yellow
Write-Host "Test email setup: http://localhost:5000/api/email/config" -ForegroundColor White
Write-Host "Setup instructions: http://localhost:5000/api/email/instructions" -ForegroundColor White
Write-Host "`n📚 Available APIs:" -ForegroundColor Yellow
Write-Host "- Health Check: http://localhost:5000/api/health" -ForegroundColor White
Write-Host "- Stats: http://localhost:5000/api/stats" -ForegroundColor White
Write-Host "- Contests: http://localhost:5000/api/contests" -ForegroundColor White
Write-Host "- Email Test: http://localhost:5000/api/email/test" -ForegroundColor White

Write-Host "`n📝 Quick Commands:" -ForegroundColor Cyan
Write-Host "- Test backend: Invoke-WebRequest http://localhost:5000/api/health" -ForegroundColor Gray
Write-Host "- Check email: Invoke-WebRequest http://localhost:5000/api/email/config" -ForegroundColor Gray
Write-Host "- Open frontend: Start-Process http://localhost:$frontendPort" -ForegroundColor Gray

Write-Host "`n🎮 Press Ctrl+C to stop all servers" -ForegroundColor Red
Write-Host "Or close this PowerShell window to stop the application" -ForegroundColor Gray

# Keep the script running and monitor servers
try {
    Write-Host "`n⏳ Servers running... (Press Ctrl+C to stop)" -ForegroundColor Green
    while ($true) {
        Start-Sleep 30
        
        # Check if servers are still running
        $backendStatus = if (Test-Port 5000) { "✅ Running" } else { "❌ Down" }
        $frontendStatus = if ($frontendPort -and (Test-Port $frontendPort)) { "✅ Running" } else { "❌ Down" }
        
        $currentTime = Get-Date -Format "HH:mm:ss"
        Write-Host "[$currentTime] Backend: $backendStatus | Frontend: $frontendStatus" -ForegroundColor Blue
    }
} catch {
    Write-Host "`n🛑 Shutting down servers..." -ForegroundColor Red
}

# Cleanup on exit
finally {
    Write-Host "🧹 Cleaning up background jobs..." -ForegroundColor Yellow
    Stop-Job $backendJob -ErrorAction SilentlyContinue
    Stop-Job $frontendJob -ErrorAction SilentlyContinue
    Remove-Job $backendJob -ErrorAction SilentlyContinue
    Remove-Job $frontendJob -ErrorAction SilentlyContinue
    
    Write-Host "👋 CodeJarvis stopped. Thanks for using the application!" -ForegroundColor Green
}
