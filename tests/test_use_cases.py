import pytest
from unittest.mock import Mock, AsyncMock
from fastapi import UploadFile
import time

from app.modules.curriculum.application.use_cases import AnalyzeCurriculaUseCase, GetAnalysisHistoryUseCase
from app.modules.curriculum.domain.entities import CurriculumAnalysis


class TestAnalyzeCurriculaUseCase:
    """Test cases for AnalyzeCurriculaUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_ocr_service, mock_llm_service, mock_log_service, mock_repository):
        """Create use case instance with mocked dependencies."""
        return AnalyzeCurriculaUseCase(
            ocr_service=mock_ocr_service,
            llm_service=mock_llm_service,
            log_service=mock_log_service,
            repository=mock_repository
        )
    
    @pytest.fixture
    def mock_files(self, mock_upload_file):
        """Create mock files for testing."""
        files = [
            mock_upload_file("cv1.pdf", b"fake pdf content"),
            mock_upload_file("cv2.jpg", b"fake image content")
        ]
        return files
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.use_cases
    async def test_execute_with_query_success(self, use_case, mock_files, mock_ocr_service, mock_llm_service, mock_repository):
        """Test successful execution with query."""
        # Arrange
        query = "Qual candidato tem mais experiência?"
        request_id = "test-request-123"
        user_id = "test-user@example.com"
        
        # Act
        result = await use_case.execute(mock_files, query, request_id, user_id)
        
        # Assert
        assert result["code"] == 200
        assert result["status"] == "success"
        assert result["request_id"] == request_id
        assert result["user_id"] == user_id
        assert result["files_processed"] == 2
        assert "processing_time_seconds" in result
        assert result["result"]["type"] == "query_analysis"
        assert result["result"]["query"] == query
        
        # Verify service calls
        mock_ocr_service.extract_text_from_files.assert_called_once_with(mock_files)
        mock_llm_service.analyze_with_query.assert_called_once()
        mock_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.use_cases
    async def test_execute_without_query_success(self, use_case, mock_files, mock_ocr_service, mock_llm_service, mock_repository):
        """Test successful execution without query."""
        # Arrange
        query = None
        request_id = "test-request-123"
        user_id = "test-user@example.com"
        
        # Act
        result = await use_case.execute(mock_files, query, request_id, user_id)
        
        # Assert
        assert result["code"] == 200
        assert result["status"] == "success"
        assert result["request_id"] == request_id
        assert result["user_id"] == user_id
        assert result["files_processed"] == 2
        assert "processing_time_seconds" in result
        assert result["result"]["type"] == "individual_summaries"
        
        # Verify service calls
        mock_ocr_service.extract_text_from_files.assert_called_once_with(mock_files)
        mock_llm_service.generate_individual_summaries.assert_called_once()
        mock_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.use_cases
    async def test_execute_ocr_error(self, use_case, mock_files, mock_ocr_service, mock_repository):
        """Test execution when OCR service fails."""
        # Arrange
        mock_ocr_service.extract_text_from_files.side_effect = Exception("OCR Error")
        query = "Test query"
        request_id = "test-request-123"
        user_id = "test-user@example.com"
        
        # Act & Assert
        with pytest.raises(Exception, match="OCR Error"):
            await use_case.execute(mock_files, query, request_id, user_id)
        
        # Verify error was logged
        mock_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.use_cases
    async def test_execute_llm_error(self, use_case, mock_files, mock_llm_service, mock_repository):
        """Test execution when LLM service fails."""
        # Arrange
        mock_llm_service.analyze_with_query.side_effect = Exception("LLM Error")
        query = "Test query"
        request_id = "test-request-123"
        user_id = "test-user@example.com"
        
        # Act & Assert
        with pytest.raises(Exception, match="LLM Error"):
            await use_case.execute(mock_files, query, request_id, user_id)
        
        # Verify error was logged
        mock_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.use_cases
    async def test_execute_empty_files(self, use_case, mock_ocr_service, mock_llm_service, mock_repository):
        """Test execution with empty files list."""
        # Arrange
        files = []
        query = "Test query"
        request_id = "test-request-123"
        user_id = "test-user@example.com"
        
        # Act
        result = await use_case.execute(files, query, request_id, user_id)
        
        # Assert
        assert result["code"] == 200
        assert result["files_processed"] == 0
        mock_ocr_service.extract_text_from_files.assert_called_once_with(files)


class TestGetAnalysisHistoryUseCase:
    """Test cases for GetAnalysisHistoryUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_repository):
        """Create use case instance with mocked repository."""
        return GetAnalysisHistoryUseCase(repository=mock_repository)
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.use_cases
    async def test_execute_success(self, use_case, mock_repository, sample_curriculum_analysis):
        """Test successful execution."""
        # Arrange
        user_id = "test-user@example.com"
        limit = 10
        mock_repository.get_by_user_id.return_value = [sample_curriculum_analysis]
        
        # Act
        result = await use_case.execute(user_id, limit)
        
        # Assert
        assert len(result) == 1
        assert result[0]["request_id"] == sample_curriculum_analysis.request_id
        assert result[0]["user_id"] == sample_curriculum_analysis.user_id
        mock_repository.get_by_user_id.assert_called_once_with(user_id, limit)
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.use_cases
    async def test_execute_empty_history(self, use_case, mock_repository):
        """Test execution with empty history."""
        # Arrange
        user_id = "test-user@example.com"
        limit = 10
        mock_repository.get_by_user_id.return_value = []
        
        # Act
        result = await use_case.execute(user_id, limit)
        
        # Assert
        assert result == []
        mock_repository.get_by_user_id.assert_called_once_with(user_id, limit)
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.use_cases
    async def test_execute_repository_error(self, use_case, mock_repository):
        """Test execution when repository fails."""
        # Arrange
        user_id = "test-user@example.com"
        limit = 10
        mock_repository.get_by_user_id.side_effect = Exception("Database Error")
        
        # Act & Assert
        with pytest.raises(Exception, match="Database Error"):
            await use_case.execute(user_id, limit)
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.use_cases
    async def test_execute_default_limit(self, use_case, mock_repository):
        """Test execution with default limit."""
        # Arrange
        user_id = "test-user@example.com"
        mock_repository.get_by_user_id.return_value = []
        
        # Act
        await use_case.execute(user_id)
        
        # Assert
        mock_repository.get_by_user_id.assert_called_once_with(user_id, 10) 