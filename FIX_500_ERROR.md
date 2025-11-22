# Fix 500 Internal Server Error

## Quick Checklist

### 1. **Check Environment Variables in Vercel**

Go to **Vercel Dashboard → Your Project → Settings → Environment Variables**

Make sure these are ALL set:

```
✅ SUPABASE_URL=https://your-project.supabase.co
✅ SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
✅ SUPABASE_ANON_KEY=your_anon_key
```

**Important:**
- No quotes around values
- No spaces before/after values
- Copy exact values from Supabase Dashboard

### 2. **Check Vercel Function Logs**

1. Go to **Vercel Dashboard → Your Project**
2. Click on **Functions** tab
3. Click on `api/index.py`
4. Look for error messages

Common errors you might see:
- `Missing Supabase configuration`
- `ModuleNotFoundError`
- `ImportError`

### 3. **Verify Supabase Keys**

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **Settings → API**
4. Copy:
   - **Project URL** → Use for `SUPABASE_URL`
   - **service_role key** → Use for `SUPABASE_SERVICE_ROLE_KEY`
   - **anon/public key** → Use for `SUPABASE_ANON_KEY`

### 4. **Redeploy After Setting Variables**

After adding/updating environment variables:
1. Go to **Deployments** tab
2. Click **⋯** (three dots) on latest deployment
3. Click **Redeploy**
4. Wait for deployment to complete

### 5. **Test the Root Endpoint**

After redeploying, test:
```
https://your-app.vercel.app/
```

If you see an error message, it will tell you which environment variables are missing.

## Common Error Messages

### "Missing Supabase configuration"
**Fix:** Set `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` in Vercel

### "ModuleNotFoundError: No module named 'X'"
**Fix:** Check `requirements.txt` includes all dependencies

### "ImportError"
**Fix:** Check Vercel logs for specific import that failed

### "Application initialization failed"
**Fix:** Check all environment variables are set correctly

## Step-by-Step Fix

1. **Open Vercel Dashboard**
   - Go to your project
   - Click **Settings** → **Environment Variables**

2. **Add Missing Variables**
   - Click **Add New**
   - Add each variable one by one:
     - Key: `SUPABASE_URL`
     - Value: `https://your-project.supabase.co`
     - Click **Save**
   
   Repeat for:
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `SUPABASE_ANON_KEY`

3. **Redeploy**
   - Go to **Deployments**
   - Click **Redeploy** on latest deployment

4. **Test**
   - Visit: `https://your-app.vercel.app/`
   - Should see: `{"success": true, "message": "API is running", ...}`

## Still Not Working?

1. **Check Build Logs**
   - Go to **Deployments** → Click on deployment
   - Check if build succeeded
   - Look for errors in build logs

2. **Check Function Logs**
   - Go to **Functions** → `api/index.py`
   - Check runtime logs for errors

3. **Verify File Structure**
   Make sure these files exist:
   ```
   ✅ api/index.py
   ✅ src/main.py
   ✅ requirements.txt
   ✅ vercel.json
   ```

4. **Test Locally** (optional)
   ```bash
   # Set environment variables
   export SUPABASE_URL=...
   export SUPABASE_SERVICE_ROLE_KEY=...
   export SUPABASE_ANON_KEY=...
   
   # Run locally
   python -m uvicorn src.main:app --reload
   ```

## Need More Help?

Check the error message at:
```
https://your-app.vercel.app/
```

The error response will show:
- Which environment variables are missing
- The exact error that occurred
- Traceback information

