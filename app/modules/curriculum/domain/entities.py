from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any

@dataclass
class CurriculumAnalysis:
    """Entidade principal para análise de currículos"""
    request_id: str
    user_id: str
    timestamp: datetime
    query: Optional[str]
    files_count: int
    file_names: List[str]
    result: Dict[str, Any]
    processing_time: float
    status: str = "completed"

@dataclass
class FileInfo:
    """Informações do arquivo"""
    filename: str
    content_type: str
    size: int
    extension: str
    is_valid: bool = True

@dataclass
class AnalysisResult:
    """Resultado da análise"""
    type: str
    analysis: str
    files_analyzed: List[str]
    processing_time: float
