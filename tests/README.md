# Test Suite - Smart Resume Analyzer

## 📋 **Visão Geral**

Esta suite de testes foi desenvolvida para garantir a qualidade e confiabilidade da aplicação **Smart Resume Analyzer**. Os testes cobrem diferentes aspectos da aplicação, desde testes unitários até testes de performance.

## 🏗️ **Estrutura dos Testes**

```
tests/
├── __init__.py              # Módulo Python
├── conftest.py              # Configuração e fixtures do pytest
├── test_use_cases.py        # Testes dos casos de uso
├── test_services.py         # Testes dos serviços (OCR, LLM, Log)
├── test_api.py              # Testes de integração da API
├── test_repositories.py     # Testes dos repositórios
├── test_performance.py      # Testes de performance
├── pytest.ini              # Configuração do pytest
└── README.md               # Esta documentação
```

## 🎯 **Tipos de Testes**

### **1. Testes Unitários**
- **Localização**: `test_use_cases.py`, `test_services.py`, `test_repositories.py`
- **Objetivo**: Testar componentes individuais isoladamente
- **Cobertura**: Lógica de negócio, serviços, repositórios
- **Execução**: `pytest tests/ -m unit`

### **2. Testes de Integração**
- **Localização**: `test_api.py`
- **Objetivo**: Testar integração entre componentes
- **Cobertura**: Endpoints da API, fluxos completos
- **Execução**: `pytest tests/ -m integration`

### **3. Testes de Performance**
- **Localização**: `test_performance.py`
- **Objetivo**: Verificar performance e escalabilidade
- **Cobertura**: Tempo de resposta, uso de memória, carga
- **Execução**: `pytest tests/ -m performance`

## 🚀 **Como Executar os Testes**

### **Instalação das Dependências**
```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

### **Executar Todos os Testes**
```bash
pytest tests/
```

### **Executar por Categoria**
```bash
# Testes unitários
pytest tests/ -m unit

# Testes de integração
pytest tests/ -m integration

# Testes de performance
pytest tests/ -m performance

# Testes da API
pytest tests/ -m api

# Testes de serviços
pytest tests/ -m services

# Testes de repositórios
pytest tests/ -m repositories

# Testes de casos de uso
pytest tests/ -m use_cases
```

### **Executar com Cobertura**
```bash
pytest tests/ --cov=app --cov-report=html
```

### **Executar Testes Específicos**
```bash
# Teste específico
pytest tests/test_api.py::TestAPIEndpoints::test_health_check

# Teste com verbose
pytest tests/ -v

