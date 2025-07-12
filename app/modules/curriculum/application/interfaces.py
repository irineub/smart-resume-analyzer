from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from app.modules.curriculum.domain.entities import CurriculumAnalysis

class AnalysisRepository(ABC):
    """Interface para repositório de análises"""
    
    @abstractmethod
    async def save(self, analysis: CurriculumAnalysis) -> None:
        """Salva uma análise"""
        pass
    
    @abstractmethod
    async def get_by_request_id(self, request_id: str) -> Optional[CurriculumAnalysis]:
        """Busca análise por request_id"""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: str, limit: int = 10) -> List[CurriculumAnalysis]:
        """Busca análises por user_id"""
        pass
