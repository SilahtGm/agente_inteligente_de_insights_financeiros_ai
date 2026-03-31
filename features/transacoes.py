
import sqlite3

from db.connection import conectar_banco
from utils.helpers import pausar



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