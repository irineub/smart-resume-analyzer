import uuid
from datetime import datetime

def generate_request_id() -> str:
    """Gera ID único para requisição"""
    return str(uuid.uuid4())

def format_timestamp() -> str:
    """Formata timestamp atual"""
    return datetime.utcnow().isoformat()