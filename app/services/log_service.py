from typing import Dict, List
import json
import os
from datetime import datetime

class LogService:
    """Serviço de log simples que salva em arquivo local"""
    
    def __init__(self):
        self.log_file = "logs/analysis_logs.json"
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Garante que o diretório de logs existe"""
        os.makedirs("logs", exist_ok=True)
    
    async def save_log(self, analysis_data: Dict) -> None:
        """Salva log da análise"""
        try:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "data": analysis_data
            }
            
            logs = []
            if os.path.exists(self.log_file):
                try:
                    with open(self.log_file, 'r') as f:
                        logs = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    logs = []
            
            logs.append(log_entry)
            
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
            print(f"✅ Log salvo: {analysis_data.get('request_id', 'unknown')}")
        except Exception as e:
            print(f"⚠️ Erro ao salvar log: {e}")
    
    async def get_logs_by_user(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Busca logs de um usuário específico"""
        try:
            if not os.path.exists(self.log_file):
                return []
            
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            
            # Filtrar por user_id
            user_logs = []
            for log in logs:
                data = log.get('data', {})
                if data.get('user_id') == user_id:
                    user_logs.append(data)
            
            # Ordenar por timestamp e limitar
            user_logs.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
            return user_logs[:limit]
            
        except Exception as e:
            print(f"⚠️ Erro ao buscar logs: {e}")
            return []