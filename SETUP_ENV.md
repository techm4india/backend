# Setting Up Your .env File

## Quick Setup

The `.env` file has been created from `.env.example`. You need to fill in your Supabase credentials.

## Step 1: Get Your Supabase Credentials

1. Go to [https://supabase.com](https://supabase.com) and sign in
2. Create a new project (or select an existing one)
3. Go to **Settings** → **API**
4. Copy the following values:

### Required Values:

- **Project URL**: Found under "Project URL" (e.g., `https://xxxxx.supabase.co`)
- **service_role key**: Found under "Project API keys" → "service_role" (⚠️ Keep this secret!)
- **anon key**: Found under "Project API keys" → "anon" (public key)

## Step 2: Update .env File

Open `.env` in your editor and replace the placeholder values:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Authentication
AUTH_MODE=custom
JWT_SECRET=your_very_secret_jwt_key_change_this_in_production
JWT_EXPIRES_IN=7d

# Razorpay Configuration (optional - only needed for payments)
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_SECRET=your_razorpay_secret

# Server Configuration
PORT=4000
ENVIRONMENT=development

# Security
BCRYPT_SALT_ROUNDS=10
```

## Step 3: Set Up Database Schema

1. Go to **SQL Editor** in your Supabase dashboard
2. Open the file `supabase-schema.sql` from this project
3. Copy and paste the entire SQL script
4. Click **Run** to execute

This creates all necessary tables (users, otp_requests, payments, orders).

## Step 4: Test the Server

After updating `.env` with your credentials:

```powershell
python run.py
```

The server should start successfully on `http://localhost:4000`

## Troubleshooting

### Error: "Missing Supabase configuration"
- Make sure `.env` file exists in the project root (`D:\backend\.env`)
- Verify you've replaced all placeholder values
- Check that there are no extra spaces around the `=` sign

### Error: "Invalid Supabase URL"
- Make sure the URL starts with `https://`
- Verify the URL is correct from your Supabase dashboard

### Error: "Authentication failed"
- Double-check your service_role key is correct
- Make sure you copied the entire key (they're very long)

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `.env` to version control (it's in `.gitignore`)
- The `service_role` key has admin access - keep it secret!
- Use different keys for development and production

