from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class CandidateAnalysis(BaseModel):
    """Análise de um candidato específico"""
    name: str = Field(description="Nome do candidato")
    filename: str = Field(description="Nome do arquivo do currículo")
    skills: List[str] = Field(description="Habilidades encontradas")
    experience_years: Optional[int] = Field(description="Anos de experiência", default=None)
    relevant_experience: str = Field(description="Experiência relevante para a vaga")
    strengths: List[str] = Field(description="Pontos fortes do candidato")
    weaknesses: List[str] = Field(description="Pontos de melhoria")
    match_score: float = Field(description="Score de adequação (0-100)", ge=0, le=100)

class QueryAnalysisResponse(BaseModel):
    """Resposta estruturada para análise com query"""
    query: str = Field(description="Query original do recrutador")
    best_candidates: List[CandidateAnalysis] = Field(description="Candidatos mais adequados")
    total_candidates_analyzed: int = Field(description="Total de candidatos analisados")
    summary: str = Field(description="Resumo geral da análise")
    recommendations: List[str] = Field(description="Recomendações para o recrutador")
    next_steps: List[str] = Field(description="Próximos passos sugeridos")

class ResumeSummary(BaseModel):
    """Resumo estruturado de um currículo"""
    filename: str = Field(description="Nome do arquivo")
    candidate_name: Optional[str] = Field(description="Nome do candidato", default=None)
    summary: str = Field(description="Resumo do currículo")
    key_skills: List[str] = Field(description="Principais habilidades")
    experience_highlights: List[str] = Field(description="Destaques da experiência")
    education: Optional[str] = Field(description="Formação acadêmica", default=None)
    contact_info: Optional[str] = Field(description="Informações de contato", default=None)

class SummaryResponse(BaseModel):
    """Resposta estruturada para resumos automáticos"""
    summaries: List[ResumeSummary] = Field(description="Resumos dos currículos")
    total_files: int = Field(description="Total de arquivos processados")
    processing_time: float = Field(description="Tempo de processamento em segundos") 