import aioboto3
import json
from app.core.config import settings

class DynamoDBClient:
    def __init__(self):
        self.session = aioboto3.Session()
        self.table_name = settings.dynamodb_table_name
    
    async def get_table(self):
        """Retorna a tabela DynamoDB"""
        async with self.session.resource(
            'dynamodb',
            endpoint_url=settings.dynamodb_endpoint_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_default_region
        ) as dynamodb:
            return await dynamodb.Table(self.table_name)
    
    async def create_table_if_not_exists(self):
        """Cria a tabela se não existir"""
        try:
            async with self.session.resource(
                'dynamodb',
                endpoint_url=settings.dynamodb_endpoint_url,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_default_region
            ) as dynamodb:
                try:
                    table = await dynamodb.Table(self.table_name)
                    await table.load()
                    print(f"Tabela {self.table_name} já existe")
                    return
                except:
                    pass
                table = await dynamodb.create_table(
                    TableName=self.table_name,
                    KeySchema=[
                        {'AttributeName': 'request_id', 'KeyType': 'HASH'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'request_id', 'AttributeType': 'S'},
                        {'AttributeName': 'user_id', 'AttributeType': 'S'},
                        {'AttributeName': 'timestamp', 'AttributeType': 'S'}
                    ],
                    GlobalSecondaryIndexes=[
                        {
                            'IndexName': 'user_id-timestamp-index',
                            'KeySchema': [
                                {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                            ],
                            'Projection': {'ProjectionType': 'ALL'},
                            'ProvisionedThroughput': {
                                'ReadCapacityUnits': 5,
                                'WriteCapacityUnits': 5
                            }
                        }
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                )
                print(f"Tabela {self.table_name} criada com sucesso!")
        except Exception as e:
            print(f"Erro ao criar tabela: {e}")

dynamodb_client = DynamoDBClient()
