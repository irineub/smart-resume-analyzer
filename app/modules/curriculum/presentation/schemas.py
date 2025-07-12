from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class AnalysisRequest(BaseModel):
    """Schema para requisição de análise"""
    query: Optional[str] = None
    request_id: str
    user_id: str

class AnalysisResponse(BaseModel):
    """Schema para resposta de análise"""
    code: int
    status: str
    request_id: str
    user_id: str
    files_processed: int
    processing_time_seconds: float
    result: Dict[str, Any]
    message: str

class AnalysisHistoryResponse(BaseModel):
    """Schema para resposta do histórico"""
    user_id: str
    history: List[Dict[str, Any]]
    total: int

class HealthResponse(BaseModel):
    """Schema para health check"""
    status: str
    service: Optional[str] = "Curriculum Analysis API"
    version: str
    timestamp: datetime
    services: Optional[Dict[str, str]] = None
