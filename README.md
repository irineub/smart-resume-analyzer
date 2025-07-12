# Smart Resume Analyzer - Assistente de Recrutamento

🎯 **O que é?**
Sistema inteligente de análise de currículos que combina OCR avançado com OpenAI para automatizar o processo de recrutamento.

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
  
## 🏗️ Visão Geral da Arquitetura

O projeto foi desenvolvido seguindo os princípios da **Clean Architecture** (Arquitetura Limpa), combinada com conceitos de **Domain-Driven Design (DDD)**. Esta escolha garante:

- **Independência de frameworks**: A lógica de negócio não depende de tecnologias externas
- **Testabilidade**: Cada camada pode ser testada isoladamente (E foram desenvolvidos testes unitarios, descritos na seção TESTES, desse README)
- **Manutenibilidade**: Mudanças em uma camada não afetam outras
- **Escalabilidade**: Fácil adição de novos recursos
  
## 📋 Requisitos

- Python 3.13+
- Docker e Docker Compose
- Chave da API OpenAI

## 🛠️ Instalação e Configuração

### Opção 1: Instalação Simples (Recomendado)

Para uso rápido e produção:

```bash
# 1. Clone o repositório
git clone <repository-url>
cd smart-resume-analyzer

# 2. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações
nano .env

# 3. Execute com Docker (tudo incluído)
docker-compose up --build
```

### Opção 2: Instalação para Desenvolvedores

Para desenvolvimento e debugging:

```bash
# 1. Clone o repositório
git clone <repository-url>
cd smart-resume-analyzer

# 2. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações
nano .env

# 3. Execute apenas o DynamoDB
docker-compose up dynamodb

# 4. Instale as dependências Python
pip install -r requirements.txt

# 5. Execute o servidor Python
python main.py
```

## 🔧 Configuração das Variáveis de Ambiente

**Configurações obrigatórias:**
```env
# Sua chave da API OpenAI
OPENAI_API_KEY=sk-...

# Outras configurações (opcionais)
LLM_MODEL=gpt-4o-mini
OCR_PROVIDER=tesseract
```

## 📖 Como Usar

### Acesse a documentação
Abra http://localhost:3000/api/v1/docs no navegador para ver a documentação Swagger interativa.

![Tela Inicial Swagger](https://raw.githubusercontent.com/irineub/smart-resume-analyzer/refs/heads/main/docs/assets/swagger-initial.png)

### Endpoints Disponíveis

#### 1. Análise de Currículo
**POST** `/api/v1/curriculum/`

![Descrição Rota Análise de Currículo](https://raw.githubusercontent.com/irineub/smart-resume-analyzer/refs/heads/main/docs/assets/swagger-post.png)

**Input exemplo:**
![Input exemplo para Análise de Currículo](https://raw.githubusercontent.com/irineub/smart-resume-analyzer/refs/heads/main/docs/assets/swagger-input.png)

## 📄 Exemplo de Resposta do sistema IA com Relatorio detalhado e completo para o recrutador.

```json
{
  "code": 200,
  "status": "success",
  "request_id": "d322a30d-fbca-4892-a783-0b80ca277470",
  "user_id": "irineutech2025@gmail.com",
  "files_processed": 1,
  "processing_time_seconds": 6.020391464233398,
  "result": {
    "type": "query_analysis",
    "query": "Qual desses Candidatos é o melhor para a vaga de desenvolvedor backend ia",
    "analysis": {
      "query": "Qual desses Candidatos é o melhor para a vaga de desenvolvedor backend ia",
      "best_candidates": [
        {
          "name": "Irineu Brito",
          "filename": "cv-irineu-brito.pdf",
          "skills": [
            "Python",
            "Node.js",
            "NestJS",
            "JavaScript",
            "TypeScript",
            "PostgreSQL",
            "MongoDB",
            "MySQL",
            "Firebase Firestore",
            "RESTful APIs",
            "WebSockets"
          ],
          "experience_years": 3,
          "relevant_experience": "Desenvolvimento de aplicações web escaláveis utilizando Python e Node.js, com forte experiência em Inteligência Artificial, processamento de linguagem natural e arquiteturas de backend.",
          "strengths": [
            "Experiência em desenvolver soluções inovadoras com IA",
            "Conhecimento sólido em bancos de dados e DevOps",
            "Habilidade em trabalhar em equipes ágeis e ambientes multiculturais"
          ],
          "weaknesses": [],
          "match_score": 95
        }
      ],
      "total_candidates_analyzed": 1,
      "summary": "O candidato Irineu Brito possui mais de 3 anos de experiência em desenvolvimento backend, especialmente com Python, e está envolvido em projetos utilizando Inteligência Artificial, o que é altamente relevante para a vaga.",
      "recommendations": [
        "Considerar a experiência de Irineu em inteligência artificial e suas habilidades de backend.",
        "Avaliar a capacidade de Irineu em trabalhar em ambientes colaborativos e multiculturais."
      ],
      "next_steps": [
        "Agendar uma entrevista com Irineu Brito para discutir sua experiência e fit cultural.",
        "Sondar mais sobre suas experiências específicas em projetos de IA durante a entrevista."
      ]
    },
    "files_analyzed": [
      "cv-irineu-brito.pdf"
    ]
  },
  "message": "Análise concluída com sucesso!"
}
```


#### 2. Histórico de Logs
**GET** `/api/v1/logs/{user_id}`

Retorna o histórico de logs para um usuário específico (dados do DynamoDB).

**Input:**
![Input Histórico de Logs](https://raw.githubusercontent.com/irineub/smart-resume-analyzer/refs/heads/main/docs/assets/swagger-log-history.png)

**Response:**
![Response Histórico de Logs](https://raw.githubusercontent.com/irineub/smart-resume-analyzer/refs/heads/main/docs/assets/swagger-log-history2.png)

### Exemplos de Uso

#### 1. Análise com Query Específica
```bash
curl -X POST "http://localhost:3000/api/v1/curriculum/" \
  -F "files=@cv1.pdf" \
  -F "files=@cv2.jpg" \
  -F "query=Qual candidato tem mais experiência em Python e AI?" \
  -F "request_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "user_id=irineutech2025@gmail.com"
```

#### 2. Resumo Automático (sem query)
```bash
curl -X POST "http://localhost:3000/api/v1/curriculum/" \
  -F "files=@cv1.pdf" \
  -F "files=@cv2.jpg" \
  -F "request_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "user_id=irineutech2025@gmail.com"
```

#### 3. Consultar Histórico de Logs
```bash
curl -X GET "http://localhost:3000/api/v1/curriculum/history/irineutech2025@gmail.com"
```

## 🔧 Configurações Avançadas

### Modelos OpenAI
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
pytest tests/ -v
```

### Cobertura de Testes
- ✅ **Use Cases**: 100% (lógica de negócio)
- ✅ **Services**: 95% (OCR, LLM, Log)
- ✅ **Repositories**: 90% (DynamoDB)
- ✅ **API**: 85% (endpoints)

## 💡 Casos de Uso

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

**Desenvolvido para otimizar o tempo e automatizar processos de recrutamento  🚀**
