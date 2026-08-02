# Ganache Startup Script for Windows PowerShell
# Starts Ganache with deterministic accounts for development

Write-Host "🚀 Starting Ganache Local Blockchain..." -ForegroundColor Green
Write-Host "=" -NoNewline; Write-Host ("=" * 59)
Write-Host ""

Write-Host "📋 Configuration:" -ForegroundColor Cyan
Write-Host "   Port: 8545"
Write-Host "   Network ID: 1337"
Write-Host "   Accounts: 10"
Write-Host "   Balance per account: 1000 ETH"
Write-Host "   Mode: Deterministic (same accounts every time)"
Write-Host ""

Write-Host "⚠️  IMPORTANT:" -ForegroundColor Yellow
Write-Host "   Keep this terminal window open while developing!"
Write-Host "   Press Ctrl+C to stop Ganache"
Write-Host ""

Write-Host "🔌 Starting Ganache..." -ForegroundColor Green
Write-Host ""

# Start Ganache with configuration
ganache --port 8545 --networkId 1337 --accounts 10 --defaultBalanceEther 1000 --deterministic

# If Ganache exits
Write-Host ""
Write-Host "⚠️  Ganache has stopped" -ForegroundColor Yellow
