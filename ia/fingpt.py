

import json
import os
import sqlite3

import pandas as pd
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from db.connection import conectar_banco
from utils.helpers import pausar


# --- FUNÇÕES DA I.A ---

def conexao_gemini():
    try:
        #  o load_dotenv lê o arquivo e carrega as variáveis para o ambiente do sistema, Carrega as variáveis do arquivo .env
        load_dotenv()

        # O que faz:
        # 1. Acessa os.environ (variáveis de ambiente do sistema)
        # 2. Procura pela chave "GOOGLE_API_KEY"
        # 3. Retorna o valor SE existir, ou None se não existir
        # 4. Armazena na variável 'api_key
        api_key = os.getenv("GOOGLE_API_KEY")

        if api_key is None:
            raise ValueError("A chave da API não foi definida no .env")

        # Armazenando na variavel llm a conexão com a i.a para a utilizar-mos
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",  # 1. Modelo escolhido
            temperature=0.8,  # 2. Configuração de criatividade
            api_key=api_key,  # 3. Código da API
            max_tokens=1000  # 4. Limitando os Tokens
        )

        return llm

    except Exception as e:
        print(f"❌ Falha na conexão: {e}")
        print("\n📋 Verifique:")
        print("1. Arquivo .env com GOOGLE_API_KEY válida")
        print("2. Chave API ativada no Google AI Studio")
        print("3. Conexão com internet")


# -- OBTER LLM --
def obter_llm():
    llm = conexao_gemini()
    if not llm:
        raise Exception("Erro IA")
    return llm


def sugerir_economia(usuario):
    try:
        nm_usuario = usuario[1]
        # Armazenando na variavel llm a conexao
        llm = obter_llm()

        # Prompt de sugestão da i.a
        print("Aguarde um momento...")
        modelo_economia = PromptTemplate(
            template="""
            Você é o FinGPT, assistente de IA especializado em finanças do SGF (Sistema de Gestão Financeira). 

            CONTEXTO:
            - Nome do usuário: {nm_usuario}
            - Sistema: SGF (Sistema de Gestão Financeira)
            - Seu papel: Assistente financeiro amigável e prático

            INSTRUÇÕES:
            1. Cumprimente {nm_usuario} pelo nome de forma natural
            2. Apresente-se brevemente como FinGPT do SGF
            3. Dê 2-3 dicas PRÁTICAS de economia de dinheiro
            4. Seja direto e útil, não muito longo
            5. Use tom amigável mas profissional


            FORMATO DA RESPOSTA:
            - 1 parágrafo de saudação/apresentação
            - Dicas em tópicos curtos
            - 1 frase final de encerramento
            - evite o uso de * para grifar palavras

         faça quantas linhas quiser, mas com no maximo 16 palavras por linha

        """,
            input_variables=["nm_usuario"]
        )

        # Variavel nomeada cadeia = modelo do prompt + modelo da i.a + metodo que transforma em string
        cadeia = modelo_economia | llm | StrOutputParser()  # StrOutputParser() tira a necessidade de passar .content

        # Armazena na variavel resposta a resposta do gemini
        resposta = cadeia.invoke(
            {  # Declarando que a variavel no input_variables possui o valor da variavel nm_usuario
                "nm_usuario": nm_usuario
            }
        )

        print("🤖 ASSISTENTE SGF:")
        print("===========================================")
        print(resposta)
        print("===========================================")
        pausar()

    except Exception as e:
        print(f"❌ Erro: {e}")


