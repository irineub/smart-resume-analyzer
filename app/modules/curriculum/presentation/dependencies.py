from fastapi import Depends
from app.modules.curriculum.infrastructure.repositories import DynamoDBAnalysisRepository
from app.modules.curriculum.domain.services import OCRService, LLMService, LogService
from app.modules.curriculum.application.use_cases import AnalyzeCurriculaUseCase, GetAnalysisHistoryUseCase
import aioboto3
from app.core.config import settings
import asyncio
import openai
import instructor
from typing import Dict, List
from app.modules.curriculum.domain.models import QueryAnalysisResponse, SummaryResponse, ResumeSummary
import json
from decimal import Decimal

class TesseractOCRService(OCRService):
    """Implementação do OCR usando Tesseract"""
    
    def __init__(self):
        import fitz
        import pytesseract
        from PIL import Image
        import io
        
        self.fitz = fitz
        self.pytesseract = pytesseract
        self.Image = Image
        self.io = io
        self.languages = 'por+eng'
    
    async def extract_text_from_files(self, files):
        """Extrai texto de múltiplos arquivos"""
        file_texts = {}
        
        for file in files:
            try:
                content = await file.read()
                text = await self._extract_text_from_content(content, file.filename)
                file_texts[file.filename] = text
            except Exception as e:
                file_texts[file.filename] = f"Erro ao processar arquivo: {str(e)}"
        
        return file_texts
    
    async def _extract_text_from_content(self, content, filename):
        """Extrai texto baseado no tipo de arquivo"""
        if filename.lower().endswith('.pdf'):
            return self._extract_from_pdf(content)
        else:
            return self._extract_from_image(content)
    
    def _extract_from_pdf(self, content):
        """Extrai texto de PDF"""
        try:
            doc = self.fitz.open(stream=content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            return f"Erro ao processar PDF: {str(e)}"
    
    def _extract_from_image(self, content):
        """Extrai texto de imagem"""
        try:
            image = self.Image.open(self.io.BytesIO(content))
            text = self.pytesseract.image_to_string(image, lang=self.languages)
            return text.strip()
        except Exception as e:
            return f"Erro ao processar imagem: {str(e)}"

class InstructorLLMService(LLMService):
    """Implementação do LLM usando instructor para respostas estruturadas"""
    
    def __init__(self):
        self.client = None
        self.use_instructor = False
        
        try:
            if settings.openai_api_key:
                openai_client = openai.OpenAI(api_key=settings.openai_api_key)
                self.client = instructor.from_openai(
                    openai_client,
                    mode=instructor.Mode.JSON,
                )
                self.use_instructor = True
                print("✅ Instructor LLM configurado com sucesso!")
            else:
                print("⚠️ OpenAI API key não configurada. Usando análise simples...")
        except Exception as e:
            print(f"⚠️ Erro ao configurar Instructor LLM: {e}")
            print("🔄 Usando fallback para análise simples...")
    
    async def analyze_with_query(self, file_texts, query):
        """Análise com instructor baseada em query específica"""
        all_text = "\n\n".join([
            f"=== {filename} ===\n{text}" 
            for filename, text in file_texts.items()
        ])
        
        if self.use_instructor and self.client:
            analysis = await self._analyze_with_instructor(all_text, query, file_texts)
        else:
            analysis = self._simple_text_analysis(all_text, query)
        
        return {
            "type": "query_analysis",
            "query": query,
            "analysis": analysis,
            "files_analyzed": list(file_texts.keys())
        }
    
    async def generate_individual_summaries(self, file_texts):
        """Gera resumo individual de cada currículo usando instructor"""
        summaries = {}
        
        for filename, text in file_texts.items():
            try:
                if self.use_instructor and self.client:
                    summary = await self._generate_instructor_summary(text, filename)
                else:
                    summary = self._generate_simple_summary(text)
                summaries[filename] = summary
            except Exception as e:
                summaries[filename] = f"Erro ao gerar resumo: {str(e)}"
        
        return {
            "type": "individual_summaries",
            "summaries": summaries
        }
    
    async def _analyze_with_instructor(self, text, query, file_texts):
        """Análise usando instructor"""
        try:
            prompt = f"""
            Você é um assistente especializado em recrutamento e seleção.
            
            ANALISE OS CURRÍCULOS FORNECIDOS E RESPONDA À PERGUNTA DO RECRUTADOR.
            
            PERGUNTA DO RECRUTADOR: {query}
            
            CURRÍCULOS ANALISADOS:
            {text[:4000]}
            
            INSTRUÇÕES IMPORTANTES:
            1. Analise APENAS o conteúdo real dos currículos fornecidos
            2. NÃO invente informações que não estão nos currículos
            3. Se não houver informações suficientes, seja honesto sobre isso
            4. Foque na pergunta específica do recrutador
            5. Forneça justificativas baseadas no conteúdo real
            6. Seja direto e objetivo na resposta
            
            IMPORTANTE: Baseie sua análise APENAS no conteúdo real dos currículos fornecidos.
            """
            
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                response_model=QueryAnalysisResponse,
                max_retries=3,
                timeout=60.0
            )
            
            return response.model_dump()
            
        except Exception as e:
            return f"Erro na análise Instructor: {str(e)}. Usando análise simples..."
    
    async def _generate_instructor_summary(self, text, filename):
        """Gera resumo usando instructor"""
        try:
            if len(text) < 100:
                return text
            
            prompt = f"""
            Você é um assistente de recrutamento especializado em resumir currículos.
            
            GERE UM RESUMO ESTRUTURADO DO CURRÍCULO FORNECIDO.
            
            CURRÍCULO: {text[:3000]}
            
            INSTRUÇÕES:
            1. Extraia as informações mais relevantes
            2. Identifique nome, habilidades, experiência e formação
            3. Seja conciso mas informativo
            4. Use linguagem profissional
            5. Estruture conforme o modelo ResumeSummary
            
            IMPORTANTE: Estruture a resposta conforme o modelo ResumeSummary.
            """
            
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                response_model=ResumeSummary,
                max_retries=3,
                timeout=30.0
            )
            
            return response.model_dump()
            
        except Exception as e:
            return f"Erro ao gerar resumo Instructor: {str(e)}"
    
    def _simple_text_analysis(self, text, query):
        """Análise simples baseada em palavras-chave (fallback)"""
        query_lower = query.lower()
        text_lower = text.lower()
        
        keywords = {
            'python': ['python', 'django', 'flask', 'fastapi'],
            'java': ['java', 'spring', 'hibernate'],
            'javascript': ['javascript', 'react', 'vue', 'angular', 'node.js'],
            'frontend': ['html', 'css', 'react', 'vue', 'angular'],
            'backend': ['python', 'java', 'node.js', 'php', 'c#'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
            'mobile': ['android', 'ios', 'react native', 'flutter'],
            'ai': ['machine learning', 'ai', 'artificial intelligence', 'tensorflow', 'pytorch'],
            'devops': ['docker', 'kubernetes', 'jenkins', 'gitlab', 'ci/cd']
        }
        
        matches = {}
        for category, words in keywords.items():
            count = sum(1 for word in words if word in text_lower)
            if count > 0:
                matches[category] = count
        
        analysis = f"Análise baseada na query: '{query}'\n\n"
        analysis += "Habilidades encontradas:\n"
        
        for category, count in matches.items():
            analysis += f"- {category.title()}: {count} habilidades\n"
        
        if not matches:
            analysis += "- Nenhuma habilidade específica encontrada\n"
        
        analysis += f"\nResumo: O texto contém {len(text.split())} palavras e "
        analysis += f"{len(matches)} categorias de habilidades identificadas."
        
        return analysis
    
    def _generate_simple_summary(self, text):
        """Gera resumo simples do texto (fallback)"""
        if len(text) < 100:
            return text
        
        import re
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        summary_sentences = []
        for sentence in sentences[:5]:
            if len(sentence) > 20:
                summary_sentences.append(sentence)
                if len(summary_sentences) >= 3:
                    break
        
        summary = ". ".join(summary_sentences)
        if summary:
            summary += "."
        
        return summary if summary else text[:200] + "..."

class DynamoDBLogService(LogService):
    """Implementação do log usando DynamoDB"""
    
    def __init__(self):
        self.session = aioboto3.Session()
        self.table_name = settings.dynamodb_table_name
    
    async def save_log(self, analysis_data):
        """Salva log no DynamoDB"""
        try:
            async with self.session.resource(
                'dynamodb',
                endpoint_url=settings.dynamodb_endpoint_url,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_default_region
            ) as dynamodb:
                table = await dynamodb.Table(self.table_name)
                
                if 'processing_time' in analysis_data:
                    analysis_data['processing_time'] = str(analysis_data['processing_time'])
                
                if 'result' in analysis_data and isinstance(analysis_data['result'], dict):
                    analysis_data['result'] = json.dumps(analysis_data['result'])
                
                if 'timestamp' in analysis_data:
                    analysis_data['timestamp'] = str(analysis_data['timestamp'])
                
                if 'processing_time' in analysis_data and isinstance(analysis_data['processing_time'], str):
                    analysis_data['processing_time'] = Decimal(analysis_data['processing_time'])
                
                await table.put_item(Item=analysis_data)
                print(f"Log salvo no DynamoDB: {analysis_data.get('request_id')}")
        except Exception as e:
            print(f"Erro ao salvar log: {e}")
    
    async def get_logs_by_user(self, user_id, limit=10):
        """Busca logs de um usuário específico"""
        try:
            async with self.session.resource(
                'dynamodb',
                endpoint_url=settings.dynamodb_endpoint_url,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_default_region
            ) as dynamodb:
                table = await dynamodb.Table(self.table_name)
                response = await table.query(
                    IndexName='user_id-timestamp-index',
                    KeyConditionExpression='user_id = :user_id',
                    ExpressionAttributeValues={':user_id': user_id},
                    ScanIndexForward=False,
                    Limit=limit
                )
                return response.get('Items', [])
        except Exception as e:
            print(f"Erro ao buscar logs: {e}")
            return []

# Dependências
def get_ocr_service() -> OCRService:
    return TesseractOCRService()

def get_llm_service() -> LLMService:
    return InstructorLLMService()

def get_log_service() -> LogService:
    return DynamoDBLogService()

def get_repository() -> DynamoDBAnalysisRepository:
    return DynamoDBAnalysisRepository()

def get_analyze_use_case(
    ocr_service: OCRService = Depends(get_ocr_service),
    llm_service: LLMService = Depends(get_llm_service),
    log_service: LogService = Depends(get_log_service),
    repository: DynamoDBAnalysisRepository = Depends(get_repository)
) -> AnalyzeCurriculaUseCase:
    return AnalyzeCurriculaUseCase(ocr_service, llm_service, log_service, repository)

def get_history_use_case(
    repository: DynamoDBAnalysisRepository = Depends(get_repository)
) -> GetAnalysisHistoryUseCase:
    return GetAnalysisHistoryUseCase(repository)
