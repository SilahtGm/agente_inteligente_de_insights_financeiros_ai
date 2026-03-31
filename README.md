# 💰 SGF - Sistema de Gestão Financeira (SQL + Python + IA)

Sistema completo de controle financeiro pessoal desenvolvido em **Python + SQLite**, com integração de **Inteligência Artificial** para geração de insights financeiros inteligentes.

---

## 📌 Visão Geral

O **SGF (Sistema de Gestão Financeira)** simula um ambiente real de análise de dados, onde as informações são estruturadas em banco relacional e processadas para gerar **indicadores financeiros, diagnósticos e previsões**.

O sistema permite:
- Cadastro de usuários
- Registro de receitas e despesas
- Criação de metas financeiras
- Análise de saúde financeira (KPIs)
- Insights inteligentes com IA

---


### 🔐 Segurança:
- Para fins didáticos, as senhas são armazenadas em texto simples.
- Em ambiente real, seria utilizado hash seguro com bcrypt ou Argon2.

## 🧠 Diferenciais do Projeto

### 🔹 Modelagem de Dados
- Uso de **chaves primárias (PK)** e **estrangeiras (FK)**
- Constraints para integridade dos dados
- Estrutura relacional bem definida

### 🔹 Análise com SQL
- Queries com:
  - `JOIN`
  - `GROUP BY`
  - `SUM`
- Extração de indicadores financeiros diretamente do banco

### 🔹 Integração com IA (FinGPT)
- Assistente financeiro inteligente
- Análise de dados do usuário
- Geração de:
  - Resumos financeiros
  - Dicas personalizadas
  - Previsões futuras

### 🔹 Visualização de Dados
- Uso de **Pandas** e **Matplotlib**
- Geração de gráficos comparativos (Entradas vs Saídas)

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.x  
- **Banco de Dados:** SQLite3  
- **IA:** Google Gemini (via LangChain)  
- **Bibliotecas:**
  - pandas
  - matplotlib
  - dotenv
  - langchain
- **Versionamento:** Git  

---

## 🗄️ Estrutura do Banco de Dados

O banco `database.db` contém 4 tabelas principais:

| Tabela              | Descrição |
|--------------------|----------|
| `usuarios`          | Dados cadastrais dos usuários |
| `categorias`        | Tipos de receitas e despesas |
| `transacoes`        | Registro do fluxo financeiro |
| `metas_economicas`  | Planejamento financeiro |

---

## ⚙️ Instalação

### 1. Clone o repositório

git clone https://github.com/SilahtGm/agente_inteligente_de_insights_financeiros_ai.git


### 2. Instale as dependências

pip install -r requirements.txt

### 3.🔑 Configuração da API (IA)

Crie um arquivo .env na pasta *ia* raiz do projeto:

GOOGLE_API_KEY=sua_chave_aqui


### 4. ▶️ Execução do Sistema
python ai_analyst.py