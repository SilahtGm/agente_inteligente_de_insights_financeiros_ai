# Importações necessarias
import sqlite3
from db.connection import conectar_banco

# Funções Principais
def login():
        print("\n======================================")
        print("      ÁREA DE ACESSO")
        print("\n======================================")

        email = input("Digite seu e-mail: ")
        senha = input("Digite sua senha: ")

        # Conecta ao banco de dados
        from db.connection import conectar_banco
        conexao, cursor = conectar_banco()

        # Busca o usuário com esse email e essa senha
        query = "SELECT id_usuario, nm_usuario FROM usuarios WHERE email = ? AND senha = ?"
        cursor.execute(query, (email, senha))

        usuario = cursor.fetchone()  # Tenta pegar uma linha
        conexao.close()

        if usuario:
            # Se encontrou, usuario[0] é o ID e usuario[1] é o Nome
            print(f"\n[+] Bem-vindo de volta, {usuario[1]}!")
            from views.menus import menu_pos_login
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