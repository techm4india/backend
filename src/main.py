import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from src.routes import api_router
from src.middlewares.error_handler import (
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

load_dotenv()

app = FastAPI(
    title="Backend API",
    description="Production-ready FastAPI backend with Supabase",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGIN", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Root route
@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse(
        content={
            "success": True,
            "message": "API is running",
            "docs": "/docs",
            "health": "/api/health",
        }
    )

# Health check
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "success": True,
            "message": "Server is running",
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        }
    )

# Include API routes
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 4000))
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)

