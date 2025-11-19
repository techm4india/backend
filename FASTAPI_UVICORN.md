# FastAPI and Uvicorn

## Yes, FastAPI Needs Uvicorn!

FastAPI is a **web framework** (like Express.js for Node.js), but it needs an **ASGI server** to actually run. Uvicorn is the most popular ASGI server for FastAPI.

## How They Work Together

```
┌─────────────┐
│   FastAPI   │  ← Web framework (handles routes, validation, etc.)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Uvicorn   │  ← ASGI server (runs the FastAPI app)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   HTTP      │  ← Serves on http://localhost:4000
└─────────────┘
```

## What's Already Installed

✅ **Uvicorn is already in your `requirements.txt`:**
```txt
uvicorn[standard]==0.27.0
```

The `[standard]` extra includes:
- `httptools` - Fast HTTP parser
- `uvloop` - Fast event loop (Linux/Mac)
- `websockets` - WebSocket support
- `watchfiles` - Auto-reload on file changes

## How to Run

### Method 1: Using run.py (Recommended)
```powershell
python run.py
```

This runs:
```python
uvicorn.run("src.main:app", host="0.0.0.0", port=4000, reload=True)
```

### Method 2: Using uvicorn CLI directly
```powershell
uvicorn src.main:app --reload --port 4000
```

### Method 3: Production (with Gunicorn + Uvicorn workers)
```powershell
pip install gunicorn
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:4000
```

## Why Uvicorn?

1. **Fast** - Built on `uvloop` (faster than asyncio)
2. **ASGI Standard** - Works with any ASGI framework
3. **Auto-reload** - `--reload` flag for development
4. **Production Ready** - Used in production with Gunicorn
5. **WebSocket Support** - Built-in WebSocket support

## Alternative ASGI Servers

While uvicorn is the standard, you could also use:
- **Hypercorn** - Alternative ASGI server
- **Daphne** - Django Channels' ASGI server
- **Granian** - Rust-based ASGI server

But **uvicorn is recommended** and what most FastAPI projects use.

## Summary

✅ FastAPI = Web framework (your app code)
✅ Uvicorn = ASGI server (runs your app)
✅ Both are installed and ready to use!

Just run: `python run.py` 🚀

