import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError(
        "JWT_SECRET environment variable is required. "
        "Please set it in your environment variables."
    )
JWT_EXPIRES_IN = os.getenv("JWT_EXPIRES_IN", "7d")
JWT_ALGORITHM = "HS256"


def _parse_expires_in(expires_in: str) -> timedelta:
    """Parse JWT_EXPIRES_IN string to timedelta"""
    if expires_in.endswith("d"):
        days = int(expires_in[:-1])
        return timedelta(days=days)
    elif expires_in.endswith("h"):
        hours = int(expires_in[:-1])
        return timedelta(hours=hours)
    elif expires_in.endswith("m"):
        minutes = int(expires_in[:-1])
        return timedelta(minutes=minutes)
    else:
        return timedelta(days=7)  # default


def generate_token(payload: dict) -> str:
    """Generate JWT token"""
    expire = datetime.utcnow() + _parse_expires_in(JWT_EXPIRES_IN)
    to_encode = payload.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("Invalid or expired token")


def decode_token(token: str) -> dict:
    """Decode JWT token without verification (for inspection)"""
    return jwt.decode(token, options={"verify_signature": False})

