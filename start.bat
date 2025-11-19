@echo off
REM Start FastAPI with Uvicorn (Windows)
echo Starting FastAPI server with Uvicorn...
uvicorn src.main:app --reload --host 0.0.0.0 --port 4000



