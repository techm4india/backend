# Running FastAPI with Uvicorn

## ✅ Uvicorn is Already Installed!

Your project is set up to use **Uvicorn** with FastAPI.

## Method 1: Using run.py (Easiest)

```powershell
python run.py
```

This automatically runs:
```python
uvicorn.run("src.main:app", host="0.0.0.0", port=4000, reload=True)
```

## Method 2: Using Uvicorn CLI Directly

### Development (with auto-reload):
```powershell
uvicorn src.main:app --reload --port 4000
```

### Production:
```powershell
uvicorn src.main:app --host 0.0.0.0 --port 4000
```

### With more options:
```powershell
uvicorn src.main:app --reload --port 4000 --host 0.0.0.0 --log-level info
```

## Method 3: Using Python -m uvicorn

```powershell
python -m uvicorn src.main:app --reload --port 4000
```

## Uvicorn Options

| Option | Description |
|--------|-------------|
| `--reload` | Auto-reload on code changes (development) |
| `--host 0.0.0.0` | Listen on all interfaces |
| `--port 4000` | Port number |
| `--log-level info` | Logging level (debug/info/warning/error) |
| `--workers 4` | Number of worker processes (production) |

## Production with Multiple Workers

For production, use multiple workers:

```powershell
uvicorn src.main:app --host 0.0.0.0 --port 4000 --workers 4
```

Or with Gunicorn + Uvicorn workers:

```powershell
pip install gunicorn
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:4000
```

## Quick Start

1. **Activate virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Run with uvicorn:**
   ```powershell
   uvicorn src.main:app --reload --port 4000
   ```

3. **Access your API:**
   - API: http://localhost:4000/api/health
   - Docs: http://localhost:4000/docs

## What Happens When You Run

```
Uvicorn → Loads src.main:app → FastAPI App → Your Routes
```

Your FastAPI app (`src/main.py`) is loaded by Uvicorn and serves all your endpoints!

