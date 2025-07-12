from pydantic_settings import BaseSettings
from typing import Set

class Settings(BaseSettings):
    # App
    app_name: str = "Smart Resume Analyzer"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # DynamoDB
    aws_access_key_id: str = "local"
    aws_secret_access_key: str = "local"
    aws_default_region: str = "us-east-1"
    dynamodb_endpoint_url: str = "http://localhost:8000"
    dynamodb_table_name: str = "cv_analysis_logs"
    
    # OCR
    ocr_provider: str = "easyocr"
    ocr_languages: str = "pt,en"
    
    # LLM
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    
    # Security
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: Set[str] = {'.pdf', '.jpg', '.jpeg', '.png'}
    max_files_per_request: int = 10
    
    class Config:
        env_file = ".env"

settings = Settings()