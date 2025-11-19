# Quick activation script for PowerShell
# Run this from D:\backend directory

Write-Host "Activating virtual environment..." -ForegroundColor Green

if (Test-Path ".\venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1
    Write-Host "Virtual environment activated!" -ForegroundColor Green
    Write-Host "You can now run: python run.py" -ForegroundColor Yellow
} else {
    Write-Host "Virtual environment not found. Creating it..." -ForegroundColor Yellow
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
    Write-Host "Virtual environment created and activated!" -ForegroundColor Green
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}
