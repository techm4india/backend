import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Optional
import sys

load_dotenv()

_supabase_client: Optional[Client] = None
_supabase_anon_client: Optional[Client] = None

def _init_supabase_client():
    """Initialize Supabase service role client (lazy initialization)"""
    global _supabase_client
    
    if _supabase_client is not None:
        return _supabase_client
        
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or supabase_url == "your_supabase_project_url":
        raise ValueError(
            "Missing Supabase configuration. Please set SUPABASE_URL in .env file.\n"
            "Get your Supabase URL from: https://supabase.com/dashboard/project/_/settings/api"
        )
    
    if not supabase_service_role_key or supabase_service_role_key == "your_service_role_key":
        raise ValueError(
            "Missing Supabase configuration. Please set SUPABASE_SERVICE_ROLE_KEY in .env file.\n"
            "Get your service_role key from: https://supabase.com/dashboard/project/_/settings/api\n"
            "⚠️  WARNING: Keep the service_role key secret! Never commit it to version control."
        )
    
    try:
        # Try with options first (newer versions)
        _supabase_client = create_client(
            supabase_url,
            supabase_service_role_key,
            options={
                "auto_refresh_token": False,
                "persist_session": False
            }
        )
    except (TypeError, Exception) as e:
        # Fallback: create without options (older versions or compatibility issue)
        try:
            _supabase_client = create_client(supabase_url, supabase_service_role_key)
        except TypeError as e2:
            # This is the proxy argument error - provide helpful message
            if "proxy" in str(e2).lower():
                raise RuntimeError(
                    "Supabase client initialization failed due to version incompatibility.\n"
                    "This is a known issue with certain versions of supabase-py and httpx.\n\n"
                    "To fix, run:\n"
                    "  pip install --upgrade 'supabase>=2.3.0' 'httpx==0.27.0'\n\n"
                    f"Original error: {str(e2)}"
                ) from e2
            raise
        except Exception as e2:
            raise RuntimeError(
                f"Failed to initialize Supabase client.\n"
                f"Error: {str(e2)}\n"
                f"Try: pip install --upgrade supabase httpx"
            ) from e2
    
    return _supabase_client

def _init_supabase_anon_client():
    """Initialize Supabase anon client (lazy initialization)"""
    global _supabase_anon_client
    
    if _supabase_anon_client is not None:
        return _supabase_anon_client
        
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
    
    if supabase_anon_key:
        try:
            _supabase_anon_client = create_client(
                supabase_url,
                supabase_anon_key,
                options={
                    "auto_refresh_token": False,
                    "persist_session": False
                }
            )
        except (TypeError, Exception):
            _supabase_anon_client = create_client(supabase_url, supabase_anon_key)
    
    return _supabase_anon_client

# Module-level __getattr__ for lazy initialization (Python 3.7+)
def __getattr__(name: str):
    if name == "supabase":
        return _init_supabase_client()
    elif name == "supabase_anon":
        return _init_supabase_anon_client()
    elif name == "supabase_url":
        return os.getenv("SUPABASE_URL")
    elif name == "supabase_anon_key":
        return os.getenv("SUPABASE_ANON_KEY")
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Export URL and keys for convenience (eager, but safe)
supabase_url = os.getenv("SUPABASE_URL")
supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")

__all__ = ["supabase", "supabase_anon", "supabase_url", "supabase_anon_key"]
