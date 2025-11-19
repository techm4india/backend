# PowerShell Setup Guide

## Activating Virtual Environment in PowerShell

### Method 1: Direct Activation (Recommended)

```powershell
# Create virtual environment (if not already created)
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1
```

### Method 2: If You Get Execution Policy Error

If you see an error like:
```
cannot be loaded because running scripts is disabled on this system
```

Run this command first (as Administrator):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate:
```powershell
.\venv\Scripts\Activate.ps1
```

### Method 3: Alternative Activation (if above doesn't work)

```powershell
& .\venv\Scripts\Activate.ps1
```

## Complete Setup Steps

**IMPORTANT: Make sure you're in the `D:\backend` directory first!**

```powershell
# 0. Navigate to project directory (if not already there)
cd D:\backend

# 1. Create virtual environment (if not already created)
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (copy from .env.example and fill in your keys)
Copy-Item .env.example .env

# 5. Run the server
python run.py
```

## Verify Installation

After activation, you should see `(venv)` in your prompt:
```
(venv) PS D:\backend>
```

## Running the Server

Once activated and dependencies installed:

```powershell
# Development mode (auto-reload)
python run.py

# Or using uvicorn directly
uvicorn src.main:app --reload --port 4000
```

## Deactivating Virtual Environment

When you're done:
```powershell
deactivate
```

