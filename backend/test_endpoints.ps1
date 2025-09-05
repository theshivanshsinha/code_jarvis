# Test script for CodeJarvis stats endpoints
# Make sure the backend is running on port 5000

Write-Host "Testing CodeJarvis Stats API Endpoints" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Test basic stats endpoint
Write-Host "`nTesting /api/stats (main stats)..." -ForegroundColor Yellow
try {
    $stats = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/stats" -Method GET
    Write-Host "✓ Main stats endpoint working" -ForegroundColor Green
    Write-Host "  - Platforms: $($stats.perPlatform.Keys -join ', ')" -ForegroundColor Cyan
    Write-Host "  - Total Problems: $($stats.overview.problemsSolved.total)" -ForegroundColor Cyan
} catch {
    Write-Host "✗ Main stats endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test daily activity endpoint
Write-Host "`nTesting /api/stats/daily..." -ForegroundColor Yellow
try {
    $daily = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/stats/daily?platform=codeforces&days=7" -Method GET
    Write-Host "✓ Daily activity endpoint working" -ForegroundColor Green
    Write-Host "  - Platform: $($daily.platform)" -ForegroundColor Cyan
    Write-Host "  - Total Activity: $($daily.totalActivity)" -ForegroundColor Cyan
    Write-Host "  - Active Days: $($daily.activeDays)" -ForegroundColor Cyan
} catch {
    Write-Host "✗ Daily activity endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test problems endpoint
Write-Host "`nTesting /api/stats/problems..." -ForegroundColor Yellow
try {
    $problems = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/stats/problems?platform=all&days=30&limit=5" -Method GET
    Write-Host "✓ Problems endpoint working" -ForegroundColor Green
    Write-Host "  - Total Problems: $($problems.total)" -ForegroundColor Cyan
    Write-Host "  - Showing: $($problems.showing)" -ForegroundColor Cyan
    Write-Host "  - Success Rate: $($problems.statistics.successRate)%" -ForegroundColor Cyan
} catch {
    Write-Host "✗ Problems endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test demo endpoint
Write-Host "`nTesting /api/stats/demo..." -ForegroundColor Yellow
try {
    $demo = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/stats/demo" -Method GET
    Write-Host "✓ Demo endpoint working" -ForegroundColor Green
    Write-Host "  - Codeforces problems: $($demo.perPlatform.codeforces.totalSolved)" -ForegroundColor Cyan
    Write-Host "  - LeetCode problems: $($demo.perPlatform.leetcode.totalSolved)" -ForegroundColor Cyan
} catch {
    Write-Host "✗ Demo endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nAPI Testing Complete!" -ForegroundColor Green
