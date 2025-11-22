"""
Vercel serverless function entry point for FastAPI
This file is required for Vercel to properly handle FastAPI requests
"""
import os
import json
import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Try to import the main app
try:
    from mangum import Mangum
    from src.main import app
    
    # Wrap FastAPI app with Mangum for Vercel serverless compatibility
    handler = Mangum(app, lifespan="off", api_gateway_base_path="")
except Exception as e:
    # If import fails, create a minimal FastAPI app with error info
    error_app = FastAPI()
    
    @error_app.get("/{full_path:path}")
    async def error_handler(full_path: str):
        """Error handler when app fails to initialize"""
        error_details = {
            "success": False,
            "error": "Application initialization failed",
            "message": str(e),
            "traceback": "".join(traceback.format_exception(type(e), e, e.__traceback__)),
            "missing_env_vars": [],
            "help": "Check Vercel logs and ensure all environment variables are set"
        }
        
        # Check which env vars are missing
        required_vars = ["SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_ANON_KEY"]
        for var in required_vars:
            if not os.getenv(var):
                error_details["missing_env_vars"].append(var)
        
        return JSONResponse(
            status_code=500,
            content=error_details
        )
    
    handler = Mangum(error_app, lifespan="off", api_gateway_base_path="")

