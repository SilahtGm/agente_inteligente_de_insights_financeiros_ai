import os
import sqlite3


# --- FUNÇÃO BANCO DE DADOS ---

DB_PATH = "./database.db"
SCHEMA_PATH = "./data/schema.sql"
INSERTS_PATH = "./data/inserts.sql"

def conectar_banco():
    try:
        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        return conexao, cursor
    except sqlite3.Error as e:
        print(f"[!] Erro ao conectar ao banco: {e}")
        return None, None


# -- FUNÇÃO PRINCIPAL DE CRIAÇÃO/CONEXÃO DE BANCO DE DADOS ==
def inicializar_banco():
    try:
        # Guardando na variavel a checagem de se o banco de dados ja existe
        banco_existe = os.path.exists(DB_PATH)

        # Conecta ao banco
        conexao, cursor = conectar_banco()

        # Se o banco é novo, executa schema e inserts
        if not banco_existe:
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                cursor.executescript(f.read())
            with open(INSERTS_PATH, 'r', encoding='utf-8') as g:
                cursor.executescript(g.read())
            print(">>> Sucesso: Banco criado e populado pela primeira vez.")
        else:
            print(">>> Conectado: Banco de dados já existente.")

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

