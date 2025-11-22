"""
Vercel serverless function entry point for FastAPI
This file is required for Vercel to properly handle FastAPI requests
"""
from mangum import Mangum
from src.main import app

# Wrap FastAPI app with Mangum for Vercel serverless compatibility
# api_gateway_base_path is set to empty string to handle root path correctly
handler = Mangum(app, lifespan="off", api_gateway_base_path="")

