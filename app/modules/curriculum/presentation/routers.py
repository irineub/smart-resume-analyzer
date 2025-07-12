from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import List, Optional
from app.modules.curriculum.presentation.schemas import AnalysisResponse, HealthResponse
from app.modules.curriculum.presentation.dependencies import get_analyze_use_case, get_history_use_case
from app.modules.curriculum.application.use_cases import AnalyzeCurriculaUseCase, GetAnalysisHistoryUseCase
from app.core.security import validate_files
from datetime import datetime

router = APIRouter(prefix="/api/v1")
misc = APIRouter(prefix="/api/v1")

@misc.get("/health", response_model=HealthResponse, include_in_schema=False)
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
    query: Optional[str] = Form(None, description="Pergunta opcional para análise específica"),
    request_id: str = Form(..., description="ID único da requisição"),
    user_id: str = Form(..., description="ID do usuário solicitante"),
    use_case: AnalyzeCurriculaUseCase = Depends(get_analyze_use_case)
):
    """
    Analisa currículos usando OCR e LLM para extrair informações e comparar candidatos.
    
    **Parâmetros:**
    - **files**: Lista de arquivos (PDF, JPG, PNG) - obrigatório
    - **query**: Pergunta opcional para análise específica. Se não informada, retorna resumo individual de cada currículo
    - **request_id**: ID único da requisição - obrigatório
    - **user_id**: ID do usuário solicitante - obrigatório
    
    **Tipos de Análise:**
    
    1. **Análise com Query Específica**: Quando uma pergunta é fornecida, o sistema compara os candidatos
       baseado na pergunta específica e retorna rankings, scores de compatibilidade e recomendações.
    
    2. **Resumo Individual**: Quando nenhuma pergunta é fornecida, o sistema gera resumos individuais
       detalhados de cada currículo com informações estruturadas.
    
    
    **Resposta Exemplo da pergunta: Qual desses Candidatos é o melhor para a vaga de desenvolvedor backend ia**
    ```json
    {
      "code": 200,
      "status": "success",
      "request_id": "256dbf8d-4cd1-4664-b25c-c466fd458eab",
      "user_id": "irineutech2025@gmail.com",
      "files_processed": 2,
      "processing_time_seconds": 7.745771408081055,
      "result": {
        "type": "query_analysis",
        "query": "Qual desses Candidatos é o melhor para a vaga de desenvolvedor backend ia",
        "analysis": {
          "query": "Qual desses Candidatos é o melhor para a vaga de desenvolvedor backend ia",
          "best_candidates": [
            {
              "name": "Irineu Brito",
              "filename": "cv-irineu-brito.pdf",
              "skills": ["Python", "Node.js", "NestJS", "Machine Learning", "Inteligência Artificial"],
              "experience_years": 3,
              "relevant_experience": "Desenvolvimento de ferramentas internas usando IA...",
              "strengths": ["Experiência robusta em IA e desenvolvimento backend"],
              "weaknesses": [],
              "match_score": 95
            }
          ],
          "total_candidates_analyzed": 2,
          "summary": "Entre os candidatos analisados, Irineu Brito se destaca...",
          "recommendations": ["Priorizar Irineu para uma entrevista..."],
          "next_steps": ["Agendar entrevistas com os candidatos selecionados..."]
        },
        "files_analyzed": ["cv2.jpg", "cv-irineu-brito.pdf"]
      },
      "message": "Análise concluída com sucesso!"
    }
    ```
    
    **Notas:**
    - O sistema suporta múltiplos formatos de arquivo (PDF, JPG, PNG)
    - O tempo de processamento varia conforme o número e tamanho dos arquivos
    - Todos os arquivos são processados usando OCR antes da análise por LLM
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
