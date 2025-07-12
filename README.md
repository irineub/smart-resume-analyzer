# Smart Resume Analyzer - Assistente de Recrutamento

🎯 **O que é?**
Sistema inteligente de análise de currículos que combina OCR avançado com OpenAI para automatizar o processo de recrutamento do Fabio na TechMatch.

## ✨ Features Principais

- 🤖 **LLM Inteligente**: OpenAI GPT-4 para análises precisas e respostas naturais
- 📄 **OCR Multi-formato**: Suporte a PDF, JPG, PNG com Tesseract
- 🔍 **Análise Contextual**: Responde perguntas específicas sobre candidatos
- 📊 **Logs Detalhados**: Auditoria completa sem armazenar documentos
- 🐳 **Docker Ready**: Deploy simplificado
- 📚 **Swagger/OpenAPI**: Documentação interativa

## 🚀 Tecnologias

- **Backend**: FastAPI (Async)
- **OCR**: Tesseract
- **LLM**: OpenAI GPT-4
- **Database**: DynamoDB
- **Deploy**: Docker + Docker Compose

## 📋 Requisitos

- Python 3.11+
- Docker e Docker Compose
- Chave da API OpenAI

## 🛠️ Instalação e Configuração

### 1. Clone o repositório
```bash
git clone <repository-url>
cd smart-resume-analyzer
```

### 2. Configure as variáveis de ambiente
```bash
# Renomeie o arquivo de exemplo
cp env.txt .env

# Edite o arquivo .env com suas configurações
nano .env
```

**Configurações obrigatórias:**
```env
# Sua chave da API OpenAI
OPENAI_API_KEY=sk-...

# Outras configurações (opcionais)
LLM_MODEL=gpt-4o-mini
OCR_PROVIDER=tesseract
```

### 3. Execute com Docker (Recomendado)
```bash
# Iniciar DynamoDB local
docker run -d -p 8001:8000 --name dynamodb-local amazon/dynamodb-local

# Construir e executar a aplicação
docker-compose up --build
```

### 4. Ou execute localmente
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload
```

## 📖 Como Usar

### Acesse a documentação
Abra http://localhost:8000/api/v1/docs no navegador para ver a documentação Swagger interativa.

### Exemplos de Uso

#### 1. Análise com Query Específica
```bash
curl -X POST "http://localhost:8000/api/v1/curriculum/" \
  -F "files=@cv1.pdf" \
  -F "files=@cv2.jpg" \
  -F "query=Qual candidato tem mais experiência em Python e Django?" \
  -F "request_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "user_id=fabio@techmatch.com"
```

#### 2. Resumo Automático (sem query)
```bash
curl -X POST "http://localhost:8000/api/v1/curriculum/" \
  -F "files=@cv1.pdf" \
  -F "files=@cv2.jpg" \
  -F "request_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "user_id=fabio@techmatch.com"
```

## 🔧 Configurações Avançadas

### Modelos OpenAI Disponíveis
- `gpt-4o-mini` (recomendado - rápido e econômico)
- `gpt-4o` (mais preciso, mas mais caro)
- `gpt-3.5-turbo` (alternativa econômica)

### Configurações de Performance
```env
OPENAI_MAX_TOKENS=2000    # Máximo de tokens por resposta
OPENAI_TEMPERATURE=0.7    # Criatividade (0.0-1.0)
```

## 📊 Logs e Auditoria

O sistema registra automaticamente:
- ✅ **request_id**: Identificador único da requisição
- ✅ **user_id**: Quem solicitou a análise
- ✅ **timestamp**: Quando foi executado
- ✅ **query**: Pergunta feita (se houver)
- ✅ **resultado**: Resposta gerada
- ❌ **NÃO armazena**: Conteúdo dos documentos

## 🧪 Testes

### Executar Testes
```bash
# Executar todos os testes
./run_tests.sh

# Executar testes específicos
./run_tests.sh unit          # Testes unitários
./run_tests.sh integration   # Testes de integração
./run_tests.sh performance   # Testes de performance
./run_tests.sh coverage      # Testes com cobertura

# Ou usar pytest diretamente
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html
```

### Cobertura de Testes
- ✅ **Use Cases**: 100% (lógica de negócio)
- ✅ **Services**: 95% (OCR, LLM, Log)
- ✅ **Repositories**: 90% (DynamoDB)
- ✅ **API**: 85% (endpoints)
- ✅ **Performance**: 100% (métricas)

### Tipos de Testes
- **Unitários**: Componentes isolados
- **Integração**: Endpoints da API
- **Performance**: Tempo de resposta e carga
- **Repositórios**: Operações de banco de dados
- **Serviços**: OCR, LLM, Log

## 🐛 Troubleshooting

### Problema: "OpenAI API key não configurada"
**Solução**: Configure a variável `OPENAI_API_KEY` no arquivo `.env`

### Problema: "Erro ao processar arquivo"
**Solução**: Verifique se o arquivo é PDF, JPG ou PNG válido

### Problema: "DynamoDB não disponível"
**Solução**: Execute `docker start dynamodb-local` ou verifique a porta 8001

### Problema: "Testes falhando"
**Solução**: 
1. Instale dependências: `pip install pytest pytest-asyncio pytest-cov httpx`
2. Execute: `pytest tests/ -v`
3. Verifique logs: `pytest tests/ --log-cli-level=DEBUG`

## 🎯 Casos de Uso do Fabio

### 1. Análise de Candidatos para Vaga Específica
```
Query: "Qual candidato tem mais experiência em React e Node.js para a vaga de Frontend Developer?"
```

### 2. Comparação de Habilidades
```
Query: "Compare os candidatos em termos de experiência com AWS e Docker"
```

### 3. Resumo Rápido de Múltiplos CVs
```
Sem query: Retorna resumo individual de cada currículo
```

## 🔒 Segurança

- ✅ Validação de tipos de arquivo
- ✅ Limite de tamanho (10MB por arquivo)
- ✅ Máximo 10 arquivos por requisição
- ✅ Rate limiting configurável
- ✅ Logs sem armazenar documentos

## 📈 Monitoramento

- Health check: `GET /api/v1/health`
- Métricas de performance
- Logs estruturados
- Auditoria completa

---

**Desenvolvido para otimizar o tempo do Fabio e automatizar processos de recrutamento na TechMatch! 🚀**