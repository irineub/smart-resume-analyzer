import pytest
from unittest.mock import Mock, AsyncMock, patch
import json
from decimal import Decimal

from app.modules.curriculum.infrastructure.repositories import DynamoDBAnalysisRepository
from app.modules.curriculum.infrastructure.models import AnalysisModel
from app.modules.curriculum.domain.entities import CurriculumAnalysis


class TestDynamoDBAnalysisRepository:
    """Test cases for DynamoDBAnalysisRepository."""
    
    @pytest.fixture
    def repository(self):
        """Create repository instance."""
        repo = DynamoDBAnalysisRepository()
        return repo
    
    @pytest.fixture
    def sample_curriculum_analysis(self):
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
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.repositories
    async def test_save_success(self, repository, sample_curriculum_analysis):
        """Test successful save operation."""
        # Arrange
        with patch.object(repository, 'session') as mock_session:
            # Mock the async context manager
            mock_resource = Mock()
            mock_table = Mock()
            mock_table.put_item = AsyncMock()
            mock_resource.Table = AsyncMock(return_value=mock_table)
            
            # Create async context manager
            async def aenter(*args, **kwargs):
                return mock_resource
            async def aexit(*args, **kwargs):
                pass
            
            mock_context = Mock()
            mock_context.__aenter__ = aenter
            mock_context.__aexit__ = aexit
            mock_session.resource.return_value = mock_context
            
            # Act
            await repository.save(sample_curriculum_analysis)
            
            # Assert
            mock_table.put_item.assert_awaited_once()
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.repositories
    async def test_save_error_handling(self, repository, sample_curriculum_analysis):
        """Test save operation error handling."""
        # Arrange
        with patch.object(repository, 'session') as mock_session:
            mock_session.resource.side_effect = Exception("DynamoDB Error")
            
            # Act & Assert
            # Should not raise an exception, just log the error
            await repository.save(sample_curriculum_analysis)
            assert True  # If we get here, no exception was raised
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.repositories
    async def test_get_by_request_id_success(self, repository, sample_curriculum_analysis):
        """Test successful get by request_id operation."""
        # Arrange
        with patch.object(repository, 'session') as mock_session:
            mock_resource = Mock()
            mock_table = Mock()
            mock_item = AnalysisModel.to_dynamodb_item(sample_curriculum_analysis.__dict__)
            mock_table.get_item = AsyncMock(return_value={'Item': mock_item})
            mock_resource.Table = AsyncMock(return_value=mock_table)
            
            # Create async context manager
            async def aenter(*args, **kwargs):
                return mock_resource
            async def aexit(*args, **kwargs):
                pass
            
            mock_context = Mock()
            mock_context.__aenter__ = aenter
            mock_context.__aexit__ = aexit
            mock_session.resource.return_value = mock_context
            
            # Act
            result = await repository.get_by_request_id("test-request-123")
            
            # Assert
            assert result is not None
            assert result.request_id == sample_curriculum_analysis.request_id
            assert result.user_id == sample_curriculum_analysis.user_id
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.repositories
    async def test_get_by_request_id_not_found(self, repository):
        """Test get by request_id when item not found."""
        # Arrange
        with patch.object(repository, 'session') as mock_session:
            mock_resource = Mock()
            mock_table = Mock()
            mock_table.get_item = AsyncMock(return_value={})
            mock_resource.Table = AsyncMock(return_value=mock_table)
            
            # Create async context manager
            async def aenter(*args, **kwargs):
                return mock_resource
            async def aexit(*args, **kwargs):
                pass
            
            mock_context = Mock()
            mock_context.__aenter__ = aenter
            mock_context.__aexit__ = aexit
            mock_session.resource.return_value = mock_context
            
            # Act
            result = await repository.get_by_request_id("non-existent-id")
            
            # Assert
            assert result is None
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.repositories
    async def test_get_by_request_id_error(self, repository):
        """Test get by request_id error handling."""
        # Arrange
        with patch.object(repository, 'session') as mock_session:
            mock_session.resource.side_effect = Exception("DynamoDB Error")
            
            # Act
            result = await repository.get_by_request_id("test-request-123")
            
            # Assert
            assert result is None
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.repositories
    async def test_get_by_user_id_success(self, repository, sample_curriculum_analysis):
        """Test successful get by user_id operation."""
        # Arrange
        with patch.object(repository, 'session') as mock_session:
            mock_resource = Mock()
            mock_table = Mock()
            mock_item = AnalysisModel.to_dynamodb_item(sample_curriculum_analysis.__dict__)
            mock_table.query = AsyncMock(return_value={'Items': [mock_item]})
            mock_resource.Table = AsyncMock(return_value=mock_table)
            
            # Create async context manager
            async def aenter(*args, **kwargs):
                return mock_resource
            async def aexit(*args, **kwargs):
                pass
            
            mock_context = Mock()
            mock_context.__aenter__ = aenter
            mock_context.__aexit__ = aexit
            mock_session.resource.return_value = mock_context
            
            # Act
            result = await repository.get_by_user_id("test-user@example.com", 10)
            
            # Assert
            assert len(result) == 1
            assert result[0].request_id == sample_curriculum_analysis.request_id
            assert result[0].user_id == sample_curriculum_analysis.user_id
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.repositories
    async def test_get_by_user_id_empty(self, repository):
        """Test get by user_id with empty results."""
        # Arrange
        with patch.object(repository, 'session') as mock_session:
            mock_resource = Mock()
            mock_table = Mock()
            mock_table.query = AsyncMock(return_value={'Items': []})
            mock_resource.Table = AsyncMock(return_value=mock_table)
            
            # Create async context manager
            async def aenter(*args, **kwargs):
                return mock_resource
            async def aexit(*args, **kwargs):
                pass
            
            mock_context = Mock()
            mock_context.__aenter__ = aenter
            mock_context.__aexit__ = aexit
            mock_session.resource.return_value = mock_context
            
            # Act
            result = await repository.get_by_user_id("test-user@example.com", 10)
            
            # Assert
            assert len(result) == 0
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.repositories
    async def test_get_by_user_id_error(self, repository):
        """Test get by user_id error handling."""
        # Arrange
        with patch.object(repository, 'session') as mock_session:
            mock_session.resource.side_effect = Exception("DynamoDB Error")
            
            # Act
            result = await repository.get_by_user_id("test-user@example.com", 10)
            
            # Assert
            assert len(result) == 0


