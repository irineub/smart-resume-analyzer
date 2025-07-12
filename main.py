import asyncio
from app.app import app
from app.core.database import dynamodb_client

async def init_database():
    """Inicializa o banco de dados"""
    try:
        await dynamodb_client.create_table_if_not_exists()
        print("✅ Database inicializado com sucesso!")
    except Exception as e:
        print(f"⚠️ Aviso: Não foi possível inicializar o database: {e}")

if __name__ == "__main__":
    import uvicorn
    
    asyncio.run(init_database())
    
    uvicorn.run(
        "app.app:app",
        host="0.0.0.0",
        port=3000,
        reload=True
    )