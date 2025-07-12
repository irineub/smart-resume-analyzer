from pydantic import BaseModel
from typing import List

class FileInfo(BaseModel):
    """Informações dos arquivos"""
    filename: str
    content_type: str
    size: int
    extension: str