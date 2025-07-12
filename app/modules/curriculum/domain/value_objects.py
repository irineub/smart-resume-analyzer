from dataclasses import dataclass
from typing import Set
from enum import Enum

class AnalysisType(Enum):
    """Tipos de análise"""
    QUERY_ANALYSIS = "query_analysis"
    INDIVIDUAL_SUMMARIES = "individual_summaries"

class FileType(Enum):
    """Tipos de arquivo suportados"""
    PDF = "pdf"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"

@dataclass(frozen=True)
class SupportedExtensions:
    """Extensões de arquivo suportadas"""
    extensions: Set[str] = frozenset({'.pdf', '.jpg', '.jpeg', '.png'})
    
    def is_supported(self, filename: str) -> bool:
        """Verifica se o arquivo é suportado"""
        return any(filename.lower().endswith(ext) for ext in self.extensions)

@dataclass(frozen=True)
class FileSizeLimit:
    """Limite de tamanho de arquivo"""
    max_size_bytes: int = 10 * 1024 * 1024  # 10MB
    
    def is_within_limit(self, size_bytes: int) -> bool:
        """Verifica se o tamanho está dentro do limite"""
        return size_bytes <= self.max_size_bytes
