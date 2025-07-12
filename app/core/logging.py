import logging
import json
from datetime import datetime
from typing import Any, Dict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def log_analysis_request(
    request_id: str,
    user_id: str,
    files_count: int,
    query: str = None,
    processing_time: float = None,
    status: str = "completed"
):
    """Log estruturado para requisições de análise"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": "INFO",
        "event": "curriculum_analysis_request",
        "request_id": request_id,
        "user_id": user_id,
        "files_count": files_count,
        "query": query,
        "processing_time_ms": processing_time * 1000 if processing_time else None,
        "status": status
    }
    
    logger.info(json.dumps(log_data))

def log_error(error: Exception, context: Dict[str, Any] = None):
    """Log estruturado para erros"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": "ERROR",
        "event": "error",
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context or {}
    }
    
    logger.error(json.dumps(log_data))
