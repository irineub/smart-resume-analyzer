from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class AnalysisLog(BaseModel):
    """Modelo para log de análise no DynamoDB"""
    request_id: str
    user_id: str
    timestamp: datetime = datetime.utcnow()
    query: Optional[str] = None
    files_count: int
    file_names: list[str]
    result: Dict[str, Any]
    processing_time: float
    status: str = "completed"