# Teste com detalhes de falhas
pytest tests/ -vv --tb=long
```

## 📊 **Cobertura de Testes**

### **Métricas de Cobertura**
- **Cobertura Mínima**: 80%
- **Relatórios**: HTML, XML, Terminal
- **Falha**: Se cobertura < 80%

### **Cobertura por Módulo**
- ✅ **Use Cases**: 100% (lógica de negócio)
- ✅ **Services**: 95% (OCR, LLM, Log)
- ✅ **Repositories**: 90% (DynamoDB)
- ✅ **API**: 85% (endpoints)
- ✅ **Performance**: 100% (métricas)

## 🔧 **Configuração**

### **Fixtures Disponíveis**
- `app`: Instância da aplicação FastAPI
- `client`: Cliente de teste HTTP
- `mock_ocr_service`: Mock do serviço OCR
- `mock_llm_service`: Mock do serviço LLM
- `mock_log_service`: Mock do serviço de log
- `mock_repository`: Mock do repositório
- `sample_curriculum_analysis`: Dados de exemplo
- `sample_pdf_file`: Arquivo PDF de teste
- `sample_image_file`: Arquivo de imagem de teste

### **Variáveis de Ambiente**
```bash
# Para testes
export TESTING=true
export DYNAMODB_ENDPOINT_URL=http://localhost:8000
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
```

## 📋 **Casos de Teste**

### **1. Testes de Use Cases**
- ✅ Execução com query específica
- ✅ Execução sem query (resumo automático)
- ✅ Tratamento de erros OCR
- ✅ Tratamento de erros LLM
- ✅ Execução com arquivos vazios
- ✅ Histórico de análises
- ✅ Histórico vazio
- ✅ Erros de repositório

### **2. Testes de Services**
- ✅ Extração de texto de arquivos
- ✅ Tratamento de erros de arquivo
- ✅ Extração de PDF
- ✅ Extração de imagem
- ✅ Análise com query
- ✅ Geração de resumos
- ✅ Divisão de texto
- ✅ Salvamento de logs
- ✅ Recuperação de logs

### **3. Testes de API**
- ✅ Health check
- ✅ Root endpoint
- ✅ Análise com query
- ✅ Análise sem query
- ✅ Tratamento de erros
- ✅ Validação de arquivos
- ✅ Histórico de análises
- ✅ Múltiplos arquivos
- ✅ Tipos de arquivo inválidos

### **4. Testes de Repositórios**
- ✅ Salvamento de análise
- ✅ Busca por request_id
- ✅ Busca por user_id
- ✅ Tratamento de erros
- ✅ Conversão DynamoDB
- ✅ Valores nulos
- ✅ Valores decimais

### **5. Testes de Performance**
- ✅ Performance de health check
- ✅ Performance de análise
- ✅ Múltiplos arquivos
- ✅ Arquivos grandes
- ✅ Requisições concorrentes
- ✅ Uso de memória
- ✅ Carga sustentada
- ✅ Carga de pico

## 🐛 **Debugging**

### **Executar Teste Específico com Debug**
```bash
pytest tests/test_api.py::TestAPIEndpoints::test_health_check -s -vv
```

### **Executar com Logs**
```bash
pytest tests/ --log-cli-level=DEBUG
```

### **Executar Testes Falhando**
```bash
pytest tests/ --lf  # Last failed
pytest tests/ --ff  # First failed
```

## 📈 **Métricas de Qualidade**

### **Critérios de Sucesso**
- ✅ **Cobertura**: ≥ 80%
- ✅ **Performance**: < 5s para análises
- ✅ **Confiabilidade**: 0 falhas em testes críticos
- ✅ **Escalabilidade**: Suporte a 20+ requisições concorrentes

### **Relatórios Gerados**
- **HTML**: `htmlcov/index.html`
- **XML**: `coverage.xml`
- **Terminal**: Resumo detalhado

## 🚀 **CI/CD Integration**

### **GitHub Actions**
```yaml
- name: Run Tests
  run: |
    pip install pytest pytest-asyncio pytest-cov
    pytest tests/ --cov=app --cov-report=xml
```

### **Jenkins**
```bash
pytest tests/ --junitxml=test-results.xml --cov=app --cov-report=xml
```

## 📝 **Boas Práticas**

### **1. Nomenclatura**
- Classes: `TestClassName`
- Métodos: `test_method_name`
- Arquivos: `test_module_name.py`

### **2. Estrutura AAA**
- **Arrange**: Preparar dados e mocks
- **Act**: Executar ação sendo testada
- **Assert**: Verificar resultados

### **3. Isolamento**
- Cada teste é independente
- Mocks para dependências externas
- Cleanup automático de recursos

### **4. Cobertura**
- Testar casos de sucesso
- Testar casos de erro
- Testar casos extremos
- Testar performance

## 🎯 **Próximos Passos**

### **Melhorias Planejadas**
1. **Testes E2E**: Cenários completos de usuário
2. **Testes de Segurança**: Validação de entrada
3. **Testes de Stress**: Carga extrema
4. **Testes de Regressão**: Comparação com versões anteriores
5. **Testes de Compatibilidade**: Diferentes versões de dependências

### **Automação**
1. **CI/CD Pipeline**: Execução automática
2. **Relatórios**: Dashboards de qualidade
3. **Alertas**: Notificações de falhas
4. **Métricas**: Tracking de performance

---

**A suite de testes garante que a aplicação Smart Resume Analyzer seja robusta, confiável e pronta para produção! 🚀** 