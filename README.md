# FastAPI Backend with Supabase

Production-ready FastAPI backend using Supabase as the database and authentication provider.

## Features

- ✅ **Supabase Integration**: Postgres database, Auth, and Storage
- ✅ **Supabase Auth**: Full authentication via Supabase
- ✅ **User Management**: Profile management with role-based access
- ✅ **Payment Integration**: Razorpay payment processing
- ✅ **Order Management**: Complete order lifecycle management
- ✅ **Production Ready**: Error handling, validation, logging

## Tech Stack

- **Framework**: FastAPI
- **Runtime**: Python 3.11+
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth
- **Payment**: Razorpay
- **Deployment**: Render

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create `.env` file:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_ANON_KEY=your_anon_key
ENVIRONMENT=production
CORS_ORIGIN=https://your-frontend-domain.com
```

### 3. Run Locally

```bash
python run.py
```

Or with uvicorn directly:

```bash
uvicorn src.main:app --reload --port 8000
```

## Deployment

### Render Deployment

See `RENDER_DEPLOYMENT.md` for detailed instructions.

**Quick steps:**
1. Push code to Git
2. Connect to Render
3. Use `render.yaml` or set:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn src.main:app --host 0.0.0.0 --port $PORT --workers 4`
4. Set environment variables
5. Deploy

## API Endpoints

- `GET /` - Root endpoint
- `GET /api/health` - Health check
- `GET /docs` - Swagger UI documentation
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/users/me` - Get current user
- And more...

## Environment Variables

See `ENVIRONMENT_VARIABLES.md` for complete list.

**Required:**
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_ANON_KEY`

## License

ISC

