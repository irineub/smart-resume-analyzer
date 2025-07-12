from pydantic_settings import BaseSettings
from typing import Set
import os

class Settings(BaseSettings):
    # App
    app_name: str = "Curriculum Vitae Query Assistant"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # DynamoDB
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "local")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "local")
    aws_default_region: str = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    dynamodb_endpoint_url: str = os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8000")
    dynamodb_table_name: str = os.getenv("DYNAMODB_TABLE_NAME", "cv_analysis_logs")
    
    # OCR
    ocr_provider: str = os.getenv("OCR_PROVIDER", "tesseract")
    ocr_languages: str = os.getenv("OCR_LANGUAGES", "por+eng")
    
    # LLM
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    openai_max_tokens: int = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
    openai_temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # Security
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: Set[str] = {'.pdf', '.jpg', '.jpeg', '.png'}
    max_files_per_request: int = 10
    
    class Config:
        env_file = ".env"

settings = Settings()
