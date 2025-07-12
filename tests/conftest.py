import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
import tempfile
import os
from io import BytesIO
from PIL import Image
import fitz 

from app.app import create_app
from app.modules.curriculum.domain.entities import CurriculumAnalysis
from app.modules.curriculum.application.use_cases import AnalyzeCurriculaUseCase, GetAnalysisHistoryUseCase
from app.services.ocr_service import OCRService
from app.services.llm_service import LLMService
from app.services.log_service import LogService
from app.modules.curriculum.infrastructure.repositories import DynamoDBAnalysisRepository


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def app():
    """Create a test instance of the FastAPI app."""
    return create_app()


@pytest.fixture
def client(app):
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_ocr_service():
    """Mock OCR service for testing."""
    mock = Mock(spec=OCRService)
    mock.extract_text_from_files = AsyncMock(return_value={
        "cv1.pdf": "João Silva\nDesenvolvedor Python\n5 anos de experiência",
        "cv2.jpg": "Maria Santos\nEngenheira de Software\n3 anos de experiência"
    })
    return mock


@pytest.fixture
def mock_llm_service():
    """Mock LLM service for testing."""
    mock = Mock(spec=LLMService)
    mock.analyze_with_query = AsyncMock(return_value={
        "type": "query_analysis",
        "query": "Qual candidato tem mais experiência?",
        "analysis": "João Silva tem mais experiência (5 anos vs 3 anos)",
        "files_analyzed": ["cv1.pdf", "cv2.jpg"]
    })
    mock.generate_individual_summaries = AsyncMock(return_value={
        "type": "individual_summaries",
        "summaries": {
            "cv1.pdf": "João Silva - Desenvolvedor Python com 5 anos de experiência",
            "cv2.jpg": "Maria Santos - Engenheira de Software com 3 anos de experiência"
        }
    })
    return mock


@pytest.fixture
def mock_log_service():
    """Mock log service for testing."""
    mock = Mock(spec=LogService)
    mock.save_log = AsyncMock()
    mock.get_logs_by_user = AsyncMock(return_value=[])
    return mock


@pytest.fixture
def mock_repository():
    """Mock repository for testing."""
    mock = Mock(spec=DynamoDBAnalysisRepository)
    mock.save = AsyncMock()
    mock.get_by_request_id = AsyncMock(return_value=None)
    mock.get_by_user_id = AsyncMock(return_value=[])
    return mock


@pytest.fixture
def sample_curriculum_analysis():
    """Sample curriculum analysis for testing."""
    return CurriculumAnalysis(
        request_id="test-request-123",
        user_id="test-user@example.com",
        timestamp=1234567890.0,
        query="Qual candidato tem mais experiência?",
        files_count=2,
        file_names=["cv1.pdf", "cv2.jpg"],
        result={
            "type": "query_analysis",
            "query": "Qual candidato tem mais experiência?",
            "analysis": "João Silva tem mais experiência",
            "files_analyzed": ["cv1.pdf", "cv2.jpg"]
        },
        processing_time=2.5,
        status="success"
    )


@pytest.fixture
def sample_pdf_file():
    """Create a sample PDF file for testing."""
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "João Silva\nDesenvolvedor Python\n5 anos de experiência")
    doc.save("tests/sample_cv.pdf")
    doc.close()
    
    with open("tests/sample_cv.pdf", "rb") as f:
        content = f.read()
    
    yield content
    
    if os.path.exists("tests/sample_cv.pdf"):
        os.remove("tests/sample_cv.pdf")


@pytest.fixture
def sample_image_file():
    """Create a sample image file for testing."""
    img = Image.new('RGB', (400, 200), color='white')
    img.save("tests/sample_cv.jpg")
    
    with open("tests/sample_cv.jpg", "rb") as f:
        content = f.read()
    
    yield content
    
    if os.path.exists("tests/sample_cv.jpg"):
        os.remove("tests/sample_cv.jpg")


@pytest.fixture
def mock_upload_file():
    """Mock upload file for testing."""
    class MockUploadFile:
        def __init__(self, filename, content):
            self.filename = filename
            self.content = content
            self.size = len(content)
        
        async def read(self):
            return self.content
    
    return MockUploadFile


@pytest.fixture
def test_settings():
    """Test settings for the application."""
    return {
        "app_name": "Test Curriculum Analyzer",
        "app_version": "1.0.0",
        "debug": True,
        "max_file_size": 10 * 1024 * 1024,  # 10MB
        "allowed_extensions": {'.pdf', '.jpg', '.jpeg', '.png'},
        "max_files_per_request": 10
    } 