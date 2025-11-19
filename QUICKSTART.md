# Quick Start Guide - FastAPI

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up Supabase

1. **Create a Supabase Project**
   - Go to [https://supabase.com](https://supabase.com)
   - Sign up or log in
   - Create a new project

2. **Get Your Supabase Keys**
   - Go to **Settings** → **API** in your Supabase dashboard
   - Copy:
     - **Project URL** (e.g., `https://xxxxx.supabase.co`)
     - **service_role** key (keep this secret!)
     - **anon** key

3. **Set Up Database Schema**
   - Go to **SQL Editor** in Supabase dashboard
   - Open the file `supabase-schema.sql` from this project
   - Copy and paste the entire SQL script
   - Click **Run** to execute
   - This creates all necessary tables (users, otp_requests, payments, orders)

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

Then edit `.env` and fill in your values:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
SUPABASE_ANON_KEY=your_anon_key_here

# Authentication (use 'custom' or 'supabase')
AUTH_MODE=custom
JWT_SECRET=your_very_secret_jwt_key_change_this_in_production
JWT_EXPIRES_IN=7d

# Razorpay (optional - only needed for payments)
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_SECRET=your_razorpay_secret

# Server Configuration
PORT=4000
ENVIRONMENT=development

# Security
BCRYPT_SALT_ROUNDS=10
```

### 4. Run the Server

**Development mode (with auto-reload):**
```bash
python run.py
```

**Or using uvicorn directly:**
```bash
uvicorn src.main:app --reload --port 4000
```

**Production mode:**
```bash
uvicorn src.main:app --host 0.0.0.0 --port 4000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:4000
INFO:     Application startup complete.
```

### 5. Test the Server

Open your browser or use curl:

```bash
# Health check
curl http://localhost:4000/api/health
```

Expected response:
```json
{
  "success": true,
  "message": "Server is running",
  "timestamp": "2024-..."
}
```

### 6. Access API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:4000/docs
- **ReDoc**: http://localhost:4000/redoc

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run in development mode (auto-reload on changes)
python run.py

# Run in production mode
uvicorn src.main:app --host 0.0.0.0 --port 4000

# Run tests
pytest

# Run tests with coverage
pytest --cov=src
```

## Troubleshooting

### Error: "Missing Supabase configuration"
- Make sure `.env` file exists and has `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`

### Error: "Cannot find module"
- Run `pip install -r requirements.txt` to install dependencies
- Make sure you're in the virtual environment

### Error: "Port already in use"
- Change `PORT` in `.env` to a different port (e.g., 4001)

### Database connection issues
- Verify your Supabase URL and keys are correct
- Check that you've run the SQL schema in Supabase SQL Editor
- Ensure your Supabase project is active

### Python version issues
- Make sure you're using Python 3.9 or higher
- Check with: `python --version`

## Next Steps

1. **Test Registration:**
   ```bash
   curl -X POST http://localhost:4000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"password123","name":"Test User"}'
   ```

2. **Test Login:**
   ```bash
   curl -X POST http://localhost:4000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"password123"}'
   ```

3. **Explore API Docs**: Visit http://localhost:4000/docs for interactive API documentation

4. **See README.md** for complete API documentation and more examples