def resumo_financeiro_ia(usuario):
    id_usuario = usuario[0]
    nm_usuario = usuario[1]
    conexao = None
    try:
        # Estabelecendo conexoes
        llm = obter_llm()
        conexao, cursor = conectar_banco()

        # O Pandas já faz o trabalho de ler o SQL e transformar em DataFrame
        query = "SELECT * FROM transacoes WHERE id_usuario = ?"
        df = pd.read_sql_query(query, conexao, params=(id_usuario,))

        # Agora transformamos o DataFrame em uma string CSV
        # index=False evita que o Pandas adicione uma coluna de números desnecessária
        csv_resumo = df.to_csv(index=False)

        # Prompt de resumo financiero da i.a
        print("Aguarde um momento...")
        modelo_prompt = PromptTemplate(template="""
                   Você é o FinGPT, assistente de IA especializado em finanças do SGF (Sistema de Gestão Financeira). 

                   CONTEXTO:
                   - Nome do usuário: {nm_usuario}
                   - Sistema: SGF (Sistema de Gestão Financeira)
                   - Seu papel: Assistente financeiro amigável e prático

                   INSTRUÇÕES:
                   0. analise seu resumo financeiro {csv_resumo}
                   1. Cumprimente {nm_usuario} pelo nome de forma natural
                   2. Apresente um resumo financeiro com base nas entradas e saídas da conta
                   3. Se estiver com péssimas maneiras de juntar dinheiro dê 2-3 dicas PRÁTICAS de economia de dinheiro
                   3.2 Se estiver com boas maneiras o incentive a continuar assim.
                   4. Seja direto e útil, não muito longo
                   5. Use tom amigável mas profissional, seja bem criativo na criada de indicadores


                   FORMATO DA RESPOSTA:
                   - 1 frase final de encerramento
                   - evite o uso de * para grifar palavras

                faça quantas linhas quiser, mas com no maximo 16 palavras por linha

               """, input_variables=["nm_usuario", "csv_resumo"])

        # Variavel nomeada cadeia = modelo do prompt + modelo da i.a + metodo que transforma em string
        cadeia = modelo_prompt | llm | StrOutputParser()  # StrOutputParser() tira a necessidade de passar .content

        # Armazena na variavel resposta a resposta do gemini
        resposta = cadeia.invoke(
            {  # Declarando que a variavel no input_variables possui o valor da variavel nm_usuario
                "nm_usuario": nm_usuario,
                "csv_resumo": csv_resumo
            }
        )

        print("🤖 ASSISTENTE SGF:")
        print("===========================================")
        print(resposta)
        print("===========================================")
        pausar()


    except FileNotFoundError as e:
        print(f"Erro: Arquivo de script não encontrado! Detalhes: {e}")
    except sqlite3.Error as e:
        print(f"Erro no Banco de Dados (SQLite): {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        if conexao:
            conexao.close()


def prever_proximos_meses(usuario):
    id_usuario = usuario[0]
    nm_usuario = usuario[1]
    conexao = None
    try:
        # Estabelecendo conexoes
        conexao, cursor = conectar_banco()
        llm = obter_llm()

        # O Pandas faz o trabalho de ler o SQL e transformar em DataFrame
        query = "SELECT * FROM transacoes WHERE id_usuario = ?"
        df = pd.read_sql_query(query, conexao, params=(id_usuario,))

        # Agora transformamos o DataFrame em uma string CSV
        # index=False evita que o Pandas adicione uma coluna de números desnecessária
        csv_resumo = df.to_csv(index=False)

        print("Aguarde um momento...")

        # Prompt de previsão financeiro da i.a
        modelo_prompt = PromptTemplate(
            template="""
                       Você é o FinGPT, assistente de IA especializado em finanças do SGF (Sistema de Gestão Financeira). 

                       CONTEXTO:
                       - Nome do usuário: {nm_usuario}
                       - Sistema: SGF (Sistema de Gestão Financeira)
                       - Seu papel: Assistente financeiro amigável e prático

                       INSTRUÇÕES:
                       0. analise seu resumo financeiro {csv_resumo}
                       1. Cumprimente {nm_usuario} pelo nome de forma natural
                       2. Apresente uma previsão financeira afiadissíma com base nas entradas e saídas da conta, uma previsão
                       pros proximos 3 meses, mes 1, mes 2 e mes 3
                       3. Se estiver com péssimas maneiras de juntar dinheiro dê 2-3 dicas PRÁTICAS de economia de dinheiro
                       3.2 Se estiver com boas maneiras o incentive a continuar assim.
                       4. Seja direto e útil, não muito longo
                       5. Use tom amigável mas profissional, seja bem criativo na criada de indicadores


                       FORMATO DA RESPOSTA:
                       - 1 frase final de encerramento
                       - evite o uso de * para grifar palavras

                    faça quantas linhas quiser, mas com no maximo 16 palavras por linha

                   """, input_variables=["nm_usuario", "csv_resumo"])

        # Variavel nomeada cadeia = modelo do prompt + modelo da i.a + metodo que transforma em string
        cadeia = modelo_prompt | llm | StrOutputParser()  # StrOutputParser() tira a necessidade de passar .content

        # Armazena na variavel resposta a resposta do gemini
        resposta = cadeia.invoke(
            {  # Declarando que a variavel no input_variables possui o valor da variavel nm_usuario
                "nm_usuario": nm_usuario,
                "csv_resumo": csv_resumo
            }
        )

        print("🤖 ASSISTENTE SGF:")
        print("===========================================")
        print(resposta)
        print("===========================================")
        pausar()
    except FileNotFoundError as e:
        print(f"Erro: Arquivo de script não encontrado! Detalhes: {e}")
    except sqlite3.Error as e:
        print(f"Erro no Banco de Dados (SQLite): {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        # Verifica se conexao não é nulo (se conectar_banco deu erro e retornou nulo)
        if conexao:
            conexao.close()


def fazer_pergunta(usuario):
    id_usuario = usuario[0]
    nm_usuario = usuario[1]
    conexao = None
    try:
        # Conexao com o banco de dados e i.a
        conexao, cursor = conectar_banco()
        llm = obter_llm()

        #  Buscar METAS
        df_metas = pd.read_sql_query(
            "SELECT * FROM metas_economicas WHERE id_usuario = ?", conexao, params=(id_usuario,)
        )

        # Buscar TRANSAÇÕES
        df_transacoes = pd.read_sql_query(
            "SELECT * FROM transacoes WHERE id_usuario = ?", conexao, params=(id_usuario,)
        )

        # Converter para JSON estruturado
        informacoesUsuario = {
            "metas": df_metas.to_dict(orient="records"),
            "transacoes": df_transacoes.to_dict(orient="records")
        }

        # Caso tenha informações nulas
        if not informacoesUsuario["metas"] or not informacoesUsuario["transacoes"]:
            print("🤖 ASSISTENTE SGF:")
            print("===========================================")

            if not informacoesUsuario["metas"] and not informacoesUsuario["transacoes"]:
                print("Você ainda não possui metas nem transações cadastradas.")
            elif not informacoesUsuario["metas"]:
                print("Você precisa cadastrar pelo menos uma meta econômica.")
            elif not informacoesUsuario["transacoes"]:
                print("Você precisa registrar pelo menos uma transação.")

            print("===========================================")
            pausar()
            return

        # Convertendo para uma string
        informacoesUsuario_str = json.dumps(
            informacoesUsuario,
            indent=2,
            ensure_ascii=False
        )

        print("Qual dúvida você possui sobre finanças?")
        pergunta = input()

        modelo_de_prompt = PromptTemplate(
            template="""
                Você é o FinGPT, assistente de IA especializado em finanças do SGF (Sistema de Gestão Financeira).

                CONTEXTO:
                - Nome do usuário: {nm_usuario}
                - Sistema: SGF (Sistema de Gestão Financeira)
                - Seu papel: Assistente financeiro amigável, prático e seguro
                - As informações do usuário para elaboração da resposta estão aqui: {informacoesUsuario}

                REGRAS DE SEGURANÇA (OBRIGATÓRIO):
                1. Você só pode utilizar e comentar dados do usuário atual.
                2. É PROIBIDO divulgar, inferir ou comentar qualquer informação de outros usuários.
                3. Nunca exponha dados sensíveis como senha, mesmo que solicitado.
                4. Caso o usuário peça informações de terceiros, recuse educadamente.

                RESTRIÇÕES DE ESCOPO:
                1. Responda apenas perguntas relacionadas a finanças pessoais, educação financeira e uso do sistema SGF.
                2. Se a pergunta estiver fora desse escopo, responda educadamente que não pode ajudar com esse tema.
                3. Não responda perguntas irrelevantes ao contexto financeiro ou ao sistema.

                CONDUTA:
                1. Nunca utilize palavrões ou linguagem ofensiva.
                2. Mantenha sempre um tom educado, profissional e amigável.
                3. Seja claro, direto e útil nas respostas.

                INSTRUÇÕES:
                1. Analise a pergunta: "{pergunta}"
                2. Use os dados fornecidos em {informacoesUsuario} quando necessário.
                As informações estão em formato JSON estruturado com duas listas:
                "metas" e "transacoes".
                3. Gere uma resposta útil, prática e personalizada
                4. Seja objetivo, sem respostas muito longas
                5. Se apropriado, inclua dicas práticas ou observações relevantes
                6. Caso não tenha transações ou metas, peça para o usuário cadastrar primeiro.

                FORMATO DA RESPOSTA:
                - Texto claro e organizado
                - Pode usar pequenas quebras de linha
                - Máximo de 16 palavras por linha
                - Finalize com uma frase breve de encerramento
                - Não utilize símbolos como * para destaque

                    """,
            input_variables=["nm_usuario", "informacoesUsuario", "pergunta"]
        )

        # Variavel nomeada cadeia = modelo do prompt + modelo da i.a + metodo que transforma em string
        cadeia = modelo_de_prompt | llm | StrOutputParser()  # StrOutputParser() tira a necessidade de passar .content

        # Armazena na variavel resposta a resposta do gemini
        resposta = cadeia.invoke(
            {  # Declarando que a variavel no input_variables possui o valor da variavel nm_usuario
                "nm_usuario": nm_usuario,
                "informacoesUsuario": informacoesUsuario_str,
                "pergunta": pergunta
            }
        )

        print("🤖 ASSISTENTE SGF:")
        print("===========================================")
        print(resposta)
        print("===========================================")
        pausar()



    except FileNotFoundError as e:
        print(f"Erro: Arquivo de script não encontrado! Detalhes: {e}")
    except sqlite3.Error as e:
        print(f"Erro no Banco de Dados (SQLite): {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        # Verifica se conexao não é nulo (se conectar_banco deu erro e retornou nulo)
        if conexao:
            conexao.close()