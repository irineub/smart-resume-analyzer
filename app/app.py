from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from app.core.config import settings
from app.modules.curriculum.presentation.routers import router as curriculum_router
from app.modules.curriculum.presentation.routers import misc 
from app.core.database import dynamodb_client

def create_app() -> FastAPI:
    """Cria e configura a aplicação FastAPI"""
    
    app = FastAPI(
        title=settings.app_name,
        description="Ferramenta com IA que extrai, resume e responde perguntas sobre currículos usando OCR e LLMs",
        version=settings.app_version,
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        openapi_url="/api/v1/openapi.json",
        contact={
            "name": "Irineu Brito",
            "url": "https://github.com/irineub",
            "email": ""
        },
        license_info={
            "name": "Mais informações sobre o desenvolvedor (Linkedin)",
            "url": "https://linkedin.com/in/irineu-brito"
        }
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(curriculum_router, tags=["Curriculo"])
    app.include_router(misc, tags=["Misc"])
    
    @app.on_event("startup")
    async def startup_event():
        """Evento executado na inicialização da aplicação"""
        try:
            await dynamodb_client.create_table_if_not_exists()
            print("✅ Database inicializado com sucesso!")
        except Exception as e:
            print(f"⚠️ Aviso: Não foi possível inicializar o database: {e}")
    
    @app.get("/", include_in_schema=False)
    async def root():
        """Root endpoint"""
        return {
            "message": settings.app_name,
            "version": settings.app_version,
            "docs": "/api/v1/docs",
            "status": "running"
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
    
    return app

app = create_app() 