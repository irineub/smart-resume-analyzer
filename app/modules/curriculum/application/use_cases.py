import time
from typing import List, Optional, Dict
from fastapi import UploadFile
from app.modules.curriculum.domain.entities import CurriculumAnalysis, AnalysisResult
from app.modules.curriculum.domain.services import OCRService, LLMService, LogService
from app.modules.curriculum.application.interfaces import AnalysisRepository
from app.core.logging import log_analysis_request, log_error

class AnalyzeCurriculaUseCase:
    """Caso de uso para análise de currículos"""
    
    def __init__(
        self,
        ocr_service: OCRService,
        llm_service: LLMService,
        log_service: LogService,
        repository: AnalysisRepository
    ):
        self.ocr_service = ocr_service
        self.llm_service = llm_service
        self.log_service = log_service
        self.repository = repository
    
    async def execute(
        self,
        files: List[UploadFile],
        query: Optional[str],
        request_id: str,
        user_id: str
    ) -> Dict:
        """Executa a análise de currículos"""
        
        start_time = time.time()
        
        try:
            file_texts = await self.ocr_service.extract_text_from_files(files)
            
            if query:
                result = await self.llm_service.analyze_with_query(file_texts, query)
            else:
                result = await self.llm_service.generate_individual_summaries(file_texts)
            
            processing_time = time.time() - start_time
            
            analysis = CurriculumAnalysis(
                request_id=request_id,
                user_id=user_id,
                timestamp=time.time(),
                query=query,
                files_count=len(files),
                file_names=[f.filename for f in files],
                result=result,
                processing_time=processing_time
            )
            
            await self.repository.save(analysis)
            
            await self.log_service.save_log(analysis.__dict__)
            
            log_analysis_request(
                request_id=request_id,
                user_id=user_id,
                files_count=len(files),
                query=query,
                processing_time=processing_time
            )
            
            return {
                "code": 200,
                "status": "success",
                "request_id": request_id,
                "user_id": user_id,
                "files_processed": len(files),
                "processing_time_seconds": processing_time,
                "result": result,
                "message": "Análise concluída com sucesso!"
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            log_error(e, {
                "request_id": request_id,
                "user_id": user_id,
                "files_count": len(files),
                "query": query,
                "processing_time": processing_time
            })
            
            error_analysis = CurriculumAnalysis(
                request_id=request_id,
                user_id=user_id,
                timestamp=time.time(),
                query=query,
                files_count=len(files),
                file_names=[f.filename for f in files],
                result={"error": str(e)},
                processing_time=processing_time,
                status="error"
            )
            
            await self.repository.save(error_analysis)
            await self.log_service.save_log(error_analysis.__dict__)
            
            raise e

class GetAnalysisHistoryUseCase:
    """Caso de uso para buscar histórico de análises"""
    
    def __init__(self, repository: AnalysisRepository):
        self.repository = repository
    
    async def execute(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Executa a busca do histórico"""
        analyses = await self.repository.get_by_user_id(user_id, limit)
        return [analysis.__dict__ for analysis in analyses]
