# Setup Guide for Windows PowerShell

## Quick Setup (PowerShell)

### Option 1: Use the activation script (Recommended)

```powershell
# First, create the virtual environment
python -m venv venv

# Then activate it using the .ps1 script
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Option 2: Use the batch file

```powershell
# Create virtual environment
python -m venv venv

# Activate using batch file (works without execution policy changes)
.\venv\Scripts\activate.bat
```

### Option 3: Use the automated setup script

```powershell
# Run the setup script
.\activate.ps1
```

## Complete Setup Steps

1. **Create Virtual Environment**
   ```powershell
   python -m venv venv
   ```

2. **Activate Virtual Environment**
   ```powershell
   # PowerShell (may need execution policy)
   .\venv\Scripts\Activate.ps1
   
   # OR use batch file (no execution policy needed)
   .\venv\Scripts\activate.bat
   ```

3. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Create .env file**
   ```powershell
   Copy-Item .env.example .env
   # Then edit .env with your Supabase keys
   ```

5. **Run the server**
   ```powershell
   python run.py
   ```

## Troubleshooting

### "Execution Policy" Error

If you see: `cannot be loaded because running scripts is disabled on this system`

Run this command:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```powershell
.\venv\Scripts\Activate.ps1
```

### "venv module not found"

Make sure Python is installed and in your PATH:
```powershell
python --version
```

If that doesn't work, try:
```powershell
py --version
py -m venv venv
```

### Alternative: Use Command Prompt

If PowerShell continues to give issues, use Command Prompt (cmd) instead:

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

