from abc import ABC, abstractmethod
from typing import Dict, List
from fastapi import UploadFile

class OCRService(ABC):
    """Interface para serviços OCR"""
    
    @abstractmethod
    async def extract_text_from_files(self, files: List[UploadFile]) -> Dict[str, str]:
        """Extrai texto de múltiplos arquivos"""
        pass

class LLMService(ABC):
    """Interface para serviços LLM"""
    
    @abstractmethod
    async def analyze_with_query(self, file_texts: Dict[str, str], query: str) -> Dict:
        """Analisa currículos com query específica"""
        pass
    
    @abstractmethod
    async def generate_individual_summaries(self, file_texts: Dict[str, str]) -> Dict:
        """Gera resumo individual de cada currículo"""
        pass

class LogService(ABC):
    """Interface para serviços de log"""
    
    @abstractmethod
    async def save_log(self, analysis_data: Dict) -> None:
        """Salva log da análise"""
        pass
    
    @abstractmethod
    async def get_logs_by_user(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Busca logs de um usuário específico"""
        pass
