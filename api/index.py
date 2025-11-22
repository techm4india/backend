"""
Vercel serverless function entry point for FastAPI
"""
import os
import traceback

# Try to import the main app
try:
    from mangum import Mangum
    from src.main import app
    
    # Wrap FastAPI app with Mangum
    handler = Mangum(app, lifespan="off", api_gateway_base_path="")
    
except Exception as e:
    # If import fails, create minimal FastAPI app with error details
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from mangum import Mangum
    
    error_app = FastAPI(title="Error App")
    
    # Store error info
    init_error = str(e)
    init_error_type = type(e).__name__
    init_traceback = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    
    @error_app.get("/{full_path:path}")
    @error_app.post("/{full_path:path}")
    @error_app.put("/{full_path:path}")
    @error_app.delete("/{full_path:path}")
    @error_app.patch("/{full_path:path}")
    async def error_handler(full_path: str):
        """Error handler - shows what went wrong"""
        # Check missing env vars
        missing_vars = []
        required_vars = ["SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_ANON_KEY"]
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Application initialization failed",
                "error_type": init_error_type,
                "message": init_error,
                "missing_env_vars": missing_vars,
                "traceback": init_traceback,
                "help": "Set missing environment variables in Vercel Dashboard → Settings → Environment Variables",
                "path": full_path
            }
        )
    
    handler = Mangum(error_app, lifespan="off", api_gateway_base_path="")

