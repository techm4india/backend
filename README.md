# FastAPI Backend with Supabase

Production-ready FastAPI backend using Supabase as the database and authentication provider. Features include authentication (with OTP verification), user management, role-based access control, Razorpay payment integration, and order management.

## Features

- ✅ **Supabase Integration**: Postgres database, Auth, and Storage
- ✅ **Dual Auth Modes**: Support for both Supabase Auth and Custom JWT
- ✅ **OTP Verification**: Email/Phone OTP for user verification
- ✅ **User Management**: Profile management with role-based access
- ✅ **Payment Integration**: Razorpay payment processing
- ✅ **Order Management**: Complete order lifecycle management
- ✅ **Row Level Security**: RLS-enabled queries
- ✅ **Comprehensive Testing**: Pytest test suite
- ✅ **Production Ready**: Error handling, validation, logging
- ✅ **FastAPI**: Modern, fast Python web framework with automatic API docs

## Tech Stack

- **Framework**: FastAPI
- **Runtime**: Python 3.9+
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth / Custom JWT
- **Payment**: Razorpay
- **Testing**: Pytest
- **Validation**: Pydantic

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Supabase account and project
- Razorpay account (for payment features)

## Setup Instructions

### 1. Install Dependencies

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

### 2. Configure Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **Settings** → **API** to get your keys:
   - Project URL
   - `service_role` key (keep secret!)
   - `anon` key

3. Run the database schema:
   - Go to **SQL Editor** in Supabase dashboard
   - Copy and paste the contents of `supabase-schema.sql`
   - Execute the SQL script

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

Update `.env` with your credentials:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_ANON_KEY=your_anon_key

# Authentication
AUTH_MODE=custom
JWT_SECRET=your_custom_jwt_secret_key_change_in_production
JWT_EXPIRES_IN=7d

# Razorpay Configuration
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_SECRET=your_razorpay_secret

# Server Configuration
PORT=4000
ENVIRONMENT=development

# Security
BCRYPT_SALT_ROUNDS=10
```

### 4. Run the Server

```bash
# Development mode (with auto-reload)
python run.py

# Or using uvicorn directly
uvicorn src.main:app --reload --port 4000

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 4000
```

The server will start on `http://localhost:4000`

### 5. Access API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:4000/docs
- **ReDoc**: http://localhost:4000/redoc

### 6. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest src/tests/test_auth.py
```

## API Endpoints

### Authentication

#### Register User
```bash
curl -X POST http://localhost:4000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe",
    "phone": "+1234567890"
  }'
```

#### Login
```bash
curl -X POST http://localhost:4000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

#### Send OTP
```bash
curl -X POST http://localhost:4000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{
    "target": "user@example.com",
    "type": "register"
  }'
```

#### Verify OTP
```bash
curl -X POST http://localhost:4000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "target": "user@example.com",
    "code": "123456",
    "type": "register"
  }'
```

### Users

#### Get Current User Profile
```bash
curl -X GET http://localhost:4000/api/users/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Update Profile
```bash
curl -X PATCH http://localhost:4000/api/users/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "phone": "+9876543210"
  }'
```

### Payments

#### Create Payment Order
```bash
curl -X POST http://localhost:4000/api/payments/create-order \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100.00,
    "currency": "INR"
  }'
```

#### Verify Payment
```bash
curl -X POST http://localhost:4000/api/payments/verify \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "razorpay_order_id": "order_xxx",
    "razorpay_payment_id": "pay_xxx",
    "razorpay_signature": "signature_xxx"
  }'
```

### Orders

#### Create Order
```bash
curl -X POST http://localhost:4000/api/orders \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "id": "item-1",
        "name": "Product 1",
        "quantity": 2,
        "price": 50.00
      }
    ],
    "total": 100.00,
    "paymentId": "payment-id-optional"
  }'
```

## Database Schema

See `supabase-schema.sql` for the complete database schema with all tables, indexes, and Row Level Security policies.

## Project Structure

```
backend/
├── src/
│   ├── config/
│   │   └── supabase.py          # Supabase client configuration
│   ├── models/
│   │   ├── user_model.py
│   │   ├── otp_model.py
│   │   ├── payment_model.py
│   │   └── order_model.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── otp_service.py
│   │   ├── payment_service.py
│   │   └── order_service.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── payment_routes.py
│   │   ├── order_routes.py
│   │   └── __init__.py
│   ├── middlewares/
│   │   ├── auth_middleware.py    # JWT/Supabase auth dependency
│   │   └── error_handler.py     # Global error handling
│   ├── validators/
│   │   ├── auth_validator.py     # Pydantic models
│   │   ├── payment_validator.py
│   │   └── order_validator.py
│   ├── utils/
│   │   ├── jwt.py                # JWT utilities
│   │   ├── response.py           # Standard API responses
│   │   └── logger.py              # Logging utilities
│   ├── tests/
│   │   └── (test files)
│   └── main.py                   # FastAPI app entry point
├── .env.example
├── requirements.txt
├── run.py                        # Run script
├── supabase-schema.sql           # Database schema
└── README.md
```

## Authentication Modes

### Custom JWT Mode (Default)

- Passwords are hashed with bcrypt
- JWT tokens generated using `JWT_SECRET`
- Set `AUTH_MODE=custom` in `.env`

### Supabase Auth Mode

- Uses Supabase's built-in authentication
- Set `AUTH_MODE=supabase` in `.env`
- Users are created via Supabase Auth API
- Backend verifies Supabase JWT tokens

## FastAPI Features

- **Automatic API Documentation**: Visit `/docs` for Swagger UI
- **Type Safety**: Full type hints with Pydantic
- **Async Support**: All endpoints are async
- **Validation**: Automatic request/response validation
- **OpenAPI Schema**: Auto-generated OpenAPI 3.0 schema

## Security Best Practices

1. **Never commit `.env` file** - It contains sensitive keys
2. **Use service role key only server-side** - Never expose it to clients
3. **Enable RLS policies** - Row Level Security is configured in the schema
4. **Validate all inputs** - Pydantic models handle validation
5. **Hash passwords** - bcrypt with configurable salt rounds
6. **Use HTTPS in production** - Always use SSL/TLS
7. **Rate limit OTP requests** - Implemented in OTP service

## Error Handling

The API returns standardized error responses:

```json
{
  "success": false,
  "message": "Error message",
  "errors": [] // Optional validation errors
}
```

Success responses:

```json
{
  "success": true,
  "message": "Success message",
  "data": {} // Response data
}
```

## Production Deployment

1. Set `ENVIRONMENT=production`
2. Use strong `JWT_SECRET`
3. Configure proper CORS origins
4. Set up Razorpay webhook URL
5. Enable HTTPS
6. Use production ASGI server (Gunicorn + Uvicorn workers)
7. Set up monitoring and logging
8. Configure rate limiting

### Running with Gunicorn

```bash
pip install gunicorn
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:4000
```

## License

ISC
