from typing import List, Optional, Dict
from app.modules.curriculum.application.interfaces import AnalysisRepository
from app.modules.curriculum.domain.entities import CurriculumAnalysis
from app.modules.curriculum.infrastructure.models import AnalysisModel
from app.core.config import settings
import aioboto3
import json
from decimal import Decimal

class DynamoDBAnalysisRepository(AnalysisRepository):
    """Implementação do repositório usando DynamoDB"""
    
    def __init__(self):
        self.session = aioboto3.Session()
        self.table_name = settings.dynamodb_table_name
    
    async def save(self, analysis: CurriculumAnalysis) -> None:
        """Salva uma análise no DynamoDB"""
        try:
            async with self.session.resource(
                'dynamodb',
                endpoint_url=settings.dynamodb_endpoint_url,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_default_region
            ) as dynamodb:
                table = await dynamodb.Table(self.table_name)
                item = AnalysisModel.to_dynamodb_item(analysis.__dict__)
                
                if 'processing_time' in item and isinstance(item['processing_time'], str):
                    item['processing_time'] = Decimal(item['processing_time'])
                
                await table.put_item(Item=item)
                print(f"Análise salva no DynamoDB: {analysis.request_id}")
        except Exception as e:
            print(f"Erro ao salvar análise: {e}")
            pass
    
    async def get_by_request_id(self, request_id: str) -> Optional[CurriculumAnalysis]:
        """Busca análise por request_id"""
        try:
            async with self.session.resource(
                'dynamodb',
                endpoint_url=settings.dynamodb_endpoint_url,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_default_region
            ) as dynamodb:
                table = await dynamodb.Table(self.table_name)
                response = await table.get_item(Key={'request_id': request_id})
                
                if 'Item' in response:
                    item = AnalysisModel.from_dynamodb_item(response['Item'])
                    return CurriculumAnalysis(**item)
                return None
        except Exception as e:
            print(f"Erro ao buscar análise: {e}")
            return None
    
    async def get_by_user_id(self, user_id: str, limit: int = 10) -> List[CurriculumAnalysis]:
        """Busca análises por user_id"""
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
                
                analyses = []
                for item in response.get('Items', []):
                    data = AnalysisModel.from_dynamodb_item(item)
                    analyses.append(CurriculumAnalysis(**data))
                
                return analyses
        except Exception as e:
            print(f"Erro ao buscar análises por usuário: {e}")
            return []