class TestAnalysisModel:
    """Test cases for AnalysisModel."""
    
    @pytest.fixture
    def sample_analysis_data(self):
        """Sample analysis data for testing."""
        return {
            "request_id": "test-request-123",
            "user_id": "test-user@example.com",
            "timestamp": 1234567890.0,
            "query": "Qual candidato tem mais experiência?",
            "files_count": 2,
            "file_names": ["cv1.pdf", "cv2.jpg"],
            "result": {
                "type": "query_analysis",
                "query": "Qual candidato tem mais experiência?",
                "analysis": "João Silva tem mais experiência",
                "files_analyzed": ["cv1.pdf", "cv2.jpg"]
            },
            "processing_time": 2.5,
            "status": "success"
        }
    
    @pytest.mark.unit
    @pytest.mark.repositories
    def test_to_dynamodb_item(self, sample_analysis_data):
        """Test conversion to DynamoDB item."""
        # Act
        item = AnalysisModel.to_dynamodb_item(sample_analysis_data)
        
        # Assert
        assert item["request_id"] == "test-request-123"
        assert item["user_id"] == "test-user@example.com"
        assert item["timestamp"] == "1234567890.0"
        assert item["query"] == "Qual candidato tem mais experiência?"
        assert item["files_count"] == 2
        assert item["file_names"] == ["cv1.pdf", "cv2.jpg"]
        # Result is stored as JSON string
        result_dict = json.loads(item["result"])
        assert result_dict["type"] == "query_analysis"
        assert item["processing_time"] == "2.5"
        assert item["status"] == "success"
    
    @pytest.mark.unit
    @pytest.mark.repositories
    def test_from_dynamodb_item(self, sample_analysis_data):
        """Test conversion from DynamoDB item."""
        # Arrange
        item = AnalysisModel.to_dynamodb_item(sample_analysis_data)
        
        # Act
        result = AnalysisModel.from_dynamodb_item(item)
        
        # Assert
        assert result["request_id"] == "test-request-123"
        assert result["user_id"] == "test-user@example.com"
        assert result["timestamp"] == 1234567890.0
        assert result["query"] == "Qual candidato tem mais experiência?"
        assert result["files_count"] == 2
        assert result["file_names"] == ["cv1.pdf", "cv2.jpg"]
        assert result["result"]["type"] == "query_analysis"
        assert result["processing_time"] == 2.5
        assert result["status"] == "success"
    
    @pytest.mark.unit
    @pytest.mark.repositories
    def test_to_dynamodb_item_with_decimal(self, sample_analysis_data):
        """Test conversion to DynamoDB item with decimal values."""
        # Arrange
        sample_analysis_data["processing_time"] = Decimal("2.5")
        
        # Act
        item = AnalysisModel.to_dynamodb_item(sample_analysis_data)
        
        # Assert
        assert item["processing_time"] == "2.5"
    
    @pytest.mark.unit
    @pytest.mark.repositories
    def test_from_dynamodb_item_with_decimal(self, sample_analysis_data):
        """Test conversion from DynamoDB item with decimal values."""
        # Arrange
        item = AnalysisModel.to_dynamodb_item(sample_analysis_data)
        item["processing_time"] = Decimal("2.5")
        
        # Act
        result = AnalysisModel.from_dynamodb_item(item)
        
        # Assert
        assert result["processing_time"] == 2.5
    
    @pytest.mark.unit
    @pytest.mark.repositories
    def test_to_dynamodb_item_none_values(self, sample_analysis_data):
        """Test conversion to DynamoDB item with None values."""
        # Arrange
        sample_analysis_data["query"] = None
        
        # Act
        item = AnalysisModel.to_dynamodb_item(sample_analysis_data)
        
        # Assert
        assert item["query"] is None
    
    @pytest.mark.unit
    @pytest.mark.repositories
    def test_from_dynamodb_item_none_values(self, sample_analysis_data):
        """Test conversion from DynamoDB item with None values."""
        # Arrange
        item = AnalysisModel.to_dynamodb_item(sample_analysis_data)
        item["query"] = None
        
        # Act
        result = AnalysisModel.from_dynamodb_item(item)
        
        # Assert
        assert result["query"] is None 