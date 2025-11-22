# Render Deployment Guide

This guide will help you deploy your FastAPI backend on Render.

## Prerequisites

1. Render account (sign up at [render.com](https://render.com))
2. Git repository (GitHub, GitLab, or Bitbucket)

---

## Quick Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push your code to Git** (make sure `render.yaml` is committed)

2. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Click **"New +"** → **"Blueprint"**

3. **Connect Repository**
   - Connect your Git repository
   - Render will detect `render.yaml` automatically

4. **Set Environment Variables**
   - Go to your service → **Environment**
   - Add these variables:
     ```
     SUPABASE_URL=https://your-project.supabase.co
     SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
     SUPABASE_ANON_KEY=your_anon_key
     ENVIRONMENT=production
     CORS_ORIGIN=https://your-frontend.vercel.app
     RAZORPAY_KEY_ID=your_razorpay_key_id (optional)
     RAZORPAY_SECRET=your_razorpay_secret (optional)
     ```

5. **Deploy**
   - Click **"Apply"**
   - Render will build and deploy automatically

### Option 2: Manual Setup

1. **Go to Render Dashboard**
   - Click **"New +"** → **"Web Service"**

2. **Connect Repository**
   - Connect your Git repository
   - Select the repository and branch

3. **Configure Service**
   - **Name**: `backend-api` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

4. **Set Environment Variables**
   - Go to **Environment** tab
   - Add all required variables (see below)

5. **Deploy**
   - Click **"Create Web Service"**

---

## Environment Variables

Set these in Render Dashboard → Your Service → Environment:

### Required
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_ANON_KEY=your_anon_key
```

### Optional
```
ENVIRONMENT=production
CORS_ORIGIN=https://your-frontend.vercel.app
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_SECRET=your_razorpay_secret
PORT=8000 (Render sets this automatically)
```

---

## Render Configuration

### Build Command
```
pip install -r requirements.txt
```

### Start Command
```
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

**Explanation:**
- `gunicorn` - Production WSGI/ASGI server
- `src.main:app` - Your FastAPI app location
- `-w 4` - 4 worker processes
- `-k uvicorn.workers.UvicornWorker` - Use Uvicorn workers for async support
- `--bind 0.0.0.0:$PORT` - Bind to all interfaces on Render's port

---

## Differences from Vercel

| Aspect | Vercel | Render |
|--------|--------|--------|
| **Type** | Serverless functions | Traditional server |
| **Entry Point** | `api/index.py` | `src/main.py` |
| **Adapter** | Mangum (ASGI→Lambda) | Gunicorn (ASGI server) |
| **Scaling** | Auto-scaling per request | Fixed workers |
| **Cold Starts** | Yes (serverless) | No (always running) |

---

## Testing After Deployment

1. **Get your Render URL**
   - Render provides: `https://your-service.onrender.com`

2. **Test endpoints:**
   ```
   https://your-service.onrender.com/
   https://your-service.onrender.com/api/health
   https://your-service.onrender.com/docs
   ```

3. **Update Frontend**
   - Set `VITE_API_URL=https://your-service.onrender.com/api`

---

## Troubleshooting

### Service won't start
- Check **Logs** tab in Render dashboard
- Verify all environment variables are set
- Check build logs for dependency errors

### 500 errors
- Check Render logs for Python errors
- Verify Supabase credentials are correct
- Ensure database schema is set up in Supabase

### Slow response times
- Render free tier spins down after 15 min inactivity
- First request after spin-down takes ~30 seconds
- Upgrade to paid plan for always-on service

### Build fails
- Check Python version (should be 3.11)
- Verify `requirements.txt` is correct
- Check build logs for specific errors

---

## Advantages of Render

✅ **Always-on** (paid plans) - No cold starts  
✅ **Traditional server** - Easier debugging  
✅ **Better for long-running tasks**  
✅ **More predictable performance**  
✅ **Free tier available** (with spin-down)

---

## Cost

- **Free Tier**: 
  - Spins down after 15 min inactivity
  - 750 hours/month
  - First request after spin-down is slow

- **Starter Plan**: $7/month
  - Always on
  - No spin-down
  - Better performance

---

## Next Steps

1. Deploy to Render
2. Test all endpoints
3. Update frontend API URL
4. Monitor logs for any issues

Your API will be available at: `https://your-service.onrender.com`

