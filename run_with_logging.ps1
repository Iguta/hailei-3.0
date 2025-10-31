# PowerShell script to run app.py with uv and capture all logs
# Usage: .\run_with_logging.ps1

# Set UTF-8 encoding to handle emojis properly
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

$logFile = "crewai_logs_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').log"

Write-Host "Starting app with uv and logging..." -ForegroundColor Green
Write-Host "Log file: $logFile" -ForegroundColor Yellow
Write-Host "Encoding set to UTF-8 to handle emojis" -ForegroundColor Cyan

# Run app with uv and capture both stdout and stderr
uv run app.py *> $logFile 2>&1

Write-Host "`nLogging complete. Check: $logFile" -ForegroundColor Green
