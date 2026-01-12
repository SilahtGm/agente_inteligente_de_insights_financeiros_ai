# 💰 SGF - Sistema de Gestão Financeira (SQL + Python)

Sistema de controle financeiro desenvolvido para demonstrar a integração entre linguagem de programação Python e bancos de dados relacionais (SQLite), focado em análise de indicadores e saúde financeira.

---

## 📌 Sobre o Projeto
Este projeto simula um ambiente real de análise de dados onde as informações não estão em arquivos soltos, mas estruturadas em um banco de dados SQL. O sistema permite o cadastro de usuários, registro de movimentações e gera diagnósticos automáticos de saúde financeira.

### 🧠 O que este projeto demonstra:
* **Modelagem de Dados:** Criação de tabelas com chaves primárias (PK), chaves estrangeiras (FK) e constraints de integridade.
* **Análise via SQL:** Uso de queries complexas com `JOIN`, `GROUP BY` e funções de agregação (`SUM`).
* **Data Visualization:** Integração com **Pandas** e **Matplotlib** para gerar gráficos de performance.
* **Lógica de Negócio:** Implementação de KPIs (Indicadores-chave de Desempenho) para diagnosticar a eficiência financeira.

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Banco de Dados:** SQLite3
* **Bibliotecas de Dados:** Pandas e Matplotlib
* **Versionamento:** Git

---

## 📊 Estrutura do Banco de Dados
O banco de dados `database.db` é composto por quatro tabelas principais:
1.  **usuarios:** Dados cadastrais.
2.  **categorias:** Segmentação de tipos de Receita e Despesa.
3.  **transacoes:** Onde ocorrem os registros de fluxo de caixa.
4.  **metas_economicas:** Planejamento financeiro de longo prazo.

# Instale as dependências:

## Bash

- pip install pandas matplotlib
  
## Execute o sistema:

- main.py

---

O sistema utiliza o modelo Gemini 2.5 Flash, disponibilizado gratuitamente pela Google AI Studio, integrado via LangChain. O modelo foi escolhido por oferecer bom desempenho em tarefas de linguagem natural, baixo custo computacional e compatibilidade com aplicações acadêmicas de pequeno e médio porte.

de um pip install requirements.txt

Inicialmente foi considerada a utilização de APIs de IA em nuvem. Contudo, devido às severas limitações de requisições diárias na camada gratuita, optou-se pela adoção de um modelo de linguagem local executado via Ollama, garantindo viabilidade de desenvolvimento, testes e demonstração do sistema.
