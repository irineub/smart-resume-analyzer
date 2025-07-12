from transformers import pipeline
from typing import Dict, List
import asyncio

class LLMService:
    def __init__(self):
        self.model_name = "huggingface/summarization"
        self.summarizer = pipeline("summarization", model=self.model_name)
    
    async def analyze_with_query(self, file_texts: Dict[str, str], query: str) -> Dict:
        """Analisa currículos com query específica"""
        all_text = "\n\n".join([
            f"=== {filename} ===\n{text}" 
            for filename, text in file_texts.items()
        ])
        
        prompt = f"""
        Query do recrutador: {query}
        
        Currículos analisados:
        {all_text}
        
        Por favor, analise os currículos e responda à query do recrutador.
        Forneça uma resposta detalhada com justificativas baseadas no conteúdo dos currículos.
        """
        
        response = await self._process_with_llm(prompt)
        
        return {
            "type": "query_analysis",
            "query": query,
            "analysis": response,
            "files_analyzed": list(file_texts.keys())
        }
    
    async def generate_individual_summaries(self, file_texts: Dict[str, str]) -> Dict:
        """Gera resumo individual de cada currículo"""
        summaries = {}
        
        for filename, text in file_texts.items():
            try:
                summary = await self._summarize_text(text)
                summaries[filename] = summary
            except Exception as e:
                summaries[filename] = f"Erro ao gerar resumo: {str(e)}"
        
        return {
            "type": "individual_summaries",
            "summaries": summaries
        }
    
    async def _summarize_text(self, text: str) -> str:
        """Gera resumo do texto"""
        if len(text) < 100:
            return text
        
        chunks = self._split_text(text, max_length=1000)
        summaries = []
        
        for chunk in chunks:
            try:
                summary = self.summarizer(chunk, max_length=150, min_length=50)
                summaries.append(summary[0]['summary_text'])
            except Exception as e:
                summaries.append(f"Erro no chunk: {str(e)}")
        
        return "\n\n".join(summaries)
    
    async def _process_with_llm(self, prompt: str) -> str:
        """Processa prompt com LLM"""
        return f"Análise baseada na query: {prompt[:200]}... (implementação completa pendente)"
    
    def _split_text(self, text: str, max_length: int) -> List[str]:
        """Divide texto em chunks menores"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) > max_length:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks

