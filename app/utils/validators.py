from fastapi import UploadFile, HTTPException
from typing import List
from app.config import settings

def validate_files(files: List[UploadFile]):
    """Valida arquivos enviados pelo Fabio"""
    if not files:
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado")
    
    if len(files) > 10:  
        raise HTTPException(
            status_code=400, 
            detail="Máximo de 10 arquivos por requisição"
        )
    
    for file in files:
        if not any(file.filename.lower().endswith(ext) for ext in settings.allowed_extensions):
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de arquivo não suportado: {file.filename}. "
                       f"Tipos aceitos: {', '.join(settings.allowed_extensions)}"
            )
        
        if file.size and file.size > settings.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo muito grande: {file.filename}. "
                       f"Tamanho máximo: {settings.max_file_size // (1024*1024)}MB"
            )