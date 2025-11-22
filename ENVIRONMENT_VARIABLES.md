# Environment Variables for Vercel Deployment

Add these environment variables in **Vercel Dashboard → Your Project → Settings → Environment Variables**

---

## 🔴 REQUIRED Environment Variables

### Supabase Configuration

| Variable Name | Description | Example Value | Where to Get It |
|--------------|-------------|---------------|-----------------|
| `SUPABASE_URL` | Your Supabase project URL | `https://xxxxx.supabase.co` | Supabase Dashboard → Settings → API → Project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key (keep secret!) | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | Supabase Dashboard → Settings → API → service_role key |
| `SUPABASE_ANON_KEY` | Supabase anonymous/public key | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | Supabase Dashboard → Settings → API → anon/public key |

### Authentication

**Note:** Authentication is handled entirely by Supabase Auth. No additional authentication environment variables are needed.

### Payment (Razorpay)

| Variable Name | Description | Example Value | Where to Get It |
|--------------|-------------|---------------|-----------------|
| `RAZORPAY_KEY_ID` | Razorpay API Key ID | `rzp_test_xxxxx` or `rzp_live_xxxxx` | Razorpay Dashboard → Settings → API Keys |
| `RAZORPAY_SECRET` | Razorpay API Secret | `your_razorpay_secret_key` | Razorpay Dashboard → Settings → API Keys |

**Note:** If you're not using payment features, you can skip Razorpay variables, but payment endpoints will not work.

---

## 🟡 OPTIONAL Environment Variables (with defaults)

| Variable Name | Default Value | Description |
|--------------|--------------|-------------|
| `ENVIRONMENT` | `development` | Set to `production` for production |
| `CORS_ORIGIN` | `*` | Comma-separated list of allowed origins (e.g., `https://your-frontend.vercel.app,https://www.yourdomain.com`) |
| `PORT` | `4000` | Server port (Vercel handles this automatically) |

---

## 📋 Complete Environment Variables List

Copy and paste this into Vercel Dashboard:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
SUPABASE_ANON_KEY=your_anon_key_here
ENVIRONMENT=production
CORS_ORIGIN=https://your-frontend.vercel.app
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_SECRET=your_razorpay_secret
```

---

## 📍 Where to Find Your Keys

### Supabase Keys
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **Settings** → **API**
4. You'll find:
   - **Project URL** → Use for `SUPABASE_URL`
   - **anon/public key** → Use for `SUPABASE_ANON_KEY`
   - **service_role key** → Use for `SUPABASE_SERVICE_ROLE_KEY` (⚠️ Keep secret!)

### Razorpay Keys
1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com)
2. Go to **Settings** → **API Keys**
3. You'll find:
   - **Key ID** → Use for `RAZORPAY_KEY_ID`
   - **Key Secret** → Use for `RAZORPAY_SECRET`

---

## ✅ Verification Checklist

After adding environment variables in Vercel:

- [ ] All required variables are set
- [ ] `SUPABASE_URL` starts with `https://`
- [ ] `CORS_ORIGIN` includes your frontend URL (if you have one)
- [ ] `ENVIRONMENT` is set to `production`
- [ ] No spaces or quotes around values in Vercel

---

## 🚨 Security Notes

1. **Never commit** `.env` files to Git
2. **Never share** `SUPABASE_SERVICE_ROLE_KEY` publicly
3. **Rotate secrets** if they're ever exposed
4. **Restrict** `CORS_ORIGIN` to your actual frontend domains in production
5. **Use Supabase Auth** - All authentication is handled securely by Supabase

---

## 🔄 After Deployment

1. Test health endpoint: `https://your-app.vercel.app/api/health`
2. Check API docs: `https://your-app.vercel.app/docs`
3. Verify environment variables are loaded (check Vercel logs)
4. Test authentication endpoints
5. Update frontend `VITE_API_URL` to your backend URL

