from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from datetime import datetime

app = FastAPI(
    title="Curriculum Vitae Query Assistant",
    description="AI-powered tool that extracts and summarizes resumes using OCR and LLMs",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Curriculum Vitae Query Assistant API",
        "version": "1.0.0",
        "docs": "/api/v1/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "uptime": "running"
    }

@app.get("/api/v1/health")
async def api_health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "endpoints": {
            "docs": "/api/v1/docs",
            "health": "/api/v1/health",
            "curriculum": "/api/v1/curriculum/"
        }
    }

@app.post("/api/v1/curriculum/")
async def analyze_curriculum():
    """Placeholder for curriculum analysis endpoint"""
    return {
        "code": 200,
        "status": "success",
        "message": "Curriculum analysis endpoint - To be implemented",
        "timestamp": datetime.utcnow().isoformat(),
        "path": "/api/v1/curriculum/",
        "method": "POST"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )