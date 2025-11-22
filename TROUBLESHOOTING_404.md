# Troubleshooting 404 Error on Vercel

## Quick Fixes Applied

I've updated your configuration to fix common 404 issues:

1. ✅ Updated `vercel.json` routing
2. ✅ Updated `api/index.py` with proper Mangum configuration
3. ✅ Added root route (`/`) for testing

## Steps to Fix 404 Error

### 1. **Redeploy After Changes**
After the configuration updates, you need to:
- Commit and push the changes to your repository
- Vercel will automatically redeploy
- OR manually trigger a redeploy in Vercel Dashboard

### 2. **Check Vercel Logs**
Go to Vercel Dashboard → Your Project → Logs
Look for:
- Import errors
- Missing dependencies
- Environment variable errors

### 3. **Test These URLs**
After redeploying, try these endpoints:

```
https://your-app.vercel.app/
https://your-app.vercel.app/api/health
https://your-app.vercel.app/docs
https://your-app.vercel.app/api/auth/login
```

### 4. **Verify Environment Variables**
Make sure ALL required environment variables are set in Vercel:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_ANON_KEY`
- `JWT_SECRET`
- `AUTH_MODE`

### 5. **Check Build Logs**
In Vercel Dashboard → Deployments → Click on latest deployment
Check if:
- ✅ Build succeeded
- ✅ Dependencies installed correctly
- ✅ No import errors

## Common Causes of 404

### Cause 1: Missing Environment Variables
**Symptom:** 404 on all routes
**Fix:** Set all required environment variables in Vercel Dashboard

### Cause 2: Import Errors
**Symptom:** 404 with errors in logs
**Fix:** Check Vercel logs for Python import errors

### Cause 3: Incorrect Route Configuration
**Symptom:** 404 on specific routes
**Fix:** Already fixed in `vercel.json` - just redeploy

### Cause 4: Missing Dependencies
**Symptom:** 404 with module not found errors
**Fix:** Ensure `requirements.txt` has all dependencies

## Testing Checklist

After redeploying, test in this order:

1. **Root endpoint:**
   ```bash
   curl https://your-app.vercel.app/
   ```
   Should return: `{"success": true, "message": "API is running", ...}`

2. **Health check:**
   ```bash
   curl https://your-app.vercel.app/api/health
   ```
   Should return: `{"success": true, "message": "Server is running", ...}`

3. **API Docs:**
   ```
   https://your-app.vercel.app/docs
   ```
   Should show Swagger UI

4. **Auth endpoint:**
   ```bash
   curl -X POST https://your-app.vercel.app/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@test.com","password":"test"}'
   ```

## If Still Getting 404

### Check Vercel Function Logs:
1. Go to Vercel Dashboard
2. Click on your project
3. Go to **Functions** tab
4. Click on `api/index.py`
5. Check for runtime errors

### Verify File Structure:
Make sure you have:
```
backend/
├── api/
│   └── index.py          ✅ Must exist
├── src/
│   └── main.py           ✅ Must exist
├── requirements.txt      ✅ Must exist
└── vercel.json          ✅ Must exist
```

### Manual Test:
Try accessing the function directly:
```
https://your-app.vercel.app/api/index
```

## Still Not Working?

1. **Check Vercel Build Logs** - Look for Python errors
2. **Verify all files are committed** - Make sure `api/index.py` is in your repo
3. **Check Python version** - Vercel uses Python 3.9 by default
4. **Try redeploying** - Sometimes a fresh deploy fixes issues

## Expected Behavior

After fixes:
- ✅ `GET /` → Returns API info
- ✅ `GET /api/health` → Returns health status
- ✅ `GET /docs` → Shows Swagger UI
- ✅ `POST /api/auth/login` → Handles login requests

If these work, your API is properly deployed!

