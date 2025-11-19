# Supabase Integration Guide

## ✅ Your Backend is Already Configured for Supabase!

Your FastAPI backend is fully integrated with Supabase. Here's what's set up:

## 🔧 What's Configured

### 1. **Supabase Client** (`src/config/supabase.py`)
- ✅ Service role client (bypasses RLS - server-side only)
- ✅ Anon client (for client-side operations)
- ✅ Automatic configuration from `.env`

### 2. **Database Models** (All use Supabase)
- ✅ `UserModel` - Users table operations
- ✅ `OtpModel` - OTP requests table
- ✅ `PaymentModel` - Payments table
- ✅ `OrderModel` - Orders table

### 3. **Authentication Modes**
- ✅ **Supabase Auth Mode** - Uses Supabase's built-in auth
- ✅ **Custom JWT Mode** - Custom auth with Supabase database

### 4. **Database Schema** (`supabase-schema.sql`)
- ✅ All tables defined
- ✅ RLS (Row Level Security) policies
- ✅ Indexes for performance
- ✅ Triggers for auto-updates

## 📋 Setup Steps

### Step 1: Get Your Supabase Credentials

1. Go to [https://supabase.com/dashboard](https://supabase.com/dashboard)
2. Select your project (or create a new one)
3. Go to **Settings** → **API**
4. Copy:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **service_role** key (⚠️ Keep secret!)
   - **anon** key

### Step 2: Update `.env` File

Open `.env` and add your credentials:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 3: Run Database Schema

1. Go to **SQL Editor** in Supabase dashboard
2. Open `supabase-schema.sql` from your project
3. Copy and paste the entire SQL script
4. Click **Run** to execute

This creates:
- `users` table
- `otp_requests` table
- `payments` table
- `orders` table
- All indexes and RLS policies

## 🎯 How Supabase is Used

### Database Operations

All database operations use Supabase Postgres:

```python
# Example: Creating a user
from src.models.user_model import UserModel

user = await UserModel.create({
    "email": "user@example.com",
    "name": "John Doe"
})
```

This uses:
```python
supabase.table("users").insert(user_data).execute()
```

### Authentication

You can use **either** mode:

#### Option 1: Supabase Auth (Recommended)
```env
AUTH_MODE=supabase
```

- Uses Supabase's built-in authentication
- Handles sign up, login, password reset
- JWT tokens managed by Supabase
- Refresh tokens supported

#### Option 2: Custom JWT
```env
AUTH_MODE=custom
```

- Custom password hashing (bcrypt)
- Custom JWT generation
- Still uses Supabase database for user storage

### Row Level Security (RLS)

Your schema includes RLS policies:
- Users can only view their own data
- Users can only update their own profile
- Service role key bypasses RLS (server-side only)

## 🔐 Security Best Practices

1. **Service Role Key**
   - ⚠️ **NEVER** expose to client
   - Only use server-side
   - Already configured correctly in your code

2. **Anon Key**
   - Safe for client-side
   - Respects RLS policies
   - Use for direct client access (if needed)

3. **RLS Policies**
   - Already configured in schema
   - Users can only access their own data
   - Admin operations use service role

## 📊 Supabase Features You're Using

### ✅ Postgres Database
- All tables stored in Supabase Postgres
- Full SQL support
- Indexes for performance

### ✅ Authentication (Optional)
- Can use Supabase Auth
- Or custom JWT with Supabase database

### ✅ Row Level Security
- Policies configured
- Service role bypasses RLS

### 🔜 Available but Not Yet Used
- **Storage** - For file uploads (can add later)
- **Realtime** - For live updates (can add later)
- **Edge Functions** - Serverless functions (can add later)

## 🚀 Quick Start

1. **Add Supabase credentials to `.env`**
2. **Run the SQL schema in Supabase dashboard**
3. **Start your server:**
   ```powershell
   python run.py
   ```

## 📝 Example API Calls

### Register (Supabase Auth Mode)
```bash
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

### Login (Supabase Auth Mode)
```bash
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

Returns:
```json
{
  "user": {...},
  "session": {
    "access_token": "...",
    "refresh_token": "..."
  }
}
```

## 🎉 You're All Set!

Your FastAPI backend is fully integrated with Supabase. Just:
1. Add your Supabase credentials to `.env`
2. Run the database schema
3. Start coding! 🚀



