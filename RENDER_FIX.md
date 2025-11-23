# Fix Render Deployment Error

## Error: `ModuleNotFoundError: No module named 'app'`

This happens because Render is using the wrong start command.

## Quick Fix

### In Render Dashboard:

1. Go to your service → **Settings**
2. Scroll to **"Start Command"**
3. Change it to:
   ```
   uvicorn src.main:app --host 0.0.0.0 --port $PORT --workers 4
   ```
4. Click **"Save Changes"**
5. Render will automatically redeploy

## Alternative: Use Procfile

If `render.yaml` isn't being read, Render will use `Procfile`:

Make sure `Procfile` contains:
```
web: uvicorn src.main:app --host 0.0.0.0 --port $PORT --workers 4
```

## Python Version Issue

The error shows Python 3.13, but we specified 3.11.0. To fix:

1. Go to **Settings** → **Environment**
2. Add/Update: `PYTHON_VERSION=3.11.0`
3. Or in **Build & Deploy** → **Environment**, set Python version to 3.11

## Correct Start Command

**Must be:**
```
uvicorn src.main:app --host 0.0.0.0 --port $PORT --workers 4
```

**NOT:**
```
gunicorn app:app  ❌
uvicorn app:app   ❌
```

## After Fixing

1. Save the start command
2. Render will redeploy automatically
3. Check logs - should see "Application startup complete"
4. Test: `https://your-service.onrender.com/api/health`

