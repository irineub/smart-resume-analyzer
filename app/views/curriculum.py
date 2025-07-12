from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
from app.controllers.curriculum_controller import CurriculumController

router = APIRouter(prefix="/api/v1")

@router.post("/curriculum/")
async def analyze_curriculum(
    files: List[UploadFile] = File(..., description="Arquivos PDF, JPG ou PNG"),
    query: Optional[str] = Form(None, description="Query opcional para análise específica"),
    request_id: str = Form(..., description="ID único da requisição"),
    user_id: str = Form(..., description="ID do usuário solicitante")
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
      -F "user_id=fabio@techmatch.com"
    ```
    
    **Sem query (resumo automático):**
    ```
    curl -X POST "http://localhost:8000/api/v1/curriculum/" \
      -F "files=@cv1.pdf" \
      -F "files=@cv2.jpg" \
      -F "request_id=123e4567-e89b-12d3-a456-426614174000" \
      -F "user_id=fabio@techmatch.com"
    ```
    """
    try:
        controller = CurriculumController()
        result = await controller.analyze_curricula(files, query, request_id, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check para monitoramento"""
    return {
        "status": "healthy",
        "service": "Curriculum Analysis API",
        "version": "1.0.0"
    }