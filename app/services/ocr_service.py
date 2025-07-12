import fitz  
from typing import List, Dict
from fastapi import UploadFile
import io
from PIL import Image
import pytesseract

class OCRService:
    def __init__(self):
        self.model_name = "tesseract"
        self.languages = 'por+eng'
    
    async def extract_text_from_files(self, files: List[UploadFile]) -> Dict[str, str]:
        """Extrai texto de múltiplos arquivos usando Tesseract"""
        file_texts = {}
        
        for file in files:
            try:
                content = await file.read()
                text = await self._extract_text_from_content(content, file.filename)
                file_texts[file.filename] = text
            except Exception as e:
                file_texts[file.filename] = f"Erro ao processar arquivo: {str(e)}"
        
        return file_texts
    
    async def _extract_text_from_content(self, content: bytes, filename: str) -> str:
        """Extrai texto baseado no tipo de arquivo"""
        if filename.lower().endswith('.pdf'):
            return self._extract_from_pdf(content)
        else:
            return self._extract_from_image(content)
    
    def _extract_from_pdf(self, content: bytes) -> str:
        """Extrai texto de PDF usando PyMuPDF"""
        try:
            doc = fitz.open(stream=content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            return f"Erro ao processar PDF: {str(e)}"
    
    def _extract_from_image(self, content: bytes) -> str:
        """Extrai texto de imagem usando Tesseract"""
        try:
            image = Image.open(io.BytesIO(content))
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(
                image, 
                lang=self.languages,
                config=custom_config
            )
            return text.strip()
        except Exception as e:
            return f"Erro ao processar imagem: {str(e)}"
