from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class AnalysisType(str, Enum):
    """Tipos de análise disponíveis"""
    QUERY_ANALYSIS = "query_analysis"
    INDIVIDUAL_SUMMARIES = "individual_summaries"

class CandidateInfo(BaseModel):
    """Informações detalhadas de um candidato"""
    name: str = Field(..., description="Nome do candidato")
    filename: str = Field(..., description="Nome do arquivo original")
    skills: List[str] = Field(..., description="Lista de habilidades identificadas")
    experience_years: int = Field(..., description="Anos de experiência")
    relevant_experience: str = Field(..., description="Descrição da experiência relevante")
    strengths: List[str] = Field(..., description="Pontos fortes do candidato")
    weaknesses: List[str] = Field(..., description="Pontos fracos do candidato")
    match_score: int = Field(..., description="Score de compatibilidade (0-100)")

class AnalysisSummary(BaseModel):
    """Resumo da análise comparativa"""
    query: str = Field(..., description="Query original utilizada")
    best_candidates: List[CandidateInfo] = Field(..., description="Lista dos melhores candidatos")
    total_candidates_analyzed: int = Field(..., description="Total de candidatos analisados")
    summary: str = Field(..., description="Resumo geral da análise")
    recommendations: List[str] = Field(..., description="Recomendações baseadas na análise")
    next_steps: List[str] = Field(..., description="Próximos passos sugeridos")

class IndividualSummary(BaseModel):
    """Resumo individual de um currículo"""
    filename: str = Field(..., description="Nome do arquivo original")
    candidate_name: str = Field(..., description="Nome do candidato")
    summary: str = Field(..., description="Resumo geral do perfil")
    key_skills: List[str] = Field(..., description="Principais habilidades identificadas")
    experience_highlights: List[str] = Field(..., description="Destaques da experiência profissional")
    education: str = Field(..., description="Informações educacionais")
    contact_info: str = Field(..., description="Informações de contato")

class QueryAnalysisResult(BaseModel):
    """Resultado de análise com query específica"""
    type: AnalysisType = Field(AnalysisType.QUERY_ANALYSIS, description="Tipo de análise")
    query: str = Field(..., description="Query utilizada na análise")
    analysis: AnalysisSummary = Field(..., description="Análise detalhada dos candidatos")
    files_analyzed: List[str] = Field(..., description="Lista de arquivos analisados")

class IndividualSummariesResult(BaseModel):
    """Resultado de resumos individuais"""
    type: AnalysisType = Field(AnalysisType.INDIVIDUAL_SUMMARIES, description="Tipo de análise")
    summaries: Dict[str, IndividualSummary] = Field(..., description="Resumos individuais por arquivo")

class AnalysisRequest(BaseModel):
    """Schema para requisição de análise"""
    query: Optional[str] = Field(None, description="Pergunta opcional para análise específica")
    request_id: str = Field(..., description="ID único da requisição")
    user_id: str = Field(..., description="ID do usuário solicitante")

class AnalysisResponse(BaseModel):
    """Schema para resposta de análise de currículos"""
    code: int = Field(200, description="Código de status HTTP")
    status: str = Field("success", description="Status da operação")
    request_id: str = Field(..., description="ID único da requisição")
    user_id: str = Field(..., description="ID do usuário solicitante")
    files_processed: int = Field(..., description="Número de arquivos processados")
    processing_time_seconds: float = Field(..., description="Tempo de processamento em segundos")
    result: Union[QueryAnalysisResult, IndividualSummariesResult] = Field(..., description="Resultado da análise")
    message: str = Field(..., description="Mensagem de status da operação")

    class Config:
        schema_extra = {
            "example": {
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
                                "relevant_experience": "Desenvolvimento de ferramentas internas usando IA, criação de sistemas avançados de agentes de IA",
                                "strengths": ["Experiência robusta em IA e desenvolvimento backend", "Fluente em inglês"],
                                "weaknesses": [],
                                "match_score": 95
                            }
                        ],
                        "total_candidates_analyzed": 2,
                        "summary": "Entre os candidatos analisados, Irineu Brito se destaca por sua extensa experiência em desenvolvimento backend e inteligência artificial",
                        "recommendations": ["Priorizar Irineu para uma entrevista, dada sua experiência em inteligência artificial"],
                        "next_steps": ["Agendar entrevistas com os candidatos selecionados"]
                    },
                    "files_analyzed": ["cv2.jpg", "cv-irineu-brito.pdf"]
                },
                "message": "Análise concluída com sucesso!"
            }
        }

class AnalysisHistoryResponse(BaseModel):
    """Schema para resposta do histórico"""
    user_id: str
    history: List[Dict[str, Any]]
    total: int

class HealthResponse(BaseModel):
    """Schema para health check da API"""
    status: str = Field(..., description="Status do serviço")
    timestamp: datetime = Field(..., description="Timestamp da verificação")
    version: str = Field(..., description="Versão da API")
    services: Dict[str, str] = Field(..., description="Status dos serviços dependentes")

    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T10:30:00.000Z",
                "version": "1.0.0",
                "services": {
                    "ocr": "tesseract",
                    "llm": "openai",
                    "database": "dynamodb"
                }
            }
        }

class ValidationErrorDetail(BaseModel):
    loc: List[Union[str, int]] = Field(..., example=["body", "files"])
    msg: str = Field(..., example="field required")
    type: str = Field(..., example="value_error.missing")

class ValidationError(BaseModel):
    detail: List[ValidationErrorDetail]

    class Config:
        schema_extra = {
            "example": {
                "detail": [
                    {
                        "loc": ["body", "files"],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ]
            }
        }

class ErrorResponse(BaseModel):
    code: int = Field(..., example=400)
    status: str = Field(..., example="error")
    message: str = Field(..., example="Arquivo inválido ou parâmetros obrigatórios ausentes.")

    class Config:
        schema_extra = {
            "example": {
                "code": 400,
                "status": "error",
                "message": "Arquivo inválido ou parâmetros obrigatórios ausentes."
            }
        }
