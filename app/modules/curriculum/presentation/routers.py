from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import List, Optional
from app.modules.curriculum.presentation.schemas import AnalysisResponse, HealthResponse
from app.modules.curriculum.presentation.dependencies import get_analyze_use_case, get_history_use_case
from app.modules.curriculum.application.use_cases import AnalyzeCurriculaUseCase, GetAnalysisHistoryUseCase
from app.core.security import validate_files
from datetime import datetime

router = APIRouter(prefix="/api/v1")

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "services": {
            "ocr": "tesseract",
            "llm": "openai",
            "database": "dynamodb"
        }
    }

@router.post("/curriculum/", response_model=AnalysisResponse)
async def analyze_curriculum(
    files: List[UploadFile] = File(..., description="Arquivos PDF, JPG ou PNG"),
    query: Optional[str] = Form(None, description="Query opcional para análise específica"),
    request_id: str = Form(..., description="ID único da requisição"),
    user_id: str = Form(..., description="ID do usuário solicitante"),
    use_case: AnalyzeCurriculaUseCase = Depends(get_analyze_use_case)
):
    """
    Analisa currículos usando OCR e LLM.
    
    - **files**: Lista de arquivos (PDF, JPG, PNG)
    - **query**: Query opcional. Se não informada, retorna resumo individual
    - **request_id**: ID único da requisição
    - **user_id**: ID do usuário
    
    **Exemplos de uso:**
    
    **Com query específica:**
    ```
    curl -X POST "http://localhost:8000/api/v1/curriculum/" \
      -F "files=@cv1.pdf" \
      -F "files=@cv2.jpg" \
      -F "query=Qual candidato tem mais experiência em Python?" \
      -F "request_id=123e4567-e89b-12d3-a456-426614174000" \
      -F "user_id=irineutech2025@gmail.com"
    ```
    
    **Sem query (resumo automático):**
    ```
    curl -X POST "http://localhost:8000/api/v1/curriculum/" \
      -F "files=@cv1.pdf" \
      -F "files=@cv2.jpg" \
      -F "request_id=123e4567-e89b-12d3-a456-426614174000" \
      -F "user_id=irineutech2025@gmail.com"
    ```
    """
    try:
        validate_files(files)
        
        result = await use_case.execute(files, query, request_id, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/curriculum/history/{user_id}")
async def get_analysis_history(
    user_id: str,
    limit: int = 10,
    use_case: GetAnalysisHistoryUseCase = Depends(get_history_use_case)
):
    """
    Busca histórico de análises de um usuário específico.
    
    - **user_id**: ID do usuário
    - **limit**: Número máximo de resultados (padrão: 10)
    """
    try:
        history = await use_case.execute(user_id, limit)
        return {
            "user_id": user_id,
            "history": history,
            "total": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
