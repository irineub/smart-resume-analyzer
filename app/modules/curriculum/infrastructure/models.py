from typing import Dict, Any, List
from datetime import datetime
import json
from decimal import Decimal

def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj

class AnalysisModel:
    """Modelo DynamoDB para análises"""
    
    @staticmethod
    def to_dynamodb_item(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Converte dados da análise para formato DynamoDB"""
        # Convert processing_time to string to avoid JSON serialization issues
        processing_time = analysis_data['processing_time']
        if isinstance(processing_time, (int, float)):
            processing_time_str = str(processing_time)
        else:
            processing_time_str = str(processing_time)
            
        return {
            'request_id': analysis_data['request_id'],
            'user_id': analysis_data['user_id'],
            'timestamp': str(analysis_data['timestamp']),
            'query': analysis_data.get('query'),
            'files_count': analysis_data['files_count'],
            'file_names': analysis_data['file_names'],
            'result': json.dumps(analysis_data['result']),
            'processing_time': processing_time_str,  # Store as string to avoid Decimal issues
            'status': analysis_data.get('status', 'completed')
        }
    
    @staticmethod
    def from_dynamodb_item(item: Dict[str, Any]) -> Dict[str, Any]:
        """Converte dados do DynamoDB para formato da aplicação"""
        return {
            'request_id': item['request_id'],
            'user_id': item['user_id'],
            'timestamp': float(item['timestamp']),
            'query': item.get('query'),
            'files_count': item['files_count'],
            'file_names': item['file_names'],
            'result': convert_decimals(json.loads(item['result'])),
            'processing_time': float(item['processing_time']),
            'status': item.get('status', 'completed')
        }
