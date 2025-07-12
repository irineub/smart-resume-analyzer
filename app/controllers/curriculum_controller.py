from app.services.ocr_service import OCRService
from app.services.llm_service import LLMService
from app.services.log_service import LogService
from app.utils.validators import validate_files
from app.models.analysis_log import AnalysisLog
import time
from typing import List, Optional
from fastapi import UploadFile

class CurriculumController:
    def __init__(self):
        self.ocr_service = OCRService()
        self.llm_service = LLMService()
        self.log_service = LogService()
        self._init_dynamodb()
    
    async def _init_dynamodb(self):
        """Inicializa a tabela DynamoDB"""
        try:
            await self.log_service.create_table_if_not_exists()
        except Exception as e:
            print(f"Aviso: Não foi possível inicializar DynamoDB: {e}")
    
    async def analyze_curricula(
        self, 
        files: List[UploadFile], 
        query: Optional[str], 
        request_id: str, 
        user_id: str
    ):
        """Controla o fluxo de análise de currículos para o Fabio"""
        
        start_time = time.time()
        
        try:
            validate_files(files)
            
            file_texts = await self.ocr_service.extract_text_from_files(files)
            
            if query:
                result = await self.llm_service.analyze_with_query(file_texts, query)
            else:
                result = await self.llm_service.generate_individual_summaries(file_texts)
            
            processing_time = time.time() - start_time
            
            log_entry = AnalysisLog(
                request_id=request_id,
                user_id=user_id,
                query=query,
                files_count=len(files),
                file_names=[f.filename for f in files],
                result=result,
                processing_time=processing_time
            )
            await self.log_service.save_log(log_entry)
            
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
            error_log = AnalysisLog(
                request_id=request_id,
                user_id=user_id,
                query=query,
                files_count=len(files),
                file_names=[f.filename for f in files],
                result={"error": str(e)},
                processing_time=time.time() - start_time,
                status="error"
            )
            await self.log_service.save_log(error_log)
            raise e
 