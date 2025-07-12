import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi.testclient import TestClient
from PIL import Image
import io
from fastapi import status

from app.app import app
from app.modules.curriculum.presentation.dependencies import get_analyze_use_case, get_history_use_case

@pytest.fixture
def sample_pdf_content():
    # PDF-like bytes
    return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Test PDF Content) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF"

@pytest.fixture
def sample_image_content():
    img = Image.new('RGB', (100, 100), color='white')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.getvalue()


class TestAPIEndpoints:
    """Test cases for API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_health_check(self, client):
        """Test health check endpoint."""
        # Act
        response = client.get("/api/v1/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        assert "services" in data
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert "status" in data
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_analyze_curriculum_with_query_success(self, client, sample_pdf_content):
        """Test successful curriculum analysis with query."""
        # Arrange
        mock_use_case = Mock()
        mock_use_case.execute = AsyncMock(return_value={
            "code": 200,
            "status": "success",
            "request_id": "test-request-123",
            "user_id": "test-user@example.com",
            "files_processed": 1,
            "processing_time_seconds": 2.5,
            "result": {
                "type": "query_analysis",
                "query": "Qual candidato tem mais experiência?",
                "analysis": "João Silva tem mais experiência",
                "files_analyzed": ["cv1.pdf"]
            },
            "message": "Análise concluída com sucesso!"
        })
        
        # Override dependency
        app.dependency_overrides = {
            get_analyze_use_case: lambda: mock_use_case
        }
        
        try:
            # Act
            files = {"files": ("cv1.pdf", sample_pdf_content, "application/pdf")}
            data = {
                "query": "Qual candidato tem mais experiência?",
                "request_id": "test-request-123",
                "user_id": "test-user@example.com"
            }
            response = client.post("/api/v1/curriculum/", files=files, data=data)
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 200
            assert data["status"] == "success"
            assert data["request_id"] == "test-request-123"
            assert data["user_id"] == "test-user@example.com"
            assert data["files_processed"] == 1
            assert "processing_time_seconds" in data
            assert data["result"]["type"] == "query_analysis"
        finally:
            app.dependency_overrides = {}
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_analyze_curriculum_without_query_success(self, client, sample_pdf_content):
        """Test successful curriculum analysis without query."""
        # Arrange
        mock_use_case = Mock()
        mock_use_case.execute = AsyncMock(return_value={
            "code": 200,
            "status": "success",
            "request_id": "test-request-123",
            "user_id": "test-user@example.com",
            "files_processed": 1,
            "processing_time_seconds": 2.5,
            "result": {
                "type": "individual_summaries",
                "summaries": {
                    "cv1.pdf": "João Silva - Desenvolvedor Python com 5 anos de experiência"
                }
            },
            "message": "Análise concluída com sucesso!"
        })
        
        # Override dependency
        app.dependency_overrides = {
            get_analyze_use_case: lambda: mock_use_case
        }
        
        try:
            # Act
            files = {"files": ("cv1.pdf", sample_pdf_content, "application/pdf")}
            data = {
                "request_id": "test-request-123",
                "user_id": "test-user@example.com"
            }
            response = client.post("/api/v1/curriculum/", files=files, data=data)
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 200
            assert data["status"] == "success"
            assert data["result"]["type"] == "individual_summaries"
        finally:
            app.dependency_overrides = {}
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_analyze_curriculum_error(self, client, sample_pdf_content):
        """Test curriculum analysis error handling."""
        # Arrange
        mock_use_case = Mock()
        mock_use_case.execute = AsyncMock(side_effect=Exception("Processing error"))
        
        # Override dependency
        app.dependency_overrides = {
            get_analyze_use_case: lambda: mock_use_case
        }
        
        try:
            # Act
            files = {"files": ("cv1.pdf", sample_pdf_content, "application/pdf")}
            data = {
                "query": "Test query",
                "request_id": "test-request-123",
                "user_id": "test-user@example.com"
            }
            response = client.post("/api/v1/curriculum/", files=files, data=data)
            
            # Assert
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
            assert "Processing error" in data["detail"]
        finally:
            app.dependency_overrides = {}
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_analyze_curriculum_missing_files(self, client):
        """Test curriculum analysis with missing files."""
        # Act
        data = {
            "query": "Test query",
            "request_id": "test-request-123",
            "user_id": "test-user@example.com"
        }
        response = client.post("/api/v1/curriculum/", data=data)
        
        # Assert
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_analyze_curriculum_missing_required_fields(self, client, sample_pdf_content):
        """Test curriculum analysis with missing required fields."""
        # Act
        files = {"files": ("cv1.pdf", sample_pdf_content, "application/pdf")}
        data = {
            "query": "Test query"
            # Missing request_id and user_id
        }
        response = client.post("/api/v1/curriculum/", files=files, data=data)
        
        # Assert
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_get_analysis_history_success(self, client):
        """Test successful analysis history retrieval."""
        # Arrange
        mock_use_case = Mock()
        mock_use_case.execute = AsyncMock(return_value=[
            {
                "request_id": "test-request-123",
                "user_id": "test-user@example.com",
                "timestamp": 1234567890.0,
                "query": "Test query",
                "result": {"type": "test", "data": "test data"},
                "processing_time": 2.5
            }
        ])
        
        # Override dependency
        app.dependency_overrides = {
            get_history_use_case: lambda: mock_use_case
        }
        
        try:
            # Act
            response = client.get("/api/v1/curriculum/history/test-user@example.com")
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["user_id"] == "test-user@example.com"
            assert "history" in data
            assert len(data["history"]) == 1
            assert data["total"] == 1
        finally:
            app.dependency_overrides = {}
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_get_analysis_history_empty(self, client):
        """Test analysis history retrieval with empty results."""
        # Arrange
        mock_use_case = Mock()
        mock_use_case.execute = AsyncMock(return_value=[])
        
        # Override dependency
        app.dependency_overrides = {
            get_history_use_case: lambda: mock_use_case
        }
        
        try:
            # Act
            response = client.get("/api/v1/curriculum/history/test-user@example.com")
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["user_id"] == "test-user@example.com"
            assert "history" in data
            assert len(data["history"]) == 0
            assert data["total"] == 0
        finally:
            app.dependency_overrides = {}
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_get_analysis_history_error(self, client):
        """Test analysis history retrieval error handling."""
        # Arrange
        mock_use_case = Mock()
        mock_use_case.execute = AsyncMock(side_effect=Exception("Database error"))
        
        # Override dependency
        app.dependency_overrides = {
            get_history_use_case: lambda: mock_use_case
        }
        
        try:
            # Act
            response = client.get("/api/v1/curriculum/history/test-user@example.com")
            
            # Assert
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
            assert "Database error" in data["detail"]
        finally:
            app.dependency_overrides = {}
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_get_analysis_history_with_limit(self, client):
        """Test analysis history retrieval with limit parameter."""
        # Act
        response = client.get("/api/v1/curriculum/history/test-user@example.com?limit=5")
        
        # Assert
        assert response.status_code == 200


class TestFileValidation:
    """Test cases for file validation."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_invalid_file_type(self, client):
        """Test upload with invalid file type."""
        # Act
        files = {"files": ("test.txt", b"invalid content", "text/plain")}
        data = {
            "request_id": "test-request-123",
            "user_id": "test-user@example.com"
        }
        response = client.post("/api/v1/curriculum/", files=files, data=data)
        
        # Assert
        assert response.status_code in [422, 500]
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_multiple_files(self, client, sample_pdf_content, sample_image_content):
        """Test upload with multiple files."""
        # Act
        files = [
            ("files", ("cv1.pdf", sample_pdf_content, "application/pdf")),
            ("files", ("cv2.jpg", sample_image_content, "image/jpeg"))
        ]
        data = {
            "request_id": "test-request-123",
            "user_id": "test-user@example.com"
        }
        response = client.post("/api/v1/curriculum/", files=files, data=data)
        
        # Assert
        # Should accept multiple files (validation will be handled by the use case)
        assert response.status_code in [200, 422]


class TestErrorHandling:
    """Test cases for error handling."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_global_exception_handler(self, client):
        """Test global exception handler."""
        # Act
        response = client.get("/non-existent-endpoint")
        
        # Assert
        assert response.status_code == 404
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_malformed_request(self, client):
        """Test handling of malformed requests."""
        # Act
        response = client.post("/api/v1/curriculum/", data="invalid json")
        
        # Assert
        assert response.status_code == 422 