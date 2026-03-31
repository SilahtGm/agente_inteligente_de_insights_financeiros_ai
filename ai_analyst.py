# Importações necessarias
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import sqlite3 #sqlite para banco de dados
import os #os para informações do sistema
import matplotlib.pyplot as plt
import pandas as pd
import json

# -- FUNÇÃO PRINCIPAL DE CRIAÇÃO/CONEXÃO DE BANCO DE DADOS ==
def inicializar_banco():
    try:
        # Guardando na variavel a checagem de se o banco de dados ja existe
        banco_existe = os.path.exists('database.db')

        # Guardando na variavel conexao a conexao do sqlite3, e fazendo a conexao
        # com o banco de dados localizado no arquivp database.db, se ele não existir
        # vai ser criado agora
        conexao = sqlite3.connect('database.db')
        cursor = conexao.cursor()

        # 1. Tenta abrir e rodar o Schema, guardadp no arquivo schema.sql
        with open('schema.sql', 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())

        # 2. Tenta abrir e rodar os Inserts apenas se o banco for novo, caso
        # contrario, apenas exibira que estará estabelecendo a conexão, os inserts
        # armazenado em inserts.sql
        if not banco_existe:
            with open('inserts.sql', 'r', encoding='utf-8') as g:
                cursor.executescript(g.read())
            print(">>> Sucesso: Banco criado e populado pela primeira vez.")
        else:
            print(">>> Conectado: Banco de dados já existente.")

        # Salvando e fechando a conexão
        conexao.commit()
        conexao.close()

        # Salvando e fechando a conexão
        conexao.commit()
        conexao.close()

    # Excepts trazendo possiveis mensagens de erro
    except FileNotFoundError as e:
        print(f"Erro: Arquivo de script não encontrado! Detalhes: {e}")
    except sqlite3.Error as e:
        print(f"Erro no Banco de Dados (SQLite): {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# --- FUNÇÃO BANCO DE DADOS ---

def conectar_banco():
    try:
        conexao = sqlite3.connect('database.db')
        cursor = conexao.cursor()
        return conexao, cursor
    except sqlite3.Error as e:
        print(f"[!] Erro ao conectar ao banco: {e}")
        return None, None

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
            temperature=0.8,              # 2. Configuração de criatividade
            api_key=api_key,                  # 3. Código da API
            max_tokens=1000                       # 4. Limitando os Tokens
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
        cadeia = modelo_economia | llm | StrOutputParser() # StrOutputParser() tira a necessidade de passar .content

        # Armazena na variavel resposta a resposta do gemini
        resposta = cadeia.invoke(
            { # Declarando que a variavel no input_variables possui o valor da variavel nm_usuario
                "nm_usuario" : nm_usuario
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
        modelo_prompt = PromptTemplate(template = """
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

               """, input_variables= ["nm_usuario", "csv_resumo"] )

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
            template = """
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
            template= """
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
        cadeia = modelo_de_prompt | llm | StrOutputParser() # StrOutputParser() tira a necessidade de passar .content

        # Armazena na variavel resposta a resposta do gemini
        resposta = cadeia.invoke(
            { # Declarando que a variavel no input_variables possui o valor da variavel nm_usuario
                "nm_usuario" : nm_usuario,
                "informacoesUsuario" : informacoesUsuario_str,
                "pergunta" : pergunta
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






# --- FUNÇÕES UTILITÁRIAS ---
def pausar():
    # ESSA FUNÇÃO SEGURA A TELA PARA VOCÊ LER A MENSAGEM ANTES DE LIMPAR
    input("\nPRESSIONE [ENTER] PARA CONTINUAR...")
    print("\n\n\n\n")









# Funções Principais
def login():
        print("\n======================================")
        print("      ÁREA DE ACESSO")
        print("\n======================================")

        email = input("Digite seu e-mail: ")
        senha = input("Digite sua senha: ")

        # Conecta ao banco de dados
        conexao, cursor = conectar_banco()

        # Busca o usuário com esse email e essa senha
        query = "SELECT id_usuario, nm_usuario FROM usuarios WHERE email = ? AND senha = ?"
        cursor.execute(query, (email, senha))

        usuario = cursor.fetchone()  # Tenta pegar uma linha
        conexao.close()

        if usuario:
            # Se encontrou, usuario[0] é o ID e usuario[1] é o Nome
            print(f"\n[+] Bem-vindo de volta, {usuario[1]}!")
            menu_pos_login(usuario)
            return usuario  # Retorna (id, nome) para usar no sistema

        else:
            print("\n[!] E-mail ou senha incorretos.")
            return None

# ⚠️ EM AMBIENTE REAL, A SENHA DEVERIA SER ARMAZENADA COM HASH
def criar_conta():
    print("\n======================================")
    print("      CRIAÇÃO DE CONTA")
    print("======================================")
    nome = str(input("Digite o seu nome: "))
    email = str(input("Digite o seu email: "))
    senha = str(input("Digite a sua senha: "))

    try:
        conexao, cursor = conectar_banco()

        # 1. Executa a inserção
        query = "INSERT INTO usuarios (nm_usuario, email, senha) VALUES (?, ?, ?);"
        cursor.execute(query, (nome, email, senha))

        # 2. IMPORTANTE: Salva a alteração no banco de dados
        conexao.commit()

        # 3. Verifica se o ID foi gerado (confirmação de sucesso)
        if cursor.lastrowid:
            print("\n[+] Conta criada com sucesso!")
            print("[+] Acesse na área de Login")
        else:
            print("\n[!] Ocorreu um erro na criação da sua conta.")
        conexao.close()
    except sqlite3.IntegrityError:
        print("\n[!] Erro: Este e-mail já está cadastrado!")
    except sqlite3.Error as e:
        print(f"\n[!] Erro no Banco de Dados (SQLite): {e}")
    except Exception as e:
        print(f"\n[!] Erro inesperado: {e}")




def encerrando():
    print("\nEncerrando o sistema. Até mais!")

# Funções secundarias

def checar_saldo(usuario):
    id_usuario = usuario[0]
    try:
        conexao, cursor = conectar_banco()

        tipo = "Entrada"
        query1 = "SELECT SUM(valor) FROM transacoes WHERE id_usuario = ? AND tipo = ?"
        cursor.execute(query1, (id_usuario, tipo))
        entrada = cursor.fetchone()

        if entrada[0] is None:
            print("Você não possui transações de entrada")
            return

        tipo2 = "Saída"
        query2 = "SELECT SUM(valor) FROM transacoes WHERE id_usuario = ? AND tipo = ?"
        cursor.execute(query2,(id_usuario, tipo2))
        saida = cursor.fetchone()

        if saida[0] is None:
            print("Você não possui transações de saída")
            return

        entrada_valor = entrada[0] or 0
        saida_valor = saida[0] or 0
        saldo = entrada_valor - saida_valor

        print(f"\n=============================")
        print(f"   SALDO ATUAL: R$ {saldo}")
        print(f"Entradas: R$ {entrada_valor} | Saídas: R$ {saida_valor}")
        print(f"=============================")

        pausar()

        conexao.commit()
        conexao.close()




    except sqlite3.Error as e:
        print(f"\n[!] Erro no Banco de Dados: {e}")




def registrar_transacao(usuario):
    id_usuario = usuario[0]

    conexao = None

    try:
        conexao, cursor = conectar_banco()


        while True:
            print("====================================")
            print("  NOVO REGISTRO")
            print("====================================")
            tipo = input("Tipo (1 - ENTRADA / 2 - SAÍDA / 0 - VOLTAR): ")

            if tipo == "0":
                print("Voltando...")
                break

            id_categoria = None

            if tipo == "1":
                tipo_db = "Entrada"
                print("\nCategorias de RECEITA:")
                op = input("1 - SALÁRIO / 2 - INVESTIMENTO: ")
                match op:
                    case "1":
                        id_categoria = 3
                    case "2":
                        id_categoria = 4
                    case _:
                        print("[!] Opção inválida."); continue

            elif tipo == "2":
                tipo_db = "Saída"
                print("\nCategorias de DESPESA:")
                op = input("1 - ALIMENTAÇÃO / 2 - LAZER / 3 - EDUCAÇÃO / 4 - TRANSPORTE: ")
                match op:
                    case "1":
                        id_categoria = 1
                    case "2":
                        id_categoria = 2
                    case "3":
                        id_categoria = 5
                    case "4":
                        id_categoria = 6
                    case _:
                        print("[!] Opção inválida."); continue
            else:
                print("[!] Tipo inválido.")
                continue

            # Se chegamos aqui, os tipos estão certos
            try:
                valor = float(input("Valor: R$ "))
                descricao = str(input("Descrição: "))

                from datetime import date
                data_hoje = date.today().isoformat()

                # 3. INSERT (Incluindo a coluna 'tipo' para facilitar seu saldo depois)
                query = """
                    INSERT INTO transacoes (id_usuario, id_categoria, valor, tipo, data, descricao) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                cursor.execute(query, (id_usuario, id_categoria, valor, tipo_db, data_hoje, descricao))
                conexao.commit()
                print("\n[+] Transação registrada com sucesso!")

                # Pergunta se quer continuar
                continuar = str(input("\nDeseja registrar outra? (S/N): ")).upper()
                if continuar != 'S':
                    break

            except ValueError:
                print("\n[!] Erro: Use apenas números e ponto para o valor.")

    except sqlite3.Error as e:
        print(f"\n[!] Erro no Banco de Dados: {e}")
    finally:
        if conexao:
            conexao.close()



def exibir_transacoes(usuario):
    id_usuario = usuario[0]

    conexao = None

    try:
        conexao, cursor = conectar_banco()
        query = "SELECT valor, tipo, data, descricao FROM transacoes WHERE id_usuario = ?"
        cursor.execute(query,(id_usuario,))
        movimentacoes = cursor.fetchall()


        if not movimentacoes:
            print("\n[!] Você ainda não possui transações cadastradas.")
        else:
            contador = 0
            for m in movimentacoes:
                print("===================================================")
                print(f" Valor: R${m[0]} | Tipo: {m[1]} | Data: {m[2]}")
                print(f" Descrição: {m[3]}")
                print("===================================================")

                contador += 1  # Aumenta 1 a cada volta
                if contador >= 10:  # Se já mostrou 10, para aqui
                    print("... (Existem mais metas, mas estas são as principais)")
                    break
            pausar()


    except sqlite3.Error as e:
        print(f"\n[!] Erro no Banco de Dados: {e}")
    finally:
        if conexao:
            conexao.close()


def criar_metas(usuario):
   id_usuario = usuario[0]

   conexao = None

   try:
        conexao, cursor = conectar_banco()

        while True:
            objetivo = str(input("Descrição da meta: "))
            valor_objetivo = float(input("Digite o valor da meta: R$"))
            prazo = str(input("Digite o prazo (AAAA-MM-DD): "))

            query = ("INSERT INTO metas_economicas (id_usuario, valor_objetivo, objetivo, prazo) VALUES (?, ?, ?, ?)")
            cursor.execute(query,(id_usuario, valor_objetivo, objetivo, prazo))
            conexao.commit()

            # 3. Verifica se o ID foi gerado (confirmação de sucesso)
            if cursor.lastrowid:
                print("\n[+] Meta criada com sucesso!")
            else:
                print("\n[!] Ocorreu um erro na criação da sua meta.")


            # Pergunta se quer continuar
            continuar = input("\nDeseja registrar outra? (S/N): ").upper()
            if continuar != 'S':
                break

   except sqlite3.Error as e:
       print(f"\n[!] Erro no Banco de Dados: {e}")
   finally:
       if conexao:
           conexao.close()


def exibir_metas(usuario):
    id_usuario = usuario[0]

    conexao = None

    try:
        conexao, cursor = conectar_banco()
        query = "SELECT  objetivo, valor_objetivo, prazo FROM metas_economicas WHERE id_usuario = ?"
        cursor.execute(query,(id_usuario,))
        metas = cursor.fetchall()


        if not metas:
            print("\n[!] Você ainda não possui metas cadastradas.")
        else:
            contador = 0
            for m in metas:
                print("===================================================")
                print(f" Objetivo: {m[0]} | Valor: R${m[1]} | Prazo: {m[2]}")
                print("===================================================")

                contador += 1  # Aumenta 1 a cada volta
                if contador >= 10:  # Se já mostrou 10, para aqui
                    print("... (Existem mais metas, mas estas são as principais)")
                    break

            pausar()


    except sqlite3.Error as e:
        print(f"\n[!] Erro no Banco de Dados: {e}")
    finally:
        if conexao:
            conexao.close()


def exibir_saude_financeira(usuario):
    id_usuario = usuario[0]

    try:
        conexao, cursor = conectar_banco()

        tipo = "Entrada"
        query1 = "SELECT SUM(valor) FROM transacoes WHERE id_usuario = ? AND tipo = ?"
        cursor.execute(query1, (id_usuario, tipo))
        entrada = cursor.fetchone()

        if entrada[0] is None:
            print("Você não possui transações de entrada")
            return

        tipo2 = "Saída"
        query2 = "SELECT SUM(valor) FROM transacoes WHERE id_usuario = ? AND tipo = ?"
        cursor.execute(query2, (id_usuario, tipo2))
        saida = cursor.fetchone()

        if saida[0] is None:
            print("Você não possui transações de saída")
            return

        saldo = entrada[0] - saida[0]

        # Cálculo de Eficiência Financeira (Quanto % do que ganho eu guardo?)
        if entrada[0] > 0:
            eficiencia = (saldo / entrada[0]) * 100
        else:
            eficiencia = 0

        print(f"\n=============================")
        print(f"   DIAGNÓSTICO DE SAÚDE")
        print(f"=============================")
        print(f" Total Entradas: R$ {entrada[0]}")
        print(f" Total Saídas:   R$ {saida[0]}")
        print(f" ---------------------------")
        print(f" SALDO ATUAL:    R$ {saldo}")
        print(f" TAXA DE SOBRA:  {eficiencia}")
        print(f"=============================")

        if eficiencia > 20:
            print("SITUAÇÃO: [ÓTIMA] - Você está poupando como um profissional!")
        elif eficiencia > 0:
            print("SITUAÇÃO: [ALERTA] - Sua margem de segurança é pequena.")
        else:
            print("SITUAÇÃO: [CRÍTICA] - Você está gastando mais do que recebe.")


        pausar()
        # Pergunta se quer ver o gráfico
        op = input("\nDeseja visualizar o comparativo em gráfico? (S/N): ").upper()
        if op == 'S':


            # Usando Pandas para preparar os dados de forma simples
            df = pd.DataFrame({
                'Categoria': ['Entradas', 'Saídas'],
                'Valores': [entrada[0], saida[0]]
            })

            # Gerando um gráfico de barras simples
            df.plot(kind='bar', x='Categoria', y='Valores', color=['green', 'red'], legend=False)
            plt.title("Comparativo: Entradas vs Saídas")
            plt.ylabel("Valor em R$")
            plt.xticks(rotation=0)
            plt.show()

        elif op == 'N':
            print("Vizualização encerrada.")


        conexao.close()
    except sqlite3.Error as e:
        print(f"\n[!] Erro no Banco de Dados: {e}")


def exibir_ranking_gastos(usuario):
    id_usuario = usuario[0]

    try:
        conexao, cursor = conectar_banco()

        # Usamos o Pandas para ler a query direto do banco
        query = """
            SELECT t.valor, c.nm_categoria, t.descricao
            FROM transacoes t
            JOIN categorias c ON t.id_categoria = c.id_categoria
            WHERE t.id_usuario = ? AND t.tipo = 'Saída'
            ORDER BY t.valor DESC
        """
        cursor.execute(query, (id_usuario,))
        ranking = cursor.fetchall()
        conexao.close()

        # Verifica se a lista está vazia
        if not ranking:
            print("\n[!] Você ainda não possui transações de saída para gerar um ranking.")
            return

        print("\n==============================================")
        print("      TOP 10 MAIORES GASTOS (RANKING)")


        if not ranking:
            print("\n[!] Você ainda não possui transações cadastradas.")
        else:
            contador = 0
            for m in ranking:
                print("==============================================")
                print(f" {contador + 1}º - MAIOR GASTO: R${m[0]}")
                print(f" CATEGORIA: {m[1]}")
                print(f" MOTIVO/DESC: {m[2]}")
                print("===================================================")


                contador += 1  # Aumenta 1 a cada volta
                if contador >= 10:  # Se já mostrou 10, para aqui
                    print("... (Existem mais transações, mas estas são as principais)")
                    break

            pausar()



    except Exception as e:
        print(f"\n[!] Ocorreu um erro: {e}")







# Funções Menu


def menu():
    inicializar_banco()
    while True:
        print("\n=============================")
        print(" Sistema de Gestão Financeira ")
        print("=============================")
        print(" 1 - Fazer Login")
        print(" 2 - Criar Nova Conta")
        print(" 0 - Sair do Sistema")
        print("=============================")
        op = input("Escolha uma opção: ")

        match op:

            case "1":
                login()
            case "2":
                criar_conta()
            case "0":
                encerrando()
                break
            case _:
                print("\n[!] Opção inválida. Tente novamente.")



def menu_pos_login(usuario):
    id_usuario = usuario[0]
    nm_usuario = usuario[1]

    while True:
        print(f"\n==========================================")
        print(f"       SGF - PAINEL DE CONTROLE           ")
        print(f"       Usuário: {nm_usuario.upper()}")
        print(f"==========================================")
        print(" [1] VISÃO GERAL (Saldo)")
        print(" [2] TRANSAÇÕES (ENTRADA/SAÍDA)")
        print(" [3] RELATÓRIOS E GRÁFICOS")
        print(" [4] PLANEJAMENTO (Metas Econômicas)")
        print(" [5] INSIGHTS I.A (FinGPT)")
        print(" [0] LOGOUT")
        print("==========================================")

        opcao = input("Escolha uma operação: ")

        match opcao:
            case "1":
                checar_saldo(usuario)


            case "2":
               menu_transacoes(usuario)


            case "3":
                menu_relatorios(usuario)
            case "4":
               menu_metas_economicas(usuario)

            case "5":
                menu_ia(usuario)


            case "0":
                print(f"\nEncerrando sessão de {nm_usuario}...")
                break

            case _:
                print("\n[!] Opção incorreta. Tente novamente.")

def menu_transacoes(usuario):

        nm_usuario = usuario[1]
        while True:
            print("============================")
            print(" SGF - MOVIMENTAÇÕES FINANCEIRAS")
            print(f" Usuário: {nm_usuario.upper()}")
            print("============================")
            print(" [1] EFETUAR ENTRADA/SAÍDA")
            print(" [2] EXIBIR MOVIMENTAÇÕES EXISTENTES")
            print(" [0] VOLTAR")
            print("==========================================")
            opcao = input("Escolha uma operação: ")

            match opcao:
                case "1":
                    registrar_transacao(usuario)
                case "2":
                    exibir_transacoes(usuario)
                case "0":
                    print("Voltando...")
                    break
                case _:
                    print("\n[!] Opção incorreta. Tente novamente.")



def menu_metas_economicas(usuario):

    nm_usuario = usuario[1]
    while True:
        print("============================")
        print(" SGF - METAS ECONÔMICAS")
        print(f" Usuário: {nm_usuario.upper()}")
        print("============================")
        print(" [1] LANÇAR NOVA META")
        print(" [2] EXIBIR METAS EXISTENTES")
        print(" [0] VOLTAR")
        print("==========================================")
        opcao = input("Escolha uma operação: ")

        match opcao:
            case "1": criar_metas(usuario)
            case "2": exibir_metas(usuario)
            case "0":
                print("Voltando...")
                break
            case _:
                print("\n[!] Opção incorreta. Tente novamente.")


def menu_relatorios(usuario):
    while True:
        print("=================================")
        print("    SGF - INSIGHTS FINANCEIROS")
        print(f"    Analista: {usuario[1].upper()}")
        print("=================================")
        print(" [1] DIAGNÓSTICO DE SAÚDE (KPIs)")
        print(" [2] MAIORES GASTOS (Ranking)")
        print(" [0] VOLTAR")
        print("=================================")
        opcao = input("Escolha o insight desejado: ")

        if opcao == "1":
            exibir_saude_financeira(usuario)
        elif opcao == "2":
            exibir_ranking_gastos(usuario)
        elif opcao == "0":
            break
        else:
            print("[!] Opção inválida.")


def menu_ia(usuario):
    nm_usuario = usuario[1]
    while True:
        print("===================================================")
        print("          🤖 ASSISTENTE IA - FinGPT")
        print(f"          👤 Usuário: {nm_usuario}")
        print("===================================================")
        print("[1] 📊 Analisar meus dados")
        print("    -> Ver resumo financeiro")
        print("[2] 💰 Sugerir economia")
        print("    -> Dicas para gastar menos")
        print("[3] 🔮 Prever próximos meses")
        print("    -> Como estarei financeiramente")
        print("[4] ❓ Fazer pergunta")
        print("    -> Qualquer dúvida sobre finanças")
        print("[0] ↩️  Voltar ao menu principal")
        print("===================================================")
        opcao = input("\nEscolha uma opção: ")
        match opcao:
            case "1":
                resumo_financeiro_ia(usuario)
            case "2":
                sugerir_economia(usuario)
            case "3":
                prever_proximos_meses(usuario)
            case "4":
                fazer_pergunta(usuario)
            case "0":
                print("Voltando...")
                break
            case _:
                print("\n[!] Opção incorreta. Tente novamente.")



# Start do sistema
menu()


# APOIO DE ESTUDOS
# ==============================================================================
# GUIA DE MÉTODOS DO CURSOR (SQLITE3)
# ==============================================================================

# cursor.execute(query, params)
# -> O MAIS USADO: Envia um comando SQL para o banco de dados.
# -> Use '?' como placeholder para passar variáveis com segurança.
# Ex: cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_user,))

# cursor.fetchone()
# -> BUSCA UMA LINHA: Retorna a primeira linha do resultado da consulta.
# -> Útil para: Logins, somas de saldo (SUM) ou buscar um item específico.
# -> Retorna: Uma TUPLA se achar algo, ou NONE se não achar nada.

# cursor.fetchall()
# -> BUSCA TUDO: Retorna uma LISTA contendo todas as linhas da consulta.
# -> Útil para: Listar extratos, mostrar todas as categorias ou metas.
# -> Retorna: Uma lista de tuplas [ (id1, nome1), (id2, nome2) ].

# cursor.lastrowid
# -> O "RG" DO NOVO REGISTRO: Retorna o ID (PK) da última linha que você inseriu.
# -> Útil para: Confirmar se o INSERT funcionou ou vincular dados na hora.
# -> Só funciona após comandos INSERT.

# cursor.executescript(string_sql)
# -> MÚLTIPLOS COMANDOS: Executa vários comandos SQL de uma vez (separados por ;).
# -> Útil para: Rodar o arquivo 'schema.sql' ou 'inserts.sql' na inicialização.

# cursor.rowcount
# -> LINHAS AFETADAS: Diz quantas linhas foram alteradas pelo último comando.
# -> Útil para: Saber se um UPDATE ou DELETE realmente alterou algo no banco.
# ==============================================================================



